# Session 1 — TODAY (45–90 min, hands-on in Clay)

**Goal:** A working 2-provider email waterfall with a measured coverage rate. This is Week 1
of the fast-track. You're not reading about waterfalls — you're building one.

**Read alongside (don't pre-read, reference as you build):** `01_beginner/03_first_waterfall.md`

## Steps

1. **Import the seed list** → `01_beginner/seed_companies_25.csv` (25 real B2B SaaS companies).
   New Clay table → Import CSV. You'll have `company_name` + `company_domain`.

2. **Get a real contact per company (list-building, the skill before the waterfall):**
   Add an **Apollo → Find People** (a.k.a. "Find Decision Makers") enrichment.
   - Input: `company_domain`
   - Filter title: `VP Sales` OR `Head of Revenue Operations` OR `RevOps`
   - Output: first_name, last_name, title, linkedin_url
   - This pulls a live, real contact — no fabricated data.

3. **Build the email waterfall** (follow module 1.3 Steps 2–5 exactly):
   - Provider 1: **Apollo People Search** → output Email → run condition `Always` → name `email_apollo`
   - Provider 2: **Hunter Email Finder** → run condition `only if email_apollo is empty` → name `email_hunter`
   - Consolidate: formula `email_final = {{COALESCE(email_apollo, email_hunter)}}`
   - Source: formula `email_source = {{IF(email_apollo != "", "Apollo", IF(email_hunter != "", "Hunter", "Not found"))}}`
   - Coverage: formula `coverage_status = {{IF(email_final != "", "Found", "Not found")}}`

4. **Test on 5 rows first** (module 1.3 Step 6). Confirm the stop condition works — Hunter
   should be skipped on rows where Apollo already found the email. Watch your credit spend.

5. **Run the full 25.** Then compute: `coverage % = Found rows / 25 × 100`.

## Close the session (the part that makes it stick — don't skip)
- **Screenshot** the table showing `email_source` + coverage.
- **Log the number** in `00_meta/progress_tracker.md` → Coverage Rate Log row.
- **3 Anki cards** from what was new (e.g. "What does a waterfall stop condition do?",
  "Apollo vs Hunter — which is provider 1 and why?", "How do you measure coverage rate?").
- **One-line retrieval:** close Clay, write from memory what each of the 5 columns does.

## Gate to pass Week 1
Coverage ≥ 70% on the 25 rows. If lower → your input domains or title filter are off, not the
waterfall. Tell me the number and I'll help you debug.
