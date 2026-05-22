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
