# Phase 2 Project — 100-Row Enrichment Pipeline

**Objective:** Build a production-quality enrichment pipeline for 100 B2B contacts at 85%+ coverage with ICP scoring, Claygent research, and documented metrics.

**Estimated time:** 4–6 hours over 2–3 sessions  
**Pass criteria:** 85%+ email coverage, ICP score column, documented provider contribution breakdown

---

## Why This Project Matters

This is the project that moves you from "I know how Clay works" to "I can show someone a working pipeline."

Companies like OpenAI ran this exact experiment: single provider (Apollo alone) gave 40% coverage. After building a proper waterfall, they reached 80%+. You're building the same thing.

This also becomes Portfolio Project 1 if you document it properly.

---

## Input Data Requirements

100 rows minimum. Your input CSV should have:

| Column | Required? | Notes |
|--------|-----------|-------|
| first_name | Required | |
| last_name | Required | |
| company_name | Required | |
| company_domain | Required | Most important — verify these are real domains |
| linkedin_url | Optional | Improves Apollo match rate significantly |
| job_title | Optional | Helps with filtering + personalization |

**Where to get 100 rows:**
- Apollo's free search (50/month on free tier — run twice over 2 months)
- LinkedIn Sales Navigator export (if you have access)
- Manual research from LinkedIn search (time-consuming but free)
- Expand your Phase 1 25-row list by adding more companies from the same ICP

**ICP for this project:** B2B SaaS companies, 50–500 employees, US-based, with VP/Director level decision-makers in Sales, Marketing, or RevOps.

---

## Full Table Architecture

Build all columns in this exact order. Order matters for waterfall logic.

### Input Columns (static)
```
first_name, last_name, company_name, company_domain, linkedin_url (if available)
```

### Company Enrichment (do this before person enrichment)
```
company_data → Apollo Company Search
  Outputs: employee_count, industry, hq_country, hq_city
  Run condition: Always
```

### Email Waterfall (4 providers)
```
email_apollo    → Apollo People Search (Always)
email_prospeo   → Prospeo (if email_apollo empty)
email_findymail → Findymail (if above empty)
email_dropcontact → Dropcontact (if above empty)
```

### Claygent Columns (gated)
```
claygent_tech_stack → Tech stack detection
  Run condition: Only if (industry != "" AND employee_count >= 50)
  Prompt: Visit {company_domain}. Find the CRM they use (Salesforce, HubSpot, Pipedrive, or other). Check careers page job postings for tool mentions. Return: CRM=[tool or "unknown"]. Max 15 words.

claygent_signal → Recent funding or hiring signal
  Run condition: Only if (email_apollo is not empty OR email_prospeo is not empty) [only for found contacts]
  Prompt: Search for news about {company_name} in the last 12 months. Look for funding rounds, key exec hires (VP Sales, CTO), or major product launches. If found, return the signal in 20 words. If nothing, return "No recent signal".
```

### Formula Columns
```
email_final       → COALESCE of all 4 waterfall columns
email_source      → which provider found it
email_verified    → IF Findymail found → "Verified" ELSE "Unverified"
coverage_status   → "Found" / "Not found"
size_tier         → Enterprise/Mid-Market/SMB
icp_score         → numeric score 0–100
icp_tier          → Tier A/B/C label
crm_detected      → IF CONTAINS(claygent_tech_stack, "Salesforce") → "Salesforce" ELSE...
has_signal        → IF claygent_signal != "No recent signal" AND claygent_signal != "" → "Signal found"
```

### AI Personalization Column (add after Claygent)
```
ai_opener → Claude or GPT column

Prompt:
You are writing a personalized cold email opening line.

Contact: {first_name} {last_name}, {job_title} at {company_name}
Signal: {claygent_signal}
CRM: {crm_detected}

Write ONE sentence (max 25 words) that:
1. References the specific signal OR their CRM stack
2. Creates a connection to GTM data or enrichment challenges
3. Sounds like a human wrote it, not a template

If signal = "No recent signal" or is empty: reference the CRM instead.
Output ONLY the sentence. No quotes, no labels, no "Hi {first_name}".
```

---

## Running the Table: Step-by-Step Execution

### Session 1 (90 min): Setup + Company Enrichment

1. Import your 100-row CSV
2. Verify domains are correct format (no "Salesforce Inc", must be "salesforce.com")
3. Add Apollo Company Search column, run on 10 rows, verify output
4. Run Apollo Company Search on all 100 rows
5. Add all formula columns (don't run enrichment yet — formulas are free)
6. Log: How many rows have employee_count populated? What's the industry distribution?

### Session 2 (90 min): Email Waterfall

1. Add all 4 email enrichment columns with correct run conditions
2. Verify run conditions by testing on 5 rows manually
3. Check: does provider 2 skip rows where provider 1 succeeded?
4. Run full 100-row enrichment (watch credit spend)
5. Calculate interim coverage after each provider
6. Log credits used per provider

### Session 3 (60 min): Claygent + AI

1. Add Claygent tech stack column
2. Test on 5 rows, evaluate output quality
3. If prompts look good, run on qualifying rows (those with employee_count >= 50)
4. Add Claygent signal column, test, run
5. Add AI opener column
6. Test AI opener on 5 rows — does it sound human?
7. Run AI opener on all rows with email found

---

## Measuring Success

Calculate these metrics after every session:

### Coverage Metrics
```
Total rows: 100
Apollo found: ___  (___%)
Prospeo found: ___  (___%)
Findymail found: ___  (___%)
Dropcontact found: ___  (___%)
Still not found: ___  (___%)
Total coverage: ___% ← target: 85%+
```

### Quality Metrics
```
Email bounce rate (check after sending): target < 5%
ICP Tier A rows: ___  (target: 30%+ of total)
Rows with signal: ___
Rows with AI opener: ___
Credits used total: ___
Credits per enriched lead: ___  (target: < 3.0)
```

### Provider Contribution Analysis
Build this table to understand your waterfall efficiency:

| Provider | Found | % of found | % of total |
|----------|-------|-----------|-----------|
| Apollo | | | |
| Prospeo | | | |
| Findymail | | | |
| Dropcontact | | | |
| Claygent | | | |
| Not found | | | |

This table is the most important thing you'll share if you want to demonstrate Clay expertise.

---

## Documenting for Portfolio

If you intend this for your portfolio, capture:

1. **Screenshot of the full Clay table** with all columns visible
2. **Provider contribution table** (built above)
3. **Before/after coverage** (show starting state + final state)
4. **3 example rows** with full enrichment + AI opener visible
5. **Loom walkthrough** (optional but impressive): 3-minute walkthrough explaining the waterfall logic

Write a case study entry:
```
Problem: Enriching 100 B2B contacts for personalized outbound
Approach: 4-provider waterfall + Claygent signal detection + AI personalization
Result: 87% email coverage (from ~40% with single provider), 3.2 credits/lead, 
        30 Tier A leads identified, personalized opener for each enriched contact
Time: ~4.5 hours active work
```

---

## Troubleshooting Common Issues

**Coverage stuck at 70%:**
- Are the not-found rows all the same type? (All EU? All small companies?)
- Did Findymail return "invalid" emails that you're not filtering?
- Is company_domain accurate for the not-found rows?

**Claygent returning wrong format:**
- Rewrite the prompt with stricter format instructions
- Add an example output: "For example, return: CRM=Salesforce"
- Test on 5 more diverse rows

**AI opener sounds robotic:**
- Check if the signal or CRM columns are empty for those rows
- The AI needs real data to work with — "No recent signal + unknown CRM" produces generic output
- Add a fallback in the prompt: "If signal and CRM are unknown, reference {industry} instead"

**Credits running out faster than expected:**
- Check if auto-enrich is ON (should be OFF for learning)
- Did any Claygent columns run on rows they shouldn't?
- Review the credits transaction log in Settings → Credits

---

## You've Completed Phase 2 When:

- [ ] 100-row table built and enriched
- [ ] 4-provider waterfall with correct run conditions
- [ ] Coverage rate ≥ 85%
- [ ] Provider contribution table documented
- [ ] ICP score formula working
- [ ] At least one Claygent column working
- [ ] AI opener column generating real sentences (not template-style)
- [ ] Metrics logged in `00_meta/progress_tracker.md`

→ [03_advanced/01_claygent_mastery.md](../03_advanced/01_claygent_mastery.md)
