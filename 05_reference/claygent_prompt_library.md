# Claygent Prompt Library

Copy-paste prompts. Test on 5 rows before bulk run. Always set a max word limit.

---

## Email Recovery

```
Visit https://www.linkedin.com/search/results/people/?keywords={first_name}+{last_name}+{company_name} if {linkedin_url} is empty, otherwise visit {linkedin_url}.
Find the current work email for {first_name} {last_name}.
Check profile contact info section.
If no email found: return "Not found".
Output: email address only, or "Not found".
Max 10 words.
```
**Gate:** Only run if all database providers returned empty.  
**Expected success rate:** 25–40%.

---

## Job Title Verification

```
Visit {linkedin_url}.
Find {first_name}'s current job title and current company as shown today.
If profile unavailable: return "Profile not accessible".
Return format: "[Title] at [Company]"
Max 15 words.
```
**Gate:** Run when you suspect Apollo returned a stale title.

---

## Company Description (for AI openers)

```
Visit {company_domain}.
Find what the company sells and who their primary customer is. Use homepage hero or /about page.
Return: "{company_name} helps [customer type] [do X]" — max 20 words.
If unclear after checking /about: return "Description not found".
```
**Gate:** Always (no credits concern — this feeds AI personalization).  

---

## LinkedIn Post Extractor (Personalization Signal)

```
Visit {linkedin_url}.
Find {first_name}'s most recent post or article published in the last 90 days.
Extract the single most important insight or claim they made.
Return: "In [month], {first_name} posted about [topic]. Key insight: [their main point in 15 words]"
If no posts in 90 days: return "No recent LinkedIn activity".
If private: return "Profile not accessible".
Max 50 words.
```
**Gate:** icp_score >= 60 AND email found.

---

## Funding Signal Detector

```
Search for news about {company_name} raising a funding round in the last 12 months.
Check TechCrunch, Crunchbase, and {company_domain}/news or {company_domain}/press.
If funding found: return "FUNDING: [Series type] [amount if available] [approx date]"
Example: "FUNDING: Series B $25M Q1 2026"
If not found: return "No funding signal".
Max 25 words.
```
**Gate:** icp_tier != "Tier C".

---

## Leadership Change Signal

```
Search LinkedIn for new executive hires at {company_name} in the last 6 months.
Look specifically for: VP Sales, Chief Revenue Officer, Head of Growth, VP Marketing, Revenue Operations leader.
If found: return "HIRE: [Name] joined as [Title] [Month Year]"
If not found: return "No leadership signal".
Max 30 words.
```
**Gate:** icp_score >= 55.

---

## RevOps / GTM Hiring Signal

```
Visit {company_domain}/careers. Also check https://jobs.lever.co/{company_name_clean} and https://boards.greenhouse.io/{company_name_clean}.
Look for open positions with titles containing: RevOps, Revenue Operations, GTM, Sales Operations, Marketing Operations.
If found: return "HIRING: [Job title]" for most relevant role.
If not found: return "No GTM hiring signal".
Max 20 words.
```
**Gate:** icp_score >= 50.  
**Note:** Replace spaces in company_name with hyphens for the URL.

---

## Tech Stack Detection (CRM Focus)

```
Visit {company_domain}/careers, {company_domain}/integrations, and {company_domain}.
Look for mentions of: Salesforce, HubSpot, Pipedrive, Marketo, Pardot in job requirements or integration lists.
Return: "CRM: [detected tool or 'unknown']"
If multiple detected: "CRM: [primary], also uses [others]"
Max 20 words.
```
**Gate:** employee_count >= 50.

---

## ICP Qualifier (Pre-Filter)

```
Visit {company_domain}.
Answer based on what you can read on the website:
1. B2B or B2C? (B2B / B2C / Both / Unclear)
2. Primary customer size? (SMB / Mid-Market / Enterprise / Mixed / Unclear)
3. Any mention of sales, growth, or revenue operations? (Yes / No)
Return: "Type:[answer] Customer:[answer] RevOps:[answer]"
Max 20 words.
```
**Gate:** Use this as a pre-enrichment filter on raw company lists.

---

## Competitive Alternatives Research

```
Visit {company_domain}/pricing, {company_domain}/integrations, and {company_domain}.
Find which competitors or alternatives they mention or integrate with.
Return a comma-separated list of tools mentioned.
If none found: return "No alternatives mentioned".
Max 30 words.
```

---

## Custom Prompt Template (Build Your Own)

```
VISIT: [exact URL(s) to visit]
FIND: [specific data to extract]
CONDITION: If not found [return this specific fallback string]
RETURN FORMAT: [exact output format with example]
Max [N] words. Do not [specific exclusion].
```

---

## Quality Checklist Before Bulk Run

```
□ Tested on 5 diverse rows (large US, small US, EU, active LinkedIn, no LinkedIn)
□ Fallback returns a detectable string ("Not found", "No signal", etc.)
□ Word limit set
□ Format instruction includes an example
□ Run condition gates the column appropriately
□ 4/5 test rows returned correctly structured output
```
