# CQ Competitive Intelligence Brief Engine

> AI-powered weekly competitive intelligence for capq.ai — fetches 4 competitor sites, AI-classifies what changed, AI-writes a marketer-grade brief, publishes it as a polished web page. $0 cost. Runs on a cron, ships every Monday.

**▸ Live demo:** https://giaptran4work-tech.github.io/cq-competitive-intel/
**▸ Sample brief:** [`samples/2026-05-22-brief.md`](samples/2026-05-22-brief.md)

## What it does

```
   ┌────────────────┐
   │  watchlist.yml │   4 competitors, 9 URLs
   └────────┬───────┘
            ▼
   ┌────────────────┐
   │   1. FETCH     │   Pull all 9 pages at once  (httpx async)
   └────────┬───────┘
            ▼  raw HTML
   ┌────────────────┐
   │   2. EXTRACT   │   Strip nav/ads, keep article content
   └────────┬───────┘
            ▼  clean text
   ┌────────────────┐      last week's
   │   3. DIFF      │ ◄─── snapshots
   └────────┬───────┘
            ▼  changed paragraphs
   ┌────────────────┐
   │   4. CLASSIFY  │   Gemini Flash: tag + score 1-5
   │     (AI #1)    │
   └────────┬───────┘
            ▼  only score ≥3 survive
   ┌────────────────┐      CQ positioning
   │   5. SYNTHESIZE│ ◄─── (cq-context.md)
   │     (AI #2)    │   Writes the brief
   └────────┬───────┘
            ▼  Markdown
   ┌────────────────┐
   │   6. RENDER    │   Jinja2 + Tailwind → polished HTML
   └────────┬───────┘
            ▼  styled page
   ┌────────────────┐
   │   7. PUBLISH   │   git commit → GitHub Pages
   └────────────────┘
```

Cost per run: **$0** (Gemini Flash free tier). Runtime end-to-end: ~60–90s.

## Try it instantly

- **See real output:** open the [latest brief](https://giaptran4work-tech.github.io/cq-competitive-intel/) or browse [`samples/`](samples/).

## Run it yourself

```bash
# 1. Clone
git clone https://github.com/giaptran4work-tech/cq-competitive-intel.git
cd cq-competitive-intel

# 2. Set up Python
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Get a free Google AI Studio key (https://aistudio.google.com)
cp .env.example .env
# edit .env, paste your key after GOOGLE_API_KEY=

# 4. Run
python -m src.main --github-handle YOUR_GITHUB_USERNAME
```

This produces `docs/archive/{today}.html` and updates `docs/index.html`. Open them in a browser.

For a dry run (no AI calls, just fetch + diff to verify networking):

```bash
python -m src.main --dry-run
```

## Why these tools

| Layer              | Choice                       | Why                                          |
|--------------------|------------------------------|----------------------------------------------|
| AI                 | Google Gemini 2.5 Flash      | Free tier, fast, structured JSON output      |
| HTTP fetch         | `httpx`                      | Async, fast, stdlib-shaped                   |
| Content extract    | `readability-lxml`           | Reliable on SSR'd marketing pages            |
| Diff               | `difflib` (stdlib)           | Deterministic, no LLM tokens spent on noise  |
| Render             | `python-markdown` + Jinja2   | Standard, well-documented                    |
| Styling            | Tailwind CSS via CDN         | No build step, looks polished                |
| Hosting            | GitHub Pages                 | Free, public URL                             |
| Schedule           | GitHub Actions               | Free at weekly cadence                       |

Each choice rejects an alternative for a stated reason — see [`docs/superpowers/specs/2026-05-21-workflow-alignment.md`](../docs/superpowers/specs/2026-05-21-workflow-alignment.md) for the full comparison.

## Project layout

```
.
├── README.md
├── src/                Python package — the workflow code
│   ├── main.py         CLI entry point
│   ├── fetch.py        async HTTP + content extraction
│   ├── diff.py         paragraph-level diff
│   ├── classify.py     AI #1 (Gemini)
│   ├── synthesize.py   AI #2 (Gemini)
│   ├── render.py       Markdown → HTML
│   ├── publish.py      write to docs/ for GitHub Pages
│   ├── storage.py      snapshot save/load
│   └── models.py       Pydantic types
├── config/             watchlist + CQ positioning context
├── prompts/            AI system prompts (versioned, editable)
├── templates/          Jinja2 HTML templates
├── samples/            committed example briefs
├── snapshots/          git-tracked baselines (so cron diffs work)
├── docs/               GitHub Pages source (auto-updated)
├── tests/              pytest unit tests
└── .github/workflows/  weekly cron config
```

## Tests

```bash
pytest tests/
```

Unit tests cover the deterministic pieces: models, storage, diff logic, HTML render. AI calls are verified end-to-end by running the pipeline.

## License

MIT.
