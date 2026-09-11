"""
Scores a job posting against the master resume using the Claude API.
Returns a match percentage (0-100) and a short reasoning string, plus any
flags worth a human's attention (e.g. visa sponsorship language, degree
year mismatches) — the model is told never to silently ignore these.
"""

import os
import json
import anthropic
from resume_data import MASTER_RESUME_TEXT

_workspace_id = os.environ.get("ANTHROPIC_WORKSPACE_ID")
_extra_headers = {"anthropic-workspace-id": _workspace_id} if _workspace_id else {}

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    default_headers=_extra_headers,
)

MATCH_MODEL = "claude-sonnet-4-6"

SCORING_PROMPT_TEMPLATE = """You are scoring how well a candidate's resume matches a job posting.

CANDIDATE'S RESUME:
{resume}

JOB POSTING:
Title: {title}
Company: {company}
Location: {location}
Description:
{description}

Score the match from 0-100 based on genuine skill/experience overlap — not
keyword-stuffing. Be honest and calibrated: a 90+ means the candidate is a
strong, direct fit; a 50 means partial overlap with real gaps; below 30
means largely unrelated.

Also flag anything in the posting that could block this candidate from
being eligible regardless of skill fit — e.g. explicit visa sponsorship
restrictions, a specific graduation-year requirement that doesn't match,
a security clearance requirement, or a seniority level clearly above or
below the candidate's experience. Do not guess at the candidate's
citizenship or visa status — just surface the posting's own language so
the human can judge it themselves.

Respond with ONLY valid JSON, no other text, in this exact shape:
{{
  "match_score": <integer 0-100>,
  "reasoning": "<2-3 sentences on why, citing specific overlapping skills/experience>",
  "eligibility_flags": ["<flag 1>", "<flag 2>"]  // empty list if none
}}
"""


def score_job(job: dict) -> dict:
    """job is a normalized dict from job_fetcher.py. Returns the parsed score dict."""
    prompt = SCORING_PROMPT_TEMPLATE.format(
        resume=MASTER_RESUME_TEXT,
        title=job.get("title", ""),
        company=job.get("company", ""),
        location=job.get("location", ""),
        description=job.get("description", "")[:6000],  # keep prompts a reasonable size
    )

    response = client.messages.create(
        model=MATCH_MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = "".join(block.text for block in response.content if block.type == "text")

    try:
        result = json.loads(raw_text.strip().strip("`").removeprefix("json").strip())
    except (json.JSONDecodeError, AttributeError):
        print(f"[matcher] Could not parse model output for '{job.get('title')}': {raw_text[:200]}")
        result = {"match_score": 0, "reasoning": "Could not score — parsing error.", "eligibility_flags": []}

    return result


if __name__ == "__main__":
    # Quick manual test
    test_job = {
        "title": "AI Engineer",
        "company": "Virtusa",
        "location": "New York, NY",
        "description": "Master's degree in AI/ML required. Python, PyTorch, LangChain, RAG, agentic architectures. 2025 grads only, no sponsorship.",
    }
    print(json.dumps(score_job(test_job), indent=2))
