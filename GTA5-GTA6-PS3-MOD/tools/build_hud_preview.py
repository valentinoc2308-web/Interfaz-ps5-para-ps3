#!/usr/bin/env python3
"""Render registered original SVG interface assets into PNG previews.

Requires CairoSVG. Outputs are design previews only, not PS3-native textures.
"""
import json
import re
import struct
from pathlib import Path
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets"
REGISTRY = ASSET_ROOT / "asset-manifest.json"
OUTPUT_ROOT = ROOT / "build"


def main() -> None:
    manifest = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = manifest.get("assets", [])
    if not entries:
        raise SystemExit("No registered UI assets to render.")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        asset_id = entry.get("id", "")
        relative = entry.get("path", "")
        if not isinstance(asset_id, str) or not re.fullmatch(r"[a-z0-9_]+", asset_id):
            raise SystemExit(f"Unsafe asset id: {asset_id!r}")
        if (
            not isinstance(relative, str)
            or not relative
            or "\\" in relative
            or relative.startswith("/")
            or ".." in Path(relative).parts
        ):
            raise SystemExit(f"Unsafe asset path: {relative!r}")

        source = (ASSET_ROOT / relative).resolve()
        try:
            source.relative_to(ASSET_ROOT.resolve())
        except ValueError:
            raise SystemExit(f"Asset path escapes assets directory: {relative}")
        if not source.is_file():
            raise SystemExit(f"Missing source artwork: {source}")

        output = OUTPUT_ROOT / f"{asset_id}.png"
        cairosvg.svg2png(
            url=str(source),
            write_to=str(output),
            output_width=int(entry["width"]),
            output_height=int(entry["height"]),
        )
        if not output.is_file() or output.stat().st_size < 1024:
            raise SystemExit(f"PNG preview was not generated correctly: {output}")
        with output.open("rb") as stream:
            header = stream.read(24)
        if len(header) != 24 or header[:8] != b"\\x89PNG\\r\\n\\x1a\\n":
            raise SystemExit(f"Invalid PNG signature: {output}")
        png_width, png_height = struct.unpack(">II", header[16:24])
        if png_width != int(entry["width"]) or png_height != int(entry["height"]):
            raise SystemExit(f"Unexpected PNG dimensions for {output}: {png_width}x{png_height}")
        print(f"Rendered and verified preview: {output} ({png_width}x{png_height}, {output.stat().st_size} bytes)")

    print("These PNG files are visual previews, not PS3 game textures or a PKG.")


if __name__ == "__main__":
    main()
