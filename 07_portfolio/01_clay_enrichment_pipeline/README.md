# Clay Enrichment Pipeline

**A 4-provider waterfall that takes a raw company list from ~40% to 85%+ verified email coverage at ~$0.22/lead — with AI-personalized openers and ICP scoring, in under an hour of active work per 100 rows.**

![stack](https://img.shields.io/badge/stack-Clay%20·%20Apollo%20·%20Claygent%20·%20HubSpot-blue)

## The Problem

B2B teams waste 40–60% of outreach budget on bad data — wrong emails, stale titles, out-of-ICP companies. A single data provider (Apollo alone) covers ~40% of a typical list, so more than half the prospects are unreachable or wrong. Buying a second full database is expensive and still leaks.

## The Result

| Metric | Before (single provider) | After (this pipeline) |
|--------|--------------------------|------------------------|
| Email coverage | ~40% | **85%+** (target 88–93% on US SaaS) |
| Cost per enriched lead | ~$0.55 | **~$0.22** |
| Verified emails | none | Findymail-verified subset flagged |
| Personalization | manual / none | AI opener per row, signal-aware |
| Active work / 100 rows | hours | **<60 min** |

_Benchmark reference: OpenAI reported 40%→80% coverage moving to a Clay waterfall; this pipeline targets the same curve._

## Architecture

```
Input CSV (100 companies + domains)
        │
        ▼
  Clay table
   ├─ Apollo Company Search        → size, industry, country
   ├─ Email waterfall (stop-on-hit):
   │     Apollo → Prospeo → Findymail → Dropcontact
   ├─ Claygent: tech stack + funding signal  (gated to ICP-qualified rows)
   ├─ Formulas: email_final, email_source, ICP score (0-100), tier A/B/C
   └─ AI column (Claude): 1-sentence opener using signal/tech
        │
        ▼
  HubSpot (Tier A/B only, dedup on email)  +  webhook → n8n → Supabase
```

## How It Works

1. **Company enrichment first** — score ICP fit *before* spending email credits (pre-filter saves ~50% of credits).
2. **Stop-on-hit waterfall** — each provider runs only if the prior one missed; cheapest providers first.
3. **Claygent gated** — AI web research runs only on ICP-qualified rows that databases couldn't fill.
4. **AI personalization** — one specific opener per contact, built from the strongest available signal.
5. **Routed export** — only Tier A/B reach HubSpot; everything logged to Supabase for audit.

## Proof

- 🎥 Loom walkthrough (waterfall logic + coverage breakdown): _[add link]_
- 📊 Provider contribution table (the artifact recruiters care about):

| Provider | Found | % of total | Cumulative coverage |
|----------|-------|-----------|--------------------|
| Apollo | _45_ | _45%_ | _45%_ |
| Prospeo | _18_ | _18%_ | _63%_ |
| Findymail | _12_ | _12%_ | _75%_ |
| Dropcontact | _10_ | _10%_ | _85%_ |
| Not found | _15_ | _15%_ | — |

- 📷 Screenshots: `./screenshots/`
- 🧮 Coverage-analysis script: `./analyze_coverage.py` _(exports the table from Clay, computes the breakdown above)_

## What I'd Do Next

- Swap provider order per ICP geography (Cognism/Dropcontact earlier for EU lists).
- Add bounce-rate feedback loop from the sending tool back into provider scoring.

## Why a data engineer built this

The waterfall is a `COALESCE` across data sources with cost-aware short-circuiting — exactly the ETL fallback logic I've shipped in 50+ production Alteryx workflows, now pointed at the GTM stack. I don't just run Clay; I reason about coverage, cost-per-lead, and provider economics like a pipeline.

---

### Build checklist
```
⬜ Import 100-row CSV (clean domains first)
⬜ Apollo Company Search + ICP score formulas
⬜ 4-provider email waterfall with stop conditions
⬜ Claygent tech + funding columns (gated)
⬜ AI opener column
⬜ Capture provider contribution table + coverage %
⬜ HubSpot export (Tier A/B) + Loom + LinkedIn post
```
Full build steps: see `../../02_intermediate/04_project_100row.md`.
