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
