# GTM Engineer Portfolio — Build Plan

**Goal:** Convert the 4 projects already on your resume from *claims* into *real, demonstrable, metric-backed artifacts* — sized for 5 hrs/week, so you keep applying in parallel.

**Owner:** Rajasekhar Nagella · GitHub: github.com/Rajasekhar-Chowdary  
**Deadline pressure:** Offer target Aug 29 2026. Apply NOW, build in parallel. Do not wait for portfolio completion to apply.

---

## The one rule that makes recruiters care

A recruiter spends ~8 seconds on a GitHub repo. They scan for **numbers and proof**, not prose. Every project README must answer four things *above the fold*:

```
1. PROBLEM   — the business pain, in one sentence with a cost ($/time/%)
2. RESULT    — the headline metric, bolded, first screen (e.g., "40% → 89% email coverage")
3. HOW       — the architecture diagram (ASCII is fine) + stack badges
4. PROOF     — Loom link + screenshot + (for code) a runnable script
```

If a project doesn't have a hard number in the first paragraph, it's not a portfolio project — it's a hobby.

---

## Build order (do NOT do all at once)

| # | Project | Effort | Status | Headline metric to capture |
|---|---------|--------|--------|---------------------------|
| 1 | [Python CRM Audit Script](./03_crm_audit/) | ~4 hrs | ⬜ | "Scores X contacts on 3 quality dimensions in <Ys" |
| 2 | [Clay Enrichment Pipeline](./01_clay_enrichment_pipeline/) | ~6 hrs | ⬜ | "40% → 85%+ email coverage, $0.22/lead" |
| 3 | [Signal-Triggered Agentic System](./02_signal_triggered_system/) | ~12 hrs | ⬜ | "Signal → personalized HubSpot task in <10 min, zero human input" |

Start with #1 — it's the fastest, runs with free tools, and is the purest proof of your rare differentiator (you can code).

---

## The differentiator thread (state it in every README)

> Most GTM candidates come from an SDR background and can use tools but can't build. I come from 5.5 years of production data engineering (SQL, Redshift, Python, 50+ Alteryx workflows). These projects show I build the **data layer that GTM automation breaks without** — not just click around in Clay.

Put a version of this line in every repo. It's the whole reason you get interviews over the 200 other GTM applicants.

---

## Result-driven README template (copy into every project)

```markdown
# [Project Name]

**[One-line value prop with the headline metric bolded]**

![stack](https://img.shields.io/badge/stack-Clay%20·%20n8n%20·%20Claude%20·%20HubSpot-blue)

## The Problem
[1-2 sentences. Name the business cost: wasted spend, hours, bad data %.]

## The Result
| Metric | Before | After |
|--------|--------|-------|
| [e.g. Email coverage] | 40% | 89% |
| [e.g. Cost per lead] | $0.55 | $0.22 |
| [e.g. Time per 100 rows] | manual / hours | <X min |

## Architecture
[ASCII diagram of the data flow]

## How It Works
[Numbered steps, each tied to a real component]

## Proof
- 🎥 Loom walkthrough: [link]
- 📊 Screenshot: [./screenshots/...]
- 💻 Run it: `python ...` / import the n8n JSON / Clay table link

## What I'd Do Next
[1-2 honest improvements — shows you think about production, not just demos]

## Why a data engineer built this
[The differentiator line.]
```

---

## What "result-driven" means per project (the metrics recruiters scan)

- **Enrichment projects:** coverage rate %, cost per enriched lead, time per 100 rows, provider contribution breakdown
- **Automation/signal projects:** end-to-end latency (signal → action), % automated (zero-touch), volume processed, error rate
- **Code/audit projects:** records processed, runtime, % issues surfaced, lines of config vs. manual hours replaced
- **Always:** before → after. A number with no baseline is half a number.

---

## Packaging checklist (every project ships with all 5)

```
⬜ GitHub repo, public, with the result-driven README above
⬜ One headline metric in the first paragraph, bolded
⬜ Architecture diagram (ASCII or draw.io export)
⬜ 2-3 min Loom walkthrough (you narrating the flow)
⬜ One LinkedIn post: "I built X. Here's the result: [metric]. Here's how: [3 bullets]." + repo link
```

The LinkedIn post matters as much as the repo — it's how recruiters find you, and it's a forcing function to articulate the result.

---

## Honest sequencing against your real constraints

- You have ~5 hrs/week and an Aug 29 target. That's ~12 working weeks.
- Project #1 (audit script) is shippable in week 1 — gives you something real on GitHub immediately while you keep applying.
- Project #2 needs a Clay paid tier (Starter) to hit 100 rows; do it once you upgrade. Until then, the 25-row version from the learning path is a legitimate smaller proof.
- Project #3 is the capstone — only start it once #1 and #2 are public. It's the interview-winner but it's also where time disappears. Time-box it hard.
