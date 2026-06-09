# Signal-Triggered Agentic Outreach System

**A zero-touch pipeline: a hiring/funding signal fires → Clay enriches the contact → Claude writes a confidence-scored personalized opener → high-confidence leads auto-send via SendGrid, the rest route to HubSpot for review. Signal to outreach-ready in under 10 minutes, no human in the loop.**

![stack](https://img.shields.io/badge/stack-Clay%20·%20n8n%20·%20Claude%20API%20·%20SendGrid%20·%20HubSpot-blue) ![python](https://img.shields.io/badge/Claude-structured%20outputs-green)

## The Problem

The highest-converting outbound moments — a new VP of Sales, a fresh Series B — have a 48-hour window. By the time a human researches the company, finds the email, and writes a personalized note, the window is closing and 90% of signals never get actioned at all. The work is real but every step is automatable.

## The Result

| Metric | Manual process | This system |
|--------|---------------|-------------|
| Signal → outreach-ready | hours–days (if ever) | **< 10 minutes** |
| Human steps | research + find + write + send | **zero** (high-confidence path) |
| Personalization | generic template | per-lead, signal-specific, confidence-scored |
| Reply rate (signal-triggered vs cold) | 2–4% cold | **8–15%** signal-triggered¹ |
| Bad-send protection | none | confidence gate (auto-hold < 0.65) |

¹ Industry benchmark for signal-triggered vs. generic cold outreach.

## Architecture

```
Signal source (job board / Crunchbase / LinkedIn) ──▶ n8n webhook
        │
        ▼
  n8n: ICP pre-check (size, industry, geo)
        │
        ▼
  Clay: enrich 3 target roles  (email waterfall + company data + signal verify)
        │
        ▼
  personalize.py  ── Claude API (structured output) ─▶ {opener, confidence, used_signal}
        │
        ├── confidence ≥ 0.65 ──▶ SendGrid auto-send  + HubSpot log
        └── confidence <  0.65 ──▶ HubSpot task "review before send"
```

## How It Works

1. **Signal intake** — n8n receives a webhook (funding, job change, RevOps job posting), checks ICP fit before spending any credits.
2. **Clay enrichment** — finds the decision-makers' emails (4-provider waterfall) and verifies the signal is real.
3. **AI personalization** (`personalize.py`) — Claude writes one signal-specific opener per lead **and rates its own confidence** using structured outputs, so the score is a validated number, not parsed text.
4. **Confidence routing** — openers ≥ 0.65 auto-send via SendGrid; lower-confidence ones become HubSpot review tasks. The gate is what makes zero-touch safe.

## Proof — run the AI brain yourself

```bash
pip install anthropic pydantic
export ANTHROPIC_API_KEY="sk-ant-..."
python personalize.py --demo
```

Generates real confidence-scored openers for 3 sample leads (one with no signal, to show the confidence gate working). Run against a Clay export:

```bash
python personalize.py clay_export.csv --threshold 0.65 --out scored.csv
```

- 🎥 Loom walkthrough (signal → HubSpot in real time): _[add link]_
- 📊 n8n workflow JSON: `./n8n_signal_workflow.json` _(export from your n8n)_
- 📷 Architecture + screenshots: `./screenshots/`

## Design Decisions Worth Defending in an Interview

- **Why structured outputs over prompt-and-parse?** The confidence score gates auto-send — a malformed parse could send a bad email. `messages.parse()` with a Pydantic schema guarantees a valid `{opener, confidence}` object or a safe hold.
- **Why Haiku, not Opus?** High-volume, short-output personalization is exactly Haiku's tier — ~5× cheaper per lead than Opus with no quality loss on a 25-word opener. Opus is one `--model` flag away for enterprise accounts where the deal size justifies it.
- **Why a confidence gate at all?** Zero-touch only works if bad output can't reach a prospect. The gate is the safety mechanism that makes "no human in the loop" defensible rather than reckless.

## What I'd Do Next

- Feedback loop: write reply/bounce outcomes back to Supabase, correlate with confidence buckets, and tune the threshold from real data.
- Add a second Claude pass (Opus) only on leads where the deal-size estimate clears a bar.

## Why a data engineer built this

This is an orchestration + data-quality problem wearing a sales hat: idempotent webhook intake, a confidence gate that prevents bad sends, structured outputs over fragile parsing, and a routing layer that's just conditional ETL. That's the engineering discipline from 5.5 years of production pipelines — applied to GTM, where most candidates can wire a Zapier zap but can't reason about failure modes.
