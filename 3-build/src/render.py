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
    # Imported lazily to avoid a circular import (publish imports render).
    from .publish import _extract_title

    body_html = _md_to_html(brief_md)
    title = _extract_title(brief_md)
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
