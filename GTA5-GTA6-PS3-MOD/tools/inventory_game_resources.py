#!/usr/bin/env python3
"""Inventory extracted GTA V PS3 UI/texture archive candidates without modifying them.

This records file paths, sizes and optional SHA-256 hashes only. It does not
open, decrypt, extract, patch, or redistribute game data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

CANDIDATE_SUFFIXES = {".rpf", ".ctd", ".gfx"}
CANDIDATE_NAMES = {"hudcolor.dat", "update.rpf", "common.rpf", "scaleform_generic.rpf"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_candidate(path: Path) -> bool:
    return path.name.lower() in CANDIDATE_NAMES or path.suffix.lower() in CANDIDATE_SUFFIXES


def inventory(root: Path, include_hashes: bool = True) -> list[dict]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"Input path is not a directory: {root}")

    records = []
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(
            name for name in dirs
            if not (current_path / name).is_symlink()
        )
        for name in sorted(files):
            path = current_path / name
            if path.is_symlink() or not is_candidate(path):
                continue
            try:
                stat = path.stat()
                record = {
                    "path": path.relative_to(root).as_posix(),
                    "size_bytes": stat.st_size,
                    "extension": path.suffix.lower(),
                }
                if include_hashes:
                    record["sha256"] = sha256_file(path)
                records.append(record)
            except OSError as exc:
                records.append({
                    "path": path.relative_to(root).as_posix(),
                    "error": str(exc),
                })
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extracted_root", type=Path, help="Folder containing a user-owned, already-extracted game/update copy")
    parser.add_argument("-o", "--output", type=Path, help="Write JSON report here (default: stdout)")
    parser.add_argument("--no-hashes", action="store_true", help="Skip SHA-256 for faster scans of large archives")
    args = parser.parse_args()

    try:
        records = inventory(args.extracted_root, include_hashes=not args.no_hashes)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    report = {
        "project_target": {
            "platform": "PS3",
            "title_id": "NPEB01283",
            "planned_update": "1.27",
            "verification": "not_established_by_inventory",
        },
        "scan_root_name": args.extracted_root.name,
        "matched_file_count": len(records),
        "records": records,
        "limitations": [
            "Metadata inventory only; no archive contents are parsed or modified.",
            "A filename or hash does not prove title ID, update version, or compatibility.",
            "The user must confirm the source copy belongs to their own installation.",
            "Do not upload or publish copyrighted game files; share only this metadata report if appropriate.",
        ],
    }
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {len(records)} candidate entries to {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
