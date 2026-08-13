#!/usr/bin/env python3
"""Create the 80 x 3 result-slot manifest without calling model APIs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


TASK_IDS = [f"Q{index:03d}" for index in range(1, 81)]
MODEL_IDS = ["M01", "M02", "M03"]


def build_slots(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["slot_id", "task_id", "candidate_id", "status", "image_sha256"],
        )
        writer.writeheader()
        for task_id in TASK_IDS:
            for candidate_id in MODEL_IDS:
                writer.writerow(
                    {
                        "slot_id": f"{task_id}-{candidate_id}",
                        "task_id": task_id,
                        "candidate_id": candidate_id,
                        "status": "pending",
                        "image_sha256": "",
                    }
                )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/results/slots.csv"),
        help="Result-slot CSV path.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the slot count only.")
    args = parser.parse_args()
    if args.dry_run:
        print(f"{len(TASK_IDS) * len(MODEL_IDS)} slots: 80 tasks x 3 candidates")
        return
    build_slots(args.output)
    print(f"Wrote 240 pending slots to {args.output}")


if __name__ == "__main__":
    main()
