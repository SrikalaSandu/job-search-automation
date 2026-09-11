"""
All the settings you're likely to want to change live here.
Nothing in this file needs an API key — those go in .env (see .env.example).
"""

# Companies to search for. The fetcher searches these as keywords against
# the job aggregator, AND checks direct Greenhouse/Lever boards for the ones
# that have them (mostly startups/mid-size — big companies like Nvidia/Amazon
# use Workday, which has no public API, so those come through the aggregator only).
TARGET_COMPANIES = [
    "Google", "ADP", "Virtusa", "Apple", "TCS", "Infosys", "State Farm",
    "HCL Healthcare", "IBM", "Nvidia", "Amazon", "PayPal", "Dell", "Cisco",
    "Commvault",
]

# Company slugs on Greenhouse (job-boards.greenhouse.io/<slug>) and Lever
# (jobs.lever.co/<slug>), if you know them. Add more as you find them —
# these are free to poll, no API key needed. Leave empty lists to skip.
# Verified live 2026-09-11 — Nvidia/Amazon/PayPal/Dell/Cisco/Virtusa/Google/
# Apple/IBM all use Workday or other private ATSes with no public API, so
# they only come through Adzuna. Commvault does have a Greenhouse board.
# Job titles from these boards are filtered by SEARCH_KEYWORDS (see
# job_fetcher.py) since these APIs return every open role, not just AI/ML.
GREENHOUSE_SLUGS = [
    "commvault", "anthropic", "scaleai", "togetherai", "stabilityai",
    "tavily", "imbue", "assemblyai", "arizeai", "snorkelai", "primerai",
    "databricks", "cognitionlabs",
]
LEVER_SLUGS = ["anyscale", "mistral"]

# Keywords used for the general aggregator search (broadens beyond the
# named companies to "almost any company, anywhere in the US").
SEARCH_KEYWORDS = [
    "AI Engineer", "Machine Learning Engineer", "Generative AI Engineer",
    "Applied Scientist", "MLOps Engineer", "NLP Engineer",
    "Junior AI Engineer", "AI Engineer New Grad", "Machine Learning Engineer I",
    "Associate ML Engineer", "Entry Level Machine Learning",
    "New Grad Software Engineer AI", "ML Engineer Intern to Full Time",
]

# Only postings scoring at or above this get a tailored resume/cover letter
# generated automatically. Lower it to see more, raise it to see less.
MATCH_THRESHOLD = 55

# Countries to include in aggregator search: "us" for United States only.
# Set to None to search internationally too (you mentioned being open to
# strong-pay roles outside the US).
COUNTRY = "us"

# How many new postings to fully process (score + tailor docs) per run.
# Keeps API costs predictable — raise once you trust it.
MAX_JOBS_PER_RUN = 15

# Path to your master resume (plain text extraction of your actual resume,
# used as the source of truth for tailoring — see resume_data.py).
TRACKER_PATH = "output/Job_Application_Tracker.xlsx"
