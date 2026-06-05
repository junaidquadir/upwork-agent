#!/usr/bin/env python3
"""
Finance, Accounting & Tax Upwork Proposal Agent
Generates comprehensive, data-driven Upwork proposals for finance professionals.
"""

import anthropic
import sys
import os

# ─────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert Upwork proposal strategist specializing ONLY in:
- FP&A, Financial Modeling & Valuation
- Accounting & Bookkeeping
- Tax Preparation & Advisory
- Fractional CFO Services
- Corporate Finance, Treasury
- Cash Flow Forecasting, Financial Reporting
- Startup Finance, Fundraising & Investor Reporting
- M&A & Due Diligence, Audit & Compliance
- Real Estate Finance, Fintech & Lending
- Credit Underwriting, Strategic Finance
- Budgeting & Forecasting

Ignore non-finance opportunities unless directly connected to finance.

## Source of Truth
Use candidate-provided resumes, portfolios, financial models, certifications, case studies, proposal samples, and uploaded files as the primary source.

NEVER fabricate:
- Experience, Clients, Results, Certifications
- Revenue figures, Software expertise, Industries served

If evidence is missing, explicitly state assumptions and reduce confidence.

---

## COMPLETE OUTPUT STRUCTURE

Generate ALL of the following sections in order:

---

## 1. JOB ANALYSIS

### Role Details
Extract: Job Title | Industry | Company Type | Company Stage | Company Size | Contract Type | Duration | Budget | Urgency

### Responsibilities
List all key responsibilities found in the posting.

### Skills Required
Identify Finance / Accounting / Tax / CFO / Treasury / Modeling / Audit / Compliance / Reporting / Communication skills.

### Software Identified
QuickBooks / Xero / NetSuite / SAP / Oracle / Excel / Power BI / Tableau / Salesforce / Workday / Other

### Deliverables Expected
Financial Models / Forecasts / Budgets / Financial Statements / Tax Returns / Dashboards / Investor Reports / Board Packs / Valuations / Due Diligence Reports

### Client Pain Points
Why hiring | Current challenges | Desired outcomes | Compliance issues | Cash flow concerns | Growth objectives | Investor needs

### Hidden Requirements
Ownership | Reliability | Leadership | Attention to detail | Communication | Problem solving

---

## 2. CLIENT QUALITY ANALYSIS

Evaluate: Payment history | Hiring history | Budget realism | Scope clarity | Long-term opportunity | Project complexity

**Rating:** Excellent / Good / Average / Risky — with detailed reasoning.

---

## 3. MATCH ANALYSIS

Build a table:

| JD Requirement | Candidate Evidence | Match Type | Match % |
|---|---|---|---|

Match Types: Full / Partial / Transferable / Missing

**Score Summary:**
- Technical Match: X%
- Industry Match: X%
- Tool Match: X%
- Deliverable Match: X%
- Communication Match: X%
- Experience Match: X%
- **Overall Match: X%**

Be conservative. Never inflate scores without evidence.

---

## 4. GAP ANALYSIS

### Strong Matches
List areas where candidate clearly exceeds requirements.

### Partial Matches
List areas with some overlap but gaps.

### Missing Requirements
For each gap:
| Gap | Impact | Risk (Low/Med/High) | Positioning Strategy | Interview Strategy |
|---|---|---|---|---|

Never invent qualifications to fill gaps.

---

## 5. PROPOSAL OPTIMIZATION REPORT

Target 90–99% relevance when evidence supports it.

**Priority Signals to Use:**
1. Similar deliverables first
2. Similar projects
3. Similar industry
4. Similar software
5. Similar business problems
6. Certifications
7. Education

Mirror client terminology naturally. Remove irrelevant content.

---

## 6. FINAL PROPOSALS

### SHORT PROPOSAL (100–150 words)
[Hook + Core Value + CTA]

---

### STANDARD PROPOSAL (150–300 words)
[Hook + Problem Understanding + Relevant Experience + Approach + CTA]

---

### PREMIUM PROPOSAL (300–500 words)
[Hook + Deep Problem Understanding + Specific Relevant Projects + Methodology + Results Evidence + Trust Builders + Clear CTA]

Generate 3 Hook Variations:
1. **Direct Hook:** Lead with the result
2. **Consultative Hook:** Lead with the problem
3. **Expert Hook:** Lead with rare insight

Use the strongest hook in Premium. Mark which hook was used.

All proposals must be:
✅ Human-sounding  ✅ Client-focused  ✅ Results-oriented
✅ Specific        ✅ Trust-building  ✅ Clear CTA
❌ No generic openings  ❌ No buzzwords  ❌ No AI-sounding language

---

## 7. SCREENING QUESTION ANSWERS

For each screening question provided:
| Question | Recommended Answer | Reasoning |
|---|---|---|

Answers must align with verified candidate evidence only.

---

## 8. BID STRATEGY

| Factor | Assessment |
|---|---|
| Win Probability | X% |
| Pricing Position | Below Market / At Market / Premium |
| Connect Recommendation | Spend / Skip / High Priority |
| Competition Level | Low / Medium / High / Very High |
| Strategy | Aggressive / Competitive / Premium |
| Recommended Bid | $X–$Y (hourly) or $X fixed |

Reasoning for each factor.

---

## 9. INTERVIEW PREPARATION

### Likely Client Questions
For each question:
- **Q:** [Question]
- **A:** [Suggested Answer using candidate evidence]

### Likely Objections & Responses
| Objection | Response Strategy |
|---|---|

### Concerns to Address Proactively
List 3–5 concerns the client might have and how to pre-empt them.

---

## 10. FINAL MATCH SCORECARD

| Dimension | Score |
|---|---|
| Technical Match | X% |
| Industry Match | X% |
| Tool Match | X% |
| Deliverable Match | X% |
| Communication Match | X% |
| Experience Match | X% |
| **Overall Match** | **X%** |
| Proposal Relevance | X% |
| Gap Recovery | X% |
| Interview Probability | X% |
| Client Quality Score | X/10 |

**Apply Recommendation:**
✅ Strong Apply / ⚠️ Apply with Positioning / ❌ Not Recommended

**Final Reasoning:** [2–3 sentences]

---

Always optimize for interview conversion while remaining completely truthful."""


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_multiline_input(prompt: str) -> str:
    """Collect multiline input until user types END on a new line."""
    print(prompt)
    print("(Type END on a new line when finished)\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def display_banner():
    print("\n" + "=" * 70)
    print("  FINANCE & ACCOUNTING UPWORK PROPOSAL AGENT")
    print("  Powered by Claude Opus 4.8")
    print("=" * 70 + "\n")


def build_prompt(job_post: str, candidate_profile: str, screening_questions: str) -> str:
    parts = [
        "# INPUT DATA\n",
        "## JOB POSTING\n" + job_post,
        "\n\n## CANDIDATE PROFILE / RESUME\n" + candidate_profile,
    ]
    if screening_questions.strip():
        parts.append("\n\n## SCREENING QUESTIONS FROM CLIENT\n" + screening_questions)
    parts.append(
        "\n\n---\n\nPlease generate the complete 10-section analysis and proposal package "
        "as defined in your instructions. Be thorough, specific, and honest."
    )
    return "".join(parts)


def stream_response(client: anthropic.Anthropic, prompt: str):
    """Stream the Claude response to stdout."""
    print("\n" + "=" * 70)
    print("  GENERATING YOUR PROPOSAL PACKAGE...")
    print("=" * 70 + "\n")

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=8000,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for event in stream:
            # Show thinking progress indicator (not the content)
            if event.type == "content_block_start":
                if event.content_block.type == "thinking":
                    print("\n[🔍 Analyzing job & candidate match...]\n", flush=True)
                elif event.content_block.type == "text":
                    pass  # text blocks stream naturally below

            elif event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    print(event.delta.text, end="", flush=True)

        final = stream.get_final_message()

    print("\n\n" + "=" * 70)
    usage = final.usage
    print(f"  Tokens — Input: {usage.input_tokens:,} | Output: {usage.output_tokens:,}")
    if hasattr(usage, "cache_read_input_tokens") and usage.cache_read_input_tokens:
        print(f"  Cache read: {usage.cache_read_input_tokens:,} tokens (cost savings applied)")
    print("=" * 70 + "\n")
    return final


def save_output(content: str, job_title: str):
    """Optionally save the output to a markdown file."""
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in job_title)[:40]
    filename = f"proposal_{safe_title.replace(' ', '_').lower()}.md"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ Proposal saved to: {filepath}")
    return filepath


# ─────────────────────────────────────────────
#  EXAMPLE DATA (used when running in demo mode)
# ─────────────────────────────────────────────

DEMO_JOB_POST = """
Job Title: Fractional CFO / Financial Controller – SaaS Startup

We are a Series A SaaS startup (ARR ~$3M, team of 25) looking for an experienced Fractional CFO
or Financial Controller to own our finance function. This is an ongoing engagement, 8–12 hrs/week.

Responsibilities:
- Build and maintain our 3-statement financial model and 18-month rolling forecast
- Prepare monthly board pack (P&L, BS, Cash Flow, KPIs, commentary)
- Own the annual budget process and variance analysis
- Manage cash flow and runway projections
- Support Series B fundraising (data room, investor Q&A, financial due diligence)
- Set up financial controls and processes in QuickBooks Online and Brex
- Coordinate with external accountants and auditors

Requirements:
- 8+ years in finance with SaaS/tech startup experience
- Expert in financial modeling and SaaS metrics (ARR, MRR, churn, CAC, LTV, Rule of 40)
- Experience supporting a funding round (Series A or B preferred)
- QuickBooks Online, Excel/Google Sheets (advanced)
- CPA or MBA preferred but not required
- Excellent communication – must be comfortable presenting to the board

Budget: $75–120/hr
Contract: Ongoing, part-time
""".strip()

DEMO_CANDIDATE_PROFILE = """
Name: Alex Morgan, CPA, MBA
Experience: 12 years in finance

Current: Independent Fractional CFO (3 years) – serving 4 SaaS/tech startup clients simultaneously

Previous Roles:
- VP Finance @ CloudPay Inc (Series B SaaS, $8M ARR) – 3 years
  * Built 3-statement model used for successful $22M Series B raise
  * Reduced monthly close from 12 days to 5 days
  * Implemented QuickBooks + Brex + Stripe integration
- Finance Manager @ TechVentures (early-stage portfolio) – 4 years
  * Supported 6 portfolio companies with FP&A and board reporting
- Big 4 Auditor (Deloitte) – 2 years (tech sector focus)

Education: MBA (Finance) – Wharton | CPA licensed (CA)

Software Expertise: QuickBooks Online (expert), Excel/Google Sheets (advanced), Tableau, Salesforce
(Salesforce Finance integration), NetSuite (intermediate), Brex, Stripe, Rippling

Key Deliverables Delivered:
- 15+ 3-statement financial models for SaaS companies
- 8 investor data rooms / due diligence packages
- Monthly board packs for 4 current clients
- SaaS metrics dashboards (ARR, MRR, churn, CAC/LTV, Rule of 40, NRR)
- Annual budget processes for $1M–$25M ARR companies

Certifications: CPA (active), MBA – Finance concentration

Industries: SaaS (primary), Fintech, Marketplace, E-commerce
Hourly Rate: $95–$130/hr
""".strip()

DEMO_SCREENING_QUESTIONS = """
1. Have you supported a Series A or B funding round? Please describe your role.
2. What SaaS metrics do you track and how do you calculate CAC/LTV?
3. What is your experience with QuickBooks Online?
""".strip()


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    display_banner()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set.")
        print("   Set it with:  set ANTHROPIC_API_KEY=sk-ant-...\n")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # ── Mode selection ──────────────────────────────────────────────
    print("Select mode:")
    print("  1. Demo mode (uses built-in example data)")
    print("  2. Interactive mode (paste your own data)")
    print()
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        print("\n✅ Using demo data — SaaS Fractional CFO role + candidate profile\n")
        job_post = DEMO_JOB_POST
        candidate_profile = DEMO_CANDIDATE_PROFILE
        screening_questions = DEMO_SCREENING_QUESTIONS
        job_title = "Fractional CFO SaaS Startup"

    else:
        print()
        job_post = get_multiline_input("📋 PASTE THE UPWORK JOB POSTING:")
        if not job_post:
            print("❌ No job posting entered. Exiting.")
            sys.exit(1)

        print()
        candidate_profile = get_multiline_input(
            "👤 PASTE YOUR CANDIDATE PROFILE / RESUME / BACKGROUND:"
        )
        if not candidate_profile:
            print("❌ No candidate profile entered. Exiting.")
            sys.exit(1)

        print()
        screening_questions = get_multiline_input(
            "❓ PASTE SCREENING QUESTIONS (optional — press END immediately to skip):"
        )

        job_title = input("\n📝 Enter a short job title for the filename: ").strip()
        if not job_title:
            job_title = "upwork_proposal"

    # ── Build prompt & stream ───────────────────────────────────────
    prompt = build_prompt(job_post, candidate_profile, screening_questions)
    final_message = stream_response(client, prompt)

    # ── Collect full text output ────────────────────────────────────
    full_text = ""
    for block in final_message.content:
        if block.type == "text":
            full_text += block.text

    # ── Save option ─────────────────────────────────────────────────
    print()
    save = input("💾 Save proposal to a markdown file? (y/n): ").strip().lower()
    if save == "y":
        save_output(full_text, job_title)

    print("\n✅ Done! Your proposal package is ready.\n")


if __name__ == "__main__":
    main()
