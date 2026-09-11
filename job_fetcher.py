"""
Fetches job postings from two kinds of sources:

1. Adzuna — a job aggregator with a genuinely free API tier (no credit card
   needed to start). It indexes listings from many boards and companies,
   including the big ones like Amazon/Nvidia/etc that don't have their own
   public API. Sign up at https://developer.adzuna.com/, get an app_id and
   app_key, put them in .env.

2. Greenhouse / Lever — direct, free, no-key-needed public APIs that
   startups and mid-size companies use for their own career pages. Add
   company slugs to config.GREENHOUSE_SLUGS / LEVER_SLUGS as you find them.

Every fetched job is normalized into the same dict shape so the rest of the
pipeline doesn't care which source it came from:

{
    "source": "adzuna" | "greenhouse" | "lever",
    "id": "<unique id, used to avoid re-processing the same job twice>",
    "title": str,
    "company": str,
    "location": str,
    "description": str,
    "url": str,
    "posted_date": str | None,
}
"""

import os
from datetime import datetime, timedelta, timezone
from itertools import zip_longest
import requests
from config import TARGET_COMPANIES, SEARCH_KEYWORDS, GREENHOUSE_SLUGS, LEVER_SLUGS, COUNTRY

ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY")

# Only keep postings from roughly the last day — recent enough that
# applying early actually matters, and small enough to keep each run's
# batch fresh instead of re-surfacing the same week-old listings.
RECENCY_WINDOW_HOURS = 24


def _is_recent_iso(timestamp_str, max_age_hours=RECENCY_WINDOW_HOURS):
    """For Greenhouse's updated_at (ISO 8601 with UTC offset, e.g.
    '2026-09-01T05:10:27-04:00')."""
    if not timestamp_str:
        return False
    try:
        dt = datetime.fromisoformat(timestamp_str)
    except ValueError:
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - dt <= timedelta(hours=max_age_hours)


def _is_recent_epoch_ms(epoch_ms, max_age_hours=RECENCY_WINDOW_HOURS):
    """For Lever's createdAt (epoch milliseconds). Lever's public postings
    API has no updatedAt field — createdAt is the only timestamp it exposes,
    so it's used as the recency signal here."""
    if not epoch_ms:
        return False
    dt = datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc)
    return datetime.now(timezone.utc) - dt <= timedelta(hours=max_age_hours)


def fetch_adzuna_jobs(max_pages=2):
    """Search Adzuna for each keyword. Returns a flat list of normalized jobs."""
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        print("[job_fetcher] No Adzuna credentials in .env — skipping aggregator search.")
        return []

    country_code = COUNTRY or "us"
    jobs = []
    seen_ids = set()

    for keyword in SEARCH_KEYWORDS:
        for page in range(1, max_pages + 1):
            url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/{page}"
            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "what": keyword,
                "results_per_page": 20,
                "content-type": "application/json",
                "max_days_old": 1,
            }
            try:
                resp = requests.get(url, params=params, timeout=15)
                resp.raise_for_status()
                data = resp.json()
            except requests.RequestException as e:
                print(f"[job_fetcher] Adzuna request failed for '{keyword}' page {page}: {e}")
                continue

            for item in data.get("results", []):
                job_id = str(item.get("id"))
                if job_id in seen_ids:
                    continue
                seen_ids.add(job_id)
                jobs.append({
                    "source": "adzuna",
                    "id": f"adzuna:{job_id}",
                    "title": item.get("title", "").strip(),
                    "company": (item.get("company") or {}).get("display_name", "Unknown"),
                    "location": (item.get("location") or {}).get("display_name", ""),
                    "description": item.get("description", ""),
                    "url": item.get("redirect_url", ""),
                    "posted_date": item.get("created"),
                })
    return jobs


def _title_matches_keywords(title):
    """Greenhouse/Lever boards return every open role at a company (unlike
    Adzuna, which is already keyword-searched) — filter by the same
    SEARCH_KEYWORDS so a big company's board doesn't drown out real matches
    with unrelated sales/legal/marketing roles."""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in SEARCH_KEYWORDS)


def fetch_greenhouse_jobs():
    """Poll each Greenhouse-hosted company board in config.GREENHOUSE_SLUGS."""
    jobs = []
    for slug in GREENHOUSE_SLUGS:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"[job_fetcher] Greenhouse request failed for '{slug}': {e}")
            continue

        for item in data.get("jobs", []):
            title = item.get("title", "").strip()
            if not _title_matches_keywords(title):
                continue
            updated_at = item.get("updated_at")
            if not _is_recent_iso(updated_at):
                continue
            jobs.append({
                "source": "greenhouse",
                "id": f"greenhouse:{slug}:{item.get('id')}",
                "title": title,
                "company": slug,
                "location": (item.get("location") or {}).get("name", ""),
                "description": item.get("content", ""),
                "url": item.get("absolute_url", ""),
                "posted_date": updated_at,
            })
    return jobs


def fetch_lever_jobs():
    """Poll each Lever-hosted company board in config.LEVER_SLUGS."""
    jobs = []
    for slug in LEVER_SLUGS:
        url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"[job_fetcher] Lever request failed for '{slug}': {e}")
            continue

        for item in data:
            title = item.get("text", "").strip()
            if not _title_matches_keywords(title):
                continue
            created_at = item.get("createdAt")
            if not _is_recent_epoch_ms(created_at):
                continue
            jobs.append({
                "source": "lever",
                "id": f"lever:{slug}:{item.get('id')}",
                "title": title,
                "company": slug,
                "location": (item.get("categories") or {}).get("location", ""),
                "description": item.get("descriptionPlain", ""),
                "url": item.get("hostedUrl", ""),
                "posted_date": datetime.fromtimestamp(created_at / 1000, tz=timezone.utc).isoformat(),
            })
    return jobs


def fetch_all_jobs():
    """Combine every source into one list, interleaved round-robin so a
    single source's backlog (e.g. Adzuna's hundreds of postings) can't crowd
    out the others under main.py's MAX_JOBS_PER_RUN cap. Deduplicated by id."""
    sources = [fetch_adzuna_jobs(), fetch_greenhouse_jobs(), fetch_lever_jobs()]
    all_jobs = [job for group in zip_longest(*sources) for job in group if job is not None]

    seen = set()
    deduped = []
    for job in all_jobs:
        if job["id"] in seen:
            continue
        seen.add(job["id"])
        deduped.append(job)
    print(f"[job_fetcher] Fetched {len(deduped)} unique postings.")
    return deduped


if __name__ == "__main__":
    jobs = fetch_all_jobs()
    for j in jobs[:5]:
        print(f"- {j['title']} @ {j['company']} ({j['location']}) [{j['source']}]")
