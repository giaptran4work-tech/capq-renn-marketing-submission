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
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv

from .classify import classify
from .diff import compute_diff
from .fetch import fetch_all
from .models import DiffChunk, FetchResult, Surface
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


def collect_diffs(fetched: list[FetchResult], save: bool):
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
