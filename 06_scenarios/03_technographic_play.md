# Scenario 3 — The Technographic Play

**Challenge:** Find all companies in your ICP using Salesforce but with NO dedicated RevOps/GTM role — prime buying signal for GTM tooling.

**Why it works:** A Salesforce user without RevOps = they feel the pain but haven't solved it yet. Perfect setup.

---

## Step-by-Step

### Step 1: ICP List from Apollo

Pull from Apollo:
- Industry: SaaS, Software, Technology
- Employees: 100–500
- Funding: Series A, B, C
- Geography: US, UK, Canada

Export: company_name, company_domain, employee_count, industry, hq_country

### Step 2: Clay Table — Company Research

Import Apollo list. Add:

**Clearbit company enrichment:**
- tech_stack (what technologies the company uses)
- funding_stage

**Claygent tech_stack (if Clearbit is empty):**
```
Visit {company_domain}/careers and {company_domain}/integrations.
Look for mentions of Salesforce, HubSpot, Pipedrive in job requirements or integration lists.
Return: "CRM: [detected tool]" or "CRM: unknown"
Max 15 words.
```

**Formula: uses_salesforce**
```
{{IF(CONTAINS(tech_stack_clearbit, "Salesforce") OR CONTAINS(tech_stack_claygent, "Salesforce"), "Yes", "No")}}
```

### Step 3: RevOps Job Check

**Claygent: no_revops_role**
```
Visit {company_domain}/careers.
Search for open positions with titles: RevOps, Revenue Operations, GTM Operations, Sales Operations.
If any found: return "HAS RevOps role: [title]"
If none found: return "No RevOps role"
Max 20 words.
```
**Gate:** Only run if uses_salesforce == "Yes" (no point checking companies that don't use Salesforce)

**Formula: is_target**
```
{{IF(uses_salesforce == "Yes" AND CONTAINS(no_revops_role, "No RevOps"), "TARGET", "Skip")}}
```

### Step 4: Decision Maker Enrichment

Filter to `is_target == "TARGET"` rows.

For these companies only, run email waterfall on:
- VP of Sales
- CTO
- CEO

Use Apollo Company → People search filtered to these titles.

### Step 5: AI Opener Using the Technographic Hook

```
Contact: {first_name}, {job_title} at {company_name}
Context: They use Salesforce but have no dedicated RevOps role.

Write 1 sentence (max 25 words):
"You're running Salesforce at {employee_count} people without a RevOps function — [the specific pain that creates]"

Make it specific to their company size and stage. Don't mention you know they don't have RevOps explicitly.

Output: opener only.
```

---

## Expected Output

From 500 Apollo companies:
- ~60% use Salesforce: 300 companies
- ~40% of those have no RevOps role: 120 target companies
- 3 decision-makers per company: 360 enrichment targets
- Email waterfall at 85%: ~306 enriched contacts with personalized openers

That's 306 highly targeted, signal-backed prospects from 500 raw company names.
