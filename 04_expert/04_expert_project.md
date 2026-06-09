# Expert Project — Full-Stack Real-Time Signal Pipeline

**Objective:** Build a production signal-triggered enrichment pipeline that takes a company name → enriched contacts in HubSpot in under 10 minutes, zero manual steps.

**Estimated time:** 8–12 hours over multiple sessions  
**Pass criteria:** End-to-end pipeline working, < 10 minute lead time, documented metrics, portfolio-ready case study

---

## What You're Building

```
SIGNAL INPUT (funding, job change, hiring signal)
    ↓
n8n: signal validation + ICP pre-check
    ↓
Clay API: add 3 target roles at the signaling company
    ↓
Clay: auto-enrich (email waterfall + company data + Claygent signal + AI opener)
    ↓
Clay webhook: fire when enrichment complete
    ↓
n8n: route by ICP tier
    ├── Tier A → Supabase INSERT + HubSpot CREATE + HubSpot TASK
    └── Tier B → Supabase INSERT + HubSpot CREATE
```

This is the architecture that processes 3 leads per funding event, enriches them, and has them in HubSpot with a personalized opener ready for the sales rep — all within 10 minutes of the signal.

---

## Phase 1: Production Clay Table Setup

### Table: `signals-realtime`

Create a new table specifically for signal-triggered leads. Don't reuse your test table.

**Table settings:**
- Name: `signals-realtime-[your-name]`
- Auto-enrich: ON (this is production — signals should enrich immediately)
- Duplicate detection: ON (match on email)

**Required columns (in order):**

```
Input columns:
  first_name, last_name, company_name, company_domain
  job_title (target role), linkedin_url (optional)
  signal_source, signal_date, signal_amount (for funding)
  added_via (always set to "API")

Company enrichment:
  company_data → Apollo Company Search (employee_count, industry, hq_country)

Email waterfall:
  email_apollo, email_prospeo, email_findymail, email_dropcontact

Claygent columns:
  claygent_tech → Tech stack (gated: employee_count >= 50)
  claygent_signal → Signal verification + detail (gated: email found)

Formula columns:
  email_final, email_source, coverage_status
  size_tier, icp_score, icp_tier
  signal_tier, primary_signal_text
  data_source (GDPR audit trail)

AI column:
  ai_opener (gated: email found AND icp_score >= 50)

HubSpot action:
  hubspot_sync (gated: email found AND icp_tier != Tier C)

Webhook action:
  webhook_n8n (gated: email found)
```

---

## Phase 2: n8n Signal Intake Workflow

Build this n8n workflow to receive signals and add rows to Clay.

### Workflow: "Signal Intake → Clay Row Creation"

```
[Webhook Trigger]
 URL: /webhook/signal-intake
 Auth: Header (X-Signal-Secret)
    ↓
[Function: Validate Payload]
 Check required fields: company_name, company_domain, signal_type
 If missing: respond 400 with error
    ↓
[IF: ICP Pre-check]
 Condition: signal_type in ["Series A", "Series B", "Leadership Hire", "RevOps Hiring"]
 AND company_domain matches known patterns (not personal blogs, etc.)
    ↓ (True branch)
[Function: Prepare Clay Rows]
 Build 3 rows for target roles:
   - Row 1: VP Sales at company
   - Row 2: Head of Revenue Operations at company
   - Row 3: CTO or VP Engineering at company (secondary target)
    ↓
[Loop over rows]
    ↓
[HTTP Request: Add to Clay API]
 POST to Clay API /tables/{id}/rows
 Body: {data: {first_name: "", last_name: "", company_name: ..., signal_source: ..., added_via: "API"}}
 (Note: Clay will find the actual person — we're adding a placeholder with the role)
    ↓
[Wait: 30 seconds]
 (Allow Clay to begin enrichment)
    ↓
[Respond to Webhook: 200 OK]
```

**Signal intake test:**

```bash
curl -X POST https://your-n8n.com/webhook/signal-intake \
  -H "X-Signal-Secret: your-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "company_domain": "acmecorp.com",
    "signal_type": "Series B",
    "signal_amount": "$25M",
    "signal_date": "2026-06-09"
  }'
```

---

## Phase 3: Clay Webhook → n8n Routing Workflow

Build the second n8n workflow that receives enriched rows from Clay.

### Workflow: "Clay Enrichment Complete → Route + Store"

```
[Webhook Trigger]
 URL: /webhook/clay-enrichment-complete
 Auth: Header (X-Clay-Secret)
    ↓
[Function: Parse Clay Payload]
 Extract all fields from Clay JSON
 Parse icp_score as integer
    ↓
[Supabase: INSERT enriched_leads]
 Always insert — regardless of tier
 Fields: email, name, company, icp_score, icp_tier, signal, ai_opener, enriched_at
    ↓
[IF: Tier A or B?]
 Condition: icp_tier == "Tier A" OR icp_tier == "Tier B"
    ↓ (True branch)
[HubSpot: Create or Update Contact]
 Fields: email, name, company, job_title, custom: icp_score, icp_tier, signal_tier, ai_opener
    ↓
[IF: Tier A with Tier 1 signal?]
 Condition: icp_tier == "Tier A" AND signal_tier == "Tier 1 — Immediate"
    ↓ (True branch)
[HubSpot: Create Task]
 Title: "Signal outreach — 24hr window: {ai_opener}"
 Due date: tomorrow
 Assign to: sales rep owner
    ↓
[Supabase: INSERT enrichment_log]
 Log: row_id, timestamp, status, hubspot_created, task_created
```

---

## Phase 4: Testing End-to-End

### The 10-Minute Test

1. Send a test signal to your signal intake webhook
2. Start a timer
3. Watch Clay: does the row appear?
4. Does auto-enrich start running?
5. Watch n8n: does the routing workflow trigger?
6. Check Supabase: did the row get inserted?
7. Check HubSpot: did the contact appear?
8. Stop the timer. What was the total elapsed time?

**Target: < 10 minutes from signal to contact in HubSpot**

If it's over 10 minutes, the bottleneck is usually:
- Claygent (slow per-row — reduce number of Claygent columns)
- Auto-enrich delay (Clay processes rows in queue — if table is busy, wait longer)
- n8n execution time (optimize by parallelizing Supabase and HubSpot writes)

### Reliability Test

Run 10 different companies through the pipeline. Measure:
- How many resulted in contacts in HubSpot? (target: 80%+)
- How many had AI openers generated? (target: 75%+)
- Any n8n errors? (target: 0 per 10 runs)
- Average time from signal to HubSpot: (target: < 10 min)

---

## Phase 5: Monitoring and Observability

Production pipelines need monitoring.

### Supabase Monitoring Queries

```sql
-- Enrichment success rate today
SELECT 
  COUNT(*) as total,
  COUNT(CASE WHEN email IS NOT NULL THEN 1 END) as enriched,
  ROUND(COUNT(CASE WHEN email IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100, 1) as coverage_rate
FROM enriched_leads
WHERE enriched_at > NOW() - INTERVAL '24 hours';

-- Signal breakdown
SELECT 
  signal_tier,
  icp_tier,
  COUNT(*) as count
FROM enriched_leads
WHERE enriched_at > NOW() - INTERVAL '7 days'
GROUP BY signal_tier, icp_tier
ORDER BY count DESC;

-- Average enrichment time (if you track it)
SELECT AVG(EXTRACT(EPOCH FROM (enriched_at - signal_received_at))/60) as avg_minutes
FROM enriched_leads
WHERE enriched_at > NOW() - INTERVAL '7 days';
```

---

## Deliverables for Portfolio

When this pipeline is working, document it as Portfolio Project 3:

**Case study structure:**
```
Title: Real-Time Signal-Triggered GTM Enrichment Pipeline

Problem:
B2B sales teams miss the 48-hour window after funding signals because 
research and enrichment take too long to execute manually.

Solution:
Built an automated pipeline that detects funding and leadership signals,
enriches 3 target contacts per event, and delivers personalized outreach-ready
records to HubSpot within 10 minutes — zero manual steps.

Tech Stack:
Clay (enrichment) → n8n (orchestration) → Supabase (store) → HubSpot (activate)

Results:
- Average signal → HubSpot time: X minutes
- Email coverage on signal-triggered leads: X%
- Contacts processed per week: X
- Credits per enriched lead: X.X
- HubSpot tasks auto-created per Tier A signal: X

Architecture diagram: [screenshot]
Clay table screenshot: [screenshot]
n8n workflow screenshots: [screenshot]
Supabase query output: [screenshot]
```

---

## You've Completed Phase 4 When:

- [ ] Production Clay table built with all 20+ columns
- [ ] n8n signal intake workflow working
- [ ] n8n routing workflow working
- [ ] End-to-end test: signal → HubSpot in < 10 minutes
- [ ] 10-run reliability test: 80%+ success rate
- [ ] Supabase monitoring queries returning correct data
- [ ] Case study written with real metrics
- [ ] Screenshots captured for portfolio

Completing this makes you capable of demonstrating production-grade GTM data engineering. This is what Clay-focused GTM Engineer roles actually look for.

→ [06_scenarios/](../06_scenarios/) — 5 competition-level playbooks to clone and extend
