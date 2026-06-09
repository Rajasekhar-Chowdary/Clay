# Module 3.4 — Clay Integrations: Webhook, HubSpot, and n8n

**Time:** 75–90 minutes  
**Focus:** Getting enriched data out of Clay and into your downstream systems

---

## The Output Architecture

Clay's job ends when enrichment is complete. Getting data into action (CRM, sequences, database) is what integrations do.

```
Clay Table (enriched)
    │
    ├── Option A: Manual CSV export (fine for one-off projects, not production)
    ├── Option B: HubSpot direct integration (best for direct CRM write)
    ├── Option C: Webhook to n8n (best for complex routing logic)
    └── Option D: Clay API (best for programmatic table management)
```

Production pipelines use Option B + Option C together:
- HubSpot integration for direct contact creation
- Webhook to n8n for complex logic (scoring thresholds, Supabase writes, error handling)

---

## Option A: CSV Export

When to use: Testing, one-off enrichment, sharing data with a team that doesn't use your CRM.

Steps:
1. Click "Export" at the top of any Clay table
2. Select which columns to include
3. Choose format: CSV or Excel
4. Download → import into your tool

Limitation: Manual. No automation. No syncing.

---

## Option B: HubSpot Direct Integration

Clay has a native HubSpot integration — one of the best in its category.

### Setup (One Time)

1. In Clay: Settings → Integrations → HubSpot
2. Authenticate with your HubSpot account
3. Select your HubSpot portal (if you have multiple)
4. Test connection

### Building the HubSpot Action Column

1. Add a new column → search "HubSpot" → select "Create or Update Contact"
2. Configure:
   - **Action type:** "Create or Update" (not just Create — handles duplicates)
   - **Match field:** Email (HubSpot will match on this to prevent duplicates)
3. Map fields:

| Clay Column | HubSpot Property |
|-------------|-----------------|
| email_final | Email |
| first_name | First Name |
| last_name | Last Name |
| company_name | Company |
| company_domain | Company Domain |
| job_title | Job Title |
| employee_count | Number of Employees |
| hq_country | Country |
| icp_score | Custom property: ICP Score |
| icp_tier | Custom property: ICP Tier |
| signal_tier | Custom property: Signal Tier |
| ai_opener | Custom property: AI Opener |
| email_source | Custom property: Enrichment Source |

4. **Run condition:** Only run if `coverage_status == "Found"` AND `icp_tier != "Tier C"`

Don't push Tier C leads to HubSpot — it clogs your CRM with low-quality contacts.

### Creating Custom HubSpot Properties

Before the first run, create these custom properties in HubSpot (Settings → Properties → Create property):

- `icp_score` (Number)
- `icp_tier` (Single-line text or Dropdown: Tier A, Tier B, Tier C)
- `signal_tier` (Single-line text)
- `ai_opener` (Multi-line text)
- `enrichment_source` (Single-line text)
- `enriched_at` (Date)

These properties let you segment and filter in HubSpot using your Clay enrichment data.

### Deduplication Handling

Clay's "Create or Update Contact" uses email as the deduplication key. If the contact already exists in HubSpot, it updates the existing record. If not, it creates a new one.

This means: running Clay → HubSpot multiple times is safe. It won't create duplicates.

### Adding to HubSpot Lists or Sequences

After creating/updating the contact, add a second HubSpot action column:

- **Add to Static List:** Based on `icp_tier` value
  - Tier A contacts → "Hot Prospects - Q3 2026" list
  - Tier B contacts → "Warm Prospects - Q3 2026" list

- **Enroll in Sequence:** If using HubSpot sequences
  - Only for Tier A contacts with signal_tier == "Tier 1"

---

## Option C: Webhook to n8n

### When to Use Webhook Instead of HubSpot Direct

Use webhook → n8n when:
- You need conditional logic (IF score > 70 → HubSpot, ELSE → Supabase only)
- You need to write to Supabase/database simultaneously
- You want error logging
- You need to transform data before writing to CRM
- You want a single orchestration layer managing all downstream writes

### Setting Up the Clay Webhook Output

1. Add a new column → search "Webhook" → select "HTTP Webhook"
2. Configure:
   - **URL:** Your n8n webhook trigger URL (e.g., `https://n8n.yourdomain.com/webhook/clay-export`)
   - **Method:** POST
   - **Headers:** `{"Content-Type": "application/json", "X-Clay-Secret": "your-secret-key"}`
3. **Payload mapping:** Select which columns to include in the JSON body

### Webhook Payload Structure

Map your columns to a clean JSON structure:

```json
{
  "contact": {
    "first_name": "{{first_name}}",
    "last_name": "{{last_name}}",
    "email": "{{email_final}}",
    "job_title": "{{job_title}}",
    "linkedin_url": "{{linkedin_url}}"
  },
  "company": {
    "name": "{{company_name}}",
    "domain": "{{company_domain}}",
    "size": "{{employee_count}}",
    "industry": "{{industry}}",
    "country": "{{hq_country}}"
  },
  "enrichment": {
    "email_source": "{{email_source}}",
    "icp_score": "{{icp_score}}",
    "icp_tier": "{{icp_tier}}",
    "signal_tier": "{{signal_tier}}",
    "signal_text": "{{primary_signal_text}}",
    "ai_opener": "{{ai_opener}}",
    "enriched_at": "{{TODAY()}}"
  }
}
```

### Webhook Run Condition

```
Only run if: coverage_status == "Found" AND icp_tier != "Tier C"
```

Add a second webhook column for rejected rows (optional but good for logging):
```
Only run if: coverage_status == "Not found"
URL: your-n8n-failed-leads-webhook
```

---

## n8n Workflow: Clay → Supabase + HubSpot

### The Standard Architecture

```
[Clay webhook]
    ↓
[n8n: Webhook Trigger]
    ↓
[n8n: Validate payload] — check required fields exist
    ↓
[n8n: Parse enrichment data]
    ↓
[n8n: Route by ICP tier]
    │
    ├─ Tier A → [n8n: Supabase INSERT] + [n8n: HubSpot Create/Update] + [n8n: Task create]
    ├─ Tier B → [n8n: Supabase INSERT] + [n8n: HubSpot Create/Update]
    └─ Tier C → [n8n: Supabase INSERT only] (don't push to HubSpot)
```

### Key n8n Nodes for this Workflow

**Webhook Trigger:**
```json
{
  "authentication": "Header Auth",
  "headerName": "X-Clay-Secret",
  "headerValue": "{{$env.CLAY_WEBHOOK_SECRET}}"
}
```

**Parse Clay Data (Function node):**
```javascript
const data = $json;
return {
  email: data.contact.email,
  first_name: data.contact.first_name,
  last_name: data.contact.last_name,
  company_name: data.company.name,
  icp_score: parseInt(data.enrichment.icp_score) || 0,
  icp_tier: data.enrichment.icp_tier,
  signal_tier: data.enrichment.signal_tier,
  ai_opener: data.enrichment.ai_opener,
  enriched_at: new Date().toISOString()
};
```

**Supabase INSERT (HTTP Request node):**
```json
{
  "method": "POST",
  "url": "https://[your-project].supabase.co/rest/v1/enriched_leads",
  "headers": {
    "apikey": "{{$env.SUPABASE_ANON_KEY}}",
    "Authorization": "Bearer {{$env.SUPABASE_ANON_KEY}}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
  },
  "body": {
    "email": "{{$json.email}}",
    "first_name": "{{$json.first_name}}",
    "icp_score": "{{$json.icp_score}}",
    "enriched_at": "{{$json.enriched_at}}"
  }
}
```

---

## Testing Your Integration End-to-End

### The 5-Row Integration Test

Before running the full table:

1. Select 5 rows in Clay (pick 1 Tier A, 1 Tier B, 1 Tier C, 1 not found, 1 with signal)
2. Run the webhook action column on these 5 rows only
3. In n8n: check the execution log — did all 5 rows arrive?
4. Check Supabase: did the correct rows get inserted?
5. Check HubSpot: did Tier A and B get created? Did Tier C get skipped?
6. Verify: no duplicates, correct field mapping, correct routing

Only run the full table after this test passes.

### Monitoring the Webhook Run

Clay shows webhook status per row in the run history:
- `200` or `2xx` = success
- `4xx` = your n8n workflow had a logic error (check n8n logs)
- `5xx` = n8n server error
- Timeout = n8n is too slow (add a response node at the start of your workflow)

**Common issue:** Clay webhooks timeout if n8n takes > 30 seconds to respond. Add a "Respond to Webhook" node at the very beginning of your n8n workflow to return 200 immediately, then continue processing.

---

## Hands-On Exercise

Complete the full output pipeline for your 100-row table:

1. Create HubSpot custom properties (icp_score, icp_tier, signal_tier, ai_opener)
2. Add HubSpot action column — map all fields
3. Run condition: only Tier A and B contacts
4. Test on 5 rows
5. Check HubSpot: did they appear correctly?
6. (Bonus) Add webhook column pointing to n8n, add the routing workflow

---

## Anki Cards to Create

```
Q: What deduplication field does Clay's HubSpot integration use?
A: Email — "Create or Update Contact" matches on email and updates if exists

Q: Why use webhook → n8n instead of Clay's direct HubSpot integration?
A: When you need conditional routing logic, Supabase writes, error logging, or data transformation before CRM

Q: What run condition should gatekeeper the HubSpot action column?
A: coverage_status == "Found" AND icp_tier != "Tier C" — only push enriched, qualified leads

Q: What webhook response issue causes Clay to mark rows as failed?
A: n8n taking > 30 seconds — fix with immediate "Respond to Webhook" node returning 200, then continue processing async

Q: What is the standard n8n routing logic for Clay enriched leads?
A: Tier A → Supabase + HubSpot + Task, Tier B → Supabase + HubSpot, Tier C → Supabase only
```

---

## Next Module

→ [04_expert/01_clay_api.md](../04_expert/01_clay_api.md) — Clay API: programmatic row creation and table management
