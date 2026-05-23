# Workflow #3 — AI-Edited Weekly Digest

**Status:** Designed (not built). Depth = enough to write submission Slide 8.
**Closes:** Gap 5 — CQ has zero owned audience: ~67 articles, no email capture, no remarketing list. Content spend doesn't compound.
**Layer in the story:** sense → produce → **capture**.

## Concept

Turn CQ's existing `/insights` library into a weekly email digest so readers become subscribers — building the owned-audience asset CQ completely lacks. AI does the editorial work; a human presses send.

## The flow

```
   CQ'S OWN /insights CMS
   (first-party — no third-party scraping)
            │
            ▼
   ┌──────────────────────────┐
   │ 1. SCRAPE & FILTER       │  pull the week's new articles from
   │    (AI assists filter)   │  CQ's own CMS; AI drops thin pieces
   └────────────┬─────────────┘
                ▼  shortlisted articles
   ┌──────────────────────────┐
   │ 2. COMPILE & CLUSTER     │  AI clusters selected articles into
   │    (AI)                  │  2–4 themes — gives the digest shape
   └────────────┬─────────────┘
                ▼  themed issue outline
   ┌──────────────────────────┐
   │ 3. DRAFT                 │  per article: 2–3 sentence summary +
   │    (AI)                  │  1 key takeaway. Plus editor's intro
   └────────────┬─────────────┘  + 3 subject-line variants, CQ voice
                ▼  draft issue
   ┌──────────────────────────┐
   │ 4. REVIEW & SEND         │  marketer reviews, presses send.
   │    (human)               │  No autosend — human in the loop.
   └──────────────────────────┘
```

## Tools — every tool, what it does, why over alternatives

| Tool | What it does in this workflow | Why this one |
|---|---|---|
| **feedparser** + CQ's CMS RSS feed / `sitemap.xml` | Step 1 Scrape — pulls the list of articles CQ published in the last 7 days, from CQ's own site | CQ owns the source — RSS/sitemap is the clean, sanctioned way; no third-party scraping, no licensing issue |
| **LLM via OpenRouter** (free model) | Step 1 Filter — judges editorial fit, drops thin pieces. Step 3 Draft — per-article summaries + takeaways + editor's intro + 3 subject-line variants | Same free LLM stack as Workflows #1 and #2 |
| **sentence-transformers + scikit-learn** | Step 2 Cluster — groups the week's articles into 2–4 themes to structure the digest | Same embedding + clustering pair as Workflow #2 — free, runs locally |
| **Beehiiv** (free tier) | Step 4 Send — marketer imports the AI draft, reviews, sends to subscribers. Also hosts the public archive + the on-site signup form that grows the list | Free tier; built for audience growth (signup forms, archive, referrals) — vs ConvertKit / Mailchimp, which are send-focused, not growth-focused |
| **Python** | Orchestration — ties the steps together | Consistent with the built Workflow #1 |

## Impact

Builds the owned email list CQ has zero of. Compounds every dollar of content spend, and survives SEO algorithm changes — an owned audience beats a rented one.

---

## Shared stack across the three workflows (deck point)

The three workflows aren't three random things — they share infrastructure:

```
   ALL THREE     Python  +  LLM via OpenRouter (free)
   #2 AND #3     sentence-transformers + scikit-learn (embeddings + clustering)
                 feedparser (RSS)
   #1 ONLY       Playwright (fetch) · difflib (diff)

   → "Build #1, and #2/#3 reuse ~70% of the stack."
   → A coherent marketing-ops platform — not three disconnected toys.
```
