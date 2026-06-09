# Scenario 5 — The LinkedIn Content Signal

**Challenge:** Find everyone in your ICP who posted on LinkedIn about "GTM", "outbound", "data quality", or "RevOps" in the last 30 days — then reach out referencing their specific post.

**Why it works:** People who post about a problem are publicly thinking about it. You're joining a conversation they started.

---

## Step 1: Find the Posters

**Method A: PhantomBuster**
- LinkedIn search → people + keywords (GTM, outbound, data quality, RevOps)
- Filter by 2nd-degree connections, B2B profiles
- Export with: name, company, LinkedIn URL, post snippet

**Method B: LinkedIn Sales Navigator**
- Boolean search: "GTM" OR "outbound" OR "RevOps" in posts
- Filter by role (VP, Director, Head of), company size, industry
- Export

**Method C: Clay's LinkedIn scraper**
- Clay has a native LinkedIn search that can pull recent post content
- Set up a scheduled search for keyword terms

---

## Clay Table: `content-signal-prospects`

### Columns

```
Input: first_name, last_name, company_name, company_domain, linkedin_url, post_snippet (from source)

ICP filter formula (before enrichment):
  icp_pre_check: {{IF(ISNOTEMPTY(linkedin_url) AND company_domain != "", "Enrich", "Skip")}}

Company enrichment (gated: icp_pre_check == "Enrich"):
  Apollo Company: employee_count, industry, hq_country
  icp_score formula

Email waterfall (gated: icp_score >= 40):
  4-provider waterfall

Claygent: post details (gated: email found AND icp_score >= 50)
  "Visit {linkedin_url}.
  Find {first_name}'s most recent post published in the last 30 days.
  Extract: the specific claim or insight they made.
  Return: 'They said: [their specific claim in 15 words]'
  If no post found in 30 days: return 'No recent post'
  Max 30 words."

Formula: post_usable
  {{IF(CONTAINS(claygent_post_detail, "They said:"), "Yes", "No")}}

AI opener (gated: email found AND post_usable == "Yes"):
  "Contact: {first_name}, {job_title} at {company_name}
  They recently posted: {claygent_post_detail}
  
  Write 1 sentence opener (max 25 words) that:
  1. References their specific post/insight (not a paraphrase — echo their specific point)
  2. Adds one relevant observation from your perspective
  3. Sounds like a reply from someone who actually read it (NOT: 'Great post!')
  
  Output: sentence only."

AI opener fallback (gated: email found AND post_usable == "No"):
  Use post_snippet from original source if available
  Otherwise: role-based opener
```

---

## The Post-Outreach Sequence

**Pre-email warm-up (2 days before emailing):**
1. Like their post (LinkedIn)
2. Leave a substantive comment on their post (not "great insight!")
3. Wait 24 hours
4. Connect request with a note referencing the post

**Email sequence:**
- Day 1: Email referencing post
- Day 5: Follow-up with related insight/resource
- Day 10: Final breakup email

**Why the warm-up matters:** By the time they get your email, they've seen your name twice on LinkedIn. You're not cold anymore.

---

## What to Actually Say About Their Post

The opener formula:
```
"Your take on [their specific point] matches what I keep hearing from [their peer group] — [one observation that adds to the conversation]"
```

Examples:
- "Your take on signal-to-noise in outbound sequences matches what every RevOps lead I talk to says after inheriting a bloated sequence library"
- "Your framing of data quality as a GTM input, not a cleanup task, is something most VP Sales only realize after a bad quarter"

Notice: no pitch. No "we help with that." Just adding to their conversation. The pitch comes in email 2.
