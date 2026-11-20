#!/usr/bin/env python3
"""Validate original SVG source assets without executing embedded content."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets"
ASSET = ASSET_ROOT / "ui" / "modern_hud_concept.svg"
ASSET_MANIFEST = ASSET_ROOT / "asset-manifest.json"
SVG_NS = "{http://www.w3.org/2000/svg}"


def main() -> None:
    if not ASSET_MANIFEST.is_file():
        raise SystemExit(f"ERROR: missing asset manifest: {ASSET_MANIFEST}")
    try:
        import json
        registry = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"ERROR: invalid asset manifest: {exc}")
    if not isinstance(registry, dict) or registry.get("schema_version") != 1:
        raise SystemExit("ERROR: unsupported asset manifest schema.")
    assets = registry.get("assets")
    if not isinstance(assets, list) or len(assets) != 1:
        raise SystemExit("ERROR: asset manifest must contain exactly one registered original asset.")
    entry = assets[0]
    if not isinstance(entry, dict) or entry.get("id") != "modern_hud_concept":
        raise SystemExit("ERROR: HUD asset registry entry is missing or invalid.")
    if entry.get("path") != "ui/modern_hud_concept.svg" or entry.get("format") != "svg":
        raise SystemExit("ERROR: HUD asset path/format does not match the source file.")
    if entry.get("width") != 1280 or entry.get("height") != 720 or entry.get("alpha") is not True:
        raise SystemExit("ERROR: HUD registry dimensions/alpha metadata are invalid.")
    if entry.get("target_update") != "1.27" or entry.get("target_status") != "unverified":
        raise SystemExit("ERROR: asset target must remain 1.27 and unverified until tested.")
    if entry.get("license") != "Original project artwork":
        raise SystemExit("ERROR: HUD asset must be identified as original project artwork.")
    if entry.get("integration") != "source_only_not_in_game":
        raise SystemExit("ERROR: unverified asset cannot be marked as integrated.")
    if not ASSET.is_file():
        raise SystemExit(f"ERROR: missing SVG asset: {ASSET}")
    try:
        root = ET.parse(ASSET).getroot()
    except (ET.ParseError, OSError) as exc:
        raise SystemExit(f"ERROR: invalid SVG XML: {exc}")
    if root.tag != f"{SVG_NS}svg":
        raise SystemExit("ERROR: root element is not SVG.")
    if root.attrib.get("width") != "1280" or root.attrib.get("height") != "720":
        raise SystemExit("ERROR: HUD source must be 1280x720.")
    if root.attrib.get("viewBox") != "0 0 1280 720":
        raise SystemExit("ERROR: unexpected SVG viewBox.")

    forbidden = {"script", "foreignObject", "iframe", "audio", "video"}
    for element in root.iter():
        local = element.tag.rsplit("}", 1)[-1].lower()
        if local in {name.lower() for name in forbidden}:
            raise SystemExit(f"ERROR: active/embedded element is not allowed: {local}")
        for attr, value in element.attrib.items():
            attr_name = attr.rsplit("}", 1)[-1].lower()
            if attr_name.startswith("on"):
                raise SystemExit(f"ERROR: event handler attribute is not allowed: {attr}")
            if attr_name in {"href", "src"} and ("://" in value or value.startswith("data:")):
                raise SystemExit(f"ERROR: external or embedded resource is not allowed: {attr}")

    print("PASS: asset registry and original HUD SVG are valid, 1280x720, and contain no active/external content.")
    print("NOTE: SVG is source artwork only; it is not a PS3-native texture or installed game mod.")


if __name__ == "__main__":
    main()
