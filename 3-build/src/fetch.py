"""Fetch competitor surfaces and extract clean text content.

Uses Playwright (headless Chromium) so that JavaScript-rendered pages render
correctly and basic bot/WAF "you're not a real browser" checks are bypassed.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Iterable

from bs4 import BeautifulSoup
from playwright.async_api import (
    Browser,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)
from readability import Document

from .models import FetchResult, Surface

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
VIEWPORT = {"width": 1280, "height": 800}
LOCALE = "en-US"
# Per-page navigation timeout (milliseconds).
PAGE_TIMEOUT_MS = 20_000


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


async def _fetch_one(browser: Browser, surface: Surface) -> FetchResult:
    now = datetime.now(timezone.utc)
    context = None
    try:
        context = await browser.new_context(
            user_agent=USER_AGENT,
            viewport=VIEWPORT,
            locale=LOCALE,
        )
        page = await context.new_page()
        response = await page.goto(
            surface.url,
            wait_until="domcontentloaded",
            timeout=PAGE_TIMEOUT_MS,
        )

        status_code = response.status if response is not None else None
        if status_code is not None and status_code >= 400:
            return FetchResult(
                surface=surface,
                fetched_at=now,
                status="fetch_failed",
                error=f"HTTP {status_code}",
            )

        html = await page.content()
        text = _extract_text(html)
        if len(text) < 100:
            return FetchResult(
                surface=surface,
                fetched_at=now,
                status="fetch_failed",
                error=f"Extracted content too short ({len(text)} chars) — likely blocked or JS-gated.",
            )
        return FetchResult(surface=surface, content_md=text, fetched_at=now)
    except PlaywrightTimeoutError as e:
        # PlaywrightTimeoutError is a subclass of PlaywrightError; handle it
        # first so timeouts get a clearer label.
        return FetchResult(
            surface=surface,
            fetched_at=now,
            status="fetch_failed",
            error=f"TimeoutError: {e}".splitlines()[0],
        )
    except PlaywrightError as e:
        # Genuine fetch/navigation failures (DNS, connection refused, nav
        # errors, etc.). Anything outside this — an AttributeError, a typo,
        # any programming bug — is NOT caught here and surfaces loudly.
        return FetchResult(
            surface=surface,
            fetched_at=now,
            status="fetch_failed",
            error=f"{type(e).__name__}: {e}".splitlines()[0],
        )
    finally:
        if context is not None:
            try:
                await context.close()
            except Exception:
                pass


async def fetch_all(surfaces: Iterable[Surface]) -> list[FetchResult]:
    """Fetch every surface with one shared headless browser.

    A fresh browser context is opened per URL (isolated cookies/storage) but
    the heavy browser process is launched only once.
    """
    surfaces = list(surfaces)
    results: list[FetchResult] = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            for surface in surfaces:
                results.append(await _fetch_one(browser, surface))
        finally:
            await browser.close()
    return results
