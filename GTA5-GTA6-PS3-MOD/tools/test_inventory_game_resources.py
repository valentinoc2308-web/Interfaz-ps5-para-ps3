#!/usr/bin/env python3
"""Regression tests for inventory_game_resources.py; standard library only."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("inventory_game_resources.py")
SPEC = importlib.util.spec_from_file_location("inventory_game_resources", MODULE_PATH)
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "update.rpf").write_bytes(b"sample archive")
        (self.root / "nested").mkdir()
        (self.root / "nested" / "hudcolor.dat").write_bytes(b"colors")
        (self.root / "nested" / "scaleform.GFX").write_bytes(b"ui")
        (self.root / "readme.txt").write_text("not a candidate")

    def tearDown(self):
        self.temp.cleanup()

    def test_finds_expected_candidates_case_insensitively(self):
        found = tool.inventory(self.root)
        paths = {item["path"] for item in found}
        self.assertEqual(paths, {"update.rpf", "nested/hudcolor.dat", "nested/scaleform.GFX"})

    def test_hashes_are_sha256(self):
        found = tool.inventory(self.root)
        archive = next(item for item in found if item["path"] == "update.rpf")
        self.assertEqual(archive["sha256"], tool.sha256_file(self.root / "update.rpf"))

    def test_can_skip_hashes(self):
        found = tool.inventory(self.root, include_hashes=False)
        self.assertTrue(all("sha256" not in item for item in found))

    def test_rejects_non_directory(self):
        file_path = self.root / "update.rpf"
        with self.assertRaises(ValueError):
            tool.inventory(file_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
