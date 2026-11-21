#!/usr/bin/env python3
"""Regression tests for the registered original UI artwork."""
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "asset-manifest.json"
VALIDATOR = Path(__file__).with_name("validate_assets.py")
SPEC = importlib.util.spec_from_file_location("validate_assets", VALIDATOR)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class CssSafetyTests(unittest.TestCase):
    def test_allows_local_fragment_references(self):
        validator.validate_css("fill: url(#local-gradient);", "test.svg", "style")

    def test_rejects_external_css_url(self):
        for css in (
            "background: url(https://example.invalid/image.png);",
            'background: url("https://example.invalid/image.png");',
            "background: url(remote-image.png);",
        ):
            with self.subTest(css=css):
                with self.assertRaises(SystemExit):
                    validator.validate_css(css, "test.svg", "style")

    def test_rejects_css_imports_case_insensitively(self):
        for css in (
            '@import url("https://example.invalid/theme.css");',
            '@IMPORT "theme.css";',
        ):
            with self.subTest(css=css):
                with self.assertRaises(SystemExit):
                    validator.validate_css(css, "test.svg", "<style>")


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
        self.assertIn("modern_hud_concept", ids)
        self.assertIn("modern_pause_menu", ids)
        for entry in self.registry["assets"]:
            with self.subTest(asset=entry["id"]):
                self.assertEqual(entry["format"], "svg")
                self.assertEqual(entry["license"], "Original project artwork")
                self.assertEqual(entry["integration"], "source_only_not_in_game")
                self.assertEqual(entry["target_update"], "1.27")
                self.assertEqual(entry["target_status"], "unverified")

    def test_registry_paths_are_unique_and_dimensions_are_bounded(self):
        paths = [entry["path"] for entry in self.registry["assets"]]
        self.assertEqual(len(paths), len(set(paths)))
        for entry in self.registry["assets"]:
            self.assertIs(type(entry["width"]), int)
            self.assertIs(type(entry["height"]), int)
            self.assertGreaterEqual(entry["width"], 1)
            self.assertGreaterEqual(entry["height"], 1)
            self.assertLessEqual(entry["width"], 8192)
            self.assertLessEqual(entry["height"], 8192)

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
