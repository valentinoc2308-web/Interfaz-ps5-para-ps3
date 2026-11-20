#!/usr/bin/env python3
"""Fail-closed release gate for a GTA V PS3 mod package.

This deliberately refuses to create a PKG from SVG mockups or from game files.
A real release needs a native integration project, verified target metadata,
and an original/licensed payload.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "integration"
REQUIRED = (
    INTEGRATION / "Makefile",
    INTEGRATION / "COMPATIBILITY.json",
    INTEGRATION / "PKGFILES",
)
BLOCKED = {".rpf", ".rap", ".rif", ".edat", ".pkg", ".self", ".sprx"}
BLOCKED_NAMES = {"eboot.bin", "update.rpf", "param.sfo", "act.dat", "idps.bin"}


def stop(message: str) -> None:
    print(f"RELEASE BLOCKED: {message}", file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
    if missing:
        stop("native integration is not present; missing: " + ", ".join(missing))
    try:
        data = json.loads((INTEGRATION / "COMPATIBILITY.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        stop(f"invalid COMPATIBILITY.json: {exc}")
    expected = {
        "platform": "PS3",
        "title_id": "NPEB01283",
        "region": "Europe",
        "game_update": "1.27",
        "hardware_test": "passed",
        "native_resource_roundtrip": "passed",
        "rollback_test": "passed",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            stop(f"{key} must be {value!r}; found {data.get(key)!r}")
    payload = INTEGRATION / "PKGFILES"
    files = [p for p in payload.rglob("*") if p.is_file()]
    if not files:
        stop("PKGFILES contains no installable original mod resources")
    for path in files:
        if path.is_symlink():
            stop(f"symlinks are not allowed: {path}")
        if path.suffix.lower() in BLOCKED or path.name.lower() in BLOCKED_NAMES:
            stop(f"proprietary game/license/package file is forbidden: {path.relative_to(payload)}")
        resolved = path.resolve()
        if payload.resolve() not in resolved.parents:
            stop(f"payload path escapes PKGFILES: {path}")
    makefile = (INTEGRATION / "Makefile").read_text(encoding="utf-8")
    if not re.search(r"(?m)^pkg\s*:", makefile):
        stop("integration/Makefile must define a pkg target")
    print(f"PASS: {len(files)} original/licensed payload files are ready for PKG build.")
    print("Compatibility and hardware-test gates are marked passed.")


if __name__ == "__main__":
    main()
