# Chosen Use Case for the Workflow Demo

## The workflow I will build

**Competitive Intelligence Brief Engine** — a weekly automated scan of 4–6 named competitor surfaces (product pages, pricing, blog/changelog), diff-detected against last week's snapshot, classified by change type (feature ship / pricing move / positioning shift / new content angle), and synthesized by an LLM into a one-page brief for CQ's marketing lead — including a suggested CQ response (content angle, positioning tweak, or ads/SEO move).

## Why this use case

**The pain it solves.** CQ makes the boldest positioning claim on its homepage ("the only platform covering all 8 stages, while alternatives only cover 2–3") and then defends it with literally nothing — no named competitor, no comparison page, no "vs." content. See [`pain-points.md`](pain-points.md) **Gap 4: No competitive defense despite an aggressive positioning claim.** This is the gap where a marketing team most obviously needs ongoing intelligence and most expensively gets blindsided.

**Why AI specifically (vs. manual or simpler automation).**

- A manual version is a 2–4 hour weekly task across 6 sites: pull pages, eyeball diffs, write a brief. Marketers don't do it consistently, so they drift out of date.
- Pure-automation diffing (a `wget + diff` cron) produces noise — every CSS tweak, every datestamp change, every cookie banner counts as a diff. The marketer ignores it.
- AI is the right layer because the *judgement work* is "is this diff meaningful and what should we do about it." Diff detection is plumbing; semantic classification and prescriptive response are the leverage. That's exactly where a small LLM call earns its cost.

**Expected impact / leverage.**

- Recovers ~3 hours/week of marketer time.
- Surfaces 1–2 actionable plays per week (content topic, ad headline, positioning patch).
- Long term: produces the content artifacts CQ is missing — the comparison pages, the "vs." posts, the positioning sharpening — turning a defensive workflow into an offensive content pipeline.

## The three workflows in the final write-up

Per the brief, the submission presents three workflows and builds one. The chosen three form a coherent marketing-function story: **sense → produce → convert.**

1. **(Built)** Competitive Intelligence Brief — marketing's sensing layer.
2. **(Designed)** Founder-Voice Content Engine — listens to emerging-GP conversations (LinkedIn, Reddit, niche Substacks) and generates content briefs + drafts in CQ's founder voice. Closes Gap 2 (anonymous bulk content) and Gap 3 (voice inconsistency). Producer layer.
3. **(Designed)** Hyper-Personalized Landing Hero — edge-function AI rewrites the homepage hero per visitor segment (PE GP, VC GP, HF, secondaries). Closes Gap 5 (zero top-of-funnel personalization). Conversion layer.

## Why NOT the others (as the built demo)

- **Founder-Voice Content Engine** — fixes a real pain (Gap 2/3), but the demo is harder to validate quickly: the assessor would need to read drafts and judge voice-fit, which is subjective. Better designed than built within 72 hours.
- **Hyper-Personalized Landing Hero** — clear visual demo (toggle URL params, see hero change), but requires deployment infra (Vercel / Cloudflare) and bumps against CQ's actual site (can't ship to a property I don't own). A mock-up exists in design but the *running* version would be fake. Competitive Intel runs on real data without any deployment.

## Success criteria for the demo

The assessor will judge it "working" if, given a single command (or URL click), they see:

1. The system fetches **at least 4 real competitor surfaces** live (not cached/faked).
2. It produces a **diff** vs. a baseline snapshot included in the repo.
3. It outputs a **1-page brief** with: (a) what changed, (b) why it matters, (c) a concrete suggested CQ response.
4. The brief reads like a human marketer wrote it — specific, action-oriented, not generic.
5. End-to-end runtime under 90 seconds; cost under $0.20 per run at GPT-4o-mini prices.

A second-level success criterion (nice-to-have, not required for the demo): the workflow runs on a cron and posts to Slack / sends an email — to show the production-mode shape, not just the dev-mode run.

## Open decisions (resolve in design phase)

- **Which competitors?** Initial list: Affinity, DealCloud, Carta (LP), Watershed/Juniper Square, 4Degrees. To validate against actual CQ positioning before the build.
- **Hosting model for the demo:** local Python script (assessor clones repo) vs. one-click hosted (Streamlit / HuggingFace Space). Decision belongs in `2-design/workflow.md`.
- **LLM choice:** GPT-4o-mini vs. Claude Haiku 4.5 — to evaluate on cost/quality for the brief synthesis step.
