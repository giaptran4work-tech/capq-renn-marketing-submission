# Project Progress — Renn Labs Marketing Challenge

> **Single source of truth for where the work stands.** Claude reads this at the start of every session (CLAUDE.md points here). Update it as work lands — newest state wins.

**Last updated:** 2026-05-23 (Task 3 prototype published; Task 3 deck section drafted, in review)

## Phase status

```
PHASE                          STATE          NOTES
─────────────────────────────  ────────────   ──────────────────────────────────
1  Discovery                   ✅ DONE        company / pain-points / use-case
   Workflow-1 alignment spec   ✅ DONE        docs/superpowers/specs/2026-05-21-...
3  Build — Workflow #1 code    ✅ DONE        code + tests + README committed
   Build — Workflow #1 deploy  ✅ DONE        pushed to GitHub, Pages live
2  Design — Workflow #2        ✅ DONE        2-design/workflow-2-founder-voice.md
2  Design — Workflow #3        ✅ DONE        2-design/workflow-3-weekly-digest.md
5  Submission — alignment      ✅ DONE        spec + content plan (revised 2026-05-23)
5  Deck content — Task 1       ✅ DONE        T1.1–T1.6 drafted; Giap-approved
5  Deck content — Task 2       ✅ DONE        T2.1–T2.6 + appendix A1–A3 approved
                                              (competitor swap kept; impact = qualitative)
5  Task 3 prototype            ✅ DONE        built, tested, published →
                                              github.com/giaptran4work-tech/capq-lead-discovery
5  Deck content — Task 3       🔄 IN REVIEW   T3.1–T3.7 drafted; awaiting Giap
5  Deck content — cover/close  🔄 IN REVIEW   Cover + Close drafted
5  Deck — full review/assembly ⬜ NOT STARTED
```

## Key decisions locked

- **Submission = all 3 brief tasks** (AI workflows / SEO / Growth) in **one ~20-slide PDF deck**. Three self-contained task stories — no forced cross-task narrative. Spec: `docs/superpowers/specs/2026-05-22-submission-alignment-design.md`.
- **ICP = the emerging fund manager** raising a fund from LPs — NOT a startup founder. Consistent across all 3 tasks. **The deck refers to this customer as "the user" — never "GP"** (Giap's call, 2026-05-23).
- **Deck voice:** polite and opportunity-framed — never disparaging capq.ai; each block single-minded; reasoning shown, not just conclusions; no internal scaffolding left in the file.
- **3 workflows, build 1.** WF#1 Competitive Intel = BUILT. WF#2 + WF#3 = DESIGNED only.
- **Task 2** = built from Giap's website audit. **Task 3** = built from Giap's growth mechanism (queries re-aimed to fund-manager language); prototype = a $0, ToS-safe lead-discovery engine.
- **Execution order:** write-first — Task 1 → Task 2 → prototype → Task 3 → assemble, with a Giap review gate after each.
- **LLM provider = OpenRouter** (free model). Earlier "Gemini" wording is superseded — never use it.
- **Task 2 SEO audit is presented in-deck** — full findings + screenshots as a ~3-slide appendix (A1–A3) inside the one submission PDF. No external Google Doc; Task 2 has no working link.
- **Task 3 prototype outputs a ranked contact list** — post authors (deduped, scored by fund-signal strength), not a post list. Commenter mining is the designed next step, not built. Its working link = the GitHub repo, not a hosted app.

## What's next

Task 1 deck content drafted and **Giap-approved**. Task 2 (SEO) drafted, **in review** — two items await Giap: the T2.4 competitor swap (Affinity / DealCloud / Juniper Square vs the audit's AlphaSense / Tegus / Hebbia), and the 15–30% estimate in T2.6.

Task 3 prototype is **built and published** → `github.com/giaptran4work-tech/capq-lead-discovery` (SerpAPI backend; key stays in a local gitignored `.env`).

Next: **write the Task 3 deck section** (T3.1–T3.7) into `deck-content.md`, per the logged plan `docs/superpowers/plans/2026-05-23-task3-deck-section.md`. T3.2 draft shown, awaiting Giap's approval.

## Pointers

- Deck content (the deliverable): `5-submission/deck-content.md`
- Content plan: `docs/superpowers/plans/2026-05-22-submission-content.md`
- Task 3 deck-section plan: `docs/superpowers/plans/2026-05-23-task3-deck-section.md`
- Alignment spec: `docs/superpowers/specs/2026-05-22-submission-alignment-design.md`
- Discovery: `1-discovery/` · Designs: `2-design/` · Build: `3-build/`
- Lessons: `lessons/`
