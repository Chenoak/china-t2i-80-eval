#!/usr/bin/env python3
"""Summarize completed result slots by candidate and terminal status."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slots", type=Path, nargs="?", default=Path("data/results/slots.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/slot_summary.csv"))
    args = parser.parse_args()
    with args.slots.open(encoding="utf-8", newline="") as handle:
        counts = Counter(
            (row["candidate_id"], row["status"]) for row in csv.DictReader(handle)
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {"candidate_id": candidate_id, "status": status, "count": count}
        for (candidate_id, status), count in sorted(counts.items())
    ]
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "status", "count"])
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(f"{row['candidate_id']}\t{row['status']}\t{row['count']}")


if __name__ == "__main__":
    main()
