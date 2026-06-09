# Scenario 1 — The Creator-Impressor

**Challenge:** Enrich 500 B2B contacts to 90%+ email coverage AND generate a unique personalization hook for each one in under 30 minutes of active work.

**Difficulty:** Advanced  
**What it demonstrates:** Waterfall + Claygent + AI personalization in one automated flow with measurable outcome

---

## Setup

**Input:** CSV with 500 contacts (first_name, last_name, company_domain)  
**Target:** 90%+ email coverage + unique AI opener for each enriched contact  
**Time budget:** 30 minutes active work  

---

## Architecture

```
Step 1: Import 500-row CSV
Step 2: Apollo email waterfall (4 providers)
Step 3: Claygent: most recent LinkedIn post topic (gated: icp_score >= 50)
Step 4: AI column: opener based on post (falls back to CRM if no post)
Step 5: HubSpot export: create contact + enroll in sequence
Step 6: Measure: coverage rate, time, credits used
```

---

## The Columns (Build in This Order)

```
Input: first_name, last_name, company_domain, linkedin_url

Company: Apollo Company Search → employee_count, industry, hq_country

Email waterfall:
  email_apollo (always)
  email_prospeo (if apollo empty)
  email_findymail (if above empty)
  email_dropcontact (if above empty)

Formula: email_final, email_source, coverage_status, size_tier, icp_score

Claygent (gated: email found AND icp_score >= 50):
  claygent_post:
  "Visit {linkedin_url}. Find {first_name}'s most recent post in last 90 days.
  Extract the core topic in 15 words. Return: 'Posted about: [topic]'
  If no posts: return 'No recent posts'. If private: return 'Profile not accessible'. Max 25 words."

Formula: has_post → IF(CONTAINS(claygent_post, "Posted about"), "Yes", "No")

AI opener (gated: email found):
  "Write a cold email opening line for {first_name}, {job_title} at {company_name}.
  
  If has_post == 'Yes': Use this insight: {claygent_post}
  Write: 'I saw you recently shared [topic] — [one sentence connecting to GTM/data challenge]'
  
  If has_post == 'No': Use their CRM stack instead: {crm_detected}
  Write: 'Running {crm_detected} without a coverage layer usually means the data problem surfaces eventually...'
  
  MAX 25 words. Output sentence only. No greeting."

HubSpot action (gated: email found AND icp_tier != Tier C):
  Create or Update Contact
  Enroll in sequence: "Signal-Enriched Outreach"
```

---

## Time Allocation (30-Minute Budget)

```
0–5 min:  Import CSV, verify domains, check for obvious data issues
5–10 min: Add all columns (they're pre-configured from your library)
10–12 min: 5-row test on email waterfall — verify stop conditions
12–15 min: 5-row test on Claygent — verify post extraction
15–17 min: 5-row test on AI opener — verify quality
17–20 min: Run full 500-row enrichment (watch progress)
20–25 min: Review coverage metrics, check 5 random AI openers for quality
25–30 min: Export to HubSpot or set up HubSpot action column
```

---

## Success Metrics

After completion, fill in:
```
Total rows: 500
Email found: ___  (target: 90%+ = 450)
Apollo found: ___
Prospeo found: ___
Findymail found: ___
Dropcontact found: ___
Claygent post found: ___
AI opener generated: ___
Credits used: ___
Credits/enriched lead: ___  (target: < 3.0)
Active work time: ___ minutes  (target: ≤ 30)
```

What impresses Clay experts when you share this: specific numbers + showing you measured provider contribution breakdown.
