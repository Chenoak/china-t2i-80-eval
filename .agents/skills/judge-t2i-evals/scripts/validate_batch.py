#!/usr/bin/env python3
"""Validate the draft task manifest's fixed evaluation size."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, default=Path("protocol/tasks.yaml"))
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    manifest = yaml.safe_load(args.tasks.read_text(encoding="utf-8"))
    if manifest.get("task_count") != 80:
        raise SystemExit("task_count must equal 80")
    range_count = sum(item["task_count"] for item in manifest["public_task_ranges"])
    holdout_ids = {item["task_id"] for item in manifest["tasks"]}
    expected_holdouts = {f"Q{index:03d}" for index in range(73, 81)}
    if range_count != 72 or holdout_ids != expected_holdouts:
        raise SystemExit("expected 72 public slots and Q073-Q080 holdouts")
    if manifest.get("status") != "frozen" and not args.allow_draft:
        raise SystemExit("protocol is not frozen; pass --allow-draft for structure-only validation")
    print("Valid structure: 80 tasks x 3 candidates = 240 result slots")


if __name__ == "__main__":
    main()
