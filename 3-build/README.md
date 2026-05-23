# CQ Competitive Intelligence Brief Engine

> AI-powered weekly competitive intelligence for capq.ai — fetches 4 competitor sites, AI-classifies what changed, AI-writes a marketer-grade brief, publishes it as a polished web page. $0 cost. Runs on a cron, ships every Monday.

**▸ Live demo:** https://giaptran4work-tech.github.io/cq-competitive-intel/
**▸ Sample brief:** [`samples/2026-05-22-brief.md`](samples/2026-05-22-brief.md)

---

## Why this exists

Capq.ai sells to emerging fund managers. To position the product, the
marketing team needs to know what **competing tools** (Affinity, Juniper
Square, DealCloud, 4Degrees) are saying every week — new features,
pricing shifts, ICP language changes, new content angles.

The manual version of this is **1–2 hours of tab-hopping per week** across
~13 competitor URLs, and the signal that actually matters (a single
paragraph reworded on a pricing page, a new "AI" mention in a hero
section) is the easiest thing to miss. Skip a week, and CQ's next
positioning move is built on a stale read.

Three constraints made it worth building:

1. **The cadence is fixed (weekly)** — too often = noise; less often =
   miss timely moves. A cron at a fixed time + URL solves cadence.
2. **The budget is $0** — paid intel tools (Crayon, Kompyte) start at
   ~$1k/mo. Free-tier LLM + free hosting + free cron = real $0.
3. **The output must be actionable, not raw** — a diff dump is useless to a
   marketer. The brief has to say *"do X in 2 hours because competitor Y
   moved on Z"*, tied back to CQ's positioning.

So the design target: a weekly Monday-morning brief, $0 to run, that a
marketing lead reads in under 3 minutes and acts on the same day.

---

## What you get

Every Monday at 09:00 UTC, GitHub Actions runs the pipeline and commits
a new HTML brief to `docs/archive/YYYY-MM-DD.html`, plus an `index.html`
landing page that lists all past briefs. GitHub Pages serves it at a
stable URL — no email, no PDF, no logins.

The brief always has the same shape (enforced by the synthesizer
prompt):

```
# CQ Competitive Intelligence Brief — 2026-05-22

## TL;DR — Top 3 priorities this week
1. Publish "CQ vs Juniper Square" comparison page — they reworded
   their hero to "the modern operating system for private capital",
   which directly attacks CQ's end-to-end claim.
2. ...
3. ...

## Changes worth knowing
### Juniper Square — homepage hero rewrite
- Where: junipersquare.com (homepage)
- What changed: <2-3 sentences, specific>
- Why it matters for CQ: <tied to a CQ positioning claim>
- Suggested CQ response: <concrete, 1-5 hours of work>

(...more changes, ordered by significance...)

## Noted but not pursuing this week
- <low-signal one-liners>

## Fetch failures (excluded from this brief)
- <urls that didn't load>
```

400–800 words, no emojis, always cites a real diff (never invents).

---

## How it works — the pipeline

```
   ┌────────────────┐
   │  watchlist.yml │   4 competitors, ~13 URLs
   └────────┬───────┘
            ▼
   ┌────────────────┐
   │   1. FETCH     │   Playwright headless Chromium
   └────────┬───────┘
            ▼  raw HTML
   ┌────────────────┐
   │   2. EXTRACT   │   readability-lxml → markdown-ish text
   └────────┬───────┘
            ▼  clean text
   ┌────────────────┐      last week's
   │   3. DIFF      │ ◄─── snapshot (JSON, sha1-keyed)
   └────────┬───────┘
            ▼  changed paragraphs (DiffChunk[])
   ┌────────────────┐
   │   4. CLASSIFY  │   AI #1 — tag + score 1–5
   │     (AI #1)    │   drop noise / design_only / score<3
   └────────┬───────┘
            ▼  SignificantChange[]  (sorted by significance)
   ┌────────────────┐      cq-context.md
   │   5. SYNTHESIZE│ ◄─── (positioning, claims, weaknesses)
   │     (AI #2)    │
   └────────┬───────┘
            ▼  Markdown brief (400–800 words)
   ┌────────────────┐
   │   6. RENDER    │   python-markdown + Jinja2 + Tailwind
   └────────┬───────┘
            ▼  styled HTML page
   ┌────────────────┐
   │   7. PUBLISH   │   docs/archive/{date}.html + index refresh
   └────────────────┘   GitHub Actions commits & pushes
```

Runtime end-to-end: ~60–90s. Cost per run: **$0** (OpenRouter free
model + free GitHub Actions minutes).

### Step 1 — Fetch (`src/fetch.py`)

**What:** Launch a single headless Chromium browser via Playwright. For
each of the ~13 URLs in `watchlist.yml`, open a **fresh browser context**
(isolated cookies/storage), navigate with a 20-second timeout, wait for
`domcontentloaded`. User-Agent is spoofed to Chrome 126 / Mac, viewport
1280×800, locale `en-US`.

If the response is HTTP ≥400, or the extracted text is < 100 chars
(usually means the page was bot-blocked or all content is JS-gated and
didn't render), the surface is marked `fetch_failed` and continues.

**Why Playwright instead of `requests` / `httpx`:**
- Competitor sites (Juniper Square, DealCloud) use SPA / JS rendering;
  raw HTTP gets a near-empty shell.
- They also run basic bot/WAF checks ("are you a real browser?"); a
  headless real Chromium passes without per-site workarounds.
- One browser launch + many contexts = isolated state per URL without
  re-launching the heavy browser process.

**Why a fresh context per URL:** if one site sets a cookie that
changes how another site responds (rare but possible via shared trackers),
the next request shouldn't inherit it.

**Why fail-soft on individual URLs:** one slow site shouldn't kill the
whole run. Failed surfaces are listed at the bottom of the brief
("Fetch failures excluded") so the marketing lead knows what's missing.

### Step 2 — Extract (`src/fetch.py::_extract_text`)

**What:** Run `readability-lxml` on the raw HTML to strip nav, footer,
sidebar, cookie banners. Then walk the result with BeautifulSoup,
keeping only `<h1>`–`<h4>`, `<p>`, `<li>`. Headings become `# ... ####`,
list items become `- ...`, paragraphs stay as text. Lines joined with
blank-line separators, runs of 3+ newlines collapsed.

**Why `readability-lxml`:** it was built for Firefox's reader mode — well-
tuned on SSR marketing pages (the exact thing competitor sites are).

**Why convert to markdown-ish text and not just keep HTML:** the next
step (diff) is paragraph-level. Plain text with blank-line paragraph
breaks is the cleanest input.

**Why drop everything but headings / paragraphs / list items:** nav
items and footers add noise that triggers spurious diffs every week.

### Step 3 — Diff (`src/diff.py`)

**What:** Load the last snapshot for this URL (stored as
`snapshots/{sha1(url)[:16]}.json`). Split both old and new text into
paragraphs (split on `\n\n`, drop blocks shorter than 15 chars). Run
`difflib.SequenceMatcher` on the two paragraph lists to get
insert / delete / replace opcodes.

- `insert` → a `DiffChunk(kind="added")` per new paragraph
- `delete` → a `DiffChunk(kind="removed")` per gone paragraph
- `replace` → ONE chunk shaped as `"WAS:\n{old}\n\nNOW:\n{new}"` so the
  classifier sees both sides of a rewording in context

Each chunk is capped at 1500 chars. On the very first run (no baseline
exists), the entire page would otherwise look "added"; the diff is
**capped at 5 chunks per surface** in that case to avoid flooding the
classifier.

Snapshots are **git-tracked**. The cron commits updated snapshots
alongside the brief, so the next run has a baseline to diff against.

**Why paragraph-level, not character / word / sentence level:**
character diffs are noisy ("changed a comma"); sentence diffs miss
structural changes (a whole paragraph moving). Paragraph is the unit a
marketer actually thinks in.

**Why `difflib` (stdlib) over a fancier diff:** it's deterministic, has
no dependencies, and "what changed at the paragraph level" doesn't need
ML — the LLM does the *meaning* part later.

**Why combine `replace` opcodes with `WAS:/NOW:`:** if a pricing page
just rewrote "Starter $99/mo" → "Starter $129/mo", the classifier needs
both sides to score it correctly. Sending them as two separate chunks
(one "removed", one "added") loses the relationship.

**Why a 1500-char cap:** a single block over that is almost always a
whole-page rewrite that needs eyeballs anyway; truncating saves tokens.

**Why git-track snapshots:** the cron runs in a fresh GitHub Actions
runner with no persistent disk. The repo is the storage.

### Step 4 — Classify (`src/classify.py`) — **AI #1**

**What:** Build a JSON payload of every diff chunk (id, competitor,
url, surface_type, kind, text). Send it to OpenRouter
(`openai/gpt-oss-120b:free`, temperature 0.1, max_tokens 8192) with the
system prompt at `prompts/classify.md`.

The prompt instructs the model to return a JSON array of
classifications, one per chunk:

```json
{
  "id": "ch_1",
  "change_type": "pricing_move",
  "significance": 5,
  "reason": "Starter tier moved from $0 to $99/mo."
}
```

Six possible `change_type`s:

| Type                 | What it catches                                          |
|----------------------|----------------------------------------------------------|
| `feature_ship`       | new product capability or integration                    |
| `pricing_move`       | price / plan / packaging change                          |
| `positioning_shift`  | headline, taglines, ICP language, value-prop, claims     |
| `content_angle`      | new topic / theme in blog or landing copy                |
| `design_only`        | visual refactor, color, layout — no message change       |
| `noise`              | cookie banner, datestamp, A/B whitespace, autogen IDs    |

After parsing, **drop** chunks where `change_type ∈ {noise, design_only}`
OR `significance < 3`. Sort the survivors by significance descending.

**Why a separate classify pass at all:** see [Why two AIs, not one](#why-two-ais-not-one)
below.

**Why score 1–5, not a binary keep/drop:** lets the synthesizer
prioritize. A score-5 pricing move gets a TL;DR slot; a score-3 blog
post gets a one-liner in "Noted but not pursuing".

**Why temperature 0.1:** classification should be deterministic. Two
runs over the same diff should give the same scores.

**Why the model gets to invent the `reason`:** it audits itself — when
the brief surfaces a weird item, the `reason` field tells you what the
classifier was thinking.

**Why no `response_format=json_object`:** json_object mode requires a
top-level JSON object. The classify prompt asks for a JSON *array* (one
classification per chunk). The parser strips ```` ```json ```` fences if the
model wraps the array — tolerant by design.

### Step 5 — Synthesize (`src/synthesize.py`) — **AI #2**

**What:** Take only the chunks that survived classification, plus
`config/cq-context.md` (CQ's positioning brief — claims, audience,
known weaknesses, suggested-response style guide), and send them to
OpenRouter (same model, temperature 0.3, max_tokens 8192).

The system prompt at `prompts/synthesize.md` locks the output structure
(TL;DR / Changes worth knowing / Noted but not pursuing) and the
writing rules:

- Cite only changes provided — never invent
- Specific over generic ("publish CQ vs Juniper Square comparison page
  emphasizing the data-room stage", not "improve SEO")
- Suggested responses must be tied to one of CQ's 8 product stages
- Bias for the founder voice + low-effort fixes (CQ's style guide)
- 400–800 words total, no emojis

The synthesizer never sees the noise-filtered chunks — it can only
write about what AI #1 said matters.

**Why temperature 0.3 (higher than classify):** brief writing benefits
from a little prose variation; classification benefits from
determinism.

**Why the CQ context file is fed in:** without it, suggested responses
would be generic. With it, the model knows *which* CQ weakness each
competitor move targets and *which* CQ stage to tie a response to.

**Why prompts are version-controlled `.md` files** (not inline strings):
they're the most-tuned part of the system. Editing them shouldn't need
a code change or a redeploy.

### Step 6 — Render (`src/render.py`)

**What:** `python-markdown` (with `extra` + `sane_lists` extensions)
converts the brief to HTML. Jinja2 wraps it in `templates/brief.html`
(Tailwind via CDN — no build step). `templates/index.html` is rendered
from the inventory of all archived briefs.

**Why python-markdown over a fancier renderer:** standard, well-
documented, predictable. The brief is plain prose + a couple of bullet
lists — nothing exotic.

**Why Tailwind via CDN:** no toolchain. The HTML file is self-
contained — opens correctly anywhere.

### Step 7 — Publish (`src/publish.py`)

**What:** Write three files for each brief into `docs/archive/`:

- `{date}.html` — the rendered page
- `{date}.md`   — the source-of-truth Markdown (for reproducibility / diffing across briefs)
- `{date}.title` — the H1, so `index.html` can show it without re-parsing

Then re-render `docs/index.html` with the full archive list (newest
first). GitHub Pages picks up the `docs/` folder change and serves it.

**Why three files per brief:** the `.md` makes a brief easy to grep
historically; the `.title` keeps the index render dependency-free.

### Cron — GitHub Actions (`.github/workflows/weekly.yml`)

**What:** Mondays at 09:00 UTC, Actions checks out the repo, sets up
Python 3.12, installs deps, installs Chromium for Playwright, runs
`python -m src.main --github-handle "$GITHUB_HANDLE"`. Then it commits
the updated `docs/` and `snapshots/` folders back to the repo and
pushes. `OPENROUTER_API_KEY` is a repo secret.

Also has `workflow_dispatch` so the run can be triggered manually from
the GitHub UI.

**Why GitHub Actions over a paid scheduler / VPS cron:** free at this
cadence, the runner has everything (Python, git, push permissions),
and the trigger is in the same repo as the code.

**Why commit snapshots back to the repo:** as above — the runner is
ephemeral, the repo is the storage layer.

---

## Why two AIs, not one

A single LLM call could "look at all the diffs and write a brief." Two
calls is materially better:

- **Cost.** Classify is a small + cheap call per chunk (a handful of
  fields out, no prose). Synthesize is the expensive call (writes
  400–800 words). Filtering to score-≥3 chunks first cuts the
  synthesize prompt by 80–90% on a typical week.
- **Quality.** Each AI has one job. Classify decides *is this important*
  (a yes/no decision with a score). Synthesize decides *how to write it
  up* (prose with structure + CQ-tied suggestions). Mixing them in one
  prompt produces unfocused output — the model splits attention between
  triage and writing.
- **Auditability.** When the brief misses something or includes
  something it shouldn't, the score + reason from AI #1 tells you
  whether the bug is in classification or synthesis. You can rerun just
  the broken stage with a tuned prompt.
- **Determinism where it should be.** Classify runs at temperature 0.1
  (deterministic-ish); synthesize at 0.3 (prose). One call can't have
  both temperatures.

---

## Configuration

Three editable files control behavior — no code changes needed to
re-target the system:

- **`config/watchlist.yml`** — competitors and their surfaces.
  Surfaces are tagged by `type` (`homepage`, `pricing`, `product`,
  `positioning`, `blog`, `changelog`). Tier 1 (slow-changing) and
  tier 2 (high-changing) surfaces are both monitored; the AI reads the
  content and classifies appropriately.

- **`config/cq-context.md`** — CQ's positioning, claims, audience,
  known weaknesses, suggested-response style guide. Update when CQ
  shifts. Read by the synthesizer prompt.

- **`prompts/classify.md` / `prompts/synthesize.md`** — the system
  prompts. Versioned and editable; tune these to change output
  behavior without touching code.

---

## Why these tools

| Layer              | Choice                       | Rejected alternative                          | Why                                          |
|--------------------|------------------------------|-----------------------------------------------|----------------------------------------------|
| LLM                | OpenRouter (free model)      | OpenAI direct / Anthropic direct / Gemini    | Region-agnostic free tier, OpenAI-compatible SDK; swap models without code changes |
| Fetch              | `playwright` (headless Chromium) | `httpx` / `requests`                       | Renders JS + beats basic bot detection on competitor SPAs |
| Content extract    | `readability-lxml`           | BeautifulSoup heuristics from scratch         | Reliable on SSR'd marketing pages; built for Firefox reader mode |
| Diff               | `difflib` (stdlib)           | LLM-based diff                                | Deterministic, no LLM tokens spent on noise |
| Models             | `pydantic`                   | dataclasses + manual validation              | Validates LLM JSON output, single source of truth for shapes |
| Render             | `python-markdown` + Jinja2   | mkdocs / pandoc                               | Standard, well-documented, no toolchain     |
| Styling            | Tailwind CSS via CDN         | local build + npm                             | No build step, page looks polished out of the box |
| Hosting            | GitHub Pages                 | Vercel / Netlify                              | Free, public URL, lives in the same repo    |
| Schedule           | GitHub Actions cron          | external scheduler / VPS cron                 | Free at weekly cadence, runner has push permission |
| Storage (snapshots)| git-tracked JSON             | sqlite / s3                                   | Cron runner is ephemeral; repo IS the storage |

Each row rejects an alternative for a stated reason. The deeper
write-up is in [`docs/superpowers/specs/2026-05-21-workflow-alignment.md`](../docs/superpowers/specs/2026-05-21-workflow-alignment.md).

---

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
python -m playwright install --with-deps chromium

# 3. Get a free OpenRouter key (https://openrouter.ai/keys)
cp .env.example .env
# edit .env, paste your key after OPENROUTER_API_KEY=

# 4. Run
python -m src.main --github-handle YOUR_GITHUB_USERNAME
```

This produces `docs/archive/{today}.html` and updates `docs/index.html`.
Open them in a browser.

### Run modes

| Command                                  | Effect                                                          |
|------------------------------------------|-----------------------------------------------------------------|
| `python -m src.main`                     | Full run + publish                                              |
| `python -m src.main --dry-run`           | Fetch + diff only (no AI calls). Verifies networking + extraction. |
| `python -m src.main --no-save-snapshots` | Don't update baselines (useful when iterating)                  |
| `python -m src.main --save-sample`       | Also copy outputs to `samples/`                                 |
| `python -m src.main --github-handle X`   | Set GitHub username for source links in the rendered page       |

---

## Project layout

```
.
├── README.md
├── src/                Python package — the workflow code
│   ├── main.py         CLI entry point + orchestration
│   ├── fetch.py        Playwright async fetch + content extraction
│   ├── diff.py         paragraph-level diff (SequenceMatcher)
│   ├── classify.py     AI #1 — tag + score (OpenRouter)
│   ├── synthesize.py   AI #2 — brief writer (OpenRouter)
│   ├── llm.py          shared OpenRouter client + model name
│   ├── render.py       Markdown → HTML (python-markdown + Jinja2)
│   ├── publish.py      write to docs/ for GitHub Pages
│   ├── storage.py      snapshot save/load (sha1-keyed JSON)
│   └── models.py       Pydantic types — Surface / DiffChunk / Classification / etc.
├── config/
│   ├── watchlist.yml   competitors + URLs to monitor
│   └── cq-context.md   CQ positioning brief fed to synthesizer
├── prompts/
│   ├── classify.md     AI #1 system prompt
│   └── synthesize.md   AI #2 system prompt
├── templates/
│   ├── brief.html      per-brief page (Tailwind via CDN)
│   └── index.html      archive landing page
├── samples/            committed example briefs (committed for review)
├── snapshots/          git-tracked baselines so the cron has something to diff
├── docs/               GitHub Pages source (auto-updated by the cron)
├── tests/              pytest unit tests
└── .github/workflows/
    └── weekly.yml      Mondays 09:00 UTC cron + manual trigger
```

## Tests

```bash
pytest tests/
```

Unit tests cover the deterministic pieces: Pydantic models, snapshot
storage, paragraph-diff logic, HTML render. The two AI calls are
verified end-to-end by running the pipeline (they're prompt-tuned, not
unit-testable).

## License

MIT.
