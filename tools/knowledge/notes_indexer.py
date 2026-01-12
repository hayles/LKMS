#!/usr/bin/env python3
"""Notes indexer.

Scan markdown files in a directory and build a lightweight index.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def extract_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build_index(root: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for path in sorted(root.rglob("*.md")):
        if path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = extract_title(text, path.stem)
        entries.append(
            {
                "title": title,
                "path": str(path.relative_to(root)),
            }
        )
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a markdown notes index.")
    parser.add_argument("root", type=Path, help="Root directory containing notes")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("notes_index.json"),
        help="Output JSON file path (default: notes_index.json)",
    )
    args = parser.parse_args()

    if not args.root.exists():
        raise SystemExit(f"Root path does not exist: {args.root}")

    index = build_index(args.root)
    args.output.write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Indexed {len(index)} notes -> {args.output}")


if __name__ == "__main__":
    main()
