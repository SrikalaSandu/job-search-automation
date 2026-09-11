# Job Search Automation

Fetches new job postings, scores them against your resume, auto-generates
a tailored resume + cover letter for strong matches, and logs everything
into an Excel tracker. Built to run on a schedule so it works without you
opening it every time.

## What's already built and tested

- `resume_data.py` — your real resume content (edit this if your resume changes)
- `job_fetcher.py` — pulls jobs from Adzuna + any Greenhouse/Lever boards you add
- `matcher.py` — scores each job against your resume (0-100%) via Claude
- `resume_writer.py` — generates tailored .docx resume + cover letter (tested, works)
- `tracker.py` — logs everything into `output/Job_Application_Tracker.xlsx` (tested, works)
- `main.py` — runs the whole pipeline end to end

## Setup (do this first)

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Get an Anthropic API key** (required — this is what scores jobs and
   writes your resumes/cover letters):
   - Go to https://console.anthropic.com/settings/keys
   - Create a key
   - This is pay-as-you-go; at ~15 jobs scored per run, a few times a day,
     expect roughly $5-15/month depending on volume.

3. **Get an Adzuna API key** (optional, but recommended — this is what
   finds jobs at companies without a public API, like Amazon/Nvidia/PayPal):
   - Go to https://developer.adzuna.com/ and sign up (free tier)
   - You get an `app_id` and `app_key`

4. **Set up your .env file:**
   ```
   cp .env.example .env
   ```
   Then open `.env` and paste in your keys.

5. **Edit `config.py`** to adjust your target companies, match threshold,
   or add Greenhouse/Lever company slugs as you find them (search
   `"<company> jobs greenhouse"` or `"<company> jobs lever"` to check if a
   startup uses one of these).

## Run it once, manually, first

```
python main.py
```

This will:
- Fetch new postings
- Score each one
- Generate a tailored resume + cover letter for anything scoring 65%+
  (change `MATCH_THRESHOLD` in `config.py`)
- Open `output/Job_Application_Tracker.xlsx` to see everything it found

Check the tracker and the generated resumes/cover letters in
`output/resumes/` and `output/cover_letters/` before trusting it fully.

## Making it run in the background (no laptop required)

Right now, `python main.py` only runs when you run it. To make it check
automatically on a schedule, you need it hosted somewhere that's always on.
Two good options, easiest first:

### Option A: GitHub Actions (free, simplest)
- Push this folder to a private GitHub repo
- Add a `.github/workflows/run.yml` that runs `python main.py` on a cron
  schedule (e.g. every 6 hours)
- Store your API keys as GitHub repo secrets, not in the code
- Ask Claude Code to set this up for you — it's a well-known pattern

### Option B: A small always-on server (~$5-10/month)
- Railway.app or Render.com — both let you deploy a Python script with a
  cron schedule in a few clicks
- Ask Claude Code to walk you through deploying to either one

**Either way — the AI never autofills or submits applications for you in
this version.** It gets everything ready (tailored docs, ranked in your
tracker); you review and click submit yourself. This was a deliberate
choice: auto-submission is the least reliable, highest-risk part of tools
like this, especially on Workday-based sites (Nvidia, Amazon, PayPal,
Dell, Cisco). Add it later once the rest is solid, if you still want it.

## What Claude Code should do next

Hand this whole folder to Claude Code and ask it to:
1. Verify the setup runs cleanly with your real API keys
2. Set up the scheduled/background run (Option A or B above)
3. Optionally: add a notification step (email or Slack) that pings you
   with a digest after each run, instead of you having to open the
   spreadsheet
