# Module 1.1 — The Clay Mental Model

**Time:** 30–45 minutes  
**Format:** Read → close doc → answer recall questions → create Anki cards

---

## The Core Metaphor

Clay is a **spreadsheet that calls the internet**.

Every row is a person or company. Every column is a question you ask about that row. Most columns you fill manually (name, company). Enrichment columns *call external databases* to fill the gaps.

```
Row: Jane Smith, Salesforce, jane.smith@salesforce.com

You know: first name, last name, company
You want: work email, job title, LinkedIn URL, company size, phone

Clay calls Apollo → gets email, title
Clay calls Clearbit → gets company size
Clay calls LinkedIn scraper → gets LinkedIn URL
All happen automatically. You get back a complete row.
```

---

## The 5 Building Blocks

### 1. Tables
A table is your dataset. One table = one campaign or enrichment project. You can have many tables. Think of it as a Google Sheet where the cells can make API calls.

Each table has:
- **Rows** — one person or company per row
- **Columns** — one data point per column
- **Run history** — a log of every enrichment call (important for debugging)

### 2. Column Types

| Type | What it does | Example |
|------|-------------|---------|
| **Text / Number / Date** | Static data you type or import | "Jane", "Salesforce", "2024-01-15" |
| **Enrichment** | Calls an external data provider | Apollo: returns email + title |
| **Formula** | Computes from other columns | `{{first_name}} {{last_name}}` = "Jane Smith" |
| **Claygent** | AI browses the web and returns custom data | "What does this company sell in 15 words?" |
| **AI** | GPT/Claude prompt using row data | Generate a personalized cold email opening |
| **HTTP** | Raw API call to any endpoint | Your own backend, a custom data source |
| **Webhook (Action)** | Sends row data to an external URL when triggered | Push to n8n, Zapier, HubSpot |

### 3. Credits
Credits are your currency. You spend them when you run enrichment.

**Rule 1:** Each enrichment attempt costs 1 credit — whether it succeeds or fails.
**Rule 2:** A waterfall with 5 providers costs up to 5 credits per row IF all providers fail.
**Rule 3:** The waterfall STOPS as soon as a provider succeeds → massive savings.
**Rule 4:** Claygent costs 2–5 credits per run (it browses multiple pages).

```
Practical example:
100-row table, 4-provider waterfall:
  - If Apollo finds 60% → saves 3 credits per row for those 60 rows
  - If Prospeo finds 20% more → saves 2 credits for those
  - Remaining 20% → all 4 providers tried → 4 credits each
  
Total credits: (60×1) + (20×2) + (10×3) + (10×4) = 60+40+30+40 = 170 credits
Without waterfall (running all 4 always): 100×4 = 400 credits
Savings: 57%
```

**Credit tiers:**
- Free: 100/month
- Starter: 2,000/month (~$149)
- Explorer: 10,000/month
- Pro: 50,000/month

**Beginner strategy:** Use free tier to test and learn. Upgrade to Starter only when you start real campaigns.

### 4. Data Providers

Clay connects to 100+ data providers. You don't need to know all of them. Learn the 5 that cover 90% of use cases:

| Provider | Best for | Weakness |
|----------|---------|---------|
| **Apollo** | US tech companies, emails + phone, free tier available | Weaker outside US, stale data in fast-moving companies |
| **Hunter.io** | Email pattern finding (format-based) | Lower coverage than Apollo, better verification |
| **Findymail** | High accuracy + bounce detection included | Smaller database than Apollo |
| **Prospeo** | Good EU + US coverage, cost-effective | Less known, smaller brand |
| **Clearbit (Breeze)** | Company data: funding, size, tech stack, industry | Acquired by HubSpot, pricing changed |

### 5. Claygent (The Secret Weapon)

Claygent is Clay's AI research agent. It reads web pages, LinkedIn profiles, and job boards, and returns structured data you specify.

Unlike the database providers above, Claygent can find **data that doesn't exist in any database yet** — because it reads the web in real-time.

Examples of what only Claygent can do:
- "What did this person post on LinkedIn this month?"
- "Does this company have an open RevOps position right now?"
- "What CRM do they use, based on their job postings?"
- "Did they raise funding in the last 6 months?"

Cost: 2–5x more than regular enrichment. Use it last (as the final fallback) or for specific custom research.

---

## The Data Flow (Memorize This)

```
Input (CSV or manual entry)
    ↓
Clay Table
    ├── Standard columns (static data)
    ├── Enrichment columns (provider lookups)
    │   └── Waterfall logic: try A → if fail → try B → if fail → try C
    ├── Claygent columns (AI web research)
    ├── Formula columns (compute from enriched data)
    └── AI columns (generate text using enriched data)
    ↓
Output (CSV export, HubSpot sync, webhook to n8n)
```

---

## Why Clay Beats Buying a Single Database

If you just buy Apollo ($99/month), you get ~40% email coverage for a typical B2B list.

If you run a waterfall of Apollo + 3 more providers, you get 80–90% coverage at similar or lower cost — because you only pay when each provider succeeds.

The waterfall is Clay's core value proposition. Everything else is additive.

---

## Common Beginner Mistakes

**Mistake 1: Running enrichment without a stop condition**
If you add multiple enrichment columns without telling Clay to stop when an email is found, it'll run ALL providers on ALL rows. Credits fire.

**Mistake 2: Testing on the full table first**
Always run 5 rows manually before bulk-running. Check what the provider actually returns before committing credits.

**Mistake 3: Ignoring the "Run history" tab**
The run history shows exactly what each provider returned (including error messages and null responses). It's your debugging tool.

**Mistake 4: Poor input data quality**
Apollo can't find emails for "Jane, Salesforce" if the domain is wrong. Garbage input = garbage coverage.

---

## Recall Practice

Close this doc. Answer these from memory. Don't scroll up.

1. What are the 5 column types in Clay?
2. If a 4-provider waterfall finds an email on the second provider, how many credits does that row cost?
3. What is Claygent and what can it do that database providers can't?
4. What is the expected coverage rate for a 4-provider waterfall without Claygent?
5. What's the difference between a Formula column and an AI column?
6. Name 3 common beginner mistakes.

Score yourself. Anything you couldn't answer = read that section again, then create an Anki card.

---

## Anki Cards to Create

```
Q: What are the 5 column types in Clay?
A: Text/Number/Date (static), Enrichment (provider call), Formula (computed), Claygent (AI web research), AI (GPT/Claude prompt)

Q: How much does a 4-provider waterfall cost per row if the first provider succeeds?
A: 1 credit (waterfall stops on first success)

Q: How much does a 4-provider waterfall cost per row if ALL providers fail?
A: 4 credits (one attempt per provider)

Q: What is the expected email coverage for a 4-provider waterfall without Claygent?
A: 80–90%

Q: What can Claygent do that database providers (Apollo, Hunter) cannot?
A: Research real-time data from the live web — LinkedIn posts, job postings, recent news, custom company intel

Q: What is the single most important metric in Clay enrichment?
A: Coverage rate = rows with email / total rows × 100

Q: What should you always do before bulk-running enrichment on a full table?
A: Test on 5 rows manually first
```

---

## Next Module

→ [01_beginner/02_table_columns_credits.md](./02_table_columns_credits.md) — Hands-on: build your first table
