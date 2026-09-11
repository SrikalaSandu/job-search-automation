"""
Generates a tailored resume + cover letter for a given job:

1. Ask Claude to rewrite resume bullets / pick which experience to
   emphasize, using ONLY facts from MASTER_RESUME_TEXT (never invents
   experience).
2. Build the actual .docx files from that structured output, following
   the formatting rules already defined in resume_data.py.

Output files land in output/resumes/ and output/cover_letters/.
"""

import os
import json
import re
import anthropic
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from resume_data import MASTER_RESUME_TEXT, CANDIDATE_NAME, CANDIDATE_EMAIL, CANDIDATE_PHONE, CANDIDATE_LOCATION

_workspace_id = os.environ.get("ANTHROPIC_WORKSPACE_ID")
_extra_headers = {"anthropic-workspace-id": _workspace_id} if _workspace_id else {}

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    default_headers=_extra_headers,
)
WRITE_MODEL = "claude-sonnet-4-6"

BLACK = RGBColor(0, 0, 0)
FONT = "Arial"

TAILOR_PROMPT_TEMPLATE = """You are tailoring a resume and writing a cover letter for a specific job,
using ONLY the experience in the candidate's master resume below. Never
invent skills, employers, dates, or achievements that aren't in it —
reordering, re-emphasizing, and rewording existing bullets is fine;
fabricating new ones is not.

MASTER RESUME (source of truth):
{resume}

JOB POSTING:
Title: {title}
Company: {company}
Location: {location}
Description:
{description}

Produce JSON with this exact shape:
{{
  "summary": "<2-3 sentence professional summary tailored to this job, using only real facts>",
  "experience": [
    {{
      "title": "<job title from master resume, unchanged>",
      "org": "<org name, unchanged>",
      "location": "<location, unchanged>",
      "dates": "<dates, unchanged>",
      "bullets": ["<tailored bullet 1>", "<tailored bullet 2>", "..."]
    }}
  ],
  "skills_relevant": ["<subset/reordering of skills from the master resume most relevant to this posting>"],
  "cover_letter_body": "<3-4 paragraph cover letter body text, no salutation/signature, referencing specific real experience>"
}}

Include at most 3 of the most relevant roles from the master resume
(fewer if that's all that's relevant), and at most 3 bullets per role, so
the final resume fits one page. The ACM SIGACCESS ASSETS 2025 publication
must be mentioned in at least one bullet if the candidate's Graduate
Research Assistant role is included, but do NOT invent a standalone
publications section here — the document builder adds that separately.

Respond with ONLY the JSON, no other text.
"""


def tailor_content(job: dict) -> dict:
    prompt = TAILOR_PROMPT_TEMPLATE.format(
        resume=MASTER_RESUME_TEXT,
        title=job.get("title", ""),
        company=job.get("company", ""),
        location=job.get("location", ""),
        description=job.get("description", "")[:6000],
    )
    response = client.messages.create(
        model=WRITE_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = "".join(block.text for block in response.content if block.type == "text")
    cleaned = re.sub(r"^```(json)?|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)


def _set_run(run, size=11, bold=False, italic=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.color.rgb = BLACK
    run.font.bold = bold
    run.font.italic = italic


def build_resume_docx(job: dict, tailored: dict, out_path: str):
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.4)
    section.bottom_margin = Inches(0.4)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = name_p.add_run(CANDIDATE_NAME.upper())
    _set_run(r, size=18, bold=True)

    contact_p = doc.add_paragraph()
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = contact_p.add_run(f"{CANDIDATE_EMAIL} | {CANDIDATE_LOCATION} | {CANDIDATE_PHONE}")
    _set_run(r, size=10)

    def add_section_header(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        _set_run(r, size=12, bold=True)
        pPr = p.paragraph_format
        pPr.space_before = Pt(8)
        pPr.space_after = Pt(2)

    def add_bullet(text):
        p = doc.add_paragraph(style="List Bullet")
        r = p.add_run(text)
        _set_run(r, size=10.5)

    add_section_header("PROFESSIONAL SUMMARY")
    p = doc.add_paragraph()
    r = p.add_run(tailored.get("summary", ""))
    _set_run(r, size=10.5)

    add_section_header("SKILLS")
    p = doc.add_paragraph()
    r = p.add_run(", ".join(tailored.get("skills_relevant", [])))
    _set_run(r, size=10.5)

    add_section_header("PROFESSIONAL EXPERIENCE")
    for role in tailored.get("experience", []):
        p = doc.add_paragraph()
        r = p.add_run(f"{role.get('title','')} — {role.get('location','')}")
        _set_run(r, size=11, bold=True)
        p2 = doc.add_paragraph()
        r2 = p2.add_run(f"{role.get('org','')}   {role.get('dates','')}")
        _set_run(r2, size=10.5, italic=True)
        for b in role.get("bullets", []):
            add_bullet(b)

    add_section_header("PUBLICATIONS")
    p = doc.add_paragraph()
    r = p.add_run(
        "Interactive Form Filling Assistant on Smart Glasses for Blind Users — "
        "S. Sandu, R. R. Khan, J. Hong. ACM SIGACCESS Conference on Computers and "
        "Accessibility (ASSETS), October 2025. https://doi.org/10.1145/3663547.3759722"
    )
    _set_run(r, size=10)

    doc.save(out_path)


def build_cover_letter_docx(job: dict, tailored: dict, out_path: str):
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    p = doc.add_paragraph()
    r = p.add_run(CANDIDATE_NAME)
    _set_run(r, size=11, bold=True)

    p = doc.add_paragraph()
    r = p.add_run(f"{CANDIDATE_LOCATION} | {CANDIDATE_EMAIL} | {CANDIDATE_PHONE}")
    _set_run(r, size=11)

    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run(f"Hiring Team, {job.get('company','')}")
    _set_run(r, size=11)
    p = doc.add_paragraph()
    r = p.add_run(f"Re: {job.get('title','')}, {job.get('location','')}")
    _set_run(r, size=11)

    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("Dear Hiring Team,")
    _set_run(r, size=11)

    body = tailored.get("cover_letter_body", "")
    for para_text in body.split("\n\n"):
        if not para_text.strip():
            continue
        p = doc.add_paragraph()
        r = p.add_run(para_text.strip())
        _set_run(r, size=11)

    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("Sincerely,")
    _set_run(r, size=11)
    p = doc.add_paragraph()
    r = p.add_run(CANDIDATE_NAME)
    _set_run(r, size=11)

    doc.save(out_path)


def generate_application_docs(job: dict) -> dict:
    """Full pipeline for one job: tailor content, write both docx files.
    Returns paths to the generated files."""
    tailored = tailor_content(job)

    safe_company = re.sub(r"[^A-Za-z0-9]+", "_", job.get("company", "Unknown")).strip("_")
    safe_title = re.sub(r"[^A-Za-z0-9]+", "_", job.get("title", "Role")).strip("_")[:40]

    resume_path = f"output/resumes/Resume_{safe_company}_{safe_title}.docx"
    cover_letter_path = f"output/cover_letters/CoverLetter_{safe_company}_{safe_title}.docx"

    build_resume_docx(job, tailored, resume_path)
    build_cover_letter_docx(job, tailored, cover_letter_path)

    return {"resume_path": resume_path, "cover_letter_path": cover_letter_path}
