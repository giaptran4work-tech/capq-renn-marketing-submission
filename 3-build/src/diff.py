"""Paragraph-level diffing of extracted competitor content."""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Optional

from .models import DiffChunk, Surface

MAX_CHUNK_CHARS = 1500
MIN_BLOCK_CHARS = 15


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
