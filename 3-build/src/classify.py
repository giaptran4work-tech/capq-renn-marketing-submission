"""LLM call #1: classify diff chunks by change_type + significance."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from google.genai import types
from pydantic import ValidationError, TypeAdapter

from .llm import GEMINI_MODEL, get_client
from .models import Classification, DiffChunk, SignificantChange

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

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    user_payload = _build_user_payload(chunks)

    client = get_client()
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
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
