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
