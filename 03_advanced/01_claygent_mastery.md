# Module 3.1 — Claygent Mastery: Expert Prompt Engineering

**Time:** 90–120 minutes  
**Prerequisite:** Phase 2 project complete, at least 3 Claygent prompts tested  
**Focus:** Advanced prompt patterns, multi-step research, validation techniques

---

## What Separates Beginner from Expert Claygent Use

Beginner: "Find information about {company_name} and its tech stack."
Expert: Multi-step, conditional, structured output with validation, gated by cost conditions.

The difference isn't vocabulary. It's **precision**:
- Exactly where to look (specific URLs, not vague "the internet")
- Exactly what format to return (so formulas can process it)
- Exactly what to do when the data isn't there (fallback that your code can detect)
- Gated by conditions (don't spend Claygent credits on low-value rows)

---

## The 7 Expert Prompt Patterns

These 7 patterns cover 90% of Claygent use cases in production pipelines.

---

### Pattern 1: The Specific-URL Researcher

Most beginners tell Claygent to "search" — experts tell it exactly where to go.

**Weak:**
```
Search for {company_name}'s CRM tools.
```

**Expert:**
```
Visit {company_domain}/careers.
On this page, search all visible job postings for software tools mentioned in requirements or responsibilities sections.
Specifically look for: Salesforce, HubSpot, Pipedrive, Marketo, Pardot, Outreach, Salesloft, Apollo, ZoomInfo.
Return ONLY the tools found as a comma-separated list.
If the page doesn't load or no tools are mentioned: return "Tools not found".
Max 30 words.
```

Why it works: Specific URL + specific tools to look for + exact output format + explicit fallback.

---

### Pattern 2: The Multi-Source Validator

Visit multiple sources and reconcile the data. Used when you need higher confidence.

```
Step 1: Visit {company_domain}/about and extract the company's founding year and headquarters city.
Step 2: Visit https://www.linkedin.com/company/{company_linkedin_slug} and check if founding year and HQ match.
If both sources agree: return "Verified: Founded [year], HQ: [city]"
If they disagree: return "Conflicting: Web=[web data], LinkedIn=[linkedin data]"
If only one source available: return "Single source: [data source] - [data]"
Max 30 words.
```

Use when: Enriching high-value accounts where data accuracy matters (enterprise accounts, large deal targets).

---

### Pattern 3: The Signal Detector

Detect external signals that indicate buying intent. The most valuable Claygent use case.

**Funding signal:**
```
Search for news about {company_name} raising funding in the last 12 months.
Check TechCrunch, Crunchbase, VentureBeat, and the company's own press page at {company_domain}/press or {company_domain}/news.
If funding found: return "SIGNAL: {company_name} raised [amount/round] in [month/year]"
If no funding found: return "No funding signal"
Max 30 words. Do not include speculative language.
```

**Leadership change signal:**
```
Search LinkedIn for recent changes at {company_name}.
Look for new VP of Sales, Chief Revenue Officer, Head of Growth, or VP of Marketing hired in the last 6 months.
If found: return "SIGNAL: [Name] joined as [Title] in [month/year]"
If not found: return "No leadership change signal"
Max 30 words.
```

**Hiring signal (RevOps job posting):**
```
Visit {company_domain}/careers and https://jobs.lever.co/{company_name_lowercase} and https://boards.greenhouse.io/{company_name_lowercase}.
Look for open positions with "RevOps", "Revenue Operations", "GTM Engineer", "Sales Operations", or "Marketing Operations" in the title.
If found: return "SIGNAL: Hiring [job title]"
If not found: return "No RevOps hiring signal"
Max 20 words.
```

---

### Pattern 4: The LinkedIn Post Extractor

Used for personalization — finding what someone said publicly.

```
Visit {linkedin_url}.
Find {first_name}'s most recent post, article, or comment made in the last 60 days.
Extract the single most important insight or claim they made.

Return format: "In [month], {first_name} posted about [topic]. Key insight: [their main point in 15 words max]"

If no posts in last 60 days: return "No recent LinkedIn activity (last 60 days)"
If profile is private or URL is invalid: return "Profile not accessible"
Strict max: 50 words total.
```

**Why 50 words max:** Your AI personalization column needs this as input. Long Claygent output = bloated AI prompts = worse quality openers.

---

### Pattern 5: The Competitive Intelligence Gatherer

Used when you need to know what alternatives your prospect is evaluating.

```
Visit {company_domain} and {company_domain}/pricing and {company_domain}/integrations.
Find evidence of which CRM, data enrichment, or outbound tools they currently use OR mention as integrations.

Return as structured list:
CRM: [tool or "not mentioned"]
Enrichment: [tool or "not mentioned"]  
Outbound: [tool or "not mentioned"]
Integrations mentioned: [comma-separated list or "none"]

If pages don't load: return "Pages not accessible"
Max 40 words.
```

---

### Pattern 6: The Content Analyst

Read a blog, press release, or product page and extract structured insight.

```
Visit {company_domain}/blog or {company_domain}/resources.
Find the 3 most recent articles published in the last 90 days.
For each article, extract:
- Title
- Publish date
- Core topic in 5 words

Return as:
Article 1: [title] | [date] | [topic]
Article 2: [title] | [date] | [topic]
Article 3: [title] | [date] | [topic]

If fewer than 3 articles or no blog found: return available articles or "Blog not found"
Max 60 words.
```

Use when: Preparing for a sales call where you want to reference their recent content.

---

### Pattern 7: The ICP Qualifier

Quickly assess if a company fits your ICP based on public signals.

```
Visit {company_domain}.

Answer these 3 questions based ONLY on what you can read on the website:
1. Do they sell B2B or B2C? (B2B / B2C / Both / Unclear)
2. Is their primary customer SMB, Mid-Market, or Enterprise? (SMB / Mid-Market / Enterprise / Mixed / Unclear)
3. Do they mention sales, growth, or revenue operations anywhere? (Yes / No)

Return format: "B2B/B2C: [answer] | Customer: [answer] | RevOps_mention: [answer]"
Max 20 words.
```

This is particularly powerful as a pre-filter before running expensive enrichment. Run this on raw company lists to qualify ICP fit before spending credits on email waterfall.

---

## Prompt Debugging Techniques

When Claygent returns wrong or empty output, use this diagnostic process:

### Step 1: Is the URL accessible?
Add a test prompt first: "Visit {company_domain} and return the page title." If it returns empty, the URL is wrong or the site blocks bots.

### Step 2: Is the format instruction clear enough?
Run the prompt on a company where you know the answer. If the output format is wrong, tighten the format instruction.

### Step 3: Is the fallback triggering correctly?
Manually look at a row where Claygent returned your fallback string. Open the company website yourself — was there actually data there? If yes, your "where to look" instruction missed it.

### Step 4: Is the data actually public?
Some things Claygent cannot find:
- Private LinkedIn profiles
- Internal tools (can't browse intranet)
- Pricing locked behind login
- Data that's only in PDFs (limited)

If the data isn't publicly visible, Claygent won't find it.

### Step 5: Test on 10 diverse rows
Run on: 1 large US company, 1 small US startup, 1 UK company, 1 EU company, 1 company with LinkedIn, 1 without, 1 company with a blog, 1 without, 1 with active recent news, 1 quiet company.
This coverage finds edge cases your original 5-row test missed.

---

## Claygent Cost Gating (Advanced)

Never run Claygent on all rows. Always gate with conditions.

### Basic Gate
```
Run condition: Only if email_final is empty
(Run Claygent email recovery only for rows where waterfall failed)
```

### Compound Gate
```
Run condition: email_final is not empty AND icp_tier == "Tier A" AND employee_count >= 50
(Only research signal for Tier A prospects above a size threshold)
```

### Signal Gate
```
Run condition: icp_score >= 60 AND claygent_signal_run == "false"
(Only run on high-scoring rows that haven't been researched yet)
```

### Budget Gate (Advanced Formula)
Add a column that tracks whether this row is "worth" Claygent research:
```
claygent_eligible:
{{IF(
  NUMBER(icp_score) >= 60 AND
  ISNOTEMPTY(email_final) AND
  hq_country == "US",
  "Yes",
  "No"
)}}
```

Then set Claygent run condition to: only if `claygent_eligible == "Yes"`

This ensures you only spend Claygent credits on rows that matter.

---

## Building a Claygent Prompt Library

Every good Claygent prompt should be documented for reuse. See [05_reference/claygent_prompt_library.md](../05_reference/claygent_prompt_library.md) for the full library template.

For your own library, document each prompt with:
- **Prompt name:** What it finds
- **Use case:** When to use it
- **Run condition:** How to gate it
- **Expected output format:** What it returns
- **Test results:** How many rows tested, pass rate

---

## Hands-On Exercise

Build all 3 of these Claygent columns on your 100-row table:

**Column 1: Funding signal** (Pattern 3)
Test on 10 rows. Note: how many returned "SIGNAL"? What percentage?

**Column 2: LinkedIn post** (Pattern 4)
Test on the 10 rows with highest ICP scores. Evaluate: are the extracted insights actually usable for personalization?

**Column 3: Your custom pattern** (choose from 1–7 above or build new)
Write, test, iterate. Document the final prompt in your prompt library.

---

## Anki Cards to Create

```
Q: What are the 5 elements of an expert Claygent prompt?
A: VISIT (exact URL), FIND (specific data), CONDITION (if not found do X), FORMAT (exact output structure), CONSTRAINT (word limit + what to exclude)

Q: What is the "Claygent budget gate" technique?
A: A formula column (claygent_eligible) that evaluates ICP score + email found + geography before allowing Claygent to run — saves credits by only researching high-value rows

Q: When Claygent returns empty output, what's the first thing to check?
A: Whether the URL is actually accessible — test with a simple "Visit {domain} and return page title"

Q: How many diverse rows should you test a Claygent prompt on?
A: 10 (covering: large US, small startup, UK, EU, with/without LinkedIn, with/without blog, recent news, quiet company)

Q: What is Pattern 3 (Signal Detector) used for?
A: Detecting buying signals — funding rounds, leadership changes, hiring signals — that indicate a prospect is actively building and has budget
```

---

## Next Module

→ [03_advanced/02_signal_detection.md](./02_signal_detection.md) — Signal-based enrichment: automating intent detection at scale
