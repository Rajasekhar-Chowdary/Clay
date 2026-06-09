# Module 2.2 — Company Enrichment

**Time:** 45–60 minutes  
**Focus:** Enrich the company side — size, industry, funding, tech stack, location

---

## Why Company Data Matters

Email coverage is about finding people. Company enrichment is about qualifying them.

Without company data, you can't:
- Filter by ICP (ideal customer profile)
- Score leads by company fit
- Personalize outreach by company context
- Route leads to the right sales rep
- Detect the buying signals that matter (funding, headcount growth, tech stack)

A list with email + company data is 5× more actionable than a list with email alone.

---

## The 5 Company Data Points That Drive Decisions

These are the only ones that matter for GTM:

| Field | Why it matters | Typical source |
|-------|----------------|---------------|
| `employee_count` | Size = deal size + complexity | Apollo, Clearbit |
| `industry` | ICP filtering | Apollo, Clearbit |
| `hq_country` | Geography routing + GDPR compliance | Apollo, Clearbit |
| `funding_stage` | Growth stage signal | Clearbit, Crunchbase, Claygent |
| `tech_stack` | Competitive intelligence + ICP fit | Clearbit, BuiltWith, Claygent |

Everything else (revenue estimate, year founded, SIC code) is nice-to-have. Build these 5 first.

---

## Building Company Enrichment Columns

### Apollo Company Search

Apollo has a dedicated "Company Search" enrichment type separate from People Search.

**Inputs:**
- Company Domain (required)
- Company Name (optional, improves matching)

**Outputs to select:**
- Employee Count
- Industry
- HQ Country
- HQ City
- Founded Year
- Company LinkedIn URL

**Configuration:**
```
Column: company_data_apollo
Type: Apollo Company Search
Run condition: Always (run this before person enrichment — company data doesn't waterfall)
Inputs: company_domain
Outputs: employee_count, industry, hq_country, hq_city, company_linkedin_url
```

Note: Apollo Company Search and Apollo People Search are separate calls. 2 credits per row (1 each) if you run both.

### Clearbit Company Enrichment (Breeze)

Clearbit (now HubSpot Breeze after acquisition) adds data that Apollo doesn't have:
- Exact funding amount and round
- Technologies used (broad list)
- Alexa rank / web traffic estimate
- Company description

**Inputs:** Company domain  
**Cost:** 1 credit per row  
**Note:** Clearbit requires a separate API key (free tier: 250 lookups/month)

### Deciding Between Apollo and Clearbit for Company Data

| Data point | Use Apollo | Use Clearbit |
|------------|-----------|-------------|
| Employee count | ✓ (good) | ✓ (similar) |
| Industry | ✓ | ✓ |
| Funding stage | △ (sometimes) | ✓ (better) |
| Funding amount | ✗ | ✓ |
| Tech stack | ✗ | ✓ (partial) |
| Company description | △ | ✓ |

**Practical approach:** Apollo for firmographics (size, industry, location). Clearbit for funding + tech stack. Claygent for everything else.

---

## Tech Stack Detection

### Why Tech Stack Data Is Powerful

Knowing what tools a company uses tells you:
- **Their current vendors** (direct competitors or complements)
- **Their maturity** (Salesforce + Outreach = sophisticated GTM stack)
- **Their pain points** (Salesforce but no enrichment tool = opportunity)

Example: If you're selling a data enrichment tool, a company using Salesforce but NOT Apollo is your ideal buyer.

### BuiltWith Integration

BuiltWith specializes in technology detection from website analysis.

```
Column: tech_stack_builtwith
Type: BuiltWith enrichment
Inputs: company_domain
Outputs: technologies (returns an array of detected tools)
```

From the technologies array, create formula columns:

```
uses_salesforce: {{IF(CONTAINS(tech_stack, "Salesforce"), "Yes", "No")}}
uses_hubspot:    {{IF(CONTAINS(tech_stack, "HubSpot"), "Yes", "No")}}
uses_marketo:    {{IF(CONTAINS(tech_stack, "Marketo"), "Yes", "No")}}
crm_detected:    {{IF(uses_salesforce=="Yes","Salesforce",IF(uses_hubspot=="Yes","HubSpot","Unknown"))}}
```

### Claygent for Tech Stack (When BuiltWith Fails)

For companies that don't expose their tech publicly, Claygent can infer from job postings:

```
Visit {company_domain}/careers and search for open sales, marketing, or RevOps job postings.
Extract any CRM or marketing tools mentioned in the requirements (Salesforce, HubSpot, Marketo, Outreach, etc.)
Return: CRM=[detected tool or "unknown"], Sales_tools=[list of tools or "none found"]
Max 30 words.
```

---

## The Company Enrichment Column Order

```
1. Apollo Company Search → employee_count, industry, hq_country
2. Clearbit → funding_stage, tech_stack (if available)
3. Claygent tech_stack (only if company_data_apollo.employee_count > 50 AND clearbit didn't find tech)
4. Formula columns → size_tier, icp_fit, tech_label
```

Don't run Claygent on every row — gate it with a condition like "only run if company size > 50 AND tech_stack is empty."

---

## Funding Stage as a Signal

Funding stage tells you where a company is in its growth cycle:

| Stage | What it means for GTM | How to use it |
|-------|----------------------|---------------|
| Seed / Pre-seed | Too early, no budget | Usually exclude from ICP |
| Series A | Hired first GTM team, evaluating tools | High-value prospect — they're building |
| Series B | Scaling GTM, actively spending | Highest priority |
| Series C+ | Sophisticated team, complex buying process | Longer cycle, larger deal |
| Public | Established — budget exists, procurement process | Known playbook needed |
| Bootstrapped | No VC, budget-conscious | Requires ROI-focused pitch |

**Formula:**
```
{{IF(
  funding_stage == "Series A" OR funding_stage == "Series B",
  "Growth Stage - High Priority",
  IF(
    funding_stage == "Series C" OR funding_stage == "Series D",
    "Scale Stage - Medium Priority",
    IF(
      CONTAINS(funding_stage, "Seed"),
      "Too Early",
      "Evaluate Individually"
    )
  )
)}}
```

---

## Building the ICP Score

With company data populated, you can build a real ICP score formula.

### ICP Score Components

```
Score = size_score + geography_score + tech_fit_score + funding_score

size_score:
  employee_count 50–200 = 30 points  (sweet spot for GTM tools)
  employee_count 201–500 = 25 points
  employee_count 20–49 = 15 points
  other = 5 points

geography_score:
  hq_country == "US" = 20 points
  hq_country == "UK" or "CA" or "AU" = 15 points
  other = 5 points

tech_fit_score:
  uses_salesforce == "Yes" AND has_no_enrichment_tool = 25 points
  uses_salesforce == "Yes" = 20 points
  uses_hubspot == "Yes" = 15 points
  other = 0 points

funding_score:
  funding_stage == "Series A" or "Series B" = 25 points
  funding_stage == "Series C" or above = 15 points
  other = 0 points

Max score: 100
```

**Clay formula (full ICP score):**
```
{{
  IF(NUMBER(employee_count) >= 50 AND NUMBER(employee_count) <= 200, 30,
    IF(NUMBER(employee_count) >= 201 AND NUMBER(employee_count) <= 500, 25,
      IF(NUMBER(employee_count) >= 20, 15, 5)))
  +
  IF(hq_country == "US", 20, IF(hq_country == "UK" OR hq_country == "CA" OR hq_country == "AU", 15, 5))
  +
  IF(uses_salesforce == "Yes", 20, IF(uses_hubspot == "Yes", 15, 0))
  +
  IF(funding_stage == "Series A" OR funding_stage == "Series B", 25, IF(CONTAINS(funding_stage, "Series"), 15, 0))
}}
```

**ICP tier label:**
```
{{IF(icp_score >= 70, "Tier A — Hot", IF(icp_score >= 45, "Tier B — Warm", "Tier C — Cold"))}}
```

---

## Hands-On Exercise

On your test table, add these columns:
1. Apollo Company Search → employee_count, industry, hq_country
2. `size_tier` formula
3. `icp_score` formula (build the scoring logic above)
4. `icp_tier` label formula

After running:
- How many rows are Tier A?
- What's the average ICP score?
- Which companies scored highest? Does it match your intuition?

---

## Anki Cards to Create

```
Q: What 5 company data fields matter most for GTM enrichment?
A: employee_count, industry, hq_country, funding_stage, tech_stack

Q: What does Clearbit add that Apollo Company Search doesn't?
A: Exact funding amount + tech stack detection (Apollo has limited tech data)

Q: What is the best Claygent use case for tech stack detection?
A: Prompt it to read the company's careers page job postings and extract CRM/tool mentions

Q: Which funding stages are the highest-priority GTM prospects?
A: Series A and Series B — actively building GTM, have budget, evaluating tools

Q: What formula checks if a company uses Salesforce from a tech array?
A: {{IF(CONTAINS(tech_stack, "Salesforce"), "Yes", "No")}}
```

---

## Next Module

→ [02_intermediate/03_claygent_basics.md](./03_claygent_basics.md) — Introduction to Claygent: web research for custom data
