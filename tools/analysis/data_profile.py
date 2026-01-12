#!/usr/bin/env python3
"""Generate a simple data profile report for CSV files."""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile a CSV file.")
    parser.add_argument("csv_file", type=Path, help="Input CSV file")
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Top N most common values per column (default: 5)",
    )
    args = parser.parse_args()

    if not args.csv_file.exists():
        raise SystemExit(f"CSV file does not exist: {args.csv_file}")

    with args.csv_file.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        totals = Counter()
        missing = Counter()
        samples: dict[str, Counter[str]] = {field: Counter() for field in fieldnames}

        for row in reader:
            totals["rows"] += 1
            for field in fieldnames:
                value = row.get(field, "")
                if value is None or value == "":
                    missing[field] += 1
                else:
                    samples[field][value] += 1

    print(f"Rows: {totals['rows']}")
    print(f"Columns: {len(fieldnames)}")
    for field in fieldnames:
        print(f"\n[{field}]")
        print(f"missing={missing[field]}")
        for value, count in samples[field].most_common(args.top):
            print(f"  {value}: {count}")


if __name__ == "__main__":
    main()
