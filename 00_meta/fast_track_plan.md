# Fast-Track Plan — Senior Data Analyst → GTM Engineer, Clay as the Vehicle

> **RETIRED AS A ROADMAP — 2026-06-10.** The single operating roadmap is
> `GTM_Mastery/docs/ROADMAP.md` (24-week plan). This folder remains a **build accelerator**:
> the scripts in `07_portfolio/` (`crm_audit.py`, `analyze_coverage.py`, `personalize.py`)
> feed GTM_Mastery Phases 2–3 Projects 1–3. Do not run this plan's cadence or tracker in
> parallel — two roadmaps on a 5–6 hr/week budget is how both fail.

Updated 2026-06-10. Account: **live with credits**. Budget: ~5 hrs/week (6 days × ~50 min).
Runway: Jun 10 → Aug 29 offer-deadline checkpoint. Sprint: **6 weeks + 2 flex**, done ~Aug 7,
leaving 3 weeks for application surge + interviews.

## Positioning (read this when motivation dips)
You are not "learning Clay." You are converting 5.5 yrs of SQL/Redshift/Alteryx depth into
the GTM Engineer role — Clay is the bridge tool that proves it. Most GTM candidates came up
SDR→GTM and can't write a query; you can. Every artifact below exists to make that argument
in public, with numbers.

## The principle (why this works)
Accelerated-learning's **directness** rule: you don't study Clay, you build the real thing.
Every week ends in a **portfolio artifact** — the artifact IS the exam. Pass = shipped with
a coverage number. No passive reading, no tutorial limbo.

## The daily rhythm (identical every week — only content changes)

| Day | Block (~50 min) | Why |
|-----|-----------------|-----|
| Mon | **Learn** — read the week's curriculum files; write the 1 question you'll answer by building | Reading with a build target = reading with purpose |
| Tue | **Build pt 1** — start the week's artifact in Clay | Recall 24h after reading is the actual learning |
| Wed | **Build pt 2** — finish + hit the coverage gate | A number passes or fails; no "I think I get it" |
| Thu | **Package** — README w/ real metrics, screenshot, 2-min Loom, **+ 4-line interview story** (problem → built → number → next) | Unpublished work doesn't exist to a recruiter; unspoken stories don't survive interviews |
| Fri | **Publish + apply** — GitHub/LinkedIn (★ wks), then **1 portal application + 1 warm outreach** | Freshest proof on top of your profile, same day |
| Sat | **Review** — 3 Anki cards, log numbers in `progress_tracker.md`, 1 more application | 15-min loop-close prevents drop-off |
| Sun | Off — protected | Burnout kills 6-week plans, not difficulty |

Miss a day → the week absorbs it. Miss a week → use a flex week. Never restart from zero.

## The 6-week sprint

| Wk | Learn | Build (the real thing) | Artifact | Gate | Concept to own (interview-ready) |
|----|-------|------------------------|----------|------|----------------------------------|
| 1 | 01_beginner 01–03 | 25-row email waterfall (Apollo→Hunter→stop) | Screenshot + coverage note | ≥70% | **Waterfall economics** — providers in cost order, stop on first hit; know cost-per-verified-email |
| 2 | 01_beginner 04 + 02_int 01–02 | 4-provider waterfall + company enrichment, same 25 | `07_portfolio/01_clay_enrichment_pipeline` README w/ real metrics ★ | ≥85% | **Coverage vs accuracy** — each marginal provider has worse hit-rates; know when to stop adding |
| 3 | 02_int 03–04 | Claygent LinkedIn-post hook + 100-row run | Claygent prompt library entry + 100-row case study ★ | ≥85% @ 100 | **Agent prompting = constraining outputs** — exact shape + explicit fallback |
| 4 | 03_adv 01–02 | **Job-Search Engine (Project #4):** target cos → enrich → find hiring manager → signal-triggered warm outreach. Same table doubles as the signal-detection exercise | `07_portfolio/` job-search table + `02_signal_triggered_system` w/ real personalize.py output ★ | signal precision; ≥10 hiring managers found | **Signals beat lists** — *when* you reach out matters more than *who* |
| 5 | 03_adv 03–04 + 04_exp 01 | Clay→n8n→Supabase/HubSpot wire-up + Clay API row-add | n8n workflow JSON + Clay API script working | <5 min lead→CRM | **Orchestration** — Clay is one node; lead→enrich→score→CRM is the product |
| 6 | 04_exp 02–04 + 06_scenarios | 1 competition scenario end-to-end + CRM audit on real export | `07_portfolio/03_crm_audit` real scorecard ★★ | publish all ★ | **Data quality is revenue** — translate dirty CRM into $ wasted |

★ = recruiter-facing proof to publish. ★★ = the differentiator.
Flex weeks (7–8): catch-up or deepen — **plus one mock-interview rep each** (stories spoken
aloud, pushed back on). Finishing early earns a flex week, not more curriculum.

## Applications track (parallel — never blocked by portfolio)
- **Cadence:** Fri 1 portal + 1 warm outreach · Sat 1 more → 3/wk ≈ 33 by Aug 29.
- **This Saturday (one-time):** build the 40-company target list — Series A–C SaaS, GTM-hiring,
  sponsorship-verified (AU: accredited 482 sponsor check · NL: IND recognized-sponsor public
  register · UK: licensed-sponsor register). Fridays then become pure execution.
- **Instrumentation:** track sent → response → screen in a sheet.
  **Kill-switch: 12 apps / 0 responses = stop and fix** (resume, targeting, or channel) — never grind a broken funnel.
- **Week 4 upgrade:** the Job-Search Engine table replaces manual prospecting — warm outreach
  to hiring managers converts ~5–10× portal apps, and "I built my job search on Clay" is the
  best interview opener a GTM Engineer candidate has.

## Win condition
By end of Wk 6: the portfolio projects your resume already claims are REAL — metrics + public
links — and you can *say* each one in 4 lines. By Aug 29: ≥30 applications instrumented, warm
channel running, ≥2 screens in motion. Not "finished the curriculum."

## This week's first session
See `00_meta/session_1_today.md`. Tonight regardless of anything: applications 1–2 go out.
