# Module 2.1 — Waterfall Mastery: 4-Provider Design

**Time:** 60–75 minutes  
**Prerequisite:** Phase 1 complete, beginner project at 65%+ coverage  
**Target:** Push coverage from 65% → 85%+

---

## Why You're Still at 65%

After a 2-provider waterfall, you've found the "easy" 60–65%:
- US tech companies with LinkedIn presence
- People who've been at their company 2+ years
- Mid-to-large companies with good data coverage

The remaining 35% are harder for a reason:
- Newer employees (just joined, database hasn't updated)
- Small/niche companies (Apollo has thin coverage)
- EU/international contacts (US-centric databases underperform)
- Frequent job changers (data goes stale)
- Personal email users who don't expose work email publicly

A 4-provider waterfall attacks each of these gaps with providers that have different data sourcing methods.

---

## The Anatomy of a 4-Provider Waterfall

```
Provider 1: Apollo
 └─ Why first: largest database, free tier, fastest for US tech
 └─ Who it finds well: US SaaS, tech companies, established professionals

Provider 2: Prospeo
 └─ Why second: different data sourcing than Apollo, good cost/coverage ratio
 └─ Who it fills: people Apollo missed due to database gaps

Provider 3: Findymail
 └─ Why third: uses email pattern inference + verification
 └─ Who it fills: people whose format is guessable (john.smith@company.com patterns)
 └─ Bonus: built-in email verification (reduces bounce rate)

Provider 4: Dropcontact
 └─ Why fourth: EU-strong, GDPR-native, different methodology
 └─ Who it fills: EU contacts, privacy-conscious professionals, enterprise contacts
```

Each provider has a different data sourcing method:
- **Database lookup** (Apollo, Prospeo): find the exact email from a stored record
- **Pattern inference** (Findymail): guess the format and verify it exists
- **Real-time verification** (Dropcontact): find and verify in one step

Using all 4 means you're exploiting different angles to find the same person.

---

## Building the Full 4-Provider Waterfall

### Column Structure (in order)

| Column Name | Type | Provider | Run Condition | Outputs |
|-------------|------|----------|---------------|---------|
| `email_apollo` | Enrichment | Apollo People Search | Always | email, title, linkedin_url |
| `email_prospeo` | Enrichment | Prospeo Email Finder | email_apollo is empty | email |
| `email_findymail` | Enrichment | Findymail | email_apollo AND email_prospeo are empty | email, verified status |
| `email_dropcontact` | Enrichment | Dropcontact | all above are empty | email |
| `email_final` | Formula | — | — | COALESCE of all 4 |
| `email_source` | Formula | — | — | which provider found it |
| `email_verified` | Formula | — | — | IF findymail found → "verified" ELSE "unverified" |
| `coverage_status` | Formula | — | — | Found / Not found |

### The Run Condition Chain (Critical)

Each column must skip rows where a previous column already succeeded:

```
email_apollo:     Always
email_prospeo:    Skip if (email_apollo is not empty)
email_findymail:  Skip if (email_apollo is not empty) OR (email_prospeo is not empty)
email_dropcontact: Skip if any of the above are not empty
```

In Clay's UI, "Skip if" can chain multiple conditions with AND/OR logic.

### Consolidation Formulas

**email_final:**
```
{{COALESCE(email_apollo, email_prospeo, email_findymail, email_dropcontact)}}
```

**email_source:**
```
{{IF(ISNOTEMPTY(email_apollo), "Apollo",
  IF(ISNOTEMPTY(email_prospeo), "Prospeo",
    IF(ISNOTEMPTY(email_findymail), "Findymail",
      IF(ISNOTEMPTY(email_dropcontact), "Dropcontact",
        "Not found"
      )
    )
  )
)}}
```

**email_verified:**
```
{{IF(email_source == "Findymail", "Verified", IF(ISNOTEMPTY(email_final), "Unverified", "Not found"))}}
```

---

## Provider Configuration Details

### Apollo People Search — Advanced Setup

Beyond the basics, Apollo has optional enrichment that improves match rates:

- **LinkedIn URL input:** If you have LinkedIn URLs, pass them to Apollo as an additional input. Dramatically improves match rate for hard-to-find contacts.
- **Personal email fallback:** Apollo can return personal emails when work email is unavailable. Usually not what you want — configure to "work email only" unless you're doing consumer outreach.
- **Seniority filter:** You can filter outputs to only return senior-level matches if you're targeting decision-makers.

### Findymail — Understanding Email Verification

Findymail returns both an email and a verification status:
- `verified` — the email exists (checked via SMTP ping)
- `risky` — the email might exist but verification wasn't definitive
- `invalid` — the email doesn't exist (never send to these)

Add a filter after Findymail: if `findymail_status == "invalid"`, treat as not found.

```
Formula to handle Findymail verification:
{{IF(findymail_status == "invalid", "", email_findymail)}}

This makes invalid emails empty, so the COALESCE skips them.
```

### Dropcontact — EU-Specific Setup

Dropcontact requires:
- First name
- Last name  
- Company domain

Optional but improves results:
- Phone number
- LinkedIn URL

For EU targeting: Dropcontact is GDPR-compliant and often finds contacts that Apollo misses entirely — especially French and Benelux contacts.

---

## Coverage Analysis: Understanding Your Waterfall's Performance

After running the 4-provider waterfall, you need to know WHERE coverage is coming from.

### The Provider Contribution Table

Build this table after every major enrichment run:

| Provider | Found | % of total | Cumulative coverage |
|----------|-------|-----------|-------------------|
| Apollo | 45 | 45% | 45% |
| Prospeo | 18 | 18% | 63% |
| Findymail | 12 | 12% | 75% |
| Dropcontact | 10 | 10% | 85% |
| Not found | 15 | 15% | — |

The delta between each provider tells you how valuable that provider is. If Prospeo added only 2% on your list, it may not be worth the credits.

### When to Swap Provider Order

If you're targeting EU contacts heavily:
```
Apollo → Cognism → Dropcontact → Lusha
(Cognism and Dropcontact swap positions for EU lists)
```

If you have LinkedIn URLs for most contacts:
```
Apollo (with LinkedIn input) → Findymail → Prospeo → Dropcontact
(Apollo with LinkedIn gets much higher first-pass coverage)
```

---

## The Credit Efficiency Metric

Credits per enriched lead = total credits / successfully enriched leads

```
Example:
Total credits used: 250
Successfully enriched: 85 out of 100
Credits per enriched lead = 250 / 85 = 2.94

At Starter plan ($149/month, 2,000 credits):
Max enriched leads per month = 2,000 / 2.94 = ~680 leads
Cost per lead = $149 / 680 = $0.22/lead
```

Track this metric. Your goal: get credits-per-enriched-lead below 3.0 on a 4-provider waterfall.

---

## Hands-On Exercise

Take your 25-row table from Phase 1 and expand it:

1. Import it into a new table (or duplicate the original)
2. Add Prospeo and Findymail columns to the existing Apollo + Hunter waterfall
3. Run enrichment on the "Not found" rows from Phase 1 (the 35%)
4. Calculate:
   - How many did Prospeo recover?
   - How many did Findymail recover?
   - New total coverage rate?
   - What's your credits-per-enriched-lead?

Expected result: coverage should jump from 65% to 78–85%.

Log the before/after in `00_meta/progress_tracker.md`.

---

## Recall Practice

1. Why does a 4-provider waterfall outperform a 2-provider waterfall beyond just "more providers"?
2. Findymail returns status "invalid" for an email. What should your formula do with this?
3. You're targeting French B2B contacts. Which provider would you move earlier in the waterfall?
4. What is "credits per enriched lead" and what is a good target value?
5. If Apollo has 45% contribution, Prospeo 15%, Findymail 8%, and Dropcontact 4% — total coverage is what?
6. You want to use LinkedIn URLs as an input to Apollo. Why does this help?

---

## Anki Cards to Create

```
Q: What are the 4 most common providers in a US SaaS email waterfall (in order)?
A: Apollo → Prospeo → Findymail → Dropcontact

Q: What does Findymail return beyond just an email?
A: Verification status: verified / risky / invalid — filter out "invalid" emails

Q: Which provider is best for EU/French contacts?
A: Dropcontact — GDPR-native, strong EU coverage especially France/Benelux

Q: Formula for credits-per-enriched-lead
A: total_credits / successfully_enriched_rows

Q: Why does passing LinkedIn URL to Apollo improve match rates?
A: Apollo can cross-reference the LinkedIn profile directly instead of guessing from name+domain — eliminates ambiguity for common names

Q: What is a good credits-per-enriched-lead target for a 4-provider waterfall?
A: Below 3.0 credits per successfully enriched lead
```

---

## Next Module

→ [02_intermediate/02_company_enrichment.md](./02_company_enrichment.md) — Enrich company data: size, industry, funding, tech stack
