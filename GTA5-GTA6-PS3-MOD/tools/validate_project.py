#!/usr/bin/env python3
"""Validate the safe, original-content payload for the GTA V PS3 mod project.

This tool does not patch GTA V files or build a PKG. It checks that a payload
manifest is well-formed, paths stay inside the project, and listed files match
their SHA-256 hashes. Only original or properly licensed mod assets belong in
the payload directory.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "mod" / "manifest.json"
BLOCKED_SUFFIXES = {".pkg", ".rap", ".rif", ".self", ".sprx", ".edat"}
BLOCKED_NAMES = {"eboot.bin", "update.rpf", "param.sfo"}
REQUIRED_TARGET = {
    "platform": "PS3",
    "title_id": "NPEB01283",
    "region": "Europe",
    "game_update": "1.27",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_payload_path(payload_root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        fail("Each file entry needs a non-empty relative path.")
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts or "\\" in relative:
        fail(f"Unsafe payload path: {relative!r}")
    unresolved = payload_root / Path(*posix.parts)
    current = payload_root
    for part in posix.parts:
        current = current / part
        if current.is_symlink():
            fail(f"Symbolic links are not allowed in payload paths: {relative!r}")
    candidate = unresolved.resolve()
    try:
        candidate.relative_to(payload_root.resolve())
    except ValueError:
        fail(f"Payload path escapes the payload directory: {relative!r}")
    if candidate.name.lower() in BLOCKED_NAMES:
        fail(f"Game executable/archive is not distributable: {relative}")
    if candidate.suffix.lower() in BLOCKED_SUFFIXES:
        fail(f"Restricted game/package file is not accepted: {relative}")
    return candidate


def main() -> None:
    if not MANIFEST.is_file():
        fail(f"Missing manifest: {MANIFEST}")
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot read manifest: {exc}")
    if not isinstance(manifest, dict):
        fail("Manifest root must be a JSON object.")

    target = manifest.get("target")
    if not isinstance(target, dict):
        fail("Manifest target section is missing.")
    for key, expected in REQUIRED_TARGET.items():
        actual = target.get(key)
        if actual != expected:
            fail(f"Target mismatch for {key}: expected {expected!r}, got {actual!r}")
    if target.get("update_status") != "planned_unverified":
        print("WARNING: update status is not marked planned_unverified; verify hardware first.")

    policy = manifest.get("distribution_policy")
    if not isinstance(policy, dict):
        fail("Manifest distribution_policy must be an object.")
    for key in (
        "include_rockstar_game_data",
        "include_original_game_executables",
        "include_third_party_assets_without_permission",
        "include_online_cheat_or_recovery_features",
    ):
        if policy.get(key) is not False:
            fail(f"Distribution policy must keep {key}=false.")

    payload_name = manifest.get("payload_directory", "payload")
    if not isinstance(payload_name, str) or not payload_name:
        fail("Payload directory must be a non-empty relative path.")
    payload_root = (ROOT / payload_name).resolve()
    try:
        payload_root.relative_to(ROOT.resolve())
    except ValueError:
        fail("Payload directory must remain inside the project.")
    if not payload_root.exists():
        payload_root.mkdir(parents=True, exist_ok=True)

    entries = manifest.get("files")
    if not isinstance(entries, list):
        fail("Manifest 'files' must be a list.")

    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            fail("Every file entry must be an object.")
        relative = entry.get("path")
        if not isinstance(relative, str) or not relative:
            fail("Each file entry needs a non-empty string path.")
        if relative in seen:
            fail(f"Duplicate payload entry: {relative}")
        seen.add(relative)
        path = safe_payload_path(payload_root, relative)
        if not path.is_file():
            fail(f"Missing payload file: {relative}")
        expected_hash = entry.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash):
            fail(f"Missing/invalid SHA-256 for {relative}")
        actual_hash = sha256(path)
        if actual_hash.lower() != expected_hash.lower():
            fail(f"SHA-256 mismatch for {relative}: {actual_hash}")

    print("PASS: manifest structure, target declaration, distribution policy, and payload hashes are valid.")
    print("NOTE: This is a file-integrity check only; it does not prove GTA V 1.27 compatibility.")
    print("NOTE: This tool does not create an installable PS3 PKG.")


if __name__ == "__main__":
    main()
