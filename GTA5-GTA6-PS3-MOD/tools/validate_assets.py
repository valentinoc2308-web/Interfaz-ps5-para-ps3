#!/usr/bin/env python3
"""Validate original SVG source assets without executing embedded content."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "ui" / "modern_hud_concept.svg"
SVG_NS = "{http://www.w3.org/2000/svg}"


def main() -> None:
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

    print("PASS: original HUD SVG is valid, 1280x720, and contains no active/external content.")
    print("NOTE: SVG is source artwork only; it is not a PS3-native texture or installed game mod.")


if __name__ == "__main__":
    main()
