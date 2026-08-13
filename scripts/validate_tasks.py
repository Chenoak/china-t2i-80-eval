#!/usr/bin/env python3
"""Validate task IDs, block counts, prompts, source IDs, and selected task hashes."""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from pathlib import Path

import yaml


EXPECTED_BLOCKS = {
    "instruction_following": 20,
    "knowledge_reasoning": 12,
    "text_rendering": 12,
    "visual_quality": 8,
    "safety_fairness": 8,
    "commercial_visual": 20,
}


def fail(message: str) -> None:
    raise SystemExit(f"task validation failed: {message}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path("protocol/tasks.yaml"))
    args = parser.parse_args()
    data = yaml.safe_load(args.path.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])

    expected_ids = [f"Q{i:03d}" for i in range(1, 81)]
    actual_ids = [task.get("task_id") for task in tasks]
    if actual_ids != expected_ids:
        fail("task IDs must be exactly Q001-Q080 in order")
    if data.get("task_count") != 80 or len(tasks) != 80:
        fail("task_count and tasks length must both equal 80")

    block_counts = Counter(task.get("primary_block") for task in tasks)
    if dict(block_counts) != EXPECTED_BLOCKS:
        fail(f"block counts differ: {dict(block_counts)}")

    source_ids: set[str] = set()
    for task in tasks:
        task_id = task["task_id"]
        if not task.get("used_prompt", "").strip():
            fail(f"{task_id} has no used_prompt")
        if not task.get("aspect_ratio"):
            fail(f"{task_id} has no aspect_ratio")
        if task_id <= "Q072":
            source_id = task.get("source_id")
            if not source_id or source_id in source_ids:
                fail(f"{task_id} has a missing or duplicate source_id")
            source_ids.add(source_id)
            digest = hashlib.sha256(task["source_prompt"].encode("utf-8")).hexdigest()
            if digest != task.get("source_prompt_sha256"):
                fail(f"{task_id} source_prompt_sha256 mismatch")
        elif task.get("source") != "original":
            fail(f"{task_id} must remain an original holdout task")

    print("PASS: 80 tasks, Q001-Q080, block counts and prompt hashes are valid")


if __name__ == "__main__":
    main()
