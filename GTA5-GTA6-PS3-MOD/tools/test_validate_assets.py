#!/usr/bin/env python3
"""Regression tests for the original HUD asset validator."""
import json
import subprocess
import sys
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "assets" / "ui" / "modern_hud_concept.svg"
REGISTRY = ROOT / "assets" / "asset-manifest.json"
VALIDATOR = Path(__file__).with_name("validate_assets.py")


class HudAssetTests(unittest.TestCase):
    def test_svg_is_parseable_and_1280_by_720(self):
        root = ET.parse(SVG).getroot()
        self.assertEqual(root.attrib.get("width"), "1280")
        self.assertEqual(root.attrib.get("height"), "720")
        self.assertEqual(root.attrib.get("viewBox"), "0 0 1280 720")

    def test_registry_declares_original_source_only_artwork(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(registry["schema_version"], 1)
        self.assertEqual(len(registry["assets"]), 1)
        asset = registry["assets"][0]
        self.assertEqual(asset["license"], "Original project artwork")
        self.assertEqual(asset["integration"], "source_only_not_in_game")
        self.assertEqual(asset["target_status"], "unverified")

    def test_asset_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
