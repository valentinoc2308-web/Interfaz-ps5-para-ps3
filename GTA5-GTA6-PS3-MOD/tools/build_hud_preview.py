#!/usr/bin/env python3
"""Render all registered original SVG interface assets into PNG previews.

Requires CairoSVG. Outputs are design previews only, not PS3-native textures.
"""
import json
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
        source = (ASSET_ROOT / entry["path"]).resolve()
        try:
            source.relative_to(ASSET_ROOT.resolve())
        except ValueError:
            raise SystemExit(f"Unsafe asset path in registry: {entry['path']}")
        if not source.is_file():
            raise SystemExit(f"Missing source artwork: {source}")
        output = OUTPUT_ROOT / f"{entry['id']}.png"
        cairosvg.svg2png(
            url=str(source),
            write_to=str(output),
            output_width=int(entry["width"]),
            output_height=int(entry["height"]),
        )
        if not output.is_file() or output.stat().st_size < 1024:
            raise SystemExit(f"PNG preview was not generated correctly: {output}")
        print(f"Rendered preview: {output} ({output.stat().st_size} bytes)")

    print("These PNG files are visual previews, not PS3 game textures or a PKG.")


if __name__ == "__main__":
    main()
