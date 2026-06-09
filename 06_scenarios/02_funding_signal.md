# Scenario 2 — The Funding Signal Pipeline

**Challenge:** When a target company raises Series B, automatically enrich 3 key contacts (CEO, CTO, VP Sales) and create personalized HubSpot tasks within 10 minutes — no manual work.

**Difficulty:** Expert  
**Requires:** Clay API + n8n + Supabase + HubSpot

---

## The Trigger

Signal source options:
- Crunchbase Pro alerts → webhook to n8n
- TechCrunch RSS feed → n8n RSS trigger
- Manual signal entry (for testing): n8n form or direct API call

---

## n8n Workflow 1: Signal Intake

```
[Webhook / RSS Trigger]
    ↓
[Function: Validate company]
  - Company in ICP? (B2B SaaS, 50–500 employees, US/UK)
  - Series A or B? (not Seed, not Series C+)
  - Not already in pipeline?
    ↓ (if valid)
[Function: Build Clay rows]
  Create 3 target rows:
  Row 1: {company_name}, {domain}, "VP of Sales", signal="Series B $Xm"
  Row 2: {company_name}, {domain}, "Head of Revenue Operations", signal="Series B $Xm"
  Row 3: {company_name}, {domain}, "CTO", signal="Series B $Xm"
    ↓
[HTTP Request: Clay API — add row × 3]
  POST /tables/{table_id}/rows for each target role
    ↓
[Wait: receive Clay webhook when enrichment completes]
```

---

## Clay Table: `funding-signals`

Configure with auto-enrich ON.

Enrichment columns:
1. Apollo People Search (job_title input + company_domain)
2. Prospeo fallback
3. Apollo Company Search (employee_count, funding confirmed)
4. Claygent: verify funding signal and add specifics
5. AI opener: using funding signal + role

Claygent funding prompt:
```
Search for recent funding news about {company_name}. Check Crunchbase and TechCrunch.
Confirm: did they raise funding in the last 30 days?
If yes: return "CONFIRMED: [Round] [Amount] [Date]"
If not confirmed: return "Signal unconfirmed"
Max 20 words.
```

AI opener (for VP Sales role):
```
Contact: {first_name}, VP Sales at {company_name}
Signal: {claygent_funding}
Company: {employee_count} employees, just raised growth capital

Write 1 sentence opener (max 25 words):
- Reference the funding specifically
- Connect to the outbound scaling challenge that comes after Series B
- Sound like you know what VP Sales ops look like at this stage

Output: sentence only.
```

---

## n8n Workflow 2: Enrichment Complete → HubSpot

```
[Clay Webhook Trigger]
    ↓
[Function: Parse enriched row]
    ↓
[IF: Email found AND ICP qualifies?]
    ↓ (true)
[Supabase: INSERT enriched_leads]
    ↓
[HubSpot: Create/Update Contact]
  Properties: email, name, company, icp_score, signal_text, ai_opener
    ↓
[IF: Tier A AND funding confirmed?]
    ↓ (true)
[HubSpot: Create Task]
  Title: "Funding signal — reach out within 24hrs: {ai_opener}"
  Due: tomorrow
```

---

## Time Target

Signal received → HubSpot task created: **< 10 minutes**

Bottlenecks that add time:
- Apollo: ~2 seconds per row
- Claygent: ~15–30 seconds per row (the main bottleneck)
- n8n processing: ~5 seconds

For 3 contacts: ~(3 × 30s Claygent) + overhead = ~2–3 minutes Clay enrichment time + n8n time = typically 5–8 minutes total.

If Claygent is too slow: skip it. The funding signal is already in the `signal_source` column from your n8n intake. AI opener can use that directly without Claygent confirmation.
