# Airdrop & Bounty Opportunity Scanner — prototype

Free, **rule-based** prototype. It is NOT yet an LLM agent, does not execute tasks, and cannot guarantee any payout. It searches public RSS/Atom feeds for opportunity-related keywords. Feed endpoints may change or fail; review `report.md` for errors.

## Run locally
`python scanner.py` (Python 3.10+; no pip packages needed). Results in `output/report.md` and `output/opportunities.csv`.

## Schedule on GitHub
1. Create a **private** GitHub repository (or public if you prefer) and upload `scanner.py` and `.github/workflows/scan.yml` preserving folders.
2. Open **Actions → Free opportunity scanner → Run workflow** for the first test.
3. Open the run, download the `opportunity-report` artifact, and read `report.md`.
4. GitHub Actions attempts to run every day at 08:17 WIB; scheduled runs may be delayed or skipped, and inactive public repositories can have schedules disabled.

## Safety and limits
- Matches are **not verified** as active, free, accessible from Indonesia, or rewarding.
- No wallet connections, signatures, logins, auto-submissions, or financial transactions.
- Never provide seed phrases or private keys to bots.
- ChatGPT subscription is separate from paid API usage. This version uses no API and no paid dependencies.
- Source feeds are illustrative and may be unavailable; change `FEEDS` to verified RSS/Atom sources you trust.
