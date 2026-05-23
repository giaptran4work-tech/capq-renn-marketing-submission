# Task 3 deck section — content plan (logged 2026-05-23)

> The agreed structure for the **Task 3 (Growth Hacking)** section of
> `5-submission/deck-content.md`. Supersedes the T3.1–T3.6 outline in
> `2026-05-22-submission-content.md` (Task 4). Intro-first — it mirrors Giap's
> growth-mechanism document: Observation → Mechanism → Workflow → Scaling.

## Anti-confusion rules (apply to every block)

Built from the confusion that surfaced during review:

1. **Every number is labelled** with what it is — 16 searches · 126 candidates
   · 12 checked · 5 verified · ~40% genuine · 30+ target. No bare numbers.
2. The **"5 verified" is framed only as PROOF** the leads are real (clickable,
   checkable) — never as the mechanism's yield.
3. The **lead count (→ 30+) is claimed in ONE place only** — T3.5's funnel math.
4. The process is **one numbered pipeline**, with the tool-half and the
   human-half visibly split.
5. **"Built" vs "designed next step"** is always marked.

## The 7 blocks

**T3.1 — The idea** (the introduction). Observation: emerging fund managers
publicly signal their raise on LinkedIn; Google indexes those posts. The
mechanism in one line: use Google's index to surface those posts → a precision
outreach list, $0 ad spend. A one-glance overview names the 4 steps.

**T3.2 — The hypothesis.** The falsifiable claim (30+ qualified leads / 2 weeks
/ $0 ad spend) + the explicit failure condition + why it should hold (intent is
self-identified, timing is optimal).

**T3.3 — The workflow.** The 4-step mechanism in detail — surface → mine
engagement → filter → outreach — with tool-vs-human marked, and the re-aim
shown as thinking (queries corrected from startup-founder language to
fund-manager language, because capq.ai's customer is the fund manager).

**T3.4 — The prototype.** find_leads.py automates Step 1 (the safe half) —
SerpAPI, $0, ToS-safe. How it rates posts (signal words +2 / noise −1, a
sorter). The real run: 16 searches → 126 candidates → 5 verified (labelled:
proof the leads are real, not the yield). Repo link. Steps 2–3 = designed next
step, not built.

**T3.5 — Launch plan + funnel math.** The 2-week plan + the funnel:
126 candidates per run × ~40% genuine → ~50 qualified per run → 30+ over
2 weeks. The only place the 30+ figure is claimed.

**T3.6 — Success metrics.** Measurable targets + a precise definition of
"qualified lead".

**T3.7 — Scaling.** Automate the engagement-mining layer (the next step);
expand the query set; add a post-recency filter; A/B the outreach; pipe to a
CRM; hand to a VA.

## Flow

idea → claim → how it works → what's built → the math → metrics → scaling.
The "5" and the "30+" never collide — each lives in its own block, own label.
