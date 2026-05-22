"""LLM call #2: synthesize a one-page Markdown brief from significant changes."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Iterable

from .llm import OPENROUTER_MODEL, get_client
from .models import SignificantChange

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
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    cq_context = CONTEXT_PATH.read_text(encoding="utf-8")
    user_payload = (
        f"## Run date\n{run_date.isoformat()}\n\n"
        f"## CQ context\n{cq_context}\n\n"
        f"## Significant changes (JSON)\n{_serialize_changes(changes)}\n"
    )

    client = get_client()
    resp = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload},
        ],
        max_tokens=8192,
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""
