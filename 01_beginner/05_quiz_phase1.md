# Phase 1 Mastery Quiz + Beginner Project

**Time:** 30 min quiz + 2–3 hrs project  
**Pass criteria:** 80%+ on quiz, 25-row project at 65%+ coverage

---

## Phase 1 Mastery Quiz

Answer without looking at notes. Write your answers, then check.

### Section A: Concepts (10 questions, 1 point each)

1. What are the 5 column types in Clay? List all 5.

2. You add 3 enrichment columns to a table with no run conditions. What happens when you run enrichment on 100 rows?

3. What is the formula to extract the domain from an email address?

4. A 4-provider waterfall finds the email on provider 3 for a given row. How many credits does that row cost?

5. You want to consolidate `email_apollo`, `email_prospeo`, and `email_findymail` into one column. Write the formula.

6. What does auto-enrich do, and when should it be turned on?

7. What is the expected coverage rate for a 2-provider waterfall (Apollo + Hunter) on a US SaaS list?

8. Name 3 things to check when coverage rate is lower than expected.

9. What is Claygent, and what can it find that Apollo/Hunter cannot?

10. Write a formula that labels a contact as "Enterprise" if employee_count > 500, "Mid-Market" if > 100, and "SMB" otherwise.

### Section B: Applied (5 questions, 2 points each)

11. You're building a waterfall with Apollo (provider 1) and Hunter (provider 2). Write the run condition for the Hunter column in plain English.

12. You run enrichment on a 50-row table with a 3-provider waterfall:
    - Apollo finds 30 rows at 1 credit each
    - Hunter finds 10 rows at 2 credits each
    - Findymail finds 5 rows at 3 credits each
    - 5 rows not found at 3 credits each
    What's the total credit cost? What's the coverage rate?

13. Your coverage rate is 52%. You investigate the run history and notice all failing rows have company_domain values like "Acme Corp" and "Big Company LLC". What's the problem and how do you fix it?

14. Write a formula column `lead_tier` that returns:
    - "Tier A" if: US AND employee_count 50–500 AND contains "Salesforce" in technologies
    - "Tier B" if: US AND employee_count >= 20
    - "Tier C" for everything else

15. What columns should every Clay table have after waterfall enrichment? List 5 essential formula columns and what each does.

---

## Answer Key

**Section A:**
1. Text/Number/Date, Enrichment, Formula, Claygent, AI (HTTP and Webhook Action are bonus)
2. All providers run on all rows regardless — no stop conditions means no waterfall savings. Credits fire.
3. `{{SPLIT(email_final, "@")[1]}}`
4. 3 credits (provider 1 fail = 1 credit, provider 2 fail = 1 credit, provider 3 success = 1 credit)
5. `{{COALESCE(email_apollo, email_prospeo, email_findymail)}}`
6. Auto-enrich runs enrichment automatically when a row is added. Turn ON only for production tables with fully tested waterfalls.
7. 60–70%
8. Domain quality (wrong format), input name quality (typos/missing), geography (EU/APAC lists are lower by nature)
9. Claygent is Clay's AI research agent — it browses live web pages. It can find real-time data: LinkedIn posts, job postings, funding news, custom company research.
10. `{{IF(employee_count > 500, "Enterprise", IF(employee_count > 100, "Mid-Market", "SMB"))}}`

**Section B:**
11. "Only run if `email_apollo` is empty" (skip this row if Apollo already found an email)
12. Credits: (30×1)+(10×2)+(5×3)+(5×3) = 30+20+15+15 = 80 credits. Coverage: (30+10+5)/50 = 45/50 = 90%
13. The company_domain column contains company names, not domains. Fix: clean the domain column to use actual domains (acme.com, bigcompany.com). May need a Claygent column to find the domain from the company name.
14. See formula in Module 1.4, Formula #5
15. `email_final` (COALESCE), `email_source` (which provider found it), `coverage_status` (Found/Not found), `full_name` (string concat), `company_size_tier` (IF label)

**Scoring:**
- 18–20: Ready for Phase 2
- 14–17: Review the modules where you missed, then proceed
- Below 14: Redo the hands-on exercises before moving on

---

## Beginner Project: 25-Row Enrichment

**This is mandatory before Phase 2.**

### Objective
Build a complete enrichment table for 25 people with measurable coverage rate and documented results.

### Input Data Options
- Use the `example_clay_test_companies.csv` from GTM_Mastery if you have it
- OR create your own 25-row list of real B2B contacts from LinkedIn Sales Navigator or Apollo's free search
- Columns required: first_name, last_name, company_name, company_domain

### What to Build

**Enrichment columns (in order):**
1. `email_apollo` — Apollo People Search (always run)
   - Outputs: email, job_title, linkedin_url
2. `email_hunter` — Hunter Email Finder (run if email_apollo is empty)
   - Outputs: email

**Formula columns:**
3. `email_final` — COALESCE(email_apollo, email_hunter)
4. `email_source` — IF logic showing which provider found it
5. `coverage_status` — "Found" or "Not found"
6. `full_name` — first_name + last_name concat
7. `company_domain_from_email` — extract domain from email_final (if found)
8. `lead_tier` — Enterprise/Mid-Market/SMB based on any size data you have

### Success Criteria
- [ ] Table created with 25 rows
- [ ] 2-provider waterfall built with correct run conditions
- [ ] `email_final`, `email_source`, `coverage_status` columns present
- [ ] Enrichment run on all 25 rows
- [ ] Coverage rate calculated and logged in `00_meta/progress_tracker.md`
- [ ] Coverage rate ≥ 65%
- [ ] Run history reviewed for at least 3 "Not found" rows

### Deliverable
Fill in this table in progress_tracker.md:

```
Project: 25-row beginner enrichment
Date: ___________
Total rows: 25
Apollo found: ___
Hunter found: ___
Not found: ___
Coverage rate: ___%
Credits used: ___
Biggest issue found: ___________________________
Fix applied: ___________________________
```

---

## Feynman Check

Before moving to Phase 2, explain the following to yourself out loud (or in writing) without notes:

*"Explain what a waterfall enrichment is, how credits work, and what I need to do to get from 65% to 85% coverage."*

If you can't explain it simply, you have a gap. Go back and fill it. The gap will cost you time in Phase 2.

---

## You're Ready for Phase 2 When:

- [ ] Quiz score ≥ 80% (18/20 points)
- [ ] 25-row project complete with coverage ≥ 65%
- [ ] You can explain waterfall logic without looking at notes
- [ ] Anki deck has at least 20 cards from Phase 1 modules

→ [02_intermediate/01_waterfall_mastery.md](../02_intermediate/01_waterfall_mastery.md)
