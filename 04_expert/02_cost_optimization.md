# Module 4.2 — Cost Optimization and Credit Management

**Time:** 45–60 minutes  
**Focus:** Maximizing coverage per credit, audit techniques, budget planning for scale

---

## The Credit Efficiency Mindset

At beginner level: "did it work?"
At expert level: "what did it cost per qualified lead?"

The goal is not just high coverage. It's high coverage at the lowest credits-per-enriched-lead. These are different objectives and sometimes conflict.

```
Example:
Option A: 4-provider waterfall + Claygent on all rows
  Coverage: 93%
  Cost: 4.2 credits/enriched lead

Option B: 4-provider waterfall + Claygent only on ICP-qualified rows
  Coverage: 91%
  Cost: 2.8 credits/enriched lead

Option B is better for production. 2% lower coverage, 33% cheaper.
```

---

## The 8 Credit Optimization Techniques

### Technique 1: ICP Pre-Filter Before Enrichment

Don't enrich every row in your import. Pre-filter for ICP fit first.

**Step 1:** Import raw list with company data only (domain, name)
**Step 2:** Run company enrichment only (employee_count, industry, hq_country)
**Step 3:** Score for ICP fit using formulas (no credits for formulas)
**Step 4:** Filter → only run email waterfall on rows where `icp_score >= 40`

```
Credit savings:
100 raw leads → 40 pass ICP pre-filter
Email waterfall on 100 rows: ~200 credits
Email waterfall on 40 rows: ~80 credits
Savings: 60%
```

### Technique 2: Waterfall Stop Conditions (The Basics — Enforced)

This is covered in Phase 1, but experts enforce it rigorously. Every enrichment column must have a stop condition. No exceptions.

Quick audit: In your table, check every enrichment column. If ANY column doesn't have a "skip if previous found" condition, add it now.

### Technique 3: Claygent Gating by Value

Claygent is 3–5x more expensive than standard enrichment. Gate it tightly.

**Basic gate:** Only run if email already found (meaning the contact is reachable)
```
Skip if email_final is empty
```

**Advanced gate:** Only run if ICP score + email both present
```
Skip if email_final is empty OR icp_score < 60
```

**Budget gate:** Only run if you have budget remaining
Track a manual budget column or use a timestamp-based limit.

### Technique 4: Provider Order Optimization

The first provider you use on a row costs 1 credit even if it fails. Order providers by hit rate for your specific ICP.

**How to measure hit rate by provider:**

After a run, create a pivot analysis:
```python
# In your coverage analysis
provider_hitrate = df.groupby('email_source').size() / len(df) * 100
# Example output:
# Apollo: 45%    ← put first
# Findymail: 18% ← put second (it beats Prospeo for this list)
# Prospeo: 14%
# Dropcontact: 8% ← put last
```

Reorder your waterfall based on actual hit rates for your ICP. If Findymail consistently outperforms Prospeo for your list, swap their positions.

### Technique 5: Input Data Quality First

Bad input data → low match rates → credits wasted on failed lookups.

Pre-enrichment data cleaning (free, no credits):
- Normalize company domains (remove "https://", "www.", trailing slashes)
- Validate email format if pre-existing emails exist
- Standardize name case (Title Case, not ALL CAPS or all lowercase)
- Flag rows with missing required fields → don't run enrichment on them

```python
# Python cleaning before Clay import
import pandas as pd
import re

def clean_domain(domain: str) -> str:
    """Normalize company domain for Clay enrichment."""
    if not domain:
        return ""
    # Remove protocol and www
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^www\.', '', domain)
    # Remove paths and trailing slashes
    domain = domain.split('/')[0].strip().lower()
    return domain

df['company_domain'] = df['company_domain'].apply(clean_domain)
df['first_name'] = df['first_name'].str.strip().str.title()
df['last_name'] = df['last_name'].str.strip().str.title()
```

### Technique 6: Segment Tables by ICP

Don't mix US SaaS, EU enterprise, and SMB in one table. Segment:

| Table | ICP segment | Provider stack |
|-------|------------|----------------|
| `us-saas-prospects` | US, 50–500 employees, SaaS | Apollo → Prospeo → Findymail |
| `eu-enterprise` | EU, 500+ employees | Cognism → Dropcontact → Lusha |
| `smb-us` | US, 10–50 employees | Apollo → Hunter → Claygent |

Each segment has a different optimal provider stack. Mixed tables waste credits by running EU-optimized providers on US contacts and vice versa.

### Technique 7: Re-Enrichment Scheduling

Don't re-enrich everything. Re-enrich selectively:

```
Re-enrich if:
- last_enriched_date > 60 days ago (email addresses go stale)
- AND contact is in active outreach sequences
- AND email hasn't been confirmed delivered

Don't re-enrich:
- Leads that already replied or converted
- Contacts confirmed as "wrong person"
- Rows with verified emails that bounced (domain issue, not data issue)
```

Clay formula to flag for re-enrichment:
```
{{IF(
  DATEDIFF(TODAY(), last_enriched_date) > 60 AND
  email_verified != "bounced" AND
  lead_status != "converted" AND
  lead_status != "wrong_person",
  "Re-enrich",
  "Current"
)}}
```

### Technique 8: Output Trimming

Every output field Clay returns costs nothing extra — but having too many output columns creates clutter and slows formula performance on large tables.

Best practice: select only outputs you'll actually use downstream.

For Apollo People Search:
- ✓ Email (always)
- ✓ Job Title (for ICP scoring and personalization)
- ✓ LinkedIn URL (for Claygent input)
- ○ Phone (only if you do phone outreach)
- ✗ Seniority code (use job title instead for cleaner logic)
- ✗ Social profiles except LinkedIn (rarely useful)

---

## Credit Budget Planning Template

Use this before any production run:

```
Campaign: [name]
Date: [date]
Total rows to enrich: ___

Provider 1 (Apollo):
  Expected hit rate: ___%
  Rows it will run on: 100% of table
  Credits: ___ rows × 1 credit = ___

Provider 2 (Prospeo):
  Expected hit rate (of remaining): ___%
  Rows it will run on: ___% of table (remaining after P1)
  Credits: ___ rows × 1 credit = ___

Provider 3 (Findymail):
  Expected hit rate (of remaining): ___%
  Rows: ___
  Credits: ___

Provider 4 (Dropcontact):
  Expected hit rate (of remaining): ___%
  Rows: ___
  Credits: ___

Claygent (gated):
  Will run on: ___% of table (ICP-qualified unfound rows)
  Rows: ___
  Credits: ___ rows × 3 credits = ___

Company enrichment (Apollo Company):
  Rows: all
  Credits: ___ rows × 1 credit = ___

AI column:
  Rows: all found rows
  Credits: ___ rows × 0.5 credit = ___

TOTAL ESTIMATED CREDITS: ___
CREDITS AVAILABLE: ___
SURPLUS / DEFICIT: ___
```

---

## Monthly Credit Allocation Strategy

On Starter plan (2,000 credits/month):

```
Reserve: 200 credits (10% buffer for unexpected runs)
Available: 1,800 credits

Allocation:
- New prospect enrichment (waterfall): 1,000 credits (~400 new leads)
- Re-enrichment of hot accounts: 300 credits (~150 re-enriched)
- Claygent research (Tier A only): 300 credits (~100 rows × 3 credits)
- AI column runs: 200 credits (~400 opener generations)

Total: 1,800 credits
```

Adjust allocation monthly based on what stage your pipeline is in.

---

## The Credit Audit

Run this monthly to find inefficiencies:

1. Go to Settings → Credits → Transaction log
2. Export as CSV (if available) or manually review
3. Find:
   - Which columns cost the most?
   - Are any columns running on rows they shouldn't?
   - What's your credits-per-enriched-lead for this month?
   - Are Claygent credits being spent on Tier C rows?

4. Fix: update run conditions for any column spending credits unnecessarily

---

## Anki Cards to Create

```
Q: What is the single most impactful credit optimization technique?
A: ICP pre-filter — run company enrichment first, score for ICP fit, only run email waterfall on qualifying rows. Can save 50-60% of credits.

Q: What is "provider order optimization" and how do you implement it?
A: Measure actual hit rate per provider for your ICP, then reorder waterfall to put highest hit-rate provider first. Reduces credits spent on first-provider misses.

Q: How do you calculate credits-per-enriched-lead?
A: Total credits used / number of rows with email found

Q: What is a good credits-per-enriched-lead target for a production pipeline?
A: Below 2.5 credits/lead (with ICP pre-filter and tight Claygent gating)

Q: When should you NOT re-enrich a contact?
A: If they replied/converted, are confirmed wrong person, or have a bounced email from a domain issue (not data staleness)
```

---

## Next Module

→ [04_expert/03_gdpr_compliance.md](./03_gdpr_compliance.md) — GDPR-compliant enrichment for EU/UK targeting
