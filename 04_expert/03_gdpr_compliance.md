# Module 4.3 — GDPR-Compliant Enrichment for EU/UK

**Time:** 45 minutes  
**Focus:** Legal framework, practical protocol, and data provider selection for EU/UK targeting

---

## The Bottom Line First

B2B cold email to professionals IS legal under GDPR when:
1. You email a corporate address (not personal gmail)
2. The message is relevant to their professional role
3. You include a clear unsubscribe mechanism
4. You can say how you obtained their data

GDPR enforcement targets mass B2C spam, not targeted professional B2B outreach with opt-out. Don't let GDPR paralysis stop EU/UK campaigns.

---

## The Legal Basis: Legitimate Interest

GDPR Article 6(1)(f) allows processing personal data for "legitimate interests" without explicit consent.

For B2B enrichment, legitimate interest applies when:
- You're enriching business contact information (not personal data)
- The outreach is relevant to the recipient's professional role
- You have a genuine business purpose
- The contact's privacy interests don't override your legitimate interest

The legitimate interest test (run this mentally before each campaign):
```
1. Is there a genuine purpose? (selling a B2B product/service)
2. Is enrichment necessary? (yes — you need to reach the right person)
3. Is there a privacy balance? (B2B contact data + professional relevance = balance tips your way)
```

---

## Country-by-Country Rules

| Country | Regime | B2B cold email status | Key requirement |
|---------|--------|-----------------------|-----------------|
| **UK** | PECR + UK GDPR | Generally permitted | Corporate emails exempt from consent requirement. Legitimate interest applies. |
| **Netherlands** | EU GDPR | Permitted under LI | Document your legitimate interest basis |
| **Germany** | UWG + GDPR | Stricter — implied consent preferred | Best practice: only email if publicly posted business contact |
| **France** | CNIL guidelines | Permitted under LI | Dropcontact is French-origin and CNIL-friendly |
| **Australia** | Spam Act 2003 | Opt-out model | Include unsubscribe; no prior consent needed for B2B |
| **Singapore** | PDPA | LI applies | Business contact info = LI when professionally relevant |
| **Canada** | CASL | Stricter | Needs implied or express consent. Implied = publicly posted business email |

**Practical impact on your waterfall:**
- UK: standard waterfall is fine
- Germany: prioritize publicly listed contacts (LinkedIn, company website)
- Canada: only enrich contacts whose email is publicly available (Apollo's data sourced from public profiles = generally OK)

---

## The 5-Step GDPR Compliance Protocol

### Step 1: Data Provider DPA

Every provider you use must have a signed Data Processing Agreement (DPA) meeting GDPR Article 28.

| Provider | DPA Available | Notes |
|----------|---------------|-------|
| Apollo | Yes | Download from Apollo account settings |
| Findymail | Yes | Request from support |
| Prospeo | Yes | Available on their website |
| Dropcontact | Yes | French company, GDPR-native |
| Cognism | Yes | Built for EU, most GDPR-ready |

**Action:** Before using any provider for EU leads, download and retain their DPA.

### Step 2: Data Source Tracking in Clay

Add a column that records where each email was found. This is your audit trail.

```
Column: data_source
Type: Formula
Formula:
{{IF(ISNOTEMPTY(email_apollo), "Apollo.io — public business directory",
  IF(ISNOTEMPTY(email_prospeo), "Prospeo.io — verified business database",
    IF(ISNOTEMPTY(email_findymail), "Findymail.io — email verification service",
      IF(ISNOTEMPTY(email_dropcontact), "Dropcontact.io — GDPR-compliant EU database",
        "Not found"
      )
    )
  )
)}}
```

If a contact asks "how did you get my email?" — you have the answer documented per row.

### Step 3: Article 14 Notice (First Contact)

GDPR Article 14 requires informing someone when you obtained their data from a third party.

In practice: your first email should contain a single sentence:
> "I found your contact through [data source] because [professional relevance reason]."

This one sentence makes you compliant.

Example footer text (add to all EU outreach):
```
I found your contact via professional business directories based on your role at [company].
To unsubscribe from future messages, reply with "unsubscribe" or click here: [link]
```

### Step 4: EU-Safe Claygent Prompts

Claygent must only access publicly available professional information.

**Compliant:**
```
Visit {linkedin_url} and find {first_name}'s publicly listed job title and current employer.
```

**Non-compliant:**
```
Find {first_name}'s home address or personal social media profiles.
Find any information about {first_name}'s personal life.
```

**Rule:** If the data is on a public professional profile or company website, Claygent can access it. If it requires login or is in a personal context, it cannot.

### Step 5: Opt-Out Infrastructure

Every outreach sequence must have one-click unsubscribe.

- HubSpot sequences: unsubscribe included automatically
- Instantly / Smartlead: verify unsubscribe is enabled
- Manual sequences: add unsubscribe link to every email

When someone unsubscribes: add them to a suppression list in Clay (or mark in Supabase) so they're filtered from all future enrichment and outreach.

**Clay suppression formula:**
```
Column: suppressed
Type: Formula
Formula: {{IF(email_final == "" OR unsubscribed == "true", "Suppress", "Active")}}
```

Filter all exports and HubSpot pushes to `suppressed == "Active"` only.

---

## GDPR-Optimized Provider Stack for EU/UK

For EU-heavy lists, replace the standard US waterfall:

```
Standard US waterfall:
Apollo → Prospeo → Findymail → Dropcontact

EU/UK optimized:
1. Apollo (still has EU coverage, DPA available)
2. Cognism (GDPR-native, strong UK/EU, built for compliance)
3. Dropcontact (French company, CNIL-friendly, strong EU coverage)
4. Lusha (EU coverage, DPA available)
5. Claygent (reads public professional profiles — no DPA needed for public data)
```

Note: Cognism is paid-only (no free tier). For budget constraints: Apollo + Claygent is the GDPR-safe minimum.

---

## What GDPR Enforcement Actually Targets

GDPR enforcement actions (2024–2026 cases) focus on:
1. Mass B2C spam without opt-out mechanism
2. Sensitive data categories (health, political, financial data)
3. Data breaches of personal data
4. Consent violations for cookies/tracking on websites
5. No response to Subject Access Requests

Targeted B2B professional outreach with documented sources and clear opt-out is NOT where enforcement resources are directed.

This doesn't mean do whatever you want — it means the risk profile for proper B2B outreach is low, and the compliance checklist above makes it even lower.

---

## Anki Cards to Create

```
Q: What legal basis makes B2B cold email legal under GDPR?
A: Article 6(1)(f) Legitimate Interest — processing is necessary for genuine business purpose, contact's professional privacy interest doesn't override it

Q: What 4 conditions make GDPR-compliant B2B outreach?
A: Corporate email address (not personal), relevant to professional role, clear unsubscribe mechanism, documented data source

Q: What is GDPR Article 14 and how does it apply to cold email?
A: Requires notifying someone when you got their data from a third party — one sentence in first email naming the source

Q: Which enrichment provider is most GDPR-native for EU/UK targeting?
A: Cognism — built specifically for EU compliance, GDPR-first data sourcing

Q: What should your Clay table's data_source column contain?
A: The provider that found each email (e.g., "Apollo.io — public business directory") — creates audit trail for subject access requests
```

---

## Next Module

→ [04_expert/04_expert_project.md](./04_expert_project.md) — Expert project: full-stack real-time signal pipeline
