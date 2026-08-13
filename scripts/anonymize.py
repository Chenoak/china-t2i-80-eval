#!/usr/bin/env python3
"""Copy images to deterministic blind IDs and emit a private blind map."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

from PIL import Image


def anonymize(source: Path, destination: Path, blind_map: Path) -> int:
    images = sorted(path for path in source.iterdir() if path.is_file())
    destination.mkdir(parents=True, exist_ok=True)
    blind_map.parent.mkdir(parents=True, exist_ok=True)
    with blind_map.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["blind_id", "source_name", "original_sha256", "blind_sha256"],
        )
        writer.writeheader()
        for position, image in enumerate(images, start=1):
            original_digest = hashlib.sha256(image.read_bytes()).hexdigest()
            blind_id = f"B{position:03d}"
            target = destination / f"{blind_id}.png"
            with Image.open(image) as opened:
                color_mode = "RGBA" if "A" in opened.getbands() else "RGB"
                opened.convert(color_mode).save(target, format="PNG", optimize=False)
            blind_digest = hashlib.sha256(target.read_bytes()).hexdigest()
            writer.writerow(
                {
                    "blind_id": blind_id,
                    "source_name": image.name,
                    "original_sha256": original_digest,
                    "blind_sha256": blind_digest,
                }
            )
    return len(images)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/raw_images"))
    parser.add_argument("--destination", type=Path, default=Path("data/blind_images"))
    parser.add_argument("--blind-map", type=Path, default=Path("data/results/blind_map.csv"))
    args = parser.parse_args()
    count = anonymize(args.source, args.destination, args.blind_map)
    print(f"Anonymized {count} images")


if __name__ == "__main__":
    main()
