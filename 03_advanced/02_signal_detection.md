# Module 3.2 — Signal Detection and Intent-Based Enrichment

**Time:** 75–90 minutes  
**Focus:** What signals are, how to detect them in Clay, and how to turn them into outreach triggers

---

## Why Signals Change Everything

Cold outreach without signals: 2–4% reply rate  
Signal-triggered outreach: 8–15% reply rate

The difference is timing and relevance. A signal means something changed — and change creates action. When you reach out exactly when someone is in a buying moment, you're not interrupting, you're showing up at the right time.

---

## The Signal Hierarchy

Not all signals are equal. Tier them by buying intent:

### Tier 1: High Intent (Reach out within 48 hours)

| Signal | What it means | Source |
|--------|--------------|--------|
| **New VP of Sales/CRO hired** | New exec = new tool evaluations, new budget | LinkedIn job change |
| **Series A or B funding** | Growth capital = active investment in GTM | Crunchbase, TechCrunch |
| **Open RevOps/GTM Engineer role** | No internal solution = they're buying | Job boards |
| **CRM migration posted** | "We're moving to Salesforce" = in-market | Job postings, LinkedIn posts |

### Tier 2: Medium Intent (Reach out within 1–2 weeks)

| Signal | What it means | Source |
|--------|--------------|--------|
| **Headcount grew >20% in 6 months** | Scaling = GTM tool pressure | LinkedIn headcount data |
| **New product launch** | Marketing push = more leads needed | Company blog, press |
| **Competitor acquired** | Disruption = evaluation of alternatives | TechCrunch |
| **LinkedIn post about scaling outbound** | In-market awareness post | LinkedIn |

### Tier 3: Weak Intent (Longer nurture, not immediate outreach)

| Signal | What it means | Source |
|--------|--------------|--------|
| **Company recently IPO'd** | Budget available but process is complex | Financial news |
| **Conference presentation** | Thought leader = engaged with topic | Event agendas |
| **Tech stack change** | Evaluating alternatives | BuiltWith change alerts |

---

## Building Signal Detection in Clay

### Signal Detection Strategy

For each signal type, you need:
1. A Claygent or provider column that detects the signal
2. A formula column that normalizes the output (binary: signal found / not found)
3. An AI column that uses the signal for personalization

### Signal 1: Funding Detection

**Claygent column: `signal_funding`**
```
Search for news about {company_name} raising a funding round in the last 12 months.
Search TechCrunch, Crunchbase, VentureBeat, Business Insider, and {company_domain}/news.
If funding found: return "FUNDING: [Round type] [amount if available] [approximate date]" — example: "FUNDING: Series B $25M Q1 2026"
If not found: return "No funding"
Max 25 words.
```

**Formula: `has_funding_signal`**
```
{{IF(CONTAINS(signal_funding, "FUNDING:"), "Yes", "No")}}
```

**Formula: `funding_details`**
```
{{IF(has_funding_signal == "Yes", REPLACE(signal_funding, "FUNDING: ", ""), "")}}
```

---

### Signal 2: Leadership Change (New Exec Hire)

**Claygent column: `signal_leadership`**
```
Search LinkedIn for recent job changes at {company_name} in the last 6 months.
Look specifically for new hires in these roles: VP Sales, Chief Revenue Officer, Head of Growth, VP Marketing, Head of Revenue Operations, Director of Sales.
If found: return "HIRE: [Name] joined as [Title] in [Month/Year]"
If not found: return "No leadership signal"
Max 30 words.
```

**Formula: `has_leadership_signal`**
```
{{IF(CONTAINS(signal_leadership, "HIRE:"), "Yes", "No")}}
```

---

### Signal 3: RevOps/GTM Hiring

**Claygent column: `signal_hiring`**
```
Visit {company_domain}/careers and search for open positions.
Also check https://jobs.lever.co/{company_domain_clean} and https://boards.greenhouse.io/{company_domain_clean}.
Look for job titles containing: RevOps, Revenue Operations, GTM, Sales Operations, Marketing Operations, Data Engineer, Growth Engineer.
If found: return "HIRING: [Job Title]" for the most relevant role found.
If not found: return "No GTM hiring"
Max 20 words.
```

**Formula: `has_hiring_signal`**
```
{{IF(CONTAINS(signal_hiring, "HIRING:"), "Yes", "No")}}
```

---

### Signal 4: LinkedIn Content Signal

**Claygent column: `signal_content`**
```
Visit {linkedin_url}.
Find {first_name}'s most recent post in the last 30 days that mentions: outbound, prospecting, data quality, lead enrichment, GTM, scaling, RevOps, or pipeline.
If found: return "CONTENT: [topic in 10 words]"
If no relevant post in 30 days: return "No content signal"
Max 20 words.
```

**Formula: `has_content_signal`**
```
{{IF(CONTAINS(signal_content, "CONTENT:"), "Yes", "No")}}
```

---

### The Master Signal Column

Combine all signals into a single priority column:

**Formula: `signal_tier`**
```
{{IF(
  has_leadership_signal == "Yes" OR has_funding_signal == "Yes",
  "Tier 1 — Immediate",
  IF(
    has_hiring_signal == "Yes",
    "Tier 2 — This Week",
    IF(
      has_content_signal == "Yes",
      "Tier 3 — Nurture",
      "No Signal — Cold"
    )
  )
)}}
```

**Formula: `primary_signal_text`** (the signal to use in outreach)
```
{{COALESCE(
  IF(has_funding_signal == "Yes", funding_details, ""),
  IF(has_leadership_signal == "Yes", signal_leadership, ""),
  IF(has_hiring_signal == "Yes", signal_hiring, ""),
  IF(has_content_signal == "Yes", signal_content, "")
)}}
```

This gives you one column with the best available signal, in priority order.

---

## Signal-Based AI Personalization

Once you have `primary_signal_text` populated, use it in your AI column:

```
You are writing a cold email opening line for a B2B sales rep.

Contact: {first_name} {last_name}, {job_title} at {company_name}
Signal: {primary_signal_text}
CRM in use: {crm_detected}

Rules:
- Reference the signal SPECIFICALLY — not generically
- Connect to a GTM data, enrichment, or pipeline challenge
- Sound like a human who did real research, not a template
- MAX 25 words
- No "I hope this finds you well" or "I wanted to reach out"
- Output ONLY the sentence

If signal is empty or "No Signal — Cold": write a generic but professional opener based on their industry and company size instead.
```

---

## Signal Routing: What to Do With Each Tier

After detecting signals, you need a routing strategy:

```
Tier 1 (Leadership hire or Funding):
→ Export to HubSpot immediately
→ Create HubSpot Task: "Reach out within 24 hours — [signal details]"
→ Add to priority sequence

Tier 2 (Hiring signal):
→ Export to HubSpot
→ Add to nurture sequence with signal-specific messaging
→ Set follow-up reminder: 7 days

Tier 3 (Content signal):
→ Comment on their LinkedIn post first (warm touchpoint)
→ Wait 48 hours, then send connection request
→ After connection: send email with content reference

No Signal (Cold):
→ Add to cold sequence (lower priority)
→ OR hold until signal appears (set up re-enrichment schedule)
```

---

## Automating Signal Detection: The Re-Enrichment Loop

Signals are time-sensitive. A list enriched today may have stale signals in 30 days.

**Basic re-enrichment loop:**
1. Export your table → import back with a new "re_enrich_date" column
2. Run signal Claygent columns on all rows where re_enrich_date is > 30 days ago
3. Compare new signals to old signals — rows where signal changed are your hottest prospects
4. This is the beginning of the real-time signal pipeline you'll build in Phase 4

**Formula for stale detection:**
```
{{IF(DATEDIFF(TODAY(), last_enriched_date) > 30, "Stale — re-enrich", "Fresh")}}
```

---

## Hands-On Exercise

Add signal detection to your 100-row table:

1. Add `signal_funding` Claygent column (test on 10 rows first)
2. Add `signal_hiring` Claygent column (test on 10 rows)
3. Add `has_funding_signal` and `has_hiring_signal` formula columns
4. Add `signal_tier` formula column
5. Add `primary_signal_text` formula column
6. Update your AI opener to use `primary_signal_text`

After running:
- How many Tier 1 signals found?
- How many Tier 2?
- What % of your 100 rows have at least one signal?
- What did your best AI opener look like?

---

## Anki Cards to Create

```
Q: What reply rate can signal-triggered outreach achieve vs. cold outreach?
A: Signal-triggered: 8–15%. Cold outreach: 2–4%.

Q: What are the Tier 1 signals (reach out within 48 hours)?
A: New VP Sales/CRO hire, Series A/B funding, open RevOps role, CRM migration announcement

Q: What is the `primary_signal_text` column and how is it built?
A: COALESCE of all signal columns in priority order — returns the best signal for AI personalization

Q: Why do signals go stale, and how do you handle it?
A: Signals are time-sensitive (jobs get filled, hires settle in). Re-enrich after 30 days using DATEDIFF to detect stale rows.

Q: What should you do with a Tier 1 signal row?
A: Export to HubSpot immediately, create a task for 24-hour follow-up, add to priority sequence
```

---

## Next Module

→ [03_advanced/03_ai_personalization.md](./03_ai_personalization.md) — AI columns: generating openers, subject lines, and snippets at scale
