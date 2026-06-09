# Clay Learning Path — Beginner to Expert

A structured, project-driven curriculum for mastering Clay: the GTM data enrichment platform that powers modern outbound at 85–95% coverage.

---

## Who this is for

Someone who knows what Clay is (or just heard of it) and wants to go from zero → capable of building production enrichment pipelines used by companies like OpenAI and Anthropic.

## How to use this

1. **Read `00_meta/learning_map.md` first** — 20 minutes of metalearning saves 20 hours of wasted effort
2. **Work in order** — each phase builds on the last. Don't skip to Advanced.
3. **Do the projects** — reading is 20% of learning. Projects are 80%.
4. **Use the quiz questions** — close the doc and answer from memory. Desirable difficulty = retention.
5. **Create the Anki cards** — the deck builds up over the course. 10 min/day beats cramming.

---

## Phases Overview

| Phase | Level | Focus | Duration | Project |
|-------|-------|-------|----------|---------|
| [01_beginner](./01_beginner/) | Beginner | Clay mental model, tables, columns, credits, first enrichment | 1–2 weeks | 25-row enrichment with coverage report |
| [02_intermediate](./02_intermediate/) | Intermediate | Waterfall design, provider stack, Claygent basics, company enrichment | 2–3 weeks | 100-row pipeline at 80%+ coverage |
| [03_advanced](./03_advanced/) | Advanced | Claygent mastery, signal detection, AI personalization, webhook output | 3–4 weeks | Signal-triggered enrichment pipeline |
| [04_expert](./04_expert/) | Expert | Clay API, multi-table orchestration, cost optimization, real-time | 3–4 weeks | Full-stack GTM pipeline with n8n + Supabase |
| [06_scenarios](./06_scenarios/) | All | 5 competition-level playbooks to clone and adapt | Reference | — |
| [05_reference](./05_reference/) | All | Formula cheatsheet, provider guide, Claygent prompt library | Reference | — |

---

## Quick Coverage Benchmarks

Know these before you write a single enrichment column:

| Setup | Expected Coverage |
|-------|------------------|
| Single provider (Apollo) | 40–50% |
| 2 providers (Apollo + Hunter) | 60–65% |
| 4-provider waterfall | 80–90% |
| 4-provider waterfall + Claygent | 90–95% |
| Industry benchmark (expert) | 90%+ |

**Anything below 70% means your waterfall or input data has a problem.**

---

## The One-Sentence Mental Model

Clay is a **data enrichment spreadsheet** where each column can call an external API, chain providers in sequence (waterfall), or run AI research — and the output flows straight to your CRM.

---

## Progress Tracker

→ [00_meta/progress_tracker.md](./00_meta/progress_tracker.md)
