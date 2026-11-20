#!/usr/bin/env python3
"""Render the original HUD SVG into a transparent PNG preview.

Requires CairoSVG. This is a design preview only, not a PS3-native texture.
"""
from pathlib import Path
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "ui" / "modern_hud_concept.svg"
OUTPUT = ROOT / "build" / "modern_hud_concept.png"


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing source artwork: {SOURCE}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(
        url=str(SOURCE),
        write_to=str(OUTPUT),
        output_width=1280,
        output_height=720,
    )
    if not OUTPUT.is_file() or OUTPUT.stat().st_size < 1024:
        raise SystemExit("PNG preview was not generated correctly.")
    print(f"Rendered preview: {OUTPUT} ({OUTPUT.stat().st_size} bytes)")
    print("This PNG is a visual preview, not a PS3 game texture or PKG.")


if __name__ == "__main__":
    main()
