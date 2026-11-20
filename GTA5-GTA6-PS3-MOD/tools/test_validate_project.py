#!/usr/bin/env python3
"""Small regression tests for validate_project.py; uses only Python stdlib."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("validate_project.py")
SPEC = importlib.util.spec_from_file_location("validate_project", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PayloadPathTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_nested_relative_path(self):
        result = validator.safe_payload_path(self.root, "textures/custom.dds")
        self.assertEqual(result, self.root / "textures" / "custom.dds")

    def test_rejects_parent_traversal(self):
        with self.assertRaises(SystemExit):
            validator.safe_payload_path(self.root, "../outside.bin")

    def test_rejects_absolute_path(self):
        with self.assertRaises(SystemExit):
            validator.safe_payload_path(self.root, "/outside.bin")

    def test_rejects_game_executable(self):
        with self.assertRaises(SystemExit):
            validator.safe_payload_path(self.root, "EBOOT.BIN")

    def test_rejects_game_archive(self):
        with self.assertRaises(SystemExit):
            validator.safe_payload_path(self.root, "update.rpf")

    def test_rejects_package_and_license_files(self):
        for name in ("release.pkg", "license.rap", "content.rif"):
            with self.subTest(name=name):
                with self.assertRaises(SystemExit):
                    validator.safe_payload_path(self.root, name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
