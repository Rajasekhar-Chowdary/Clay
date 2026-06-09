# Module 1.4 — Clay Formula Language

**Time:** 45–60 minutes  
**Format:** Reference + 10 practice exercises  
**Note:** Formulas are free (no credits). Master them — they replace a lot of manual data work.

---

## Syntax Basics

Clay uses double curly brace syntax to reference column values:
```
{{column_name}}
```

Column names with spaces use underscores or quotes:
```
{{first_name}}
{{company_domain}}
```

Formulas can be nested, chained, and combined.

---

## The Core Functions

### String Functions

**CONCAT / string interpolation**
```
{{first_name}} {{last_name}}
→ "Jane Smith"

{{job_title}} at {{company_name}}
→ "VP of Revenue Operations at Salesforce"
```

**TRIM** (remove leading/trailing spaces)
```
{{TRIM(first_name)}}
```

**UPPER / LOWER**
```
{{UPPER(company_name)}}   → "SALESFORCE"
{{LOWER(email_final)}}    → "jane.smith@salesforce.com"
```

**SPLIT** (split string at delimiter, return index)
```
{{SPLIT(email_final, "@")[1]}}
→ "salesforce.com"    (extracts domain from email)

{{SPLIT(full_name, " ")[0]}}
→ "Jane"    (extracts first word)
```

**CONTAINS** (returns true/false)
```
{{CONTAINS(technologies, "Salesforce")}}
→ true/false

Used in IF conditions:
{{IF(CONTAINS(technologies, "Salesforce"), "Salesforce user", "Not Salesforce")}}
```

**REPLACE** (find and replace in a string)
```
{{REPLACE(company_name, " Inc", "")}}
→ "Salesforce" (instead of "Salesforce Inc")
```

**LEN** (string length)
```
{{LEN(email_final)}}
→ number of characters in the email
```

---

### Logical Functions

**IF (single condition)**
```
{{IF(email_final != "", "Email found", "No email")}}

{{IF(employee_count > 500, "Enterprise", "Not Enterprise")}}

{{IF(hq_country == "US", "US Lead", "International")}}
```

**IF (nested — multiple conditions)**
```
{{IF(
  employee_count > 500,
  "Enterprise",
  IF(
    employee_count > 100,
    "Mid-Market",
    IF(
      employee_count > 20,
      "SMB",
      "Very Small"
    )
  )
)}}
```

**AND / OR in conditions**
```
{{IF(hq_country == "US" AND employee_count > 100, "Tier A", "Other")}}

{{IF(funding_stage == "Series A" OR funding_stage == "Series B", "Growth Stage", "Other")}}
```

**COALESCE (return first non-empty)**
```
{{COALESCE(email_apollo, email_hunter, email_findymail, "Not found")}}

Tries each in order. Returns the first that isn't empty.
The last argument can be a fallback string.
```

**ISEMPTY / ISNOTEMPTY**
```
{{ISEMPTY(email_apollo)}}   → true if apollo didn't find anything
{{ISNOTEMPTY(linkedin_url)}} → true if LinkedIn URL exists
```

---

### Math Functions

**Basic arithmetic**
```
{{employee_count * 2}}
{{revenue / employee_count}}    → revenue per employee
{{score_fico + score_intent}}   → combined score
```

**ROUND**
```
{{ROUND(coverage_rate, 2)}}    → rounds to 2 decimal places
```

**MIN / MAX**
```
{{MIN(score_a, score_b, score_c)}}
{{MAX(score_a, score_b, score_c)}}
```

**ABS** (absolute value)
```
{{ABS(score_delta)}}
```

---

### Array Functions (for multi-value fields)

Some enrichment columns return arrays (e.g., list of technologies, list of keywords).

**SPLIT** (string → array)
```
{{SPLIT(technologies_string, ",")}}
→ ["Salesforce", "HubSpot", "Outreach"]
```

**JOIN** (array → string)
```
{{JOIN(tech_array, " | ")}}
→ "Salesforce | HubSpot | Outreach"
```

**CONTAINS on arrays**
```
{{IF(CONTAINS(tech_array, "Salesforce"), "Uses Salesforce", "No Salesforce")}}
```

---

## 10 Practical Formulas (Build All of These)

These are the formulas you'll use in every real table.

### 1. Full Name Column
```
{{TRIM(first_name)}} {{TRIM(last_name)}}
```

### 2. Waterfall Email Consolidation
```
{{COALESCE(email_apollo, email_hunter, email_findymail, email_dropcontact)}}
```

### 3. Email Source Attribution
```
{{IF(ISNOTEMPTY(email_apollo), "Apollo",
  IF(ISNOTEMPTY(email_hunter), "Hunter",
    IF(ISNOTEMPTY(email_findymail), "Findymail",
      IF(ISNOTEMPTY(email_dropcontact), "Dropcontact",
        "Not found"
      )
    )
  )
)}}
```

### 4. Company Size Tier
```
{{IF(employee_count >= 1000, "Enterprise",
  IF(employee_count >= 200, "Upper Mid-Market",
    IF(employee_count >= 50, "Mid-Market",
      IF(employee_count >= 10, "SMB",
        "Micro"
      )
    )
  )
)}}
```

### 5. ICP Score Label (3-tier)
```
{{IF(
  hq_country == "US" AND
  employee_count >= 50 AND employee_count <= 500 AND
  CONTAINS(technologies, "Salesforce"),
  "Tier A",
  IF(
    (hq_country == "US" OR hq_country == "UK") AND
    employee_count >= 20,
    "Tier B",
    "Tier C"
  )
)}}
```

### 6. Domain from Email
```
{{IF(ISNOTEMPTY(email_final), SPLIT(email_final, "@")[1], company_domain)}}
```

### 7. LinkedIn Profile Status
```
{{IF(ISNOTEMPTY(linkedin_url), "Has LinkedIn", "Missing LinkedIn")}}
```

### 8. Coverage Status
```
{{IF(ISNOTEMPTY(email_final), "Enriched", "Not found")}}
```

### 9. Personalized Subject Line
```
{{first_name}}, quick question about {{company_name}}'s outbound
```

### 10. Lead Score (Numeric)
```
{{
  IF(employee_count >= 100, 30, IF(employee_count >= 50, 20, 10))
  +
  IF(hq_country == "US", 20, IF(hq_country == "UK", 15, 5))
  +
  IF(CONTAINS(technologies, "Salesforce"), 25, IF(CONTAINS(technologies, "HubSpot"), 20, 0))
  +
  IF(funding_stage == "Series B" OR funding_stage == "Series C", 25, IF(funding_stage == "Series A", 15, 0))
}}
```
This returns a numeric score (0–100). You can then add another formula column:
```
{{IF(lead_score >= 70, "Hot", IF(lead_score >= 40, "Warm", "Cold"))}}
```

---

## Common Formula Errors and Fixes

**Error: Column name not found**
```
Broken:  {{Email_Apollo}}  (wrong case)
Fixed:   {{email_apollo}}  (Clay is case-sensitive in formulas)
```

**Error: Formula returns empty instead of fallback**
```
Broken:  {{COALESCE(email_apollo, email_hunter)}}
         → returns empty if both are null

Fixed:   {{COALESCE(email_apollo, email_hunter, "Not found")}}
         → returns "Not found" string
```

**Error: SPLIT index out of bounds**
```
Broken:  {{SPLIT("one", "@")[1]}}
         → crashes if no "@" in the string

Fixed:   {{IF(CONTAINS(email_final, "@"), SPLIT(email_final, "@")[1], company_domain)}}
         → fallback if no @ symbol
```

**Error: Comparison fails on numbers stored as strings**
```
Broken:  {{IF(employee_count > 100, ...)}}
         → may fail if employee_count came back as string "150"

Fixed:   {{IF(NUMBER(employee_count) > 100, ...)}}
```

---

## Formula Practice Exercises

Build these 5 columns in a real Clay table:

1. A column that labels contacts as "Decision Maker" if their title contains "VP", "Director", "Head of", or "C" (CEO/CTO/CMO/CFO)

2. A column that shows the LinkedIn domain from a LinkedIn URL
   (e.g., `https://linkedin.com/in/jane-smith` → `jane-smith`)

3. A column that flags rows where the email is found but LinkedIn URL is missing

4. A column that calculates a simple priority score (0–60) based on:
   - Company size: 0–20 points
   - Geography: 0–20 points
   - Has email: 0–20 points

5. A column that generates a one-line personalization opener:
   `"Hi {{first_name}}, I noticed {{company_name}} is in {{industry}}..."`

---

## Anki Cards to Create

```
Q: What function returns the first non-empty value from a list?
A: COALESCE — e.g., {{COALESCE(email_apollo, email_hunter, "Not found")}}

Q: How do you extract the domain from an email address in Clay?
A: {{SPLIT(email_final, "@")[1]}}

Q: Formula for a 3-tier company size label (Enterprise/Mid-Market/SMB)?
A: {{IF(count>=1000,"Enterprise",IF(count>=200,"Mid-Market","SMB"))}}

Q: What does CONTAINS return?
A: true or false — checks if a string or array contains a specified value

Q: How do you safely extract a split value when the delimiter might not exist?
A: Wrap in IF(CONTAINS(...),...) to check first before splitting

Q: Are formula columns free in Clay?
A: Yes — formula columns never cost credits, they compute from existing column data
```

---

## Next Module

→ [01_beginner/05_quiz_phase1.md](./05_quiz_phase1.md) — Phase 1 mastery quiz + Beginner Project spec
