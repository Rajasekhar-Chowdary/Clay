# Clay Formula Cheatsheet

Quick reference for every formula you'll actually use.

---

## String

```
Full name:          {{first_name}} {{last_name}}
Trim whitespace:    {{TRIM(first_name)}}
Uppercase:          {{UPPER(company_name)}}
Lowercase:          {{LOWER(email_final)}}
Length:             {{LEN(email_final)}}
Replace:            {{REPLACE(company_name, " Inc", "")}}
Split (get domain): {{SPLIT(email_final, "@")[1]}}
Contains check:     {{CONTAINS(tech_stack, "Salesforce")}}
Join array:         {{JOIN(tech_array, ", ")}}
```

## Logic

```
Basic IF:           {{IF(email_final != "", "Found", "Not found")}}
Nested IF:          {{IF(count>500,"Enterprise",IF(count>100,"Mid-Market","SMB"))}}
AND condition:      {{IF(country=="US" AND count>100, "Tier A", "Other")}}
OR condition:       {{IF(stage=="Series A" OR stage=="Series B", "Growth", "Other")}}
COALESCE:           {{COALESCE(email_apollo, email_hunter, email_findymail, "Not found")}}
Is empty:           {{ISEMPTY(email_apollo)}}
Is not empty:       {{ISNOTEMPTY(linkedin_url)}}
```

## Math

```
Add:                {{score_a + score_b}}
Percentage:         {{found_count / total_count * 100}}
Round:              {{ROUND(coverage_rate, 1)}}
Convert to number:  {{NUMBER(employee_count)}}
Max of values:      {{MAX(score_a, score_b)}}
```

## Date

```
Today:              {{TODAY()}}
Date difference:    {{DATEDIFF(TODAY(), last_enriched_date)}}
Format date:        {{FORMATDATE(enriched_at, "YYYY-MM-DD")}}
```

---

## The 10 Must-Have Table Formulas

```
1. email_final:
   {{COALESCE(email_apollo, email_prospeo, email_findymail, email_dropcontact)}}

2. email_source:
   {{IF(ISNOTEMPTY(email_apollo),"Apollo",IF(ISNOTEMPTY(email_prospeo),"Prospeo",IF(ISNOTEMPTY(email_findymail),"Findymail",IF(ISNOTEMPTY(email_dropcontact),"Dropcontact","Not found"))))}}

3. coverage_status:
   {{IF(ISNOTEMPTY(email_final), "Found", "Not found")}}

4. full_name:
   {{TRIM(first_name)}} {{TRIM(last_name)}}

5. size_tier:
   {{IF(NUMBER(employee_count)>=1000,"Enterprise",IF(NUMBER(employee_count)>=200,"Mid-Market",IF(NUMBER(employee_count)>=50,"SMB","Micro")))}}

6. domain_from_email:
   {{IF(CONTAINS(email_final,"@"),SPLIT(email_final,"@")[1],company_domain)}}

7. icp_tier_label:
   {{IF(icp_score>=70,"Tier A — Hot",IF(icp_score>=45,"Tier B — Warm","Tier C — Cold"))}}

8. has_signal:
   {{IF(signal_tier != "No Signal — Cold", "Signal found", "No signal")}}

9. data_source (GDPR):
   {{IF(ISNOTEMPTY(email_apollo),"Apollo.io",IF(ISNOTEMPTY(email_prospeo),"Prospeo.io",IF(ISNOTEMPTY(email_findymail),"Findymail.io","Unknown")))}}

10. re_enrich_flag:
    {{IF(DATEDIFF(TODAY(),last_enriched_date)>60,"Re-enrich","Current")}}
```

---

## ICP Score Formula (Full)

```
{{
  IF(NUMBER(employee_count)>=50 AND NUMBER(employee_count)<=200, 30,
    IF(NUMBER(employee_count)>=201 AND NUMBER(employee_count)<=500, 25,
      IF(NUMBER(employee_count)>=20, 15, 5)))
  +
  IF(hq_country=="US", 20, IF(hq_country=="UK" OR hq_country=="CA" OR hq_country=="AU", 15, 5))
  +
  IF(CONTAINS(tech_stack,"Salesforce"), 20, IF(CONTAINS(tech_stack,"HubSpot"), 15, 0))
  +
  IF(funding_stage=="Series A" OR funding_stage=="Series B", 25,
    IF(CONTAINS(funding_stage,"Series"), 15, 0))
}}
```

---

## Common Gotchas

| Issue | Bad | Fixed |
|-------|-----|-------|
| Column name case | `{{Email_Apollo}}` | `{{email_apollo}}` |
| No fallback on COALESCE | `{{COALESCE(a,b)}}` | `{{COALESCE(a,b,"Not found")}}` |
| SPLIT with no delimiter | `{{SPLIT("jane","@")[1]}}` | Wrap in IF CONTAINS check first |
| Number stored as string | `{{count > 100}}` | `{{NUMBER(count) > 100}}` |
| Empty string ≠ null | `{{IF(email=="","empty","found")}}` | Use ISEMPTY() |
