# Workflow Alignment — Competitive Intel Brief Engine

**Date:** 2026-05-21
**Status:** Active alignment spec for the workflow being built for Task 1 of the Renn Labs marketing challenge.

This is the contract between user (Giap) and Claude for what we're building. Anything implemented that doesn't match this doc is wrong. Anything in this doc that doesn't match what Giap intends gets revised before more code is written.

---

## 1. Purpose

**Why this workflow exists.** CQ (capq.ai) makes a bold positioning claim — "the only platform covering all 8 stages of fundraising, while alternatives cover 2–3" — but defends it with no comparison content, no named competitors, nothing. That's Gap 3 in [`1-discovery/pain-points.md`](../../1-discovery/pain-points.md).

A marketing lead has to watch competitors weekly to defend that positioning. The manual version is a 2–4 hour weekly chore that nobody actually does consistently. This workflow makes it a 5-minute weekly review of a pre-written brief.

```
   The user value, in one line:

   "Don't lose to a competitor's move because you didn't see it."
```

## 2. Audience

**Who reads the brief.** CQ's marketing lead. In a founder-led startup that means the founder OR a single early marketer. NOT a marketing department. The brief is designed for:

- A solo person reading on Monday morning
- Used as a radar / signal-spotter, not an action prescription
- Triggers "go investigate this" or "ignore this" — not "do this specific play"

## 3. Cadence

```
   PRODUCTION   Once a week, automatically (GitHub Actions cron)
                Pulls the latest content from competitor sites,
                diffs vs last week, produces the brief.

   DEMO         Manually triggered ("Run now" button in Streamlit)
                Same pipeline, on demand, for the assessor to see.
```

## 4. What the workflow IS (in scope)

```
   ✓  Pulls 9 competitor URLs across 4 named competitors
        (Affinity, Juniper Square, DealCloud, Foundersuite)

   ✓  Extracts only the article content (no nav, no ads)

   ✓  Diffs against a snapshot from the previous run

   ✓  AI tags + scores each change 1–5
        (drops noise, design-only, and anything <3)

   ✓  AI writes a 1-page Markdown brief with:
        - Top 3 priorities this week (TL;DR)
        - Per-change: where / what / why-it-matters / suggested response
        - Tail of low-priority noted-but-not-pursuing items
        - Any fetch failures

   ✓  Saves brief to a file: 4-demo/outputs/{date}-brief.md

   ✓  Streamlit one-page UI for the demo (Run button + view brief)

   ✓  Snapshots auto-updated so next week's diff is meaningful
```

## 5. What the workflow IS NOT (deliberately out of scope)

```
   ✗  Email delivery to the marketing lead
        Reason: adds SMTP / Beehiiv / similar dependency without
        adding demo value. Brief file is enough.

   ✗  Slack delivery
        Reason: webhook URL is easy to add later if Giap wants
        production cron behavior. Not in demo scope.

   ✗  Per-individual personalization
        Reason: there's one marketing lead; personalization is
        premature.

   ✗  Sales / CRM integration
        Reason: brief is for marketing, not sales handoff.

   ✗  A/B testing of brief content / subject lines
        Reason: no subscriber base to test against.

   ✗  Tracking links inside the brief
        Reason: privacy + complexity; the brief has 9 links and
        the marketing lead doesn't need analytics on them.

   ✗  Auto-publishing comparison content
        Reason: a person should look at AI-generated competitive
        analysis before it goes public.
```

## 6. Tools chosen — what + why

```
   LAYER                CHOICE                       WHY (one line)
   ──────────────────   ────────────────────────     ─────────────────────
   AI #1 (classify)     Google Gemini Flash          Free tier + fast +
                                                     structured output OK
   AI #2 (synthesize)   Google Gemini Flash          Same; can upgrade to
                                                     Gemini Pro if needed
   Fetch                httpx + readability-lxml     Free, fast, works on
                                                     SSR'd marketing pages
   Diff                 Python difflib (stdlib)      Free, deterministic,
                                                     no LLM tokens spent
   Schema validation    Pydantic                     Catches malformed AI
                                                     output cleanly
   UI                   Streamlit                    One-page UI in <100
                                                     lines, free hosting
   Hosting (demo)       Streamlit Cloud              Free tier sufficient
   Snapshot storage     JSON files in repo           Free, version-
                                                     controlled
   Production cron      GitHub Actions               Free at this volume
```

**Why Gemini Flash over Claude Haiku** — Claude Haiku is ~$0.013/run; Gemini Flash has a free tier large enough for weekly runs forever. The user explicitly required free. Both models are capable for this task. Tradeoff: less prompt-caching cleanliness on the Google SDK, but with only 1.5K tokens of CQ-context it's not material.

**Why two AI calls instead of one big one** — ~70% of diffs are noise. A cheap classification call filters those out before paying for the synthesis call. Synthesis sees only the signal, produces a tighter brief.

## 7. The pipeline (visual)

```
   INPUTS (set once)
   ──────────────────
     watchlist.yml      competitors + URLs
     cq-context.md      CQ positioning + gaps
     GOOGLE_API_KEY     in .env (FREE, from aistudio.google.com)
     snapshots/         empty on first run


   THE RUN  (CLI: python -m src.main, or Streamlit Run button)
   ────────────────────────────────────────────────────────────

     ┌────────────┐
     │  1. FETCH  │   Pull all 9 URLs at once  (httpx async)
     └─────┬──────┘
           ▼
     ┌────────────┐
     │ 2. EXTRACT │   Strip ads / nav  (readability)
     └─────┬──────┘
           ▼
     ┌────────────┐
     │  3. DIFF   │   Paragraph diff vs snapshots/{url-hash}.json
     └─────┬──────┘
           ▼
     ┌────────────┐
     │  4. AI #1  │   Gemini Flash: tag + score each diff
     └─────┬──────┘
           ▼  (only score ≥ 3 survive)
     ┌────────────┐
     │  5. AI #2  │   Gemini Flash: write the brief
     └─────┬──────┘
           ▼
     ┌────────────┐
     │ 6. DELIVER │   Write 4-demo/outputs/{date}-brief.md
     └────────────┘


   OUTPUT
   ──────
     A Markdown file with:

     # CQ Competitive Intelligence Brief — 2026-05-21
     ## TL;DR — Top 3 priorities this week
     ## Changes worth knowing (per-change details)
     ## Noted but not pursuing this week
     ## Fetch failures (if any)
```

## 8. The files (what gets built)

```
   STATUS  PATH                            ROLE
   ──────  ──────────────────────────────  ───────────────────────────
   ✅      3-build/config/watchlist.yml    4 competitors, 9 URLs
   ✅      3-build/config/cq-context.md    CQ positioning + gaps
   ❌      3-build/.env                    Your GOOGLE_API_KEY
   ✅      3-build/prompts/classify.md     AI #1 prompt
   ✅      3-build/prompts/synthesize.md   AI #2 prompt
   ⚠️      3-build/requirements.txt        Needs swap: anthropic → google-genai
   ✅      3-build/src/models.py           Pydantic data types
   ✅      3-build/src/storage.py          Snapshot save/load
   ✅      3-build/src/fetch.py            Async HTTP + extract
   ✅      3-build/src/diff.py             Paragraph diff
   ⚠️      3-build/src/classify.py         Needs swap: Anthropic → Google SDK
   ⚠️      3-build/src/synthesize.py       Needs swap: Anthropic → Google SDK
   ✅      3-build/src/main.py             CLI runner
   ✅      3-build/src/app.py              Streamlit UI

   Auto-created on first run:
   ❌      3-build/src/snapshots/
   ❌      4-demo/outputs/

   Legend:  ✅ done   ⚠️ done but needs Gemini swap   ❌ not made yet
```

## 9. What YOU need to use it

```
   ONE-TIME SETUP                        STATUS / COST
   ──────────────────────────────────    ──────────────────
   ✓ Python 3.10+ on your machine        ✅ have 3.14.5 — FREE
   ☐ Google AI Studio API key            FREE
     (aistudio.google.com → Get API key)
   ☐ pip install -r requirements.txt     FREE

   PER RUN
   ──────────────────────────────────
   CLI:        python -m src.main
   Streamlit:  streamlit run src/app.py

   TOTAL COST OF RUNNING THIS WORKFLOW:  $0
```

## 10. Build sequence — what's left to do

```
   STEP  WHAT                                          STATUS
   ────  ────────────────────────────────────────────  ──────
   1     Swap Anthropic → Gemini in code               ❌
   2     Commit all 3-build/ files to git              ❌
   3     pip install -r requirements.txt               ❌
   4     Create .env with GOOGLE_API_KEY               ❌
   5     Dry run: fetch + diff only, no AI             ❌
   6     First full run (seeds snapshots; first        ❌
         brief treats everything as "added")
   7     Second full run (real diffs, real brief —     ❌
         the one we put in the deck)
   8     Deploy Streamlit app to Streamlit Cloud       ❌
   9     Verify demo URL works for the assessor        ❌
```

## 11. Definition of done

```
   The workflow is "done" when ALL of these are true:

   ☐  Streamlit demo URL loads publicly (no login)
   ☐  Clicking "Run now" produces a real brief in <90 seconds
   ☐  The brief reads like a marketer wrote it
        (specific, not generic; named competitors;
        named CQ responses — not "improve SEO")
   ☐  Per-run cost is $0  (Gemini free tier)
   ☐  GitHub repo is public; the code reads cleanly
   ☐  PDF deck embeds:
        - the live demo URL
        - a screenshot of a real brief
        - the GitHub repo URL
```

## 12. Risks to watch

```
   RISK                                     MITIGATION
   ─────────────────────────────────────    ───────────────────────────
   Gemini free tier hits rate limit         Streamlit shows pre-saved
   during reviewer click                    sample brief as fallback

   Competitor site blocks our fetch         Brief notes failures; rest
                                            of the brief still useful

   Streamlit Cloud cold-start is slow       App pre-loads latest brief
                                            on open so reviewer sees
                                            output instantly

   AI brief reads too generic               Upgrade synthesize.py from
                                            Gemini Flash to Gemini Pro
                                            (still free, slightly slower)

   Snapshots in repo get stale across       Acceptable for solo demo;
   weeks if not committed                   document the limitation
```

## 13. What "done" looks like for the assessor

```
   Assessor reads the PDF deck and clicks the live demo URL.
   Sees the Streamlit page with the latest brief pre-loaded.
   Clicks "Run now" → 30–60 seconds later → fresh brief in browser.
   Reads it. Thinks: "this person can ship a real thing."
   Interview invite sent.
```

---

## Self-review

- ✅ No placeholders (no "TBD" / "TODO" / "fill in details")
- ✅ Internally consistent (cost model = free across all references; same scope items repeated identically)
- ✅ Scope is one workflow, not multiple
- ✅ Every requirement is unambiguous (file paths, exact tools, exact success criteria)

## Next step after sign-off

Invoke the writing-plans skill to produce the step-by-step build plan for the items left in section 10 (the 9 ❌ rows). The plan will be the executable version of this alignment.
