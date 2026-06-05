import streamlit as st
import anthropic
import os

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance Upwork Proposal Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stTextArea textarea {
        background-color: #1e2130;
        color: #e0e0e0;
        border: 1px solid #3a3f5c;
        border-radius: 8px;
        font-size: 14px;
    }
    .stTextInput input {
        background-color: #1e2130;
        color: #e0e0e0;
        border: 1px solid #3a3f5c;
        border-radius: 8px;
    }
    .block-label { font-weight: 600; color: #a0a8c8; }
    div[data-testid="stSidebar"] { background-color: #161b2e; }
    .output-box {
        background-color: #1a1f35;
        border: 1px solid #2d3456;
        border-radius: 10px;
        padding: 20px;
        font-family: 'Segoe UI', sans-serif;
        color: #dde1f0;
        line-height: 1.7;
        white-space: pre-wrap;
    }
    .badge-green  { background:#1a4731; color:#4ade80; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-yellow { background:#3d3510; color:#facc15; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-red    { background:#3d1010; color:#f87171; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .hero-title   { font-size:2.2rem; font-weight:800; color:#e2e8f8; margin-bottom:4px; }
    .hero-sub     { font-size:1rem; color:#7b82a8; margin-bottom:24px; }
    .section-chip {
        display:inline-block;
        background:#1e2d50;
        color:#7eb3ff;
        border-radius:6px;
        padding:2px 10px;
        font-size:12px;
        font-weight:600;
        margin-right:6px;
        margin-bottom:8px;
    }
</style>
""", unsafe_allow_html=True)

# ─── System prompt (same as CLI) ───────────────────────────────────────────────
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
Use candidate-provided resumes, portfolios, certifications, and case studies ONLY.

NEVER fabricate: Experience, Clients, Results, Certifications, Revenue figures, Software expertise.
If evidence is missing, explicitly state assumptions and reduce confidence.

---

## COMPLETE OUTPUT STRUCTURE

Generate ALL sections in order:

---

## 1. JOB ANALYSIS

### Role Details
Extract: Job Title | Industry | Company Type | Company Stage | Company Size | Contract Type | Duration | Budget | Urgency

### Responsibilities
List all key responsibilities.

### Skills Required
Finance / Accounting / Tax / CFO / Treasury / Modeling / Audit / Compliance / Reporting / Communication

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

---

## 4. GAP ANALYSIS

### Strong Matches
### Partial Matches
### Missing Requirements

| Gap | Impact | Risk (Low/Med/High) | Positioning Strategy | Interview Strategy |
|---|---|---|---|---|

---

## 5. PROPOSAL OPTIMIZATION REPORT

Priority signals, terminology mirroring, content to include/exclude.

---

## 6. FINAL PROPOSALS

### SHORT PROPOSAL (100–150 words)

---

### STANDARD PROPOSAL (150–300 words)

---

### PREMIUM PROPOSAL (300–500 words)

Generate 3 Hook Variations:
1. **Direct Hook**
2. **Consultative Hook**
3. **Expert Hook**

Mark which hook was used in Premium.

All proposals: ✅ Human ✅ Client-focused ✅ Results-oriented ✅ Specific ✅ Trust-building ✅ Clear CTA
❌ No generic openings ❌ No buzzwords ❌ No AI language

---

## 7. SCREENING QUESTION ANSWERS

| Question | Recommended Answer | Reasoning |
|---|---|---|

---

## 8. BID STRATEGY

| Factor | Assessment |
|---|---|
| Win Probability | X% |
| Pricing Position | |
| Connect Recommendation | |
| Competition Level | |
| Strategy | |
| Recommended Bid | $X–$Y |

---

## 9. INTERVIEW PREPARATION

Likely client questions with suggested answers, objections and responses, proactive concerns.

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

**Apply Recommendation:** ✅ Strong Apply / ⚠️ Apply with Positioning / ❌ Not Recommended

**Final Reasoning:** 2–3 sentences.

---

Always optimize for interview conversion while remaining completely truthful."""

# ─── Demo data ─────────────────────────────────────────────────────────────────
DEMO_JOB = """Job Title: Fractional CFO / Financial Controller – SaaS Startup

We are a Series A SaaS startup (ARR ~$3M, team of 25) looking for an experienced Fractional CFO
or Financial Controller to own our finance function. Ongoing engagement, 8–12 hrs/week.

Responsibilities:
- Build and maintain our 3-statement financial model and 18-month rolling forecast
- Prepare monthly board pack (P&L, BS, Cash Flow, KPIs, commentary)
- Own the annual budget process and variance analysis
- Manage cash flow and runway projections
- Support Series B fundraising (data room, investor Q&A, financial due diligence)
- Set up financial controls in QuickBooks Online and Brex
- Coordinate with external accountants and auditors

Requirements:
- 8+ years in finance with SaaS/tech startup experience
- Expert in SaaS metrics (ARR, MRR, churn, CAC, LTV, Rule of 40)
- Experience supporting a funding round (Series A or B preferred)
- QuickBooks Online, Excel/Google Sheets (advanced)
- CPA or MBA preferred
- Excellent communication – must be comfortable presenting to the board

Budget: $75–120/hr | Contract: Ongoing, part-time"""

DEMO_CANDIDATE = """Name: Alex Morgan, CPA, MBA
Experience: 12 years in finance

Current: Independent Fractional CFO (3 years) – serving 4 SaaS/tech startup clients

Previous Roles:
- VP Finance @ CloudPay Inc (Series B SaaS, $8M ARR) – 3 years
  * Built 3-statement model used for successful $22M Series B raise
  * Reduced monthly close from 12 days to 5 days
  * Implemented QuickBooks + Brex + Stripe integration
- Finance Manager @ TechVentures (early-stage portfolio) – 4 years
  * Supported 6 portfolio companies with FP&A and board reporting
- Big 4 Auditor (Deloitte) – 2 years (tech sector)

Education: MBA (Finance) – Wharton | CPA licensed (CA)

Software: QuickBooks Online (expert), Excel/Google Sheets (advanced), Tableau, Salesforce, NetSuite (intermediate), Brex, Stripe

Key Deliverables:
- 15+ 3-statement financial models for SaaS companies
- 8 investor data rooms / due diligence packages
- Monthly board packs for 4 current clients
- SaaS metrics dashboards (ARR, MRR, churn, CAC/LTV, Rule of 40)
- Annual budget processes for $1M–$25M ARR companies

Certifications: CPA (active), MBA – Finance concentration
Industries: SaaS (primary), Fintech, Marketplace, E-commerce
Rate: $95–$130/hr"""

DEMO_QUESTIONS = """1. Have you supported a Series A or B funding round? Please describe your role.
2. What SaaS metrics do you track and how do you calculate CAC/LTV?
3. What is your experience with QuickBooks Online?"""

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-api03-...",
        help="Get yours at console.anthropic.com",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
    )
    st.markdown("---")
    st.markdown("### 📋 What this generates")
    sections = [
        "1. Job Analysis",
        "2. Client Quality Rating",
        "3. Match Analysis Table",
        "4. Gap Analysis",
        "5. Proposal Optimization",
        "6. Short / Standard / Premium Proposals",
        "7. Screening Q&A Answers",
        "8. Bid Strategy",
        "9. Interview Preparation",
        "10. Final Scorecard",
    ]
    for s in sections:
        st.markdown(f"<span class='section-chip'>{s}</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 💰 Cost per run")
    st.markdown("**~$0.10 – $0.30** per full analysis\n\nPowered by **Claude Opus 4.8**")
    st.markdown("---")
    load_demo = st.button("📂 Load Demo Data", use_container_width=True)

# ─── Hero header ───────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">💼 Finance & Accounting Proposal Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Generate winning Upwork proposals for finance, CFO, accounting & tax roles in seconds.</div>', unsafe_allow_html=True)

# ─── Input form ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 📋 Job Posting")
    job_post = st.text_area(
        label="job_post",
        label_visibility="collapsed",
        placeholder="Paste the full Upwork job posting here...",
        height=300,
        key="job_input",
    )

    st.markdown("#### ❓ Screening Questions *(optional)*")
    screening = st.text_area(
        label="screening",
        label_visibility="collapsed",
        placeholder="Paste any screening questions from the client...",
        height=120,
        key="screening_input",
    )

with col2:
    st.markdown("#### 👤 Your Profile / Resume")
    candidate = st.text_area(
        label="candidate",
        label_visibility="collapsed",
        placeholder="Paste your resume, background, key achievements, certifications, software skills...",
        height=440,
        key="candidate_input",
    )

# ─── Load demo data ────────────────────────────────────────────────────────────
if load_demo:
    st.session_state["job_input"] = DEMO_JOB
    st.session_state["candidate_input"] = DEMO_CANDIDATE
    st.session_state["screening_input"] = DEMO_QUESTIONS
    st.rerun()

# ─── Generate button ───────────────────────────────────────────────────────────
st.markdown("---")
generate_col, _ = st.columns([1, 2])
with generate_col:
    generate_btn = st.button(
        "🚀 Generate Proposal Package",
        use_container_width=True,
        type="primary",
    )

# ─── Validation & generation ───────────────────────────────────────────────────
if generate_btn:
    job_val = st.session_state.get("job_input", "").strip()
    cand_val = st.session_state.get("candidate_input", "").strip()
    screen_val = st.session_state.get("screening_input", "").strip()

    if not api_key:
        st.error("❌ Please enter your Anthropic API key in the sidebar.")
        st.stop()
    if not job_val:
        st.error("❌ Please paste a job posting.")
        st.stop()
    if not cand_val:
        st.error("❌ Please paste your candidate profile.")
        st.stop()

    # Build prompt
    prompt_parts = [
        "# INPUT DATA\n\n## JOB POSTING\n" + job_val,
        "\n\n## CANDIDATE PROFILE / RESUME\n" + cand_val,
    ]
    if screen_val:
        prompt_parts.append("\n\n## SCREENING QUESTIONS FROM CLIENT\n" + screen_val)
    prompt_parts.append(
        "\n\n---\n\nPlease generate the complete 10-section analysis and proposal package "
        "as defined in your instructions. Be thorough, specific, and honest."
    )
    full_prompt = "".join(prompt_parts)

    # Output area
    st.markdown("---")
    st.markdown("### 📄 Your Proposal Package")

    status_placeholder = st.empty()
    output_placeholder  = st.empty()
    save_placeholder    = st.empty()

    status_placeholder.info("🔍 Claude is analyzing the job and your profile...")

    collected_text = ""

    try:
        client = anthropic.Anthropic(api_key=api_key)

        with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=8000,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": full_prompt}],
        ) as stream:

            thinking_done = False

            for event in stream:
                if event.type == "content_block_start":
                    if event.content_block.type == "thinking" and not thinking_done:
                        status_placeholder.info("🧠 Thinking deeply about your match...")
                    elif event.content_block.type == "text":
                        thinking_done = True
                        status_placeholder.success("✍️ Writing your proposals...")

                elif event.type == "content_block_delta":
                    if event.delta.type == "text_delta":
                        collected_text += event.delta.text
                        output_placeholder.markdown(collected_text)

            final = stream.get_final_message()

        usage = final.usage
        status_placeholder.success(
            f"✅ Done!  •  Input: {usage.input_tokens:,} tokens  •  Output: {usage.output_tokens:,} tokens"
        )

        # Download button
        save_placeholder.download_button(
            label="💾 Download as Markdown",
            data=collected_text,
            file_name="upwork_proposal_package.md",
            mime="text/markdown",
            use_container_width=False,
        )

    except anthropic.AuthenticationError:
        status_placeholder.error("❌ Invalid API key. Check it at console.anthropic.com.")
    except anthropic.RateLimitError:
        status_placeholder.error("❌ Rate limit hit. Wait a moment and try again.")
    except Exception as e:
        status_placeholder.error(f"❌ Error: {str(e)}")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#444;font-size:12px;'>Finance Upwork Proposal Agent • Powered by Claude Opus 4.8 • Never fabricates experience or credentials</center>",
    unsafe_allow_html=True,
)
