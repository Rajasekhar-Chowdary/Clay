# Module 2.3 — Claygent Basics

**Time:** 60–90 minutes (reading + 3 hands-on prompts)  
**Focus:** What Claygent is, when to use it, and how to write basic prompts

---

## What Claygent Actually Does

Claygent is a web browsing agent. For each row, it:
1. Takes your prompt (which includes column variables like `{company_domain}`)
2. Opens a browser
3. Navigates to the URL(s) you specify
4. Reads the page content
5. Returns structured data matching your instructions

It's not a database lookup. It's a researcher that reads the live internet.

This means:
- It finds data that no database has indexed yet
- It can read job postings, press releases, LinkedIn profiles, pricing pages
- Results vary by page availability and prompt quality
- It's slower and more expensive than database lookups (2–5 credits, 10–30 seconds per row)

---

## When to Use Claygent (and When NOT To)

**Use Claygent when:**
- Database providers all failed and you need that last 10–15% coverage
- You need custom data that no provider has (recent LinkedIn post, specific job posting)
- You need to verify or supplement database data with fresh information
- You're enriching < 500 rows (Claygent on 5,000 rows gets expensive fast)

**Do NOT use Claygent when:**
- Standard providers haven't been tried first (always waterfall Claygent last)
- The table has > 2,000 rows without a tight budget plan
- You haven't tested the prompt on 5 rows first (prompts fail in unexpected ways)
- You need real-time speed (Claygent is slow — 10–30s per row)

**Cost reality check:**
```
500 rows × 3 credits (average Claygent) = 1,500 credits
On Starter plan (2,000/month): that's 75% of your monthly budget on Claygent alone.

Better approach: Run Claygent only on rows where all 4 database providers failed.
If that's 15% of 500 rows = 75 rows × 3 credits = 225 credits. Manageable.
```

---

## Claygent Prompt Anatomy

Every Claygent prompt has 5 parts. Skip any one and you get unpredictable results.

```
1. VISIT    → Where should Claygent look?
2. FIND     → What specific data should it extract?
3. CONDITION → What should it do if the data isn't found?
4. FORMAT   → How should the output be structured?
5. CONSTRAINT → What should it NOT include?
```

**Weak prompt (common beginner mistake):**
```
Research {company_name} and tell me about them.
```
What you get: A paragraph about the company. Unstructured, inconsistent, can't be used in formulas.

**Strong prompt:**
```
Visit {company_domain}.
Find the company's primary product description (what they sell and who they sell to).
If no clear description on the homepage, check the /about page.
If still not found, return "No description available".
Return max 25 words. Do not include company name in the response.
```
What you get: Consistent, short, structured. Can be used in AI personalization columns.

---

## The 5 Fundamental Claygent Prompts

Master these 5 before building custom ones.

### Prompt 1: Email Recovery (Last-Resort)

Use this when all 4 database providers failed.

```
Visit https://www.linkedin.com/in/{linkedin_username} if available, or search LinkedIn for "{first_name} {last_name}" at "{company_name}".

Find the current work email for {first_name} {last_name}.
Check their LinkedIn profile contact info section.
If no email found on LinkedIn, check if they have a personal website or GitHub profile listed.

If found: return the email address only.
If not found: return "Not found - manual research needed".
```

**Caution:** Claygent can see publicly available LinkedIn data, not private profile sections. This works ~30–40% of the time for hard-to-find contacts. Still better than nothing.

### Prompt 2: Job Title Verification

Use when Apollo returned a job title but you suspect it's outdated.

```
Visit {linkedin_url}.
Find {first_name}'s current job title and current company name as shown on their LinkedIn profile today.
If the profile is unavailable, return "Profile not accessible".
Return format: "Title: [title] | Company: [company]"
Max 15 words total.
```

### Prompt 3: Recent LinkedIn Activity (Personalization Signal)

Use when you want a personalization hook for cold outreach.

```
Visit {linkedin_url}.
Find {first_name}'s most recent post or article published in the last 90 days.
Extract the core topic or insight they shared in 1–2 sentences.
If they haven't posted in 90 days, return "No recent posts in last 90 days".
If profile is private or unavailable, return "Profile not accessible".
Max 40 words. Do not editorialize or add opinions.
```

### Prompt 4: Company Description

Use for personalization or qualification filtering.

```
Visit {company_domain}.
Find what the company sells and who their primary customer is.
Use the homepage hero text or the /about page.
Return: "[Company] helps [customer type] [do X]" — max 20 words.
If unclear, check /about. If still unclear, return "Description not found".
```

### Prompt 5: Job Posting Signal

Use to detect if a company is hiring for specific roles (buying signal).

```
Visit {company_domain}/careers or search "{company_name} jobs site:lever.co OR site:greenhouse.io OR site:ashbyhq.com".
Look for open positions with titles containing "RevOps", "Revenue Operations", "GTM", "Sales Operations", or "Data".
If found: return the top 2 matching job titles and posting dates if visible.
If none found: return "No matching open roles".
Max 40 words.
```

---

## Writing Custom Claygent Prompts

### The Variables You Can Use

Any column in your table is available as `{column_name}`:
- `{first_name}`, `{last_name}`, `{company_name}`, `{company_domain}`
- `{linkedin_url}`, `{email_final}`, `{job_title}`
- Any custom column you've created

### Rules for Better Prompts

**Rule 1: Always specify where to look**
Bad: "Find information about {company_name}"
Good: "Visit {company_domain}/about and {company_domain}/pricing"

**Rule 2: Always include a fallback**
Bad: "Find the funding stage for {company_name}"
Good: "Find the funding stage. If not found, return 'Unknown'."

**Rule 3: Set a word limit**
Without a word limit, Claygent can return paragraphs. Always set max word count.
Good: "Max 25 words."

**Rule 4: Specify the exact format**
Bad: "Return the tech stack"
Good: "Return as: CRM=[tool], Email=[tool], Analytics=[tool]. Use 'unknown' for missing."

**Rule 5: Use conditional logic in prompts**
```
If {first_name} is a VP or Director level, also find their reported team size.
Otherwise, just return their title.
```

**Rule 6: Test on 5 rows before bulk run**
Always. Prompts fail in unexpected ways. A prompt that works for US companies may fail for UK companies. Test first.

---

## Handling Claygent Failures

Claygent returns errors in several ways:
- **"Not found"** — you wrote a fallback correctly
- **Empty** — the page was inaccessible or the prompt was too ambiguous
- **Wrong format** — the output doesn't match what you specified
- **Hallucination** — Claygent invented data (rare but happens)

**Handling in formulas:**

```
Clean up Claygent output before using it in AI columns:
{{IF(
  claygent_signal == "" OR claygent_signal == "Not found" OR claygent_signal == "Profile not accessible",
  "SKIP",
  claygent_signal
)}}
```

Then use this cleaned column in your AI personalization column — the AI only writes openers for rows with real signal.

---

## The Claygent Test Protocol

Before running Claygent on a full table:

1. Select 5 rows with diverse characteristics (big company, small company, EU contact, US contact, active LinkedIn user)
2. Run Claygent on just those 5 rows
3. Review each output:
   - Did it find what you asked for?
   - Is the format consistent?
   - Any hallucinations?
   - What did it return for the "not found" fallback?
4. If output is inconsistent → refine the prompt
5. Re-test 5 rows
6. Only proceed to full table when 4/5 rows give correctly structured output

---

## Hands-On Exercise

On your test table, add 3 Claygent columns:

**Column 1:** Company description
Use Prompt 4 above with `{company_domain}`

**Column 2:** Job posting signal
Use Prompt 5 above with `{company_domain}` and `{company_name}`

**Column 3:** Your own custom prompt
Write a Claygent prompt from scratch for one of these:
- What's the company's main pain point based on their homepage copy?
- Does the company have a case studies page? If yes, what industry are most case studies from?
- What does the company say about integrations on their website?

Test all 3 on 5 rows. Evaluate output quality. Refine prompts that return inconsistent results.

---

## Anki Cards to Create

```
Q: What are the 5 parts of a strong Claygent prompt?
A: VISIT (where to look), FIND (what to extract), CONDITION (fallback if not found), FORMAT (output structure), CONSTRAINT (what to exclude)

Q: When should Claygent be run in a waterfall?
A: Last — after all database providers have been tried. Never run Claygent first.

Q: How many credits does Claygent typically cost per row?
A: 2–5 credits (vs 1 credit for database provider lookups)

Q: What does the Claygent test protocol require?
A: Test on 5 diverse rows before bulk run. Check: correct data, consistent format, no hallucinations, fallback works.

Q: How do you prevent hallucinated Claygent output from being used in downstream columns?
A: Formula: IF(output == "" OR output == "Not found" OR output == "Profile not accessible", "SKIP", output)

Q: What is the max recommended table size for running Claygent on all rows?
A: Gate Claygent — only run on rows where all database providers failed (typically 15–20% of table)
```

---

## Next Module

→ [02_intermediate/04_project_100row.md](./04_project_100row.md) — Phase 2 project: 100-row pipeline at 85%+ coverage
