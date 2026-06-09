# HubSpot CRM Data-Quality Audit

**A Python engine that scores every contact in a HubSpot portal on completeness, consistency, and freshness — surfacing the dirty data that silently breaks GTM automation before it costs pipeline.**

![stack](https://img.shields.io/badge/stack-Python%20·%20HubSpot%20API-blue) ![deps](https://img.shields.io/badge/paid%20deps-none-green) ![runnable](https://img.shields.io/badge/demo-runs%20offline-success)

## The Problem

GTM teams run sequences, lead scoring, and routing on top of CRM data they assume is clean. It isn't. Missing emails, personal addresses on B2B contacts, and records untouched for 6 months quietly poison every downstream automation — and nobody notices until reply rates crater and deals route to the wrong rep. Most teams have *no standing measure* of CRM health.

## The Result

Runs as a weekly monitor. On the included synthetic portal:

| Metric | Output |
|--------|--------|
| Contacts scored | 5 (scales to full portal via pagination) |
| Average quality score | 73.2 / 100 |
| Issues auto-surfaced | malformed email, personal-email-on-B2B, name casing, title-without-company, rotting records |
| Runtime | <1s per 100 contacts (API-bound) |
| Paid dependencies | **zero** — stdlib + `requests` |

Output is a CSV ranked **worst-first**, so the team fixes the highest-risk records first.

## Architecture

```
HubSpot Contacts API (paginated)
        │
        ▼
  Audit engine ── completeness  (weighted field coverage, 0-100)
                ├─ consistency   (email validity, personal-domain flag,
                │                 casing, title-without-company)
                └─ freshness     (days since last modified: fresh/stale/rotting)
        │
        ▼
  Weighted score (50% complete · 30% consistent · 20% fresh) → grade A–D
        │
        ▼
  reports/crm_audit.csv  (worst-first)  +  console summary
```

## How It Works

1. Pages through the HubSpot CRM v3 contacts API pulling 7 quality-bearing properties.
2. Scores each contact on three independent dimensions, each 0–100.
3. Combines them into a weighted total and an A–D grade.
4. Writes a ranked CSV and prints a portfolio-wide summary (missing-email %, personal-email %, rotting %).

## Proof — run it yourself in 5 seconds (no HubSpot account)

```bash
pip install requests
python demo.py
```

Runs the exact scoring engine against synthetic contacts that trip every rule. Live mode:

```bash
export HUBSPOT_TOKEN="pat-na1-..."   # Private App, scope: crm.objects.contacts.read
python crm_audit.py --limit 500
```

- 🎥 Loom walkthrough: _[add link]_
- 📊 Sample output: `reports/demo_audit.csv`

## What I'd Do Next

- Push scores back to HubSpot as a custom `data_quality_score` property (write scope) so they're filterable in-app.
- Schedule via GitHub Actions cron → post weekly summary to Slack.
- Add an email-verification waterfall (NeverBounce/ZeroBounce) for the consistency layer.

## Why a data engineer built this

Most GTM candidates can use HubSpot; few can write the code that audits it at scale. This is the data-quality discipline from 5.5 years of production pipelines (Redshift, 99% reporting accuracy, 94% discrepancy reduction) applied to the GTM stack — the data layer that AI automation breaks without.
