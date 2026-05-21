# Competitive Intelligence Brief Engine — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a runnable weekly competitive intelligence pipeline that fetches 4 competitor sites, AI-classifies what changed, AI-writes a polished Markdown brief, renders it as a styled HTML page, publishes to GitHub Pages, and runs weekly via GitHub Actions cron — all on free tiers.

**Architecture:** Single Python package under `3-build/`. Async HTTP for fetching; deterministic diff for change detection; two Google Gemini Flash calls (classify + synthesize); Markdown rendered to HTML via python-markdown + Jinja2 + Tailwind CDN; output committed to `docs/` for GitHub Pages serving; GitHub Actions cron triggers the same `python -m src.main` command weekly. Same code runs locally and in CI.

**Tech Stack:** Python 3.10+, `google-genai`, `httpx`, `readability-lxml`, `python-markdown`, `Jinja2`, `Pydantic`, `pyyaml`, `python-dotenv`. Hosting: GitHub Pages. Scheduling: GitHub Actions.

---

## File structure (what will exist at the end)

```
3-build/
├── README.md                       polished front door (Task 14)
├── .gitignore                       (Task 1)
├── .env.example                    (Task 1)
├── requirements.txt                 (Task 1)
├── pyproject.toml                  (Task 1, optional: tells Python this is a package)
├── samples/
│   ├── 2026-05-22-brief.md         committed real brief (Task 12)
│   └── 2026-05-22-brief.html       rendered version (Task 12)
├── src/
│   ├── __init__.py                 (Task 1)
│   ├── models.py                   Pydantic types (Task 3)
│   ├── storage.py                  snapshot I/O (Task 4)
│   ├── diff.py                     paragraph diff (Task 5)
│   ├── fetch.py                    async HTTP + extract (Task 6)
│   ├── classify.py                 AI #1 (Task 7)
│   ├── synthesize.py               AI #2 (Task 8)
│   ├── render.py                   Markdown → HTML (Task 9)
│   ├── publish.py                  write to docs/ (Task 10)
│   └── main.py                     CLI orchestrator (Task 11)
├── config/
│   ├── watchlist.yml               (Task 2)
│   └── cq-context.md               (Task 2)
├── prompts/
│   ├── classify.md                 (Task 2)
│   └── synthesize.md               (Task 2)
├── templates/
│   ├── brief.html                  Jinja2 template (Task 9)
│   └── index.html                  archive landing (Task 9)
├── snapshots/                      auto-managed JSON files (Task 4)
│   └── .gitkeep
├── docs/                           GitHub Pages source (Task 10)
│   ├── index.html                  latest brief (Task 12)
│   └── archive/                    previous briefs (Task 12)
├── .github/
│   └── workflows/
│       └── weekly.yml              cron job (Task 13)
└── tests/
    ├── __init__.py                 (Task 3)
    ├── test_models.py              (Task 3)
    ├── test_storage.py             (Task 4)
    ├── test_diff.py                (Task 5)
    └── test_render.py              (Task 9)
```

All files live under `3-build/`. When the user pushes to GitHub as the public repo `cq-competitive-intel`, the contents of `3-build/` become that repo's root.

---

## Task 1: Scaffold the package

**Files:**
- Create: `3-build/.gitignore`
- Create: `3-build/.env.example`
- Create: `3-build/requirements.txt`
- Create: `3-build/pyproject.toml`
- Create: `3-build/src/__init__.py`
- Create: `3-build/tests/__init__.py`
- Create: `3-build/snapshots/.gitkeep`

- [ ] **Step 1: Create directory structure**

```powershell
New-Item -ItemType Directory -Force -Path 3-build, 3-build/src, 3-build/config, 3-build/prompts, 3-build/templates, 3-build/snapshots, 3-build/docs, 3-build/docs/archive, 3-build/samples, 3-build/tests, 3-build/.github/workflows | Out-Null
```

- [ ] **Step 2: Write `3-build/.gitignore`**

```
.env
.venv/
venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
*.egg-info/
build/
dist/
```

- [ ] **Step 3: Write `3-build/.env.example`**

```dotenv
# Copy this file to .env and fill in.
# .env is gitignored — never commit real keys.

# FREE — get one at https://aistudio.google.com → Get API key
GOOGLE_API_KEY=
```

- [ ] **Step 4: Write `3-build/requirements.txt`**

```
google-genai>=0.5.0
httpx>=0.27.0
readability-lxml>=0.8.1
lxml>=5.3.0
beautifulsoup4>=4.12.3
pyyaml>=6.0.2
pydantic>=2.9.0
python-dotenv>=1.0.1
markdown>=3.6
Jinja2>=3.1.4
pytest>=8.0.0
```

- [ ] **Step 5: Write `3-build/pyproject.toml`**

```toml
[project]
name = "cq-competitive-intel"
version = "0.1.0"
description = "AI-powered weekly competitive intelligence brief engine"
requires-python = ">=3.10"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 6: Create empty `__init__.py` files**

```powershell
New-Item -ItemType File -Force -Path 3-build/src/__init__.py, 3-build/tests/__init__.py, 3-build/snapshots/.gitkeep | Out-Null
```

- [ ] **Step 7: Create venv and install deps**

```powershell
cd 3-build
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.venv\Scripts\python.exe -m pip install -r requirements.txt
cd ..
```

Expected: dependencies install without error. If lxml fails on Python 3.14, try `pip install --pre lxml` or fall back to `--no-binary lxml` for source build.

- [ ] **Step 8: Verify directory structure**

```powershell
Get-ChildItem -Directory 3-build | Select-Object Name
```

Expected output includes: `config`, `docs`, `prompts`, `samples`, `snapshots`, `src`, `templates`, `tests`, `.github`.

- [ ] **Step 9: Commit**

```bash
git add 3-build/.gitignore 3-build/.env.example 3-build/requirements.txt 3-build/pyproject.toml 3-build/src/__init__.py 3-build/tests/__init__.py 3-build/snapshots/.gitkeep
git commit -m "scaffold(3-build): package skeleton + dependencies"
```

---

## Task 2: Data files (watchlist, CQ context, prompts)

**Files:**
- Create: `3-build/config/watchlist.yml`
- Create: `3-build/config/cq-context.md`
- Create: `3-build/prompts/classify.md`
- Create: `3-build/prompts/synthesize.md`

- [ ] **Step 1: Write `3-build/config/watchlist.yml`**

```yaml
# Competitor surfaces to monitor.
# The pipeline fetches each, diffs against the last snapshot, and includes
# meaningful changes in the weekly brief.

competitors:
  - name: Affinity
    surfaces:
      - url: https://www.affinity.co/
        type: homepage
      - url: https://www.affinity.co/pricing
        type: pricing
      - url: https://www.affinity.co/use-cases/venture-capital
        type: positioning

  - name: Juniper Square
    surfaces:
      - url: https://www.junipersquare.com/
        type: homepage
      - url: https://www.junipersquare.com/product/fundraising
        type: product

  - name: DealCloud
    surfaces:
      - url: https://dealcloud.com/
        type: homepage
      - url: https://dealcloud.com/solutions/private-equity/
        type: positioning

  - name: Foundersuite
    surfaces:
      - url: https://foundersuite.com/
        type: homepage
      - url: https://foundersuite.com/pricing/
        type: pricing
```

- [ ] **Step 2: Write `3-build/config/cq-context.md`**

```markdown
# CQ Positioning Context

> Static positioning brief fed to the synthesizer LLM so its suggested
> responses are grounded in CQ's actual claims. Update when CQ shifts.

## What CQ is

AI-powered fundraising platform for emerging fund managers raising capital
across alternatives (private equity, venture, hedge funds, secondaries).
End-to-end coverage from LP discovery through close.

## Positioning claim

"The only platform covering all 8 stages, while alternatives only cover 2–3."

The 8 stages: LP discovery → AI matching → outreach → secure data room →
NDA signing → LP portal → analytics → updates.

## Audience

Emerging GPs raising Fund I to Fund III, often founder-operators doing
their own fundraising (no dedicated IR team).

## Differentiators CQ leans on

- End-to-end coverage (vs point solutions)
- 150K+ LP database with mandate matching
- AI throughout (matching, outreach, data-room concierge)
- Built by operators: "$455M+ invested by our team", "50+ deals closed"

## Known weaknesses to target with suggested responses

- No external customer logos / testimonials / case studies
- No named-competitor comparison content
- /insights blog is bulk-published and anonymously bylined
- No security/compliance badges (SOC 2, ISO)
- No newsletter / email capture
- No segmented landing pages by fund type

## Suggested-response style guide

When suggesting CQ marketing responses, prefer:

- Specific over generic ("publish CQ vs Affinity comparison page emphasizing
  the data-room stage" — not "do more SEO")
- Tied to a stage (name which of the 8 stages a competitor is moving on)
- Bias for the founder voice (operator-perspective posts over bulk SEO)
- Low-effort first (2-hour fixes before 2-week campaigns)

## What CQ should NOT do

- Publish more bulk anonymous content
- Make claims they can't back with named customers
- Spend on paid ads while the credibility floor is broken
- Touch LP outreach automation that crosses SEC marketing-rule lines
```

- [ ] **Step 3: Write `3-build/prompts/classify.md`**

```markdown
You are classifying diffs detected on competitor marketing pages.

You will receive a JSON list of diff chunks. Each chunk has:
- `id`: a short id
- `competitor`: company name
- `url`: where the diff was found
- `surface_type`: one of `homepage`, `pricing`, `product`, `positioning`, `blog`, `changelog`
- `kind`: one of `added`, `removed`, `modified`
- `text`: the changed text (truncated to ~400 words)

For each chunk, return a classification object with:

- `id`: echo the input id
- `change_type`: exactly one of `feature_ship`, `pricing_move`, `positioning_shift`, `content_angle`, `design_only`, `noise`
- `significance`: integer 1–5 (1 = trivial, 5 = strategic / urgent)
- `reason`: one short sentence (max 25 words) explaining the classification

Definitions:
- `feature_ship`: a new product capability or integration is announced or described
- `pricing_move`: a price, plan, or packaging change
- `positioning_shift`: changes to headline, taglines, ICP language, value props, or competitive claims
- `content_angle`: a new topic, theme, or category appearing in marketing (blog/landing copy) without product change
- `design_only`: visual refactor, button color, layout, footer year — no message change
- `noise`: cookie banner, datestamp rotation, A/B variant whitespace, autogen IDs

Significance heuristics:
- Pricing changes on a `pricing` surface → at least 4
- Headline changes on a `homepage` → at least 4
- New product line / integration → 5
- Blog topic shift → 2–3
- Trivial rewording → 1

Return ONLY a JSON array, no prose, no markdown fences. Example shape:

[
  {"id": "ch_1", "change_type": "pricing_move", "significance": 5, "reason": "Starter tier moved from $0 to $99/mo."},
  {"id": "ch_2", "change_type": "noise", "significance": 1, "reason": "Cookie banner copy."}
]

If the input list is empty, return `[]`.
```

- [ ] **Step 4: Write `3-build/prompts/synthesize.md`**

```markdown
You are CQ's marketing-intelligence analyst. You produce a one-page weekly competitive intelligence brief that a marketing lead reads in under 3 minutes and acts on.

## Inputs you will receive

1. **CQ context** — a markdown brief of CQ's positioning, claims, weaknesses, and a suggested-response style guide. Treat this as the single source of truth for what CQ stands for.
2. **Significant changes** — a JSON list of competitor diffs that passed classification. Each item has: `competitor`, `url`, `surface_type`, `change_type`, `significance` (1–5), `reason`, and the diff `text`.
3. **Run date** in ISO format.

## Your job

Write a Markdown brief with this exact structure:

```
# CQ Competitive Intelligence Brief — {{run_date}}

## TL;DR — Top 3 priorities this week

1. **{action verb} {one-line action}** — {why, one line}
2. ...
3. ...

## Changes worth knowing

### {Competitor name} — {short label of the change}

- **Where:** [url]({url}) ({surface_type})
- **What changed:** {2–3 sentences, specific, name the actual change}
- **Why it matters for CQ:** {tied to a CQ positioning claim or known weakness}
- **Suggested CQ response:** {concrete, executable in 1–5 hours, follows the CQ style guide}

(...repeat for each significant change...)

## Noted but not pursuing this week

- {one-liner per low-significance item, if any}
```

## Rules

- Cite only the changes provided. Never invent a competitor move that isn't in the input. Never reference URLs not in the input set.
- Be specific. Bad: "improve SEO." Good: "publish `CQ vs Juniper Square` comparison page emphasizing the AI data room stage; target the keyword `juniper square alternatives`."
- Follow CQ's style guide for suggested responses (bias toward specific, stage-tied, founder-voice, low-effort-first).
- Order by significance descending.
- Top 3 priorities derive from the changes — not invented separately. Each must trace to a change in the body.
- If no changes survived filtering, write a short brief saying so and note 1–2 standing recommendations from CQ's known weaknesses.
- Length: 400–800 words of Markdown total. No emojis.

Return ONLY the Markdown brief, no preamble, no JSON, no code fences.
```

- [ ] **Step 5: Commit**

```bash
git add 3-build/config/watchlist.yml 3-build/config/cq-context.md 3-build/prompts/classify.md 3-build/prompts/synthesize.md
git commit -m "feat(3-build): watchlist, CQ context, and AI prompts"
```

---

## Task 3: Pydantic models (with tests)

**Files:**
- Create: `3-build/src/models.py`
- Create: `3-build/tests/test_models.py`

- [ ] **Step 1: Write `3-build/tests/test_models.py`**

```python
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.models import (
    Classification,
    DiffChunk,
    FetchResult,
    SignificantChange,
    Surface,
)


def test_surface_basic():
    s = Surface(url="https://example.com", type="homepage", competitor="Acme")
    assert s.url == "https://example.com"
    assert s.type == "homepage"
    assert s.competitor == "Acme"


def test_surface_rejects_bad_type():
    with pytest.raises(ValidationError):
        Surface(url="https://x.com", type="totally-not-a-type", competitor="Acme")


def test_fetch_result_default_status_is_ok():
    s = Surface(url="https://x.com", type="homepage", competitor="A")
    r = FetchResult(surface=s, content_md="hello", fetched_at=datetime.now(timezone.utc))
    assert r.status == "ok"
    assert r.error is None


def test_classification_significance_must_be_1_to_5():
    Classification(id="x", change_type="noise", significance=1, reason="ok")
    Classification(id="x", change_type="noise", significance=5, reason="ok")
    with pytest.raises(ValidationError):
        Classification(id="x", change_type="noise", significance=0, reason="bad")
    with pytest.raises(ValidationError):
        Classification(id="x", change_type="noise", significance=6, reason="bad")


def test_diff_chunk_basic():
    c = DiffChunk(
        id="ch_1",
        competitor="Acme",
        url="https://acme.com",
        surface_type="pricing",
        kind="added",
        text="Free tier now $99/mo",
    )
    assert c.id == "ch_1"
    assert c.kind == "added"


def test_significant_change_basic():
    sc = SignificantChange(
        competitor="Acme",
        url="https://acme.com",
        surface_type="pricing",
        change_type="pricing_move",
        significance=5,
        reason="big",
        text="Free tier $99",
    )
    assert sc.significance == 5
```

- [ ] **Step 2: Run tests to verify they fail (no implementation yet)**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_models.py -v
cd ..
```

Expected: `ImportError` or `ModuleNotFoundError` for `src.models`.

- [ ] **Step 3: Write `3-build/src/models.py`**

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

SurfaceType = Literal[
    "homepage", "pricing", "product", "positioning", "blog", "changelog"
]
ChangeKind = Literal["added", "removed", "modified"]
ChangeType = Literal[
    "feature_ship",
    "pricing_move",
    "positioning_shift",
    "content_angle",
    "design_only",
    "noise",
]


class Surface(BaseModel):
    url: str
    type: SurfaceType
    competitor: str


class FetchResult(BaseModel):
    surface: Surface
    content_md: Optional[str] = None
    fetched_at: datetime
    status: Literal["ok", "fetch_failed"] = "ok"
    error: Optional[str] = None


class DiffChunk(BaseModel):
    id: str
    competitor: str
    url: str
    surface_type: SurfaceType
    kind: ChangeKind
    text: str


class Classification(BaseModel):
    id: str
    change_type: ChangeType
    significance: int = Field(ge=1, le=5)
    reason: str


class SignificantChange(BaseModel):
    """A diff chunk that passed the classification filter."""

    competitor: str
    url: str
    surface_type: SurfaceType
    change_type: ChangeType
    significance: int
    reason: str
    text: str
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_models.py -v
cd ..
```

Expected: all 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add 3-build/src/models.py 3-build/tests/test_models.py
git commit -m "feat(3-build): Pydantic models + tests"
```

---

## Task 4: Snapshot storage (with tests)

**Files:**
- Create: `3-build/src/storage.py`
- Create: `3-build/tests/test_storage.py`

- [ ] **Step 1: Write `3-build/tests/test_storage.py`**

```python
from pathlib import Path

import pytest

from src import storage


@pytest.fixture(autouse=True)
def _temp_snapshot_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "SNAPSHOT_DIR", tmp_path)
    yield


def test_load_returns_none_when_no_snapshot():
    assert storage.load_snapshot("https://example.com/nothing") is None


def test_save_then_load_roundtrip():
    url = "https://example.com/page"
    content = "# Hello\n\nWorld"
    storage.save_snapshot(url, content)
    assert storage.load_snapshot(url) == content


def test_save_overwrites_existing():
    url = "https://example.com/page"
    storage.save_snapshot(url, "old")
    storage.save_snapshot(url, "new")
    assert storage.load_snapshot(url) == "new"


def test_different_urls_dont_collide():
    storage.save_snapshot("https://a.com", "alpha")
    storage.save_snapshot("https://b.com", "beta")
    assert storage.load_snapshot("https://a.com") == "alpha"
    assert storage.load_snapshot("https://b.com") == "beta"
```

- [ ] **Step 2: Run tests to verify they fail**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_storage.py -v
cd ..
```

Expected: `ImportError` for `src.storage`.

- [ ] **Step 3: Write `3-build/src/storage.py`**

```python
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshots"


def _url_key(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def _snapshot_path(url: str) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    return SNAPSHOT_DIR / f"{_url_key(url)}.json"


def load_snapshot(url: str) -> Optional[str]:
    """Return the last-saved content for a URL, or None if no baseline exists."""
    p = _snapshot_path(url)
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("content")


def save_snapshot(url: str, content: str) -> None:
    """Overwrite the snapshot for a URL."""
    p = _snapshot_path(url)
    p.write_text(
        json.dumps({"url": url, "content": content}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_storage.py -v
cd ..
```

Expected: 4 tests pass.

- [ ] **Step 5: Commit**

```bash
git add 3-build/src/storage.py 3-build/tests/test_storage.py
git commit -m "feat(3-build): snapshot storage + tests"
```

---

## Task 5: Diff logic (with tests)

**Files:**
- Create: `3-build/src/diff.py`
- Create: `3-build/tests/test_diff.py`

- [ ] **Step 1: Write `3-build/tests/test_diff.py`**

```python
from src.diff import compute_diff
from src.models import Surface


def _surface():
    return Surface(url="https://example.com", type="homepage", competitor="Acme")


def test_no_baseline_returns_added_chunks():
    new = "## Para 1\n\nThis is paragraph one with enough text.\n\n## Para 2\n\nSecond paragraph here, also enough text."
    chunks = compute_diff(_surface(), old=None, new=new, id_prefix="s0")
    assert len(chunks) >= 1
    assert all(c.kind == "added" for c in chunks)
    assert all(c.competitor == "Acme" for c in chunks)


def test_identical_returns_empty():
    text = "Same text here, long enough to count.\n\nSecond block, also long enough."
    chunks = compute_diff(_surface(), old=text, new=text, id_prefix="s0")
    assert chunks == []


def test_added_paragraph_detected():
    old = "Block one is long enough to register.\n\nBlock two same here."
    new = old + "\n\nBlock three is also long enough now."
    chunks = compute_diff(_surface(), old=old, new=new, id_prefix="s0")
    assert any(c.kind == "added" and "three" in c.text for c in chunks)


def test_removed_paragraph_detected():
    old = "Block A is long.\n\nBlock B that goes away.\n\nBlock C that stays."
    new = "Block A is long.\n\nBlock C that stays."
    chunks = compute_diff(_surface(), old=old, new=new, id_prefix="s0")
    assert any(c.kind == "removed" and "B" in c.text for c in chunks)


def test_tiny_blocks_filtered_out():
    new = "tiny\n\nyo\n\nThis block here is long enough to register, more text more text."
    chunks = compute_diff(_surface(), old=None, new=new, id_prefix="s0")
    for c in chunks:
        assert "tiny" not in c.text
        assert "yo" not in c.text


def test_chunk_text_truncated_to_max():
    long_block = "x" * 5000
    new = f"Header that is long enough to register here.\n\n{long_block}"
    chunks = compute_diff(_surface(), old=None, new=new, id_prefix="s0")
    for c in chunks:
        assert len(c.text) <= 1501  # 1500 + ellipsis
```

- [ ] **Step 2: Run tests to verify they fail**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_diff.py -v
cd ..
```

Expected: `ImportError` for `src.diff`.

- [ ] **Step 3: Write `3-build/src/diff.py`**

```python
"""Paragraph-level diffing of extracted competitor content."""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Optional

from .models import DiffChunk, Surface

MAX_CHUNK_CHARS = 1500
MIN_BLOCK_CHARS = 40


def _split_blocks(text: str) -> list[str]:
    blocks = [b.strip() for b in text.split("\n\n")]
    return [b for b in blocks if len(b) >= MIN_BLOCK_CHARS]


def _truncate(s: str) -> str:
    if len(s) <= MAX_CHUNK_CHARS:
        return s
    return s[:MAX_CHUNK_CHARS].rstrip() + "…"


def compute_diff(
    surface: Surface,
    old: Optional[str],
    new: str,
    id_prefix: str,
) -> list[DiffChunk]:
    new_blocks = _split_blocks(new)

    if old is None:
        return [
            DiffChunk(
                id=f"{id_prefix}_{i}",
                competitor=surface.competitor,
                url=surface.url,
                surface_type=surface.type,
                kind="added",
                text=_truncate(b),
            )
            for i, b in enumerate(new_blocks[:5])
        ]

    old_blocks = _split_blocks(old)
    if old_blocks == new_blocks:
        return []

    sm = SequenceMatcher(a=old_blocks, b=new_blocks, autojunk=False)
    chunks: list[DiffChunk] = []
    counter = 0

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            for b in new_blocks[j1:j2]:
                chunks.append(
                    DiffChunk(
                        id=f"{id_prefix}_{counter}",
                        competitor=surface.competitor,
                        url=surface.url,
                        surface_type=surface.type,
                        kind="added",
                        text=_truncate(b),
                    )
                )
                counter += 1
        elif tag == "delete":
            for b in old_blocks[i1:i2]:
                chunks.append(
                    DiffChunk(
                        id=f"{id_prefix}_{counter}",
                        competitor=surface.competitor,
                        url=surface.url,
                        surface_type=surface.type,
                        kind="removed",
                        text=_truncate(b),
                    )
                )
                counter += 1
        elif tag == "replace":
            old_text = "\n\n".join(old_blocks[i1:i2])
            new_text = "\n\n".join(new_blocks[j1:j2])
            combined = f"WAS:\n{old_text}\n\nNOW:\n{new_text}"
            chunks.append(
                DiffChunk(
                    id=f"{id_prefix}_{counter}",
                    competitor=surface.competitor,
                    url=surface.url,
                    surface_type=surface.type,
                    kind="modified",
                    text=_truncate(combined),
                )
            )
            counter += 1

    return chunks
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_diff.py -v
cd ..
```

Expected: 6 tests pass.

- [ ] **Step 5: Commit**

```bash
git add 3-build/src/diff.py 3-build/tests/test_diff.py
git commit -m "feat(3-build): paragraph-level diff + tests"
```

---

## Task 6: Fetch + extract (no tests — network integration)

**Files:**
- Create: `3-build/src/fetch.py`

Fetching depends on real network and live competitor sites. We verify by running, not unit-testing.

- [ ] **Step 1: Write `3-build/src/fetch.py`**

```python
"""Fetch competitor surfaces and extract clean text content."""

from __future__ import annotations

import asyncio
import re
from datetime import datetime, timezone
from typing import Iterable

import httpx
from bs4 import BeautifulSoup
from readability import Document

from .models import FetchResult, Surface

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
TIMEOUT = httpx.Timeout(15.0, connect=10.0)


def _extract_text(html: str) -> str:
    """Strip chrome and return readable body text as plain markdown-ish lines."""
    doc = Document(html)
    summary_html = doc.summary(html_partial=True)
    soup = BeautifulSoup(summary_html, "lxml")

    lines: list[str] = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        tag = el.name
        if tag.startswith("h"):
            lines.append(f"{'#' * int(tag[1])} {text}")
        elif tag == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)

    out = "\n\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


async def _fetch_one(client: httpx.AsyncClient, surface: Surface) -> FetchResult:
    now = datetime.now(timezone.utc)
    try:
        resp = await client.get(
            surface.url,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html"},
            follow_redirects=True,
        )
        resp.raise_for_status()
        text = _extract_text(resp.text)
        if len(text) < 100:
            return FetchResult(
                surface=surface,
                fetched_at=now,
                status="fetch_failed",
                error=f"Extracted content too short ({len(text)} chars) — likely JS-rendered.",
            )
        return FetchResult(surface=surface, content_md=text, fetched_at=now)
    except httpx.HTTPStatusError as e:
        return FetchResult(
            surface=surface,
            fetched_at=now,
            status="fetch_failed",
            error=f"HTTP {e.response.status_code}",
        )
    except (httpx.RequestError, asyncio.TimeoutError) as e:
        return FetchResult(
            surface=surface,
            fetched_at=now,
            status="fetch_failed",
            error=f"{type(e).__name__}: {e}",
        )


async def fetch_all(surfaces: Iterable[Surface]) -> list[FetchResult]:
    async with httpx.AsyncClient(timeout=TIMEOUT, http2=False) as client:
        return await asyncio.gather(*(_fetch_one(client, s) for s in surfaces))
```

- [ ] **Step 2: Smoke-test fetch against a known-good URL**

```powershell
cd 3-build
.venv\Scripts\python.exe -c "import asyncio; from src.fetch import fetch_all; from src.models import Surface; r = asyncio.run(fetch_all([Surface(url='https://example.com', type='homepage', competitor='Test')])); print('status:', r[0].status); print('chars:', len(r[0].content_md or ''))"
cd ..
```

Expected output (something like):
```
status: ok
chars: 100
```

(example.com is short; this just verifies the pipeline works. Real watchlist will return longer.)

- [ ] **Step 3: Commit**

```bash
git add 3-build/src/fetch.py
git commit -m "feat(3-build): async fetch + content extraction"
```

---

## Task 7: AI #1 — Classify

**Files:**
- Create: `3-build/src/classify.py`

- [ ] **Step 1: Write `3-build/src/classify.py`**

```python
"""LLM call #1: classify diff chunks by change_type + significance."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable

from google import genai
from google.genai import types
from pydantic import ValidationError, TypeAdapter

from .models import Classification, DiffChunk, SignificantChange

MODEL = "gemini-2.5-flash"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "classify.md"
MIN_SIGNIFICANCE = 3
DROP_TYPES = {"noise", "design_only"}

_classifications_adapter = TypeAdapter(list[Classification])


def _build_user_payload(chunks: list[DiffChunk]) -> str:
    payload = [
        {
            "id": c.id,
            "competitor": c.competitor,
            "url": c.url,
            "surface_type": c.surface_type,
            "kind": c.kind,
            "text": c.text,
        }
        for c in chunks
    ]
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _parse_response(raw: str) -> list[Classification]:
    s = raw.strip()
    if s.startswith("```"):
        s = s.strip("`")
        if s.startswith("json"):
            s = s[4:].lstrip()
    try:
        return _classifications_adapter.validate_python(json.loads(s))
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"Classifier returned invalid JSON: {e}\n\nRaw:\n{raw[:500]}")


def classify(chunks: Iterable[DiffChunk]) -> list[SignificantChange]:
    """Classify chunks and return only those that pass the filter."""
    chunks = list(chunks)
    if not chunks:
        return []

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key "
            "from https://aistudio.google.com."
        )

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    user_payload = _build_user_payload(chunks)

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=MODEL,
        contents=user_payload,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            max_output_tokens=2048,
            temperature=0.1,
        ),
    )

    raw = resp.text or "[]"
    classifications = _parse_response(raw)

    by_id = {c.id: c for c in classifications}
    significant: list[SignificantChange] = []
    for chunk in chunks:
        cls = by_id.get(chunk.id)
        if cls is None:
            continue
        if cls.change_type in DROP_TYPES:
            continue
        if cls.significance < MIN_SIGNIFICANCE:
            continue
        significant.append(
            SignificantChange(
                competitor=chunk.competitor,
                url=chunk.url,
                surface_type=chunk.surface_type,
                change_type=cls.change_type,
                significance=cls.significance,
                reason=cls.reason,
                text=chunk.text,
            )
        )

    significant.sort(key=lambda c: c.significance, reverse=True)
    return significant
```

- [ ] **Step 2: Commit**

```bash
git add 3-build/src/classify.py
git commit -m "feat(3-build): AI #1 classify diffs via Gemini"
```

(No test — verified end-to-end in Task 12.)

---

## Task 8: AI #2 — Synthesize

**Files:**
- Create: `3-build/src/synthesize.py`

- [ ] **Step 1: Write `3-build/src/synthesize.py`**

```python
"""LLM call #2: synthesize a one-page Markdown brief from significant changes."""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from typing import Iterable

from google import genai
from google.genai import types

from .models import SignificantChange

MODEL = "gemini-2.5-flash"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "synthesize.md"
CONTEXT_PATH = Path(__file__).resolve().parent.parent / "config" / "cq-context.md"


def _serialize_changes(changes: Iterable[SignificantChange]) -> str:
    payload = [
        {
            "competitor": c.competitor,
            "url": c.url,
            "surface_type": c.surface_type,
            "change_type": c.change_type,
            "significance": c.significance,
            "reason": c.reason,
            "text": c.text,
        }
        for c in changes
    ]
    return json.dumps(payload, ensure_ascii=False, indent=2)


def synthesize(changes: Iterable[SignificantChange], run_date: date) -> str:
    """Produce the 1-page brief. Returns Markdown."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key "
            "from https://aistudio.google.com."
        )

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    cq_context = CONTEXT_PATH.read_text(encoding="utf-8")
    user_payload = (
        f"## Run date\n{run_date.isoformat()}\n\n"
        f"## CQ context\n{cq_context}\n\n"
        f"## Significant changes (JSON)\n{_serialize_changes(changes)}\n"
    )

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=MODEL,
        contents=user_payload,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=2048,
            temperature=0.3,
        ),
    )
    return resp.text or ""
```

- [ ] **Step 2: Commit**

```bash
git add 3-build/src/synthesize.py
git commit -m "feat(3-build): AI #2 synthesize brief via Gemini"
```

---

## Task 9: Render (Markdown → HTML)

**Files:**
- Create: `3-build/src/render.py`
- Create: `3-build/templates/brief.html`
- Create: `3-build/templates/index.html`
- Create: `3-build/tests/test_render.py`

- [ ] **Step 1: Write `3-build/templates/brief.html`** (the per-brief template)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    code, pre { font-family: 'JetBrains Mono', monospace; }
    .prose h1 { @apply text-3xl font-bold mt-0 mb-2; }
    .prose h2 { @apply text-xl font-semibold mt-8 mb-3 text-slate-800; }
    .prose h3 { @apply text-lg font-semibold mt-6 mb-2 text-slate-700; }
    .prose p { @apply my-3 leading-relaxed; }
    .prose ul { @apply my-3 ml-6 list-disc space-y-2; }
    .prose ol { @apply my-3 ml-6 list-decimal space-y-2; }
    .prose a { @apply text-blue-600 underline hover:text-blue-800; }
    .prose strong { @apply font-semibold text-slate-900; }
  </style>
</head>
<body class="bg-slate-50 text-slate-700">
  <div class="max-w-3xl mx-auto px-6 py-10">

    <header class="mb-10 border-b border-slate-200 pb-6">
      <a href="./index.html" class="text-sm text-slate-500 hover:text-slate-700">← Archive</a>
      <p class="mt-4 text-sm font-medium text-blue-600 uppercase tracking-wider">
        CQ Competitive Intelligence
      </p>
      <p class="mt-1 text-sm text-slate-500">Published {{ run_date }}</p>
    </header>

    <article class="prose">
      {{ body | safe }}
    </article>

    <footer class="mt-16 pt-6 border-t border-slate-200 text-sm text-slate-500">
      <p>Generated automatically by the CQ Competitive Intelligence Brief Engine.</p>
      <p class="mt-1">
        <a href="https://github.com/{{ github_handle }}/cq-competitive-intel" class="text-blue-600 hover:text-blue-800">View source</a>
      </p>
    </footer>

  </div>
</body>
</html>
```

- [ ] **Step 2: Write `3-build/templates/index.html`** (the archive landing page)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CQ Competitive Intelligence — Weekly Brief</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-700">
  <div class="max-w-3xl mx-auto px-6 py-10">

    <header class="mb-10">
      <p class="text-sm font-medium text-blue-600 uppercase tracking-wider">
        CQ Competitive Intelligence
      </p>
      <h1 class="mt-2 text-3xl font-bold text-slate-900">Weekly Brief Archive</h1>
      <p class="mt-3 text-slate-600 leading-relaxed">
        Automated weekly competitive intelligence on what
        <a href="https://capq.ai" class="text-blue-600 hover:text-blue-800">capq.ai</a>'s
        rivals are doing — and what CQ should do about it.
      </p>
    </header>

    {% if briefs %}
    <section>
      <h2 class="text-lg font-semibold text-slate-800 mb-4">Latest brief</h2>
      <a href="./{{ briefs[0].filename }}" class="block p-5 bg-white rounded-lg border border-slate-200 hover:border-blue-400 transition">
        <p class="text-sm text-slate-500">{{ briefs[0].date }}</p>
        <p class="mt-1 font-medium text-slate-900">{{ briefs[0].title }}</p>
        <p class="mt-2 text-sm text-blue-600">Read →</p>
      </a>
    </section>

    {% if briefs|length > 1 %}
    <section class="mt-10">
      <h2 class="text-lg font-semibold text-slate-800 mb-4">Previous</h2>
      <ul class="space-y-3">
        {% for brief in briefs[1:] %}
        <li>
          <a href="./{{ brief.filename }}" class="block py-3 px-4 bg-white rounded border border-slate-200 hover:border-slate-400 transition">
            <span class="text-sm text-slate-500">{{ brief.date }}</span>
            <span class="ml-3 text-slate-700">{{ brief.title }}</span>
          </a>
        </li>
        {% endfor %}
      </ul>
    </section>
    {% endif %}

    {% else %}
    <p class="text-slate-500">No briefs published yet — the first run will appear here.</p>
    {% endif %}

    <footer class="mt-16 pt-6 border-t border-slate-200 text-sm text-slate-500">
      <p>
        <a href="https://github.com/{{ github_handle }}/cq-competitive-intel" class="text-blue-600 hover:text-blue-800">Source on GitHub</a>
      </p>
    </footer>

  </div>
</body>
</html>
```

- [ ] **Step 3: Write `3-build/tests/test_render.py`**

```python
from datetime import date

from src.render import render_brief_html, render_index_html


def test_render_brief_basic():
    md = "# CQ Brief — 2026-05-22\n\n## TL;DR\n\n1. **Do thing** — reason"
    html = render_brief_html(md, run_date=date(2026, 5, 22), github_handle="testuser")
    assert "<h1>CQ Brief" in html
    assert "<ol>" in html
    assert "Do thing" in html
    assert "2026-05-22" in html
    assert "testuser" in html


def test_render_index_with_briefs():
    briefs = [
        {"filename": "2026-05-22.html", "date": "2026-05-22", "title": "Week of May 19"},
        {"filename": "2026-05-15.html", "date": "2026-05-15", "title": "Week of May 12"},
    ]
    html = render_index_html(briefs, github_handle="testuser")
    assert "Latest brief" in html
    assert "Previous" in html
    assert "2026-05-22.html" in html
    assert "2026-05-15.html" in html


def test_render_index_empty():
    html = render_index_html([], github_handle="testuser")
    assert "No briefs published yet" in html
```

- [ ] **Step 4: Run tests to verify they fail**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_render.py -v
cd ..
```

Expected: `ImportError` for `src.render`.

- [ ] **Step 5: Write `3-build/src/render.py`**

```python
"""Render the Markdown brief to styled HTML using Jinja2 + Tailwind."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def _md_to_html(text: str) -> str:
    return md.markdown(text, extensions=["extra", "sane_lists"])


def render_brief_html(brief_md: str, run_date: date, github_handle: str) -> str:
    """Convert a Markdown brief to a full styled HTML page."""
    body_html = _md_to_html(brief_md)
    title = brief_md.splitlines()[0].lstrip("#").strip() if brief_md else "Brief"
    template = _env.get_template("brief.html")
    return template.render(
        title=title,
        run_date=run_date.isoformat(),
        body=body_html,
        github_handle=github_handle,
    )


def render_index_html(briefs: Iterable[dict], github_handle: str) -> str:
    """Render the archive landing page from a list of brief metadata dicts.

    Each dict needs: filename, date, title.
    Most recent first.
    """
    template = _env.get_template("index.html")
    return template.render(briefs=list(briefs), github_handle=github_handle)
```

- [ ] **Step 6: Run tests to verify they pass**

```powershell
cd 3-build
.venv\Scripts\python.exe -m pytest tests/test_render.py -v
cd ..
```

Expected: 3 tests pass.

- [ ] **Step 7: Commit**

```bash
git add 3-build/src/render.py 3-build/templates/brief.html 3-build/templates/index.html 3-build/tests/test_render.py
git commit -m "feat(3-build): Markdown→HTML render + tests"
```

---

## Task 10: Publish module

**Files:**
- Create: `3-build/src/publish.py`

- [ ] **Step 1: Write `3-build/src/publish.py`**

```python
"""Write the rendered brief to the docs/ folder for GitHub Pages."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Iterable, Optional

from .render import render_brief_html, render_index_html

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


def _extract_title(brief_md: str) -> str:
    if not brief_md:
        return "Brief"
    first_line = brief_md.splitlines()[0].lstrip("#").strip()
    return first_line[:80] if first_line else "Brief"


def _list_archive_briefs(github_handle: str) -> list[dict]:
    """Inventory the docs/archive folder, newest first."""
    archive = DOCS_DIR / "archive"
    if not archive.exists():
        return []
    files = sorted(archive.glob("*.html"), reverse=True)
    briefs = []
    for f in files:
        name = f.stem  # e.g. "2026-05-22"
        if not re.match(r"^\d{4}-\d{2}-\d{2}", name):
            continue
        title_path = archive / f"{name}.title"
        title = title_path.read_text(encoding="utf-8").strip() if title_path.exists() else name
        briefs.append({
            "filename": f"archive/{f.name}",
            "date": name,
            "title": title,
        })
    return briefs


def publish_brief(
    brief_md: str,
    run_date: date,
    github_handle: str,
    *,
    also_save_to_samples: bool = False,
) -> Path:
    """Render brief + write to docs/archive/{date}.html + update docs/index.html.

    Returns the path of the per-date HTML file.
    """
    DOCS_DIR.mkdir(exist_ok=True)
    archive_dir = DOCS_DIR / "archive"
    archive_dir.mkdir(exist_ok=True)

    date_str = run_date.isoformat()
    title = _extract_title(brief_md)

    # Per-brief HTML
    brief_html = render_brief_html(brief_md, run_date=run_date, github_handle=github_handle)
    brief_path = archive_dir / f"{date_str}.html"
    brief_path.write_text(brief_html, encoding="utf-8")

    # Companion title file so the index can show it
    (archive_dir / f"{date_str}.title").write_text(title, encoding="utf-8")

    # Companion Markdown for the source-of-truth
    (archive_dir / f"{date_str}.md").write_text(brief_md, encoding="utf-8")

    # Refresh index
    briefs = _list_archive_briefs(github_handle)
    index_html = render_index_html(briefs, github_handle=github_handle)
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # Optional: copy into samples/ for the committed example in the repo
    if also_save_to_samples:
        SAMPLES_DIR.mkdir(exist_ok=True)
        (SAMPLES_DIR / f"{date_str}-brief.md").write_text(brief_md, encoding="utf-8")
        (SAMPLES_DIR / f"{date_str}-brief.html").write_text(brief_html, encoding="utf-8")

    return brief_path
```

- [ ] **Step 2: Commit**

```bash
git add 3-build/src/publish.py
git commit -m "feat(3-build): publish brief to docs/ for GitHub Pages"
```

---

## Task 11: Main orchestrator

**Files:**
- Create: `3-build/src/main.py`

- [ ] **Step 1: Write `3-build/src/main.py`**

```python
"""End-to-end runner.

Run modes:
    python -m src.main                           # full run + publish
    python -m src.main --dry-run                 # fetch + diff only (no AI)
    python -m src.main --no-save-snapshots       # don't update baselines
    python -m src.main --save-sample             # also copy result to samples/
    python -m src.main --github-handle <name>    # for repo source links
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv

from .classify import classify
from .diff import compute_diff
from .fetch import fetch_all
from .models import DiffChunk, Surface
from .publish import publish_brief
from .storage import load_snapshot, save_snapshot
from .synthesize import synthesize

ROOT = Path(__file__).resolve().parent.parent
WATCHLIST = ROOT / "config" / "watchlist.yml"


def load_watchlist() -> list[Surface]:
    data = yaml.safe_load(WATCHLIST.read_text(encoding="utf-8"))
    surfaces: list[Surface] = []
    for c in data["competitors"]:
        for s in c["surfaces"]:
            surfaces.append(Surface(url=s["url"], type=s["type"], competitor=c["name"]))
    return surfaces


def collect_diffs(fetched, save: bool):
    chunks: list[DiffChunk] = []
    failures: list[tuple[str, str]] = []
    for i, result in enumerate(fetched):
        if result.status == "fetch_failed":
            failures.append((result.surface.url, result.error or "unknown"))
            continue
        baseline = load_snapshot(result.surface.url)
        url_chunks = compute_diff(
            surface=result.surface,
            old=baseline,
            new=result.content_md or "",
            id_prefix=f"s{i}",
        )
        chunks.extend(url_chunks)
        if save:
            save_snapshot(result.surface.url, result.content_md or "")
    return chunks, failures


def _failures_section(failures: list[tuple[str, str]]) -> str:
    if not failures:
        return ""
    lines = ["", "## Fetch failures (excluded from this brief)", ""]
    for url, err in failures:
        lines.append(f"- {url} — {err}")
    return "\n".join(lines) + "\n"


def run(
    dry_run: bool = False,
    save_snapshots: bool = True,
    save_sample: bool = False,
    github_handle: str = "your-github",
) -> Path | None:
    load_dotenv()
    surfaces = load_watchlist()
    print(f"[1/5] Fetching {len(surfaces)} surfaces...", flush=True)
    fetched = asyncio.run(fetch_all(surfaces))

    print(f"[2/5] Diffing (save_snapshots={save_snapshots})...", flush=True)
    chunks, failures = collect_diffs(fetched, save=save_snapshots)
    print(f"      {len(chunks)} diff chunks; {len(failures)} fetch failures", flush=True)

    if dry_run:
        for c in chunks[:8]:
            print(f"  - [{c.competitor} / {c.surface_type} / {c.kind}] {c.text[:120]!r}")
        if not chunks:
            print("  (no diffs — first run after seeding produces empty briefs)")
        return None

    print(f"[3/5] Classifying {len(chunks)} chunks via Gemini...", flush=True)
    significant = classify(chunks)
    print(f"      {len(significant)} significant after filtering", flush=True)

    print("[4/5] Synthesizing brief...", flush=True)
    brief = synthesize(significant, run_date=date.today())
    brief_with_failures = brief.rstrip() + "\n" + _failures_section(failures)

    print("[5/5] Publishing to docs/...", flush=True)
    out_path = publish_brief(
        brief_with_failures,
        run_date=date.today(),
        github_handle=github_handle,
        also_save_to_samples=save_sample,
    )
    print(f"\nPublished: {out_path}")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="CQ Competitive Intel Brief Engine")
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch + diff only; skip AI calls.")
    parser.add_argument("--no-save-snapshots", action="store_true",
                        help="Don't update baselines (for testing).")
    parser.add_argument("--save-sample", action="store_true",
                        help="Also copy outputs to samples/.")
    parser.add_argument("--github-handle", default=os.environ.get("GITHUB_HANDLE", "your-github"),
                        help="Your GitHub username, used in source links.")
    args = parser.parse_args()
    run(
        dry_run=args.dry_run,
        save_snapshots=not args.no_save_snapshots,
        save_sample=args.save_sample,
        github_handle=args.github_handle,
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Dry-run smoke test (no API key needed)**

```powershell
cd 3-build
.venv\Scripts\python.exe -m src.main --dry-run --no-save-snapshots
cd ..
```

Expected output: prints "[1/5] Fetching 9 surfaces...", "[2/5] Diffing...", number of chunks, and a few sample chunks. May report fetch_failed for some URLs — that's OK.

- [ ] **Step 3: Commit**

```bash
git add 3-build/src/main.py
git commit -m "feat(3-build): CLI orchestrator (main.py)"
```

---

## Task 12: First real run + sample capture

This task needs a real `GOOGLE_API_KEY`.

- [ ] **Step 1: Get a Google AI Studio API key**

Open https://aistudio.google.com in a browser → "Get API key" → create one. Free, no credit card.

- [ ] **Step 2: Create `3-build/.env`**

```powershell
Copy-Item 3-build/.env.example 3-build/.env
```

Then edit `3-build/.env` and paste the API key after `GOOGLE_API_KEY=`.

- [ ] **Step 3: First full run — seeds snapshots, produces "all added" brief**

```powershell
cd 3-build
.venv\Scripts\python.exe -m src.main --github-handle giaptran4work-tech
cd ..
```

Expected: pipeline completes in 60-120 seconds. Writes `docs/archive/2026-05-22.html` and refreshes `docs/index.html`. First brief treats everything as "added" (no baseline yet).

- [ ] **Step 4: Verify first brief**

```powershell
Get-ChildItem 3-build/docs/archive/ | Select-Object Name
Get-Content 3-build/docs/archive/2026-05-22.md -TotalCount 30
```

Expected: file exists and shows a real brief structure (heading, TL;DR, changes).

- [ ] **Step 5: Second run — produces real diff against fresh baselines**

```powershell
cd 3-build
.venv\Scripts\python.exe -m src.main --github-handle giaptran4work-tech --save-sample
cd ..
```

Expected: second run produces a smaller brief (no diff against itself = likely empty, or only changes that happened in the time between runs). The `--save-sample` flag copies the brief into `samples/` for repo-committed showcase.

- [ ] **Step 6: Commit the first samples + initial snapshots**

```bash
git add 3-build/samples/ 3-build/snapshots/ 3-build/docs/
git commit -m "feat(3-build): first real brief + seeded snapshots"
```

(Snapshots are git-tracked so the next cron run has a baseline to diff against.)

---

## Task 13: GitHub Actions cron

**Files:**
- Create: `3-build/.github/workflows/weekly.yml`

- [ ] **Step 1: Write `3-build/.github/workflows/weekly.yml`**

```yaml
name: Weekly competitive intel brief

on:
  schedule:
    # Mondays at 09:00 UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:  # allows manual trigger from the GitHub UI

permissions:
  contents: write

jobs:
  brief:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run brief pipeline
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          GITHUB_HANDLE: ${{ github.repository_owner }}
        run: python -m src.main --github-handle "$GITHUB_HANDLE"

      - name: Commit and push updates
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/ snapshots/
          if ! git diff --staged --quiet; then
            git commit -m "chore: weekly brief $(date +%Y-%m-%d)"
            git push
          else
            echo "No changes to commit."
          fi
```

- [ ] **Step 2: Commit**

```bash
git add 3-build/.github/workflows/weekly.yml
git commit -m "feat(3-build): GitHub Actions weekly cron"
```

---

## Task 14: README.md (the front door)

**Files:**
- Create: `3-build/README.md`

- [ ] **Step 1: Write `3-build/README.md`**

````markdown
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
````

- [ ] **Step 2: Commit**

```bash
git add 3-build/README.md
git commit -m "docs(3-build): polished README front door"
```

---

## Task 15: Deploy to GitHub + verify hosted URL

This task is performed by the user via the GitHub web UI + command line.

- [ ] **Step 1: Create a new public GitHub repo named `cq-competitive-intel`**

In the GitHub UI:
1. Go to https://github.com/new
2. Name: `cq-competitive-intel`
3. Description: "AI-powered weekly competitive intel brief engine"
4. Public
5. Do NOT initialize with README (we have one)
6. Create

- [ ] **Step 2: Push the contents of `3-build/` to that repo**

```powershell
cd 3-build
git init
git add .
git commit -m "initial commit: full workflow"
git branch -M main
git remote add origin https://github.com/giaptran4work-tech/cq-competitive-intel.git
git push -u origin main
cd ..
```

(This creates a SECOND independent git repo inside `3-build/`. The outer `Tét/` repo is unaffected. Add `3-build/.git/` to root `.gitignore` if needed.)

- [ ] **Step 3: Enable GitHub Pages**

In the GitHub UI for the new repo:
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / folder: `/docs`
4. Save

GitHub will deploy. First build takes ~1 min. URL will be at `https://giaptran4work-tech.github.io/cq-competitive-intel/`.

- [ ] **Step 4: Add `GOOGLE_API_KEY` as a repo secret**

In the GitHub UI:
1. Settings → Secrets and variables → Actions → New repository secret
2. Name: `GOOGLE_API_KEY`
3. Value: your AI Studio key
4. Add

This lets the cron workflow read the key when it runs.

- [ ] **Step 5: Trigger the workflow manually to verify cron path**

In the GitHub UI:
1. Actions tab → "Weekly competitive intel brief" workflow
2. Run workflow → main → Run workflow
3. Wait ~2 min for it to complete

Check that it succeeds and that the workflow committed a new brief in `docs/archive/`.

- [ ] **Step 6: Verify the live demo URL**

Open `https://giaptran4work-tech.github.io/cq-competitive-intel/` in a browser. Confirm:
- Page loads
- Latest brief is linked from the front
- Brief opens and is properly styled

---

## Self-review

**Spec coverage check:**

| Spec section                          | Covered by task    |
|---------------------------------------|--------------------|
| §4 Watchlist + CQ context             | Task 2             |
| §4 Fetch → extract → diff             | Tasks 5, 6         |
| §4 AI classify + filter (score ≥3)    | Task 7             |
| §4 AI synthesize Style B brief        | Task 8             |
| §4 Markdown → styled HTML             | Task 9             |
| §4 Publish to GitHub Pages            | Tasks 10, 15       |
| §4 Weekly cron via GitHub Actions     | Task 13            |
| §5 No email/Slack push                | (not built — OUT)  |
| §5 No Streamlit / backend             | (not built — OUT)  |
| §6 6-step pipeline diagram            | Task 11 main.py    |
| §7 AI roles (2 Gemini calls)          | Tasks 7, 8         |
| §8 Tech stack                          | Tasks 1, 9         |
| §9 Setup (Python, key, install)        | Tasks 1, 12        |
| §10 Build sequence                     | All tasks          |
| §11 Definition of done — repo         | Tasks 14, 15       |
| §11 Definition of done — HTML page    | Tasks 12, 15       |
| §11 Definition of done — cron ran     | Task 15            |
| §11 Sample committed in samples/      | Task 12            |

All spec requirements have at least one task implementing them.

**Placeholder scan:** No "TBD", "fill in details", "similar to Task N", or "add error handling" phrases found. Every step has actual code or commands.

**Type consistency:** `compute_diff`, `classify`, `synthesize`, `publish_brief`, `render_brief_html`, `render_index_html` — names used consistently across plan. Pydantic models referenced consistently.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-22-competitive-intel-build.md`. Two execution options:

1. **Subagent-Driven (recommended)** — fresh subagent per task, spec-compliance + code-quality review between tasks, fast iteration with main context preserved.
2. **Inline Execution** — execute tasks in this session, batch with checkpoints for review.

Which approach?
