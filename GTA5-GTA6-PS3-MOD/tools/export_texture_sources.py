#!/usr/bin/env python3
"""Export deterministic RGBA pixel sources for later PS3 texture conversion.

The output is an intermediate pixel buffer, NOT a CTD/CSF/GFX resource.
"""
import json
import re
import struct
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
REGISTRY = ROOT / "assets" / "asset-manifest.json"
OUTPUT = BUILD / "texture-source"


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = registry.get("assets")
    if not isinstance(entries, list) or not entries:
        raise SystemExit("No registered assets found.")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    index = []
    for entry in entries:
        asset_id = entry.get("id")
        if not isinstance(asset_id, str) or not re.fullmatch(r"[a-z0-9_]+", asset_id):
            raise SystemExit(f"Unsafe asset id: {asset_id!r}")
        width, height = entry.get("width"), entry.get("height")
        if type(width) is not int or type(height) is not int or not (1 <= width <= 8192 and 1 <= height <= 8192):
            raise SystemExit(f"Invalid dimensions for {asset_id}")
        png = BUILD / f"{asset_id}.png"
        if not png.is_file():
            raise SystemExit(f"Missing rendered PNG: {png}")
        with Image.open(png) as image:
            rgba = image.convert("RGBA")
            if rgba.size != (width, height):
                raise SystemExit(f"Unexpected dimensions for {asset_id}: {rgba.size}")
            pixels = rgba.tobytes()
        raw_path = OUTPUT / f"{asset_id}.rgba"
        raw_path.write_bytes(pixels)
        index.append({
            "id": asset_id,
            "source_png": f"{asset_id}.png",
            "raw_rgba": f"texture-source/{asset_id}.rgba",
            "width": width,
            "height": height,
            "pixel_format": "RGBA8",
            "byte_order": "R,G,B,A",
            "bytes": len(pixels),
            "sha256": __import__("hashlib").sha256(pixels).hexdigest(),
            "integration": "intermediate_only_not_a_game_resource"
        })
    (OUTPUT / "texture-source-manifest.json").write_text(
        json.dumps({"schema_version": 1, "assets": index}, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"Exported {len(index)} deterministic RGBA8 pixel buffers to {OUTPUT}")
    print("These buffers still require a verified PS3 CTD/CSF/GFX conversion and game integration.")


if __name__ == "__main__":
    main()
