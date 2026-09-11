"""
Runs the full pipeline once:
  1. Fetch new job postings
  2. Score each against your resume
  3. For matches above config.MATCH_THRESHOLD, generate a tailored resume
     + cover letter
  4. Log every scored job (match or not) into the tracker spreadsheet

Run manually:
    python main.py

Run on a schedule (background, no laptop needed 24/7 if hosted on a
server — see README.md for deployment options):
    Add a cron job, e.g. every 6 hours:
    0 */6 * * * cd /path/to/job_search_app && python main.py >> run.log 2>&1
"""

import os
import json
import time
from dotenv import load_dotenv

load_dotenv()  # reads .env for ANTHROPIC_API_KEY, ADZUNA_APP_ID, ADZUNA_APP_KEY

from config import MATCH_THRESHOLD, MAX_JOBS_PER_RUN
from job_fetcher import fetch_all_jobs
from matcher import score_job
from resume_writer import generate_application_docs
from tracker import add_job_to_tracker

SEEN_JOBS_FILE = "output/seen_jobs.json"


def load_seen_ids():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen_ids(seen_ids):
    os.makedirs(os.path.dirname(SEEN_JOBS_FILE), exist_ok=True)
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(list(seen_ids), f)


def run():
    print("=== Job search run starting ===")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set in .env — cannot score or tailor. Stopping.")
        return

    seen_ids = load_seen_ids()
    all_jobs = fetch_all_jobs()
    new_jobs = [j for j in all_jobs if j["id"] not in seen_ids]
    print(f"[main] {len(new_jobs)} new postings out of {len(all_jobs)} fetched.")

    processed = 0
    for job in new_jobs:
        if processed >= MAX_JOBS_PER_RUN:
            print(f"[main] Hit MAX_JOBS_PER_RUN ({MAX_JOBS_PER_RUN}) — stopping this run early.")
            break

        print(f"[main] Scoring: {job['title']} @ {job['company']}")
        try:
            score_result = score_job(job)
        except Exception as e:
            print(f"[main] Scoring failed for '{job['title']}': {e}")
            seen_ids.add(job["id"])
            processed += 1
            continue

        doc_paths = None
        if score_result.get("match_score", 0) >= MATCH_THRESHOLD:
            print(f"[main]   -> {score_result['match_score']}% match, above threshold. Generating docs...")
            try:
                doc_paths = generate_application_docs(job)
            except Exception as e:
                print(f"[main]   Doc generation failed: {e}")
        else:
            print(f"[main]   -> {score_result.get('match_score', 0)}% match, below threshold. Logging only.")

        add_job_to_tracker(job, score_result, doc_paths)
        seen_ids.add(job["id"])
        processed += 1
        time.sleep(1)  # be polite to the API

    save_seen_ids(seen_ids)
    print(f"=== Run complete. Processed {processed} jobs. ===")


if __name__ == "__main__":
    run()
