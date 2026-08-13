#!/usr/bin/env python3
"""Validate a Judge JSON response against an absolute or pairwise schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response", type=Path, help="Judge response JSON to validate.")
    parser.add_argument(
        "--mode", choices=("absolute", "pairwise"), default="absolute"
    )
    args = parser.parse_args()
    schema_path = (
        Path(".agents/skills/judge-t2i-evals/references")
        / f"{args.mode}-output-schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = json.loads(args.response.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    print(f"Valid {args.mode} Judge response: {args.response}")


if __name__ == "__main__":
    main()
