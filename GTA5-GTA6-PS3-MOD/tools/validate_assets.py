#!/usr/bin/env python3
"""Validate registered original SVG assets without executing embedded content."""
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets"
ASSET_MANIFEST = ASSET_ROOT / "asset-manifest.json"
SVG_NS = "{http://www.w3.org/2000/svg}"
FORBIDDEN_ELEMENTS = {"script", "foreignobject", "iframe", "audio", "video"}
MAX_DIMENSION = 8192
EXTERNAL_URL = re.compile(r"(?:https?:|file:|ftp:|javascript:|data:)", re.IGNORECASE)


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def validate_svg(entry: dict) -> None:
    relative = entry.get("path")
    if not isinstance(relative, str) or not relative or relative.startswith(("/", "\\")) or "\\" in relative or ".." in Path(relative).parts:
        fail(f"unsafe asset path: {relative!r}")
    if entry.get("format") != "svg":
        fail(f"unsupported asset format for {relative!r}")
    if entry.get("license") != "Original project artwork":
        fail(f"asset must be identified as original project artwork: {relative}")
    if entry.get("integration") != "source_only_not_in_game":
        fail(f"unverified asset cannot be marked as integrated: {relative}")
    if entry.get("target_update") != "1.27" or entry.get("target_status") != "unverified":
        fail(f"asset target must remain 1.27 and unverified: {relative}")

    asset_path = (ASSET_ROOT / relative).resolve()
    try:
        asset_path.relative_to(ASSET_ROOT.resolve())
    except ValueError:
        fail(f"asset path escapes assets directory: {relative}")
    if not asset_path.is_file():
        fail(f"missing asset file: {relative}")

    try:
        raw_svg = asset_path.read_bytes()
        if b"<!DOCTYPE" in raw_svg.upper() or b"<!ENTITY" in raw_svg.upper():
            fail(f"DOCTYPE/entity declarations are not allowed in {relative}")
        root = ET.fromstring(raw_svg)
    except (ET.ParseError, OSError) as exc:
        fail(f"invalid SVG XML in {relative}: {exc}")
    if root.tag != f"{SVG_NS}svg":
        fail(f"root element is not SVG: {relative}")

    width = entry.get("width")
    height = entry.get("height")
    if any(type(value) is not int or value < 1 or value > MAX_DIMENSION for value in (width, height)):
        fail(f"invalid or excessive SVG dimensions in registry: {relative}")
    if root.attrib.get("width") != str(width) or root.attrib.get("height") != str(height):
        fail(f"SVG dimensions do not match registry: {relative}")
    if root.attrib.get("viewBox") != f"0 0 {width} {height}":
        fail(f"unexpected SVG viewBox: {relative}")

    for element in root.iter():
        local = element.tag.rsplit("}", 1)[-1].lower()
        if local in FORBIDDEN_ELEMENTS:
            fail(f"active/embedded element is not allowed in {relative}: {local}")
        for attr, value in element.attrib.items():
            attr_name = attr.rsplit("}", 1)[-1].lower()
            if attr_name.startswith("on"):
                fail(f"event handler attribute is not allowed in {relative}: {attr}")
            if attr_name in {"href", "src"} and value and not value.startswith("#"):
                fail(f"non-local resource reference is not allowed in {relative}: {attr}")
            if attr_name == "style" and (EXTERNAL_URL.search(value) or re.search(r"url\\s*\\(\\s*(?![#'\"])", value, re.IGNORECASE)):
                fail(f"external CSS resource is not allowed in {relative}: {attr}")


def main() -> None:
    if not ASSET_MANIFEST.is_file():
        fail(f"missing asset manifest: {ASSET_MANIFEST}")
    try:
        registry = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"invalid asset manifest: {exc}")
    if not isinstance(registry, dict) or registry.get("schema_version") != 1:
        fail("unsupported asset manifest schema.")

    assets = registry.get("assets")
    if not isinstance(assets, list) or not assets:
        fail("asset manifest must contain at least one registered asset.")
    seen = set()
    seen_paths = set()
    for entry in assets:
        if not isinstance(entry, dict):
            fail("every asset registry entry must be an object.")
        asset_id = entry.get("id")
        if not isinstance(asset_id, str) or not re.fullmatch(r"[a-z0-9_]+", asset_id) or asset_id in seen:
            fail(f"missing, unsafe, or duplicate asset id: {asset_id!r}")
        seen.add(asset_id)
        asset_path = entry.get("path")
        if not isinstance(asset_path, str) or asset_path in seen_paths:
            fail(f"missing or duplicate asset path: {asset_path!r}")
        seen_paths.add(asset_path)
        validate_svg(entry)

    print(f"PASS: {len(assets)} registered original SVG assets validated; no active/external content found.")
    print("NOTE: Artwork is source only; it is not a PS3-native texture or installed game mod.")


if __name__ == "__main__":
    main()
