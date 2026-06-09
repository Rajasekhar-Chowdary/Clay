# Data Provider Reference Guide

Quick selection guide. Don't memorize this — reference it when building a waterfall.

---

## Provider Selection Matrix

| Provider | Best ICP | Coverage | Cost | GDPR | Free Tier |
|----------|---------|---------|------|------|-----------|
| **Apollo** | US tech/SaaS | ★★★★★ | $ | ✓ (DPA available) | 50 emails/month |
| **Prospeo** | US + EU general | ★★★★ | $ | ✓ | Limited |
| **Findymail** | Pattern inference | ★★★ | $$ | ✓ | Limited |
| **Dropcontact** | EU / France | ★★★★ | $ | ✓✓ (French, CNIL) | No |
| **Cognism** | UK / EU enterprise | ★★★★★ | $$$ | ✓✓✓ | No |
| **Hunter.io** | Email format guessing | ★★★ | $ | ✓ | 25/month |
| **Lusha** | EU general | ★★★ | $$ | ✓ | 5/month |
| **Clearbit (Breeze)** | Company data | ★★★★ | $$ | ✓ | 250/month |
| **Claygent** | Custom research | ★★★★★ | $$$ | ✓ (public data only) | Included in Clay plan |

---

## Standard Waterfalls by ICP

### US SaaS (50–500 employees)
```
1. Apollo → 2. Prospeo → 3. Findymail → 4. Dropcontact → 5. Claygent
Expected coverage: 88–93%
```

### EU / UK (B2B general)
```
1. Apollo → 2. Cognism → 3. Dropcontact → 4. Lusha → 5. Claygent
Expected coverage: 80–88%
Note: Cognism is paid. For budget: Apollo → Dropcontact → Claygent (75–82%)
```

### Australia / APAC
```
1. Apollo → 2. Lusha → 3. Claygent
Expected coverage: 65–75%
Note: APAC coverage is thin across all providers. Claygent essential.
```

### Enterprise (1000+ employees)
```
1. Apollo → 2. Cognism → 3. Lusha
Expected coverage: 85–90%
Note: Enterprise contacts are more findable. Fewer providers needed.
```

---

## Provider Details

### Apollo
- **Data sourcing:** Public professional profiles + proprietary data network
- **Best for:** US tech companies, well-established professionals
- **Weakness:** Newer employees, small companies, non-US contacts
- **API available:** Yes (separate from Clay integration)
- **Free tier:** 50 email finds/month, unlimited company data

### Hunter.io
- **Data sourcing:** Pattern inference from public web sources + email format database
- **Best for:** Companies where email format is consistent (firstname@company.com)
- **Weakness:** Companies with inconsistent email formats, personal email users
- **Special:** High precision — fewer false positives than Apollo
- **Free tier:** 25 searches/month

### Findymail
- **Data sourcing:** Real-time email verification + pattern inference
- **Best for:** Hard-to-find emails where other providers failed
- **Special:** Returns verification status (verified/risky/invalid) — filter invalids before sending
- **Note:** More expensive per lookup but higher accuracy

### Prospeo
- **Data sourcing:** Proprietary database + web indexing
- **Best for:** Filling gaps after Apollo (different data sources)
- **Cost:** Generally cheaper than Apollo at scale
- **Coverage:** Strong US and growing EU coverage

### Dropcontact
- **Data sourcing:** Real-time verification against company email servers
- **Best for:** France, Benelux, broader EU
- **Special:** GDPR-native French company, no database — finds in real-time
- **Note:** Slower than database lookups (real-time verification)

### Cognism
- **Data sourcing:** Verified B2B database, GDPR consent-based where required
- **Best for:** UK, DACH, Nordics — strongest EU coverage
- **Special:** Diamond Data® = phone-verified mobile numbers
- **Cost:** Highest cost, requires contract
- **When to use:** EU-heavy campaigns where coverage > cost

### Clearbit (now HubSpot Breeze)
- **Focus:** Company-level data, not person-level
- **Best for:** Company enrichment: tech stack, funding, headcount, description
- **Note:** Person-level data quality has declined post-HubSpot acquisition
- **Free tier:** 250 company lookups/month

---

## When Providers Fail (Debugging)

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Apollo returns 0 results | Domain incorrect or unrecognized | Check domain format (no www, no https) |
| Apollo returns wrong person | Common name + small company = ambiguity | Add LinkedIn URL as additional input |
| Hunter returns "not found" | Company uses non-standard email format | Try Findymail (pattern + verify) |
| Claygent returns empty | Page is blocked to bots or uses JS-heavy loading | Use a different page or add Google search fallback |
| Dropcontact slow | Real-time verification takes 15–30 seconds per row | Normal — run overnight not real-time |
| All providers fail for a company | Private company, personal email only, or data doesn't exist | Accept as unfound; manual research if Tier A |
