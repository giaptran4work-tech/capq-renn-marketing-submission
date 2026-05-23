# Workflow #2 — Founder-Voice Content Engine

**Status:** Designed (not built). Depth = enough to write submission Slide 7.
**Closes:** Gap 2 — CQ's blog is bulk-published, anonymous, AI-feeling; it kills E-E-A-T and founder credibility.
**Layer in the story:** sense → **produce** → capture.

## Concept

Instead of more anonymous SEO filler, listen to what emerging GPs actually ask online, find the real pain themes, and draft content in CQ's founder voice that answers them.

## The flow

```
   WHERE EMERGING GPs TALK                       CQ'S FOUNDER VOICE
   Reddit · Substacks · LinkedIn                 homepage + handbook copy
            │                                              │
            ▼                                              │
   ┌────────────────────┐                                   │
   │ 1. LISTEN          │  pull recent posts from the       │
   │    (not AI)        │  places emerging GPs talk         │
   └─────────┬──────────┘                                    │
             ▼  raw posts + comments                         │
   ┌────────────────────┐                                    │
   │ 2. EXTRACT         │  AI pulls recurring questions,    │
   │    (AI)            │  objections, and exact GP wording │
   └─────────┬──────────┘                                    │
             ▼  structured pain points                       │
   ┌────────────────────┐                                    │
   │ 3. CLUSTER         │  embeddings group pain points     │
   │    (math, not AI)  │  into 3–5 themes; pick the        │
   └─────────┬──────────┘  strongest one CQ hasn't covered  │
             ▼  chosen theme                                 │
   ┌────────────────────┐ ◄──────────────────────────────────┘
   │ 4. DRAFT           │  AI writes a content brief +
   │    (AI)            │  a first-draft article in CQ voice
   └─────────┬──────────┘
             ▼  draft article
   ┌────────────────────┐
   │ 5. REVIEW          │  founder edits + publishes.
   │    (human)         │  AI drafts, human owns.
   └────────────────────┘
```

## Tools — every tool, what it does, why over alternatives

| Tool | What it does in this workflow | Why this one |
|---|---|---|
| **Reddit API** (via PRAW) | Step 1 Listen — pulls the last 7 days of posts + top comments from `r/venturecapital`, `r/privateequity` | Official API, free, ToS-clean — vs scraping Reddit HTML, which breaks and violates ToS |
| **feedparser** + a curated Substack RSS list | Step 1 Listen — pulls recent posts from ~10 alts-focused newsletters via their RSS feeds | RSS is the sanctioned free way to read newsletters — no scraping, stable |
| **LinkedIn scraper** — `joeyism/linkedin_scraper` | Step 1 Listen — pulls emerging-GP LinkedIn posts | LinkedIn is the richest surface but has no clean free read API; this scraper is Playwright-based (fits the stack), popular, maintained. Honest note: scraping LinkedIn is against LinkedIn's ToS — a real constraint, stated openly |
| **LLM via OpenRouter** (free model) | Step 2 Extract — raw posts → structured pains/questions/vocabulary. Step 4 Draft — writes the content brief + first-draft article | Same free, region-agnostic LLM stack as Workflow #1 — one provider across all three workflows |
| **sentence-transformers** (local model, e.g. `all-MiniLM-L6-v2`) | Step 3 Cluster — turns each pain point into a vector so semantically similar pains group together | Free, runs locally, real semantic grouping — vs keyword matching, which misses paraphrased pain |
| **scikit-learn** (KMeans / HDBSCAN) | Step 3 Cluster — groups the pain-point vectors into 3–5 themes | Standard free clustering library; pairs with the embeddings |
| **CQ's homepage + handbook copy** (style anchor) | Step 4 Draft — fed to the LLM as a voice reference so drafts sound like CQ's founder, not generic AI | Grounding in real CQ copy is what makes "founder voice" actually founder-voice |
| **Google Docs / Notion** | Step 5 Review — where the AI draft lands for the founder to edit before publishing | Familiar editing surface; keeps a human in the loop |

## Impact

One publish-ready, operator-credible, voice-consistent article per week — replacing anonymous bulk. Fixes the E-E-A-T problem and builds the founder's personal brand at the same time.
