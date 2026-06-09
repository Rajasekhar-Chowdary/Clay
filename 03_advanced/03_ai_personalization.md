# Module 3.3 — AI Personalization Columns

**Time:** 60–75 minutes  
**Focus:** Writing AI prompts that generate unique, human-sounding output per row

---

## The Problem with Template-Based Outreach

```
Template approach:
"Hi {first_name}, I noticed {company_name} recently raised funding — congrats!
I wanted to reach out because..."

Everyone does this. Recipients see through it immediately.
Reply rate: 2-4%.
```

The fix isn't better templates — it's *actual* personalization using real data points per row.

```
AI-personalized approach (with real signal data):
"Saw that Marcus joined as Head of RevOps last month — as you rebuild the data stack,
you'll likely hit the same coverage problems every new RevOps lead inherits."

This is specific. It references a real event. It demonstrates research.
Reply rate: 8-15%.
```

Clay's AI column is how you generate the second type at scale.

---

## How the AI Column Works

1. You write a prompt template with column variables (`{first_name}`, `{signal}`, etc.)
2. For each row, Clay substitutes the actual values
3. Sends the resulting prompt to Claude, GPT-4, or another model
4. Returns the AI response to that column

Cost: ~0.5–1 credit per row (varies by model and output length)

Available models in Clay (as of 2026):
- Claude Haiku (fastest, cheapest — good for short openers)
- Claude Sonnet (better quality, slightly more expensive)
- GPT-4o mini (fast, OpenAI's equivalent to Haiku)
- GPT-4o (higher quality)

**Recommendation:** Claude Haiku for high-volume (1000+ rows), Claude Sonnet or GPT-4o for important accounts.

---

## The AI Column Prompt Framework

Every AI personalization prompt has 4 sections:

```
[ROLE] — who the AI is writing as
[INPUT DATA] — the column data it should use
[RULES] — what to do and not do
[OUTPUT] — exactly what to return
```

### Minimal Working Prompt (email opener)

```
[ROLE]
You are writing a cold email opening line for a B2B sales development rep.

[INPUT DATA]
Contact: {first_name} {last_name}, {job_title} at {company_name}
Signal: {primary_signal_text}
CRM in use: {crm_detected}
Company size: {employee_count} employees
Industry: {industry}

[RULES]
- Be specific — reference the exact signal, not a generic "I saw your company recently..."
- Connect to a GTM data, outbound, or pipeline challenge
- Sound human — conversational, not formal
- MAX 25 words
- No filler phrases: "I hope this finds you well", "I wanted to reach out", "I came across your profile"
- No emojis

[OUTPUT]
Return ONLY the opening sentence. No greeting (no "Hi {first_name}"), no full email.
If primary_signal_text is empty: write an opener based on their role + company size + industry instead.
```

---

## 6 Proven AI Prompt Patterns

### Pattern 1: Signal-Based Opener

Used when: you have a Tier 1 or Tier 2 signal

```
You are a GTM expert writing a cold email.

Signal about {company_name}: {primary_signal_text}
Contact: {first_name}, {job_title}

Write ONE sentence (max 25 words) that:
1. References the signal naturally ("Saw that...", "Noticed...", "When I saw...")
2. Connects the signal to a relevant challenge ({first_name}'s role would care about)
3. Creates curiosity without being pushy

Output: sentence only. No greeting. No explanation.
```

**Example output:**
"Saw that Acme just brought Marcus in as CRO — new leadership usually means the enrichment stack gets a full audit."

---

### Pattern 2: Role-Based Opener (No Signal Available)

Used when: no signal found, but ICP is strong

```
You are writing a cold email first line.

Contact: {first_name}, {job_title} at {company_name}
Company: {employee_count} employees, {industry}, using {crm_detected}
No specific signal available.

Write ONE sentence (max 20 words) that:
1. Acknowledges their role specifically (VPs have different problems than Managers)
2. References a common challenge for {job_title} at {employee_count}-person companies
3. Avoids "I saw your LinkedIn", "I came across your company", or any cringe openers

Output: sentence only.
```

**Example output:**
"Running outbound at a 150-person SaaS company with Salesforce usually means the enrichment coverage question comes up eventually."

---

### Pattern 3: Tech Stack Opener

Used when: you know what tools they use

```
Contact: {first_name}, {job_title} at {company_name}
CRM: {crm_detected}
Other tools: {tech_stack}

Write a 1-sentence cold email opener (max 25 words) that:
1. References their specific CRM or tool stack
2. Points to a gap or pain that their current stack doesn't solve
3. Sounds like a peer who knows the stack, not a vendor

Output: sentence only.
```

**Example output:**
"If you're running Apollo for prospecting with Salesforce, the email coverage gap in international accounts is usually the first thing that surfaces."

---

### Pattern 4: LinkedIn Post Opener

Used when: you have Claygent LinkedIn post data

```
{first_name} recently posted on LinkedIn: "{claygent_linkedin_post}"

Write a cold email first line (max 25 words) that:
1. References their post naturally — like you actually read it
2. Connects to a challenge they'd care about in their role
3. Feels like a reply to their post, not a cold pitch

Output: sentence only. No "Great post" — that's the most common opener and it's seen through.
```

**Example output:**
"Your take on the signal-to-noise problem in outbound sequences matches what I keep hearing from RevOps leads at this stage."

---

### Pattern 5: Subject Line Generator

Used alongside opener patterns — generates matched subject lines.

```
Email opening line: {ai_opener}
Contact: {first_name}, {job_title} at {company_name}

Write a cold email subject line (max 8 words) that:
1. Matches the tone and topic of the opener
2. Avoids clickbait — no "quick question", "touching base", "follow up"
3. Could pass as a reply from a colleague (conversational)
4. Contains no emojis, no ALL CAPS

Output: subject line only.
```

**Example output:**
"outbound coverage gaps at {employee_count}-person companies"

---

### Pattern 6: Full Email Generator (Use Sparingly)

Only for high-value Tier A prospects. Full email generation is slower and costs more.

```
Write a cold B2B outreach email.

Contact: {first_name} {last_name}, {job_title} at {company_name}
Signal: {primary_signal_text}
CRM: {crm_detected}
Your product: A GTM data enrichment platform that helps B2B teams achieve 85-90% email coverage using multi-provider waterfalls.

Structure:
Line 1 (opener): Reference the signal specifically. Max 20 words.
Line 2 (problem): One sentence naming the pain this creates. Max 20 words.
Line 3 (solution bridge): One sentence connecting their situation to the product. Subtle, not a pitch. Max 20 words.
CTA: One soft ask — calendar link, reply with a question. Max 15 words.

Rules:
- No "I", start with the person/company/signal
- No "synergy", "solutions", "leverage", "circle back"
- Total email: max 80 words
- Sound like a senior rep who did research, not a template bot

Output: complete email only.
```

---

## Quality Control for AI Output

Never send AI-generated output directly. Always review.

### The 3-Second Quality Check

For each row, ask:
1. Is it specific? (Names a real signal, tool, or fact — not a generic statement)
2. Could this have been written about any company? (If yes, it's generic — regenerate)
3. Does it sound like a human? (Read it aloud. Awkward phrasing = regenerate)

### Adding a Quality Flag Column

After your AI opener column, add a formula quality filter:

```
ai_opener_quality:
{{IF(
  LEN(ai_opener) > 200, "Too long — review",
  IF(
    CONTAINS(ai_opener, "I hope") OR
    CONTAINS(ai_opener, "I wanted to") OR
    CONTAINS(ai_opener, "Great post") OR
    CONTAINS(ai_opener, "quick question"),
    "Low quality — regenerate",
    "OK"
  )
)}}
```

Filter your table to `ai_opener_quality == "Low quality"` and regenerate those rows with a different prompt.

---

## Prompting Tips for Better AI Output

**Tip 1: Show, don't tell**
Instead of "sound human" → give an example: "For example: 'Saw that Acme just raised Series B — usually that's when the outbound stack gets audited.'"

**Tip 2: Rule of constraints**
The more specific your constraints, the better the output. Specify: word limit, what to exclude, what to include, what it should feel like.

**Tip 3: Temperature and creativity**
Claude defaults to a balanced setting. For personalization, slightly higher creativity gives more varied openers across a large list. Same prompt on 100 rows will still produce noticeable repetition patterns — this is normal.

**Tip 4: Data quality in → quality out**
If `primary_signal_text` is empty or generic, the AI opener will be generic too. Better Claygent prompts = better AI openers.

**Tip 5: Test on known contacts**
Run the AI column on 3 people you know personally in similar roles. Does it sound right for that specific person? If your friend read it, would they recognize the personal touch?

---

## Anki Cards to Create

```
Q: What are the 4 sections of an AI personalization prompt?
A: ROLE (who the AI is), INPUT DATA (column variables), RULES (do/don't), OUTPUT (exactly what to return)

Q: What model should you use for high-volume AI columns (1000+ rows)?
A: Claude Haiku or GPT-4o mini — fast and cheap, sufficient for short openers

Q: What is the "could this be about any company" test?
A: Quality check — if the opener would work unchanged for a different company, it's generic and needs regeneration

Q: What 3 phrases should your quality filter flag in AI openers?
A: "I hope", "I wanted to", "Great post", "quick question" — these are template clichés that kill reply rates

Q: What determines AI opener quality more than anything else?
A: Data quality going in — a rich signal (funding, hire, LinkedIn post) produces specific openers; empty signal produces generic ones
```

---

## Next Module

→ [03_advanced/04_clay_integrations.md](./04_clay_integrations.md) — Webhook output, HubSpot sync, and routing to n8n
