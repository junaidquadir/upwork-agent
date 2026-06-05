# 💼 Finance & Accounting Upwork Proposal Agent

Generate winning Upwork proposals for finance, CFO, accounting & tax roles in seconds.

Powered by **Claude Opus 4.8** — never fabricates experience or credentials.

---

## What It Does

Paste a job posting + your resume → get a full 10-section proposal package:

1. Job Analysis
2. Client Quality Rating
3. Match Analysis Table
4. Gap Analysis
5. Proposal Optimization Report
6. Short / Standard / Premium Proposals (3 hook styles)
7. Screening Question Answers
8. Bid Strategy
9. Interview Preparation
10. Final Match Scorecard with Apply Recommendation

---

## How to Use

1. Open the app link
2. Enter your Anthropic API key in the sidebar
3. Paste the Upwork job posting
4. Paste your resume / background
5. Click **🚀 Generate Proposal Package**
6. Download as Markdown

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run upwork_ui.py
```

Set your API key:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # Mac/Linux
$env:ANTHROPIC_API_KEY="sk-ant-..."     # Windows
```

---

## Get an API Key

→ [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key

**Cost per run:** ~$0.10–$0.30

---

## Deploy Your Own (Free)

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `ANTHROPIC_API_KEY` in Secrets
5. Deploy → share the link
