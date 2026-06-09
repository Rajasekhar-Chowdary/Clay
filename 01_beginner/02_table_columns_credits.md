# Module 1.2 — Tables, Columns, and the Credits System

**Time:** 45–60 minutes (30 min reading + 30 min hands-on)  
**Prerequisite:** Module 1.1 (mental model)  
**Hands-on requirement:** You must create a real Clay table during this module.

---

## Part A: Creating and Managing Tables

### Creating Your First Table

In Clay, click **"New Table"** → you get three options:
- **Start from scratch** — blank table, add rows manually
- **Import CSV** — upload a spreadsheet
- **Use a template** — pre-built tables (useful later, skip for now)

For learning: always start from scratch or import a small CSV. Don't use templates until you understand what they're doing.

### Table Settings (the hidden details)

After creating a table, click the gear icon (table settings). Key settings:

| Setting | What it does | Recommended |
|---------|-------------|-------------|
| Auto-enrich | Automatically runs all enrichment columns when a row is added | **OFF** for learning — turn on for production only |
| Duplicate detection | Prevents adding the same contact twice (matched on email or LinkedIn URL) | **ON** always |
| Row limit | Cap how many rows can be in the table | Set when building production tables |

**Critical rule:** Keep auto-enrich OFF until your waterfall is fully tested. One misconfigured waterfall with auto-enrich on = all credits gone in minutes.

### Importing a CSV

When importing:
1. Clay auto-detects column headers — review them before confirming
2. Map your columns to Clay's standard fields (first name, last name, email, company name, domain)
3. **Always include company domain** — most enrichment providers use domain, not company name, as the primary lookup key

**Column mapping gotcha:** If your CSV has "Company" but Clay expects "Company Name", map it manually. Mismatches silently break enrichment.

---

## Part B: Column Deep Dive

### Adding an Enrichment Column

1. Click **"+"** to add a new column
2. Search for the provider (e.g., "Apollo")
3. Select the specific enrichment type (e.g., "People Search" vs "Company Search")
4. **Map inputs** — tell Clay which columns contain the inputs this provider needs
5. **Configure outputs** — select which fields the provider should return (email, title, phone, LinkedIn URL, etc.)
6. **Set run conditions** — when should this column run? (always / only if email is empty / only if company matches X)

### The Run Condition (Most Important Setting)

The run condition is what makes the waterfall work.

```
Column: email_apollo (Apollo People Search)
Run condition: Always

Column: email_hunter (Hunter.io)
Run condition: Only if [email_apollo] is empty

Column: email_findymail (Findymail)
Run condition: Only if [email_apollo] is empty AND [email_hunter] is empty
```

Without run conditions, every provider runs on every row. That's the credit fire mistake.

In Clay's UI, this is called **"Skip row if..."** or **"Only run if..."** — it appears when you configure the column.

### Output Field Selection

Each provider can return many fields. Select only what you need.

Apollo People Search can return: email, phone, LinkedIn URL, job title, seniority level, company domain, location, department, social profiles, and more.

**Select more = same credit cost, more data.** But keep it organized — too many columns becomes unmanageable. For beginners:

Must-select outputs from Apollo People Search:
- Email
- Job Title
- LinkedIn URL
- First/Last Name (to verify the match)

Optional for later:
- Phone
- Seniority
- Department

### Formula Columns

Formula columns transform existing data — no credits, instant.

**Syntax:** `{{column_name}}`

```
Full name: {{first_name}} {{last_name}}

Company + title: {{job_title}} at {{company_name}}

Email domain: {{SPLIT(email, "@")[1]}}

Conditional label:
{{IF(employee_count > 500, "Enterprise", IF(employee_count > 100, "Mid-Market", "SMB"))}}

Fallback (use first non-empty value):
{{COALESCE(email_apollo, email_hunter, email_findymail)}}
```

**The COALESCE pattern** is how you consolidate your waterfall results into a single `email_final` column. Every table should have one.

---

## Part C: Credits Deep Dive

### The Credit Ledger

In your Clay account, go to **Settings → Credits**. You'll see:
- Credits remaining
- Credits used this month
- Transaction log (every credit spend, with which column and row)

The transaction log is your forensic tool when credits disappear unexpectedly.

### Credit Cost Reference

| Action | Cost |
|--------|------|
| Apollo People Search (email + data) | 1 credit |
| Hunter.io email find | 1 credit |
| Findymail email find + verify | 1 credit |
| Apollo Company Search (firmographics) | 1 credit |
| Clearbit Company enrichment | 1 credit |
| Claygent (simple prompt, 1 page) | 2 credits |
| Claygent (multi-page research) | 3–5 credits |
| AI column (GPT/Claude prompt) | 0.5–1 credit |
| Formula column | 0 credits (always free) |
| HTTP column (custom API) | 1 credit per call |

### Credit Budget Planning

Before running enrichment on a full table:

```
Expected credit spend = rows × average credits per row

Example: 500 rows, 4-provider waterfall
Estimate:
  - 50% found in round 1 (Apollo): 500 × 0.5 × 1 = 250 credits
  - 20% found in round 2 (Prospeo): 500 × 0.2 × 2 = 200 credits
  - 15% found in round 3 (Findymail): 500 × 0.15 × 3 = 225 credits
  - 15% not found: 500 × 0.15 × 4 = 300 credits

Total estimated: ~975 credits for 500 rows
Add Claygent on unfound 15%: 75 rows × 3 credits = 225 more
Grand total: ~1,200 credits

On Starter plan (2,000/month): affordable.
On Free tier (100/month): run max 10 rows.
```

### The 5-Row Test Protocol

Every time you configure a new enrichment column:
1. Select 5 rows in the table
2. Click "Run" for just those rows
3. Review what came back: correct data? right format? credits consumed as expected?
4. If good → run on full table
5. If bad → fix the column config, re-test 5 rows, then run full

This protocol saves more credits than any other single habit.

---

## Part D: Reading the Run History

After running enrichment, click on any row → **"Run History"** tab. You'll see:

```
Column: email_apollo
Status: Found
Email: jane.smith@salesforce.com
Title: VP of Revenue Operations
Credits used: 1
Timestamp: 2026-06-09 14:23:01
Provider response time: 847ms
```

Or:

```
Column: email_apollo
Status: Not found
Reason: No match for Jane Smith at salesforce.com
Credits used: 1
```

**Debugging pattern:** If coverage is low, open run history for 10 failing rows. Look for patterns:
- All failing on bad domain? → Fix the domain column
- Provider returning data but wrong person? → Add more input fields (job title, city)
- Provider times out? → Retry or switch provider order

---

## Hands-On Exercise

**Do this now (estimated: 30 minutes)**

1. Create a new Clay table named "learning-test-01"
2. Add these 5 rows manually:

| first_name | last_name | company_name | company_domain |
|------------|-----------|-------------|----------------|
| Leandra | Witchger | Notion | notion.so |
| Howie | Liu | Airtable | airtable.com |
| Kim | Hahn | Typeform | typeform.com |
| Annie | Pearl | Calendly | calendly.com |
| Marcus | Bragg | Loom | loom.com |

3. Add an Apollo People Search column
   - Inputs: first_name, last_name, company_domain
   - Outputs: email, job_title, linkedin_url
   - Run condition: Always

4. Run on all 5 rows (manually, not auto-enrich)
5. Note: How many credits did this cost? What was your coverage? Open run history for any failed rows.
6. Add a Formula column: `{{first_name}} {{last_name}} — {{job_title}} at {{company_name}}`
7. Write your results in `00_meta/progress_tracker.md`

---

## Recall Practice

Answer without looking:

1. Where do you set the run condition for a waterfall column?
2. What does the COALESCE formula do in a waterfall?
3. How many credits does a 4-provider waterfall use per row when the third provider succeeds?
4. What is the 5-row test protocol and why does it matter?
5. How do you find out exactly why a specific row failed enrichment?
6. What's the difference between auto-enrich ON vs OFF? When should each be used?

---

## Anki Cards to Create

```
Q: What does auto-enrich do and why should it be OFF during learning?
A: Automatically runs all enrichment columns when a row is added. Keep OFF during learning — one misconfigured waterfall = all credits burned instantly.

Q: Formula for combining Apollo + Hunter + Findymail into one email column
A: {{COALESCE(email_apollo, email_hunter, email_findymail)}}

Q: How many credits does a 4-provider waterfall cost when provider 2 (out of 4) succeeds?
A: 2 credits (paid for provider 1 attempt + provider 2 success; providers 3+4 skipped)

Q: What is the 5-row test protocol?
A: Select 5 rows, run enrichment, review results + credits consumed. Fix before full run.

Q: Where do you see the exact reason a row failed enrichment?
A: Row → Run History tab → shows provider response, status, credits used

Q: What Clay column type costs 0 credits?
A: Formula columns (they compute from existing data, no API calls)

Q: What input do most Clay providers prefer over company name?
A: Company domain (e.g., salesforce.com) — more reliable than company name strings
```

---

## Next Module

→ [01_beginner/03_first_waterfall.md](./03_first_waterfall.md) — Build your first 2-provider waterfall and measure coverage
