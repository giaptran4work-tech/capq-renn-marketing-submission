# Workflow Design — Competitive Intelligence Brief Engine

> One-line: watch a curated list of competitor surfaces, detect meaningful weekly changes, and produce a marketer-ready brief with a suggested CQ response.

## Inputs

- **Sources:** A small YAML watchlist of competitor URLs grouped by competitor.
  - Initial watchlist: Affinity (`/`, `/pricing`, `/blog`), DealCloud (`/product`, `/pricing`), Carta LP (`/lp` or equivalent), Watershed/Juniper Square (`/`, `/pricing`), 4Degrees (`/`, `/pricing`). Final list locked when implementation begins.
  - Each entry: `{ competitor, url, surface_type: "homepage|pricing|product|blog|changelog" }`.
- **CQ positioning context:** A static `cq-context.md` file that captures CQ's current claims and gaps (drawn from [`1-discovery/company.md`](../1-discovery/company.md)). Used by the synthesizer to suggest specific CQ responses.
- **Baseline snapshots:** Stored JSON files in `3-build/src/snapshots/` (one per URL). Version-controlled so the demo always has a non-empty diff to show.
- **Format:** YAML watchlist + JSON snapshots + a Markdown context file.
- **Frequency / trigger:** Weekly via cron in production; one-click "Run now" via Streamlit UI for the demo.

## Steps

1. **Fetch.** `httpx` pulls HTML for each URL with a desktop user-agent and a 15-second timeout. On non-200, mark the URL as `fetch_failed` and skip it (the brief will note it).
2. **Extract.** `readability-lxml` strips chrome/nav/footer, leaving article-style content. Result is a clean markdown string per URL. Hash the normalized text.
3. **Diff.** Compare each URL's new content against its stored baseline using `difflib`. Emit semantic chunks of change (added paragraphs, removed paragraphs, modified bullet lists). If no baseline exists yet, treat the entire content as a "first observation" change.
4. **Classify (LLM call #1).** Send all diff chunks to Claude Haiku 4.5 in a single batched call with a structured-output (JSON) schema asking for, per chunk: `change_type` ∈ {feature_ship, pricing_move, positioning_shift, content_angle, design_only, noise} and `significance` ∈ 1–5. Drop everything classified as `noise` or `design_only` and everything with significance < 3.
5. **Synthesize (LLM call #2).** Send the surviving classified changes + CQ context to Claude Haiku 4.5 (or Sonnet 4.6 if quality warrants) to produce a 1-page Markdown brief. For each significant change, the brief outputs three lines:
   - **What changed:** specific, with a competitor name and URL.
   - **Why it matters for CQ:** tied to CQ's actual positioning claims.
   - **Suggested response:** concrete (e.g., "publish a `vs. Affinity` comparison page emphasizing the data-room stage", not "improve marketing").
   The brief also ends with a "Top 3 priorities this week" call-out.
6. **Persist & deliver.** Write the brief to `4-demo/outputs/{YYYY-MM-DD}-brief.md`. Update each URL's snapshot file with the new content so next week's run diffs against the right baseline. In production mode: POST a digest summary to a Slack webhook.

(Diagram in `../assets/workflow-diagram.png` — to be created after build.)

## Outputs

- **Primary:** `4-demo/outputs/{YYYY-MM-DD}-brief.md` — the 1-page weekly brief.
- **Secondary:** updated `3-build/src/snapshots/*.json` — next week's baseline.
- **Demo UI:** Streamlit page rendering the latest brief + a "Run now" button + a watchlist editor.
- **Production-mode (optional):** Slack webhook digest (top 3 priorities + link to full brief).

## Failure modes

| Failure | Likelihood | Handling |
|---|---|---|
| Competitor site returns 403 or aggressive bot blocking | Medium | Retry with backoff once, then mark as `fetch_failed` in the brief. Note in tools-comparison: production should use Firecrawl. |
| Competitor site is JS-rendered with no SSR | Medium | Same handling. Demo watchlist is curated to avoid this for first launch. |
| LLM returns malformed JSON for classification | Low | Pydantic schema validation + one retry with stricter instruction. If still invalid, fall back to "treat all chunks as significance 3 / unclassified". |
| LLM hallucinates a competitor name or URL in the brief | Medium | Constrain by passing only the actual diff chunks + URLs as the LLM's input — no free-text knowledge of competitors. Validate that every URL cited in the brief appears in the input set. |
| Baseline snapshot corrupt / missing | Low | Treat as first observation; report as such in the brief. |
| Cost runaway (huge diff for first run) | Low | Truncate each diff chunk to 1500 tokens; brief synthesis caps at ~6000 input tokens via summarization. |

## Cost / performance estimate

Assuming 6 URLs in the watchlist, average diff payload of ~600 tokens per URL, plus a ~1500-token CQ-context block.

- **LLM call #1 (classify):** input ~5,000 tokens, output ~600 tokens.
- **LLM call #2 (synthesize):** input ~4,000 tokens (surviving chunks + context), output ~800 tokens.
- **Total per run:** ~9,000 input + ~1,400 output tokens.

At **Claude Haiku 4.5** rates (~$0.80 / $4 per 1M tokens):
- Per run: ~$0.007 + ~$0.006 = **~$0.013** (1.3¢).
- Per year (weekly): **~$0.70**.

At **Claude Sonnet 4.6** rates (~$3 / $15 per 1M tokens) for the synthesizer only, Haiku for classifier:
- Per run: ~$0.004 (classifier) + ~$0.024 (synthesizer) = **~$0.028** (2.8¢).
- Per year: **~$1.50**.

**Runtime:** 30–60s end-to-end. Fetch is parallelized (asyncio) so wall-clock is bounded by the slowest competitor site. LLM calls are sequential (~10–15s each).

## Open decisions (to lock when building)

- **Classifier vs synthesizer model split.** Default both to Haiku 4.5 to start; upgrade synthesizer to Sonnet 4.6 only if a sample run is judged too generic.
- **Final watchlist.** 4–6 competitors. Validate each is fetchable before locking.
- **Streamlit vs Gradio.** Streamlit chosen for familiarity and Streamlit Cloud's free hosted tier.
- **Slack delivery for production mode.** Optional; demo doesn't require it.
