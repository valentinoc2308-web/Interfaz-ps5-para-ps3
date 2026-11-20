#!/usr/bin/env python3
"""Regression tests for the registered original UI artwork."""
import json
import subprocess
import sys
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "asset-manifest.json"
VALIDATOR = Path(__file__).with_name("validate_assets.py")


class UiAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_every_registered_svg_is_parseable_and_matches_dimensions(self):
        self.assertGreaterEqual(len(self.registry["assets"]), 1)
        for entry in self.registry["assets"]:
            with self.subTest(asset=entry["id"]):
                asset_path = ROOT / "assets" / entry["path"]
                root = ET.parse(asset_path).getroot()
                self.assertTrue(root.tag.endswith("svg"))
                self.assertEqual(root.attrib.get("width"), str(entry["width"]))
                self.assertEqual(root.attrib.get("height"), str(entry["height"]))
                self.assertEqual(
                    root.attrib.get("viewBox"),
                    f'0 0 {entry["width"]} {entry["height"]}',
                )

    def test_registry_declares_every_asset_as_original_and_unintegrated(self):
        self.assertEqual(self.registry["schema_version"], 1)
        ids = [entry["id"] for entry in self.registry["assets"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("modern_hud", ids)
        self.assertIn("modern_pause_menu", ids)
        for entry in self.registry["assets"]:
            with self.subTest(asset=entry["id"]):
                self.assertEqual(entry["format"], "svg")
                self.assertEqual(entry["license"], "Original project artwork")
                self.assertEqual(entry["integration"], "source_only_not_in_game")
                self.assertEqual(entry["target_update"], "1.27")
                self.assertEqual(entry["target_status"], "unverified")

    def test_asset_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f'PASS: {len(self.registry["assets"])}', result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
