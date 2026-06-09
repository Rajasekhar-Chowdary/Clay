# Scenario 4 — The Job Change Play

**Challenge:** Detect when ICP contacts change jobs and trigger outreach within 48 hours.

**Why it works:** People who just started a new job are in evaluation mode for 30–90 days. They inherit problems with the existing stack and are most open to change. Highest-converting signal for B2B tools.

---

## The Setup

### Source of Job Change Signals

**Option A: LinkedIn Sales Navigator** (if you have access)
- Set up "Job change alerts" for your saved accounts/contacts
- Export weekly to CSV → import to Clay

**Option B: Apollo re-enrichment loop**
- Run Apollo People Search on your existing contacts monthly
- Compare current title + company to last enriched title + company
- If different → job change detected

**Option C: PhantomBuster LinkedIn scraper**
- Monitor a list of target LinkedIn profiles
- Alert when title or company changes
- Export change events to Clay via webhook

---

## Clay Table: `job-changes`

### Columns

```
Input: first_name, last_name, old_company, old_title, old_email
       new_company_name, new_company_domain (from job change source)

Email waterfall (for new company):
  email_apollo_new (new company domain)
  email_prospeo_new
  email_findymail_new

Formula:
  email_new_final → COALESCE of new waterfall
  job_change_confirmed → IF(new_company_domain != old_company_domain, "Confirmed", "Same company")

Company enrichment (new company):
  employee_count_new, industry_new, hq_country_new, funding_stage_new

ICP score for new company:
  icp_score_new

Claygent: new company description
  "Visit {new_company_domain}. What does this company sell in 15 words? Return: '[description]'. If not found: 'Description not found'."

AI opener (for job change context):
  "Contact: {first_name}, just joined {new_company_name} as {new_title}.
  Previously was at {old_company}.
  New company: {company_description_new}
  
  Write 1 sentence opener (max 25 words):
  Reference the job change naturally ('I saw you recently joined...')
  Connect to a challenge they'd face building GTM at a new company from scratch.
  Output: sentence only."
```

### The 48-Hour Urgency Formula

```
Column: days_since_job_change
Formula: {{DATEDIFF(TODAY(), job_change_date)}}

Column: outreach_urgency
Formula: {{IF(days_since_job_change <= 7, "URGENT — this week", IF(days_since_job_change <= 30, "Priority — this month", "Standard"))}}
```

---

## Routing Logic

Job change leads should go to a dedicated HubSpot sequence:

- Days 1–7 after change: High-priority sequence (personalized, reference the change directly)
- Days 8–30: Normal priority (they've settled in, still evaluating)
- Days 31–60: Nurture (window is closing)
- Days 60+: Cold again (they've decided on tools)

---

## What Makes This Play Powerful

You're reaching out to someone who:
1. Is new to their role → hasn't inherited loyalty to existing vendors
2. Has budget authority starting fresh → actively evaluating all tools
3. Has a fresh mandate to improve GTM → your product is directly relevant
4. Isn't bored of hearing from you yet → no prior rejected outreach

The personalization angle writes itself: "Starting a new role means the first 90 days is often about inheriting the data quality problem."
