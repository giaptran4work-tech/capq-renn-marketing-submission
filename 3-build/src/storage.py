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
