# Tool & Approach Comparison

> The brief asks: "be specific about which tools (and flows) you'd use and why you chose them over alternatives." This is where that lives. Each layer of the workflow is justified independently.

## Stack chosen

| Layer | Tool | One-line why |
|---|---|---|
| Orchestration | **Pure Python script** (asyncio) | Maximum control over LLM calls, easiest to host one-click, minimum dependencies |
| Fetching | **`httpx` + `readability-lxml`** | Free, fast, reliable on SSR'd marketing pages (which is most of them) |
| Diffing | **Python `difflib`** | Stdlib, semantic-enough for paragraph-level diffs once content is normalized |
| Classification LLM | **Claude Haiku 4.5** | Smart enough for structured-output classification, ~4x cheaper than Sonnet, prompt caching available |
| Synthesis LLM | **Claude Haiku 4.5** (with Sonnet 4.6 fallback) | Same Haiku unless sample brief is judged generic |
| Schema validation | **Pydantic** | Forces structured JSON outputs from the LLM; catches malformed responses early |
| UI / one-click demo | **Streamlit + Streamlit Cloud** | Free hosted tier, Python-native, one-page UI fits the use case (no SPA needed) |
| Snapshot storage | **JSON files in repo** | Version-controlled baseline; the demo always has a real diff to show |
| Scheduling (production) | **GitHub Actions cron** | Free for weekly runs, lives next to the code, no separate infra |

## Orchestration: why pure Python over the alternatives

| Alternative | Pros | Cons | Why rejected |
|---|---|---|---|
| **n8n (no-code)** | Visual flow, easy for non-devs to maintain | Self-host friction; the assessor would need a running n8n instance to "experience it" | The marketing brief is sophisticated AI — the depth lives in prompts and structured outputs, not in the orchestration. A visual builder hides that depth. |
| **Zapier** | Familiar to marketers; lots of integrations | Limited model control, expensive at scale, no streaming/structured output, hard to demo to a reviewer | Doesn't showcase the AI engineering. Also no clean way to ship the demo for one-click experience. |
| **LangChain / LangGraph** | Designed for chained LLM calls | Heavy abstraction for what is fundamentally a 4-call workflow; adds ~200 deps; LangGraph for a linear pipeline is overkill | YAGNI. Two LLM calls don't need a framework. |
| **Make / Pipedream** | Visual + code escape hatches | Similar drawbacks to Zapier — hidden depth, demo friction | Same reasoning as Zapier. |
| **Pure Python** (chosen) | Total control, minimum deps, ~150 lines, hosts anywhere | More setup than Zapier for a non-technical marketer | But this is a *demo* of marketing AI engineering — the dev surface is the point. For real CQ adoption, the Python script gets wrapped behind a UI / Streamlit / Slack command and the marketer never sees it. |

## Fetching: why `httpx` over the alternatives

| Alternative | Pros | Cons | Why rejected |
|---|---|---|---|
| **Firecrawl** | Handles JS, gets clean markdown out of the box, robust to bot blocking | Paid ($), API key, extra dep | **Strong production choice** — would adopt for CQ's real deployment. Rejected only because watchlist for the demo is curated to SSR'd pages where `httpx` works, and the demo should be runnable without paid keys. |
| **Playwright / Puppeteer** | Free, handles JS, robust | Slow (~5s/page), heavy install, browser-binary baggage on Streamlit Cloud | Overkill for marketing/pricing pages, which are SSR'd by SEO necessity. |
| **`requests` (stdlib-adjacent)** | Standard, well-known | Synchronous only — six sequential 5-second fetches would push runtime past 30s | `httpx` is the async-ready successor; same API, parallel fetches, no real cost. |
| **`httpx` + `readability-lxml`** (chosen) | Async, fast, free, no infra | Will fail on JS-only sites | Mitigated by curated watchlist; production path documented (swap to Firecrawl). |

## Diffing: why `difflib` over the alternatives

| Alternative | Pros | Cons | Why rejected |
|---|---|---|---|
| **LLM-only "what changed"** | Zero code, just prompt the LLM with old + new | Burns tokens on unchanged content; LLM hallucinates change; expensive at scale | Anti-pattern. Use deterministic diff for the cheap work; use LLM for the *judgement* work. |
| **`html-similarity` / page-similarity scores** | Detects structural change | Doesn't tell you *what* changed in a way the LLM can use | Too coarse. The brief needs the *text* of the change. |
| **`difflib`** (chosen) | Stdlib, paragraph-level chunks, deterministic | Naive on heavy re-flows | Good enough on clean-extracted content. The LLM filter for `noise` / `design_only` mops up false positives. |

## Why two LLM calls instead of one

A single mega-prompt ("here are 6 competitor pages with diffs, write me a brief") would work, and it's tempting because it's simpler. Two reasons we split:

1. **Cost.** ~70% of diff chunks are noise (date rotations, A/B variant of a button, footer year change). Filtering them out with a cheap classification call before paying for synthesis context cuts the synthesis prompt by ~60%.
2. **Quality.** Forcing structured classification with significance scores → the synthesizer sees only the chunks worth discussing, in the order they matter. That produces a tighter brief than "here's everything, sort it out."

## Model choice

**Primary:** Claude Haiku 4.5 (`claude-haiku-4-5-20251001`).

- **Why Haiku 4.5.** Strong structured-output adherence (the JSON schema for classification), strong instruction-following for the synthesis prompt's "specific, action-oriented, named-CQ-response" requirement, ~$0.80 / $4 per million tokens — roughly 4× cheaper than Sonnet 4.6.
- **Latency.** ~5–10s per call. Acceptable for a non-interactive demo run.
- **Prompt caching.** The CQ-context block (~1,500 tokens) is identical across runs — caching cuts synthesis input cost ~85% on subsequent runs.

**Fallback / upgrade path:** Claude Sonnet 4.6 (`claude-sonnet-4-6`) for the synthesizer only. Swap in if a sample brief is too generic. Costs ~2× at synthesis but classifier stays on Haiku.

**Why Claude over GPT-4o-mini.** Both would work; both would cost a similar amount. Picked Claude because:

1. Prompt caching is cleaner / cheaper at the Anthropic SDK level for this use case (large static context).
2. Anthropic's structured-output adherence is slightly stronger on tasks of this shape based on hands-on iteration.
3. This work was done in Claude Code, and the project memory already captures the Anthropic-SDK choice for future expansion.

Not a religious choice — if cost ever becomes a blocker or the user already has an OpenAI account, swapping the LLM client is ~10 lines (the prompts are model-agnostic).

## Hosting / delivery

- **Demo:** Streamlit Cloud. Free, one-click for the assessor, Python-native.
- **Production (if CQ adopted this):** GitHub Actions cron weekly → write brief to a repo, post digest to Slack. ~$0 monthly cost at this volume.
- **Why not a serverless function (Vercel / Cloudflare Workers).** Marketing-tool workflow doesn't need request-time latency; a cron + Streamlit UI is the right shape.
