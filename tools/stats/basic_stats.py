#!/usr/bin/env python3
"""Basic statistics for numeric CSV columns."""
from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path


def is_number(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute basic stats for CSV.")
    parser.add_argument("csv_file", type=Path, help="Input CSV file")
    args = parser.parse_args()

    if not args.csv_file.exists():
        raise SystemExit(f"CSV file does not exist: {args.csv_file}")

    with args.csv_file.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns: dict[str, list[float]] = {field: [] for field in reader.fieldnames or []}
        for row in reader:
            for field, raw in row.items():
                if raw is None or raw == "":
                    continue
                if is_number(raw):
                    columns[field].append(float(raw))

    for field, values in columns.items():
        if not values:
            continue
        mean = statistics.mean(values)
        median = statistics.median(values)
        minimum = min(values)
        maximum = max(values)
        print(f"{field} -> count={len(values)} mean={mean:.4f} median={median:.4f} min={minimum:.4f} max={maximum:.4f}")


if __name__ == "__main__":
    main()
