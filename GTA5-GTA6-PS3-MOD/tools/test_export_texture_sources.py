#!/usr/bin/env python3
"""Regression tests for deterministic RGBA8 source export."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

SCRIPT = Path(__file__).with_name("export_texture_sources.py")
SPEC = importlib.util.spec_from_file_location("export_texture_sources", SCRIPT)
exporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exporter)


class TextureSourceExportTests(unittest.TestCase):
    def test_exports_exact_rgba_bytes_and_stable_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build = root / "build"
            output = build / "texture-source"
            build.mkdir()
            png = build / "sample_hud.png"
            image = Image.new("RGBA", (2, 1))
            image.putdata([(10, 20, 30, 40), (50, 60, 70, 80)])
            image.save(png)
            registry = root / "asset-manifest.json"
            registry.write_text(json.dumps({
                "assets": [{
                    "id": "sample_hud",
                    "width": 2,
                    "height": 1
                }]
            }), encoding="utf-8")

            with patch.multiple(
                exporter,
                ROOT=root,
                BUILD=build,
                REGISTRY=registry,
                OUTPUT=output,
            ):
                exporter.main()
                raw = (output / "sample_hud.rgba").read_bytes()
                manifest_path = output / "texture-source-manifest.json"
                first_manifest = manifest_path.read_bytes()
                exporter.main()
                second_manifest = manifest_path.read_bytes()

            self.assertEqual(
                raw,
                bytes((10, 20, 30, 40, 50, 60, 70, 80)),
            )
            manifest = json.loads(first_manifest)
            entry = manifest["assets"][0]
            self.assertEqual(entry["pixel_format"], "RGBA8")
            self.assertEqual(entry["bytes"], 8)
            self.assertEqual(entry["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(first_manifest, second_manifest)

    def test_rejects_unsafe_asset_identifier(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build = root / "build"
            build.mkdir()
            registry = root / "asset-manifest.json"
            registry.write_text(json.dumps({
                "assets": [{"id": "../escape", "width": 1, "height": 1}]
            }), encoding="utf-8")
            with patch.multiple(
                exporter,
                ROOT=root,
                BUILD=build,
                REGISTRY=registry,
                OUTPUT=build / "texture-source",
            ):
                with self.assertRaises(SystemExit):
                    exporter.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
