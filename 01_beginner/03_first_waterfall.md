# Module 1.3 — Building Your First Waterfall

**Time:** 60–90 minutes (reading + hands-on)  
**Prerequisite:** Module 1.2 completed + hands-on exercise done  
**Deliverable:** A working 2-provider waterfall with measured coverage rate

---

## What a Waterfall Is (Precise Definition)

A waterfall is a **sequential enrichment chain** where:
1. Each provider is tried in order
2. If a provider succeeds → the chain STOPS for that row
3. If a provider fails → the chain continues to the next provider
4. Result: maximum coverage at minimum credit spend

```
Row: Jane Smith, salesforce.com

Step 1: Apollo → Found email? YES → STOP. Cost: 1 credit. ✓
Step 2: (skipped)
Step 3: (skipped)

Row: Bob Chen, obscure-startup.io

Step 1: Apollo → Found? NO. Cost: 1 credit. ✗
Step 2: Prospeo → Found? NO. Cost: 1 credit. ✗
Step 3: Findymail → Found? YES → STOP. Cost: 1 credit. ✓
Total cost: 3 credits.

Row: Sunita Patel, tiny-consultancy.net

Step 1: Apollo → NO. 1 credit.
Step 2: Prospeo → NO. 1 credit.
Step 3: Findymail → NO. 1 credit.
Step 4: Dropcontact → NO. 1 credit.
Status: Unfound. Total cost: 4 credits. ✗
```

The goal is to find most people in steps 1–2 (cheap), and use steps 3–4 only for the hard-to-find 20%.

---

## Recommended Provider Order (2025–2026 Best Practice)

Order providers from **best coverage → specialty coverage**:

### For US Tech / SaaS Companies (Most Common ICP)
```
1. Apollo         → Best general US tech coverage, free tier available
2. Prospeo        → Good US + some EU, cost-effective
3. Findymail      → Higher accuracy, verifies before returning
4. Dropcontact    → Strong EU/France, GDPR-native
```

### For EU / UK Targeting
```
1. Apollo         → Still has reasonable EU coverage
2. Cognism        → GDPR-native, strong UK/EU (paid only)
3. Dropcontact    → Strong France + EU
4. Lusha          → Good EU business email coverage
```

### For APAC / Australia
```
1. Apollo         → Best available option
2. Lusha          → Some APAC coverage
3. Claygent       → Last resort — web research fills what databases miss
```

**Practical note:** For a first waterfall, just use Apollo + Hunter. That gets you to 60–65% and teaches the mechanics. Add providers 3–4 in Phase 2.

---

## Step-by-Step: Building a 2-Provider Waterfall

### Step 1: Structure Your Table

Your table needs these columns before adding enrichment:
- `first_name` (text)
- `last_name` (text)
- `company_name` (text)
- `company_domain` (text) ← most important
- `linkedin_url` (text, optional — improves accuracy)

If you have `email` already populated for some rows, add a formula column:
`{{IF(email != "", "pre-filled", "needs enrichment")}}` to see what needs enriching.

### Step 2: Add Provider 1 — Apollo People Search

1. Click **"+"** → Search "Apollo" → Select **"People Search"**
2. Configure inputs:
   - First Name → `first_name`
   - Last Name → `last_name`
   - Organization Domain → `company_domain`
3. Configure outputs (select all of these):
   - Email
   - Title
   - LinkedIn URL
   - Phone (optional)
4. **Run condition:** `Always` (this is provider 1 — no prior column to check)
5. Name the column: `email_apollo`

### Step 3: Add Provider 2 — Hunter.io

1. Click **"+"** → Search "Hunter" → Select **"Email Finder"**
2. Configure inputs:
   - First Name → `first_name`
   - Last Name → `last_name`
   - Domain → `company_domain`
3. Configure outputs:
   - Email
   - Email Verification Status
4. **Run condition:** `Only run if [email_apollo] is empty`
   - In Clay UI: click "Skip row if" → condition → "email_apollo is not empty"
5. Name the column: `email_hunter`

### Step 4: Add the Consolidation Column

Add a Formula column named `email_final`:
```
{{COALESCE(email_apollo, email_hunter)}}
```

Add another Formula column named `email_source`:
```
{{IF(email_apollo != "", "Apollo", IF(email_hunter != "", "Hunter", "Not found"))}}
```

The `email_source` column tells you which provider found each email — critical for measuring waterfall performance.

### Step 5: Add the Coverage Column

Add a Formula column named `coverage_status`:
```
{{IF(email_final != "", "Found", "Not found")}}
```

### Step 6: Test on 5 Rows

Before running the full table:
1. Select any 5 rows
2. Click "Run" (not bulk run) → run just those 5 rows
3. Check: Do the columns populate? Are the stop conditions working?
4. Open run history for one "Not found" row — see what Apollo + Hunter returned

### Step 7: Run Full Table

Once the 5-row test looks correct:
1. Select all rows
2. Run enrichment
3. Watch the progress bar
4. Note credits spent

### Step 8: Calculate Coverage Rate

After the run:
1. Filter by `coverage_status = "Found"` → note the count
2. Coverage rate = found rows / total rows × 100
3. Log this in `00_meta/progress_tracker.md`

Expected result for a 2-provider waterfall on a US SaaS list: **60–70%**

---

## Diagnosing Low Coverage

If your coverage is below 60%, investigate before adding more providers.

**Diagnostic checklist:**
```
□ Is company_domain accurate? (salesforce.com, not "Salesforce Inc")
□ Are names spelled correctly? (typos kill match rates)
□ Are these real working professionals (not freelancers or personal accounts)?
□ Is this a US/tech-heavy list? (EU/APAC lists will be lower — expected)
□ What does run history show for failing rows? (error message or "no match found"?)
```

**The domain quality test:**
Filter to "Not found" rows. Look at their company_domain values. If you see `salesforce.com` or `notion.so` in the unfound list, the domain is fine and the person is just hard to find. If you see `Salesforce Inc` or `SFDC` — you have domain quality issues.

---

## The Coverage Rate Formula

```python
# You'll need this when you build the Python analytics script in Phase 2

total_rows = len(df)
found_rows = len(df[df['coverage_status'] == 'Found'])
coverage_rate = (found_rows / total_rows) * 100

# By provider
apollo_found = len(df[df['email_source'] == 'Apollo'])
hunter_found = len(df[df['email_source'] == 'Hunter'])
print(f"Apollo contribution: {apollo_found/total_rows*100:.1f}%")
print(f"Hunter contribution: {hunter_found/total_rows*100:.1f}%")
```

---

## Hands-On Exercise

**Use the example CSV from Phase 1 or create your own 25-row list.**

Import or create a table with 25 rows (real companies, US SaaS focus is easiest for high coverage).

Build the full 2-provider waterfall:
1. Apollo People Search (always run)
2. Hunter Email Finder (only if Apollo failed)
3. `email_final` formula (COALESCE)
4. `email_source` formula
5. `coverage_status` formula

Run it. Log:
- Total rows: 25
- Coverage rate: \_\_\_%
- Apollo found: \_\_\_ rows
- Hunter found: \_\_\_ rows
- Not found: \_\_\_ rows
- Credits used: \_\_\_

**Bonus:** Export the not-found rows as a CSV. In Phase 2 you'll add 2 more providers to recover those.

---

## Recall Practice

1. What's the correct run condition syntax for provider 2 in a waterfall?
2. What does the `email_source` column tell you that `email_final` doesn't?
3. If Apollo finds 60% and Hunter finds 12% more, what is your total coverage rate?
4. You run a 2-provider waterfall on 100 rows. Apollo finds 60 rows (1 credit each). Hunter finds 15 more rows (2 credits each). 25 rows not found (2 credits each). How many total credits?
5. Name 3 things to check if your coverage rate is below 60%.
6. Why do you need the `email_source` column? What decision does it inform?

**Answers:**
4. (60×1) + (15×2) + (25×2) = 60 + 30 + 50 = 140 credits

---

## Anki Cards to Create

```
Q: What run condition do you set for provider 2 in a waterfall?
A: "Only run if [email_provider1] is empty" — skips the row if provider 1 already found an email

Q: What formula consolidates a 3-provider waterfall into one email column?
A: {{COALESCE(email_apollo, email_hunter, email_findymail)}}

Q: What column tells you which waterfall step found each email?
A: email_source — formula: {{IF(email_apollo!="","Apollo",IF(email_hunter!="","Hunter","..."))}}

Q: What is the expected coverage rate for a 2-provider waterfall (Apollo + Hunter) on a US SaaS list?
A: 60–70%

Q: What is the first thing to check when coverage rate is unexpectedly low?
A: Data quality of the company_domain column — providers use domain as the primary lookup key

Q: What does COALESCE do?
A: Returns the first non-empty value from a list of columns. Used to consolidate waterfall results.
```

---

## Next Module

→ [01_beginner/04_formula_language.md](./04_formula_language.md) — Complete formula reference: IF, COALESCE, SPLIT, CONTAINS, and scoring
