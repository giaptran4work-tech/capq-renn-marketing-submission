# Workflow Alignment v2 — Competitive Intel Brief Engine

**Date:** 2026-05-21 (revised 2026-05-22)
**Status:** Active alignment for Task 1 workflow. Replaces the deleted v1 spec (which used Streamlit + Anthropic). This v2 reflects the locked decisions on the workflow rebuild.

This is the contract between user (Giap) and Claude for what we're building. Anything implemented that doesn't match this doc is wrong. Anything in this doc that doesn't match what Giap intends gets revised before more code is written.

## Submission shape (two surfaces, both shipped)

```
   SURFACE 1 — GitHub repo                THE PROOF
              cq-competitive-intel/        ──────────
                                           Assessor reads README,
                                           browses code, optionally
                                           clones + runs locally.

                                           One command end-to-end:
                                               python -m src.main

                                           Proves the pipeline is
                                           real and runnable on
                                           any machine.


   SURFACE 2 — Hosted HTML page           THE DEMONSTRATION
              GitHub Pages URL             ──────────────────
                                           Assessor clicks → sees
                                           the latest weekly brief
                                           rendered as a polished
                                           publication.

                                           Proves the output is
                                           publication-grade, not
                                           a developer artifact.


   Both linked from the PDF deck under "source" and "live demo."
```

---

## 1. Purpose (the WHY)

Close **Gap 3** from `1-discovery/pain-points.md`: CQ claims "the only platform covering all 8 stages of fundraising" but defends it with nothing — no competitor comparison content, no battlecards, no positioning content.

```
   In one line:

   "Don't lose to a competitor's move because you didn't see it."
```

This workflow makes weekly competitor watching a 5-minute review of a pre-written, beautifully formatted brief — instead of a 2–4 hour manual chore that never happens.

## 2. Audience (the WHO)

```
   CQ's marketing lead.
   At CQ's stage = founder-marketer (no separate marketing dept).
   Reads the brief Monday morning. Uses it as a radar — signals
   to investigate, not actions to execute on the spot.
```

## 3. Cadence (the WHEN)

```
   PRODUCTION   Weekly cron — GitHub Actions runs every Monday.
                Diff vs last week's snapshot. New brief published.

   DEMO         For the assessor: the latest brief is the demo.
                No "Run now" button. The result IS the demo.
                Cron has run at least once before submission.
```

## 4. What the workflow IS (scope IN)

```
   ✓ Watches 9 URLs across 4 competitors:
       Affinity, Juniper Square, DealCloud, Foundersuite

   ✓ Fetches → extracts clean text → diffs vs last snapshot

   ✓ AI #1: classifies each diff (type + significance 1-5)
            drops noise / design-only / score <3

   ✓ AI #2: writes a 1-page Markdown brief
            STYLE B: per change → what / why / suggested play / link
            TL;DR + per-change body + low-priority tail + failures

   ✓ Markdown → styled HTML (Tailwind CSS via CDN)

   ✓ Publishes the HTML to GitHub Pages
            Latest brief on /index.html
            Archive at /briefs/2026-05-22.html, etc.

   ✓ Weekly GitHub Actions cron triggers the whole pipeline

   ✓ Free everything — no paid services
```

## 5. What the workflow IS NOT (scope OUT — deliberately)

```
   ✗  Email / Slack push notifications
        Reason: needs SendGrid/Resend/webhook setup. Not in v1.
        Optional v2 add: 30-min build, free tier covers volume.

   ✗  "Run now" button / interactive trigger
        Reason: requires a backend; static HTML doesn't have one.
        The cron-published latest brief is the demo.

   ✗  Per-reader personalization
        Reason: one marketing lead reads it. Premature.

   ✗  Streamlit / any backend framework
        Reason: assessor saw it as developer-y, not polished.

   ✗  Anthropic / paid LLMs
        Reason: must be free. Gemini Flash free tier covers us.

   ✗  Sales / CRM integration
        Reason: brief is for marketing, not sales handoff.

   ✗  Auto-publishing the suggested CQ responses as real content
        Reason: a human reads the suggestion before any action.
```

## 6. The pipeline (visual)

```
   INPUTS  (set once, edit when you want)
   ─────────────────────────────────────────────────────────
     config/watchlist.yml      competitors + URLs
     config/cq-context.md      CQ positioning + known gaps
     GOOGLE_API_KEY            in .env (FREE, AI Studio)
     src/snapshots/            git-tracked, last-week's content


   THE RUN  (GitHub Actions cron, weekly; manual `python -m
            src.main` works the same way locally)
   ─────────────────────────────────────────────────────────

     ┌──────────────┐
     │  1. FETCH    │   httpx async pull of 9 URLs
     └──────┬───────┘
            ▼
     ┌──────────────┐
     │  2. EXTRACT  │   readability strips chrome → clean text
     └──────┬───────┘
            ▼
     ┌──────────────┐
     │  3. DIFF     │   difflib paragraph compare vs snapshots
     └──────┬───────┘
            ▼  list of changed paragraphs
     ┌──────────────┐
     │  4. AI #1    │   Gemini Flash: tag + score (1-5)
     └──────┬───────┘
            ▼  only score ≥ 3 survive
     ┌──────────────┐
     │  5. AI #2    │   Gemini Flash: write Markdown brief
     └──────┬───────┘                  (Style B tone)
            ▼  Markdown
     ┌──────────────┐
     │  6. RENDER   │   Markdown → styled HTML (Tailwind)
     └──────┬───────┘
            ▼  styled HTML page
     ┌──────────────┐
     │  7. PUBLISH  │   git commit + push gh-pages branch
     └──────────────┘   GitHub Pages serves it publicly


   OUTPUT  (two surfaces the assessor sees)
   ─────────────────────────────────────────────────────────

   SURFACE 1 — GitHub repo (the proof / the source)
     https://github.com/<your-github-name>/cq-competitive-intel

     Front door = README.md, which contains:
       ▸ One-line description + big screenshot of a brief
       ▸ "Try it instantly" links to a committed sample
         + the live HTML demo URL
       ▸ "Run it yourself" — one-command setup
       ▸ "How it works" — pipeline diagram
       ▸ "Why these tools" — compressed tools comparison
       ▸ Cost ($0) + folder layout

     Repo layout:
       cq-competitive-intel/
       ├── README.md                ← front door
       ├── samples/                 ← committed example briefs
       │   └── 2026-05-22-brief.md
       ├── src/                     ← code
       ├── config/                  ← watchlist + cq-context
       ├── prompts/                 ← classify + synthesize
       ├── snapshots/               ← baselines
       ├── docs/                    ← GitHub Pages source
       ├── .github/workflows/       ← weekly.yml (cron)
       ├── .env.example
       └── requirements.txt


   SURFACE 2 — Hosted HTML page (the demonstration)
     https://<your-github-name>.github.io/cq-competitive-intel/

     → polished page with the latest brief
     → archive sidebar/footer linking previous briefs
     → "produced 2026-05-22 — next run Monday 2026-05-26"
```

## 7. AI roles (B5)

```
   AI #1  (classify)
     INPUT   list of diff chunks
     OUTPUT  JSON: per chunk → change_type + significance + reason
     MODEL   Gemini 2.5 Flash (free tier, structured output mode)
     COST    $0

   AI #2  (synthesize)
     INPUT   surviving chunks + cq-context.md + run date
     OUTPUT  Markdown brief in Style B (signal + suggested play)
     MODEL   Gemini 2.5 Flash
     COST    $0

   NOT AI  (deterministic plumbing)
     ▸ Fetch & extract                           httpx + readability
     ▸ Diff                                      difflib (stdlib)
     ▸ Markdown → HTML                           markdown lib + jinja
     ▸ Publish to GitHub Pages                   git + gh-pages branch
     ▸ Schedule                                  GitHub Actions cron
```

## 8. Tech stack (B6)

```
   LAYER                CHOICE                       WHY (one line)
   ──────────────────   ────────────────────────     ──────────────────────
   AI (both calls)      Gemini 2.5 Flash             Free tier, fast,
                                                     structured output
   Fetch                httpx + readability-lxml     Free, async, SSR
                                                     pages work fine
   Diff                 Python difflib (stdlib)      Free, deterministic
   Schema validation    Pydantic                     Catches malformed AI
   Markdown → HTML      python-markdown + jinja2     Free, well-known
   Styling              Tailwind CSS via CDN         Zero build step
   Hosting              GitHub Pages                 Free, public URL
   Production cron      GitHub Actions               Free at this volume
   Snapshot storage     Git-tracked JSON files       Free, versioned
```

## 9. What YOU need to run it

```
   ONE-TIME SETUP                          STATUS / COST
   ──────────────────────────────────────  ──────────────────
   ✓ Python 3.10+                          have 3.14.5 — FREE
   ☐ Google AI Studio API key              FREE
     (aistudio.google.com → Get API key)
   ☐ pip install -r requirements.txt       FREE
   ☐ Push the repo to GitHub                FREE
   ☐ Enable GitHub Pages from gh-pages      FREE
     branch
   ☐ Add GOOGLE_API_KEY as a GitHub          FREE
     repo secret (so cron can read it)

   COST OF RUNNING THIS WORKFLOW = $0
```

## 10. Build sequence (what's left to do)

```
   STEP   WHAT                                          STATUS
   ────   ───────────────────────────────────────────   ──────
   1      Re-scaffold 3-build/ folder structure         ❌
   2      Write code (or re-write):                     ❌
            models, storage, fetch, diff, classify,
            synthesize, main
   3      Add NEW pieces (not in v1):                   ❌
            ▸ render.py — markdown → HTML
            ▸ HTML template (Tailwind, Jinja2)
            ▸ publish.py — write to docs/ folder for
              GitHub Pages
            ▸ .github/workflows/weekly.yml — cron
   4      Commit all 3-build/ + .github/ to git         ❌
   5      Create .env with GOOGLE_API_KEY               ❌
   6      Dry run: fetch + diff only, no AI             ❌
   7      First full run (seeds snapshots; first        ❌
          brief is mostly "first observation" data)
   8      Second full run (real diffs)                  ❌
   9      Push to GitHub, enable Pages                  ❌
   10     Add GOOGLE_API_KEY as GitHub repo secret      ❌
   11     Trigger GitHub Actions workflow manually      ❌
          to verify cron path works
   12     Demo URL verified live for assessor           ❌
```

## 11. Definition of done

```
   The workflow is "done" when ALL of these are true:

   SURFACE 1 — GitHub repo (the proof)
   ☐ Repo is public on github.com
   ☐ README.md is polished:
        - One-line description + big screenshot
        - Try-it-instantly section (sample link + demo link)
        - Run-it-yourself section (one-command setup)
        - How-it-works pipeline diagram
        - Why-these-tools compressed comparison
        - Cost + folder layout
   ☐ samples/ contains at least one committed real brief
     (so assessor can see output without running)
   ☐ `python -m src.main` runs end-to-end on a clean
     machine with just a GOOGLE_API_KEY set
   ☐ Code reads cleanly (no dead code, no TODOs)

   SURFACE 2 — Hosted HTML page (the demonstration)
   ☐ GitHub Pages URL loads publicly (no login)
   ☐ The page shows a real brief produced by the workflow
     (not a hand-edited mockup)
   ☐ The brief reads marketer-quality
     (specific, named competitors, named CQ responses)
   ☐ The HTML looks polished (Tailwind applied;
     readable typography; archive nav)
   ☐ GitHub Actions cron has run at least once successfully
     end-to-end (proof of recurrence)

   COMMON
   ☐ Per-run cost is $0 (Gemini free tier)
   ☐ PDF deck embeds:
        - the live demo URL (Surface 2)
        - a screenshot of the rendered brief
        - the GitHub repo URL (Surface 1)
```

## 12. Risks + mitigations

```
   RISK                                      MITIGATION
   ─────────────────────────────────────     ──────────────────────────
   Gemini free tier hits rate limit          Cron retries automatically
   during cron run                           next day; manual rerun

   Competitor site blocks fetch              Brief notes failures;
                                             remaining brief still
                                             useful

   AI brief reads too generic                Tighten the synthesize
                                             prompt; if still generic,
                                             upgrade to Gemini 2.5 Pro
                                             (still free)

   HTML page looks unpolished                Time-budget the styling:
                                             ~1 hour of Tailwind work;
                                             use a clean newsletter
                                             template if rushed

   GitHub Pages cache lag                    Mention in deck — first
                                             load can be ~30s after
                                             a fresh push
```

## 13. What "done" looks like for the assessor

```
   Assessor reads the deck → clicks the live demo URL.
   Lands on a polished page (Tailwind, clean type).
   Sees the latest weekly brief: TL;DR top-3 + per-change
   bodies with named competitors, named CQ responses, links.
   Reads it in ~3 minutes. Sees the archive sidebar — clicks
   a previous week to confirm cadence is real, not a one-off.
   Thinks: "this person ships real things; the AI reasoning is
   sophisticated; the demo respects my time."
   Interview invite sent.
```

---

## Self-review

- ✅ No placeholders ("TBD" / "TODO")
- ✅ Internally consistent (free everywhere; Streamlit excised; HTML/GitHub Pages used consistently)
- ✅ Scope is one workflow, not multiple
- ✅ Every requirement is unambiguous

## Next step after sign-off

Invoke the writing-plans skill to produce the step-by-step build plan for the items in section 10. The plan will be the executable version of this alignment.
