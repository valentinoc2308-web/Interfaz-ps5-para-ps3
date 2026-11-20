#!/usr/bin/env python3
"""Regression tests for the fail-closed GTA V PS3 PKG release gate."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("package_release_gate.py")
SPEC = importlib.util.spec_from_file_location("package_release_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.integration = self.root / "integration"
        self.integration.mkdir()
        self.payload = self.integration / "PKGFILES"
        self.payload.mkdir()
        (self.integration / "Makefile").write_text("pkg:\n\t@echo package\n", encoding="utf-8")
        self.compatibility = {
            "platform": "PS3",
            "title_id": "NPEB01283",
            "region": "Europe",
            "game_update": "1.27",
            "hardware_test": "passed",
            "native_resource_roundtrip": "passed",
            "rollback_test": "passed",
        }
        (self.integration / "COMPATIBILITY.json").write_text(
            json.dumps(self.compatibility), encoding="utf-8"
        )
        self.patchers = [
            patch.object(gate, "ROOT", self.root),
            patch.object(gate, "INTEGRATION", self.integration),
            patch.object(gate, "REQUIRED", (
                self.integration / "Makefile",
                self.integration / "COMPATIBILITY.json",
                self.payload,
            )),
        ]
        for p in self.patchers:
            p.start()

    def tearDown(self):
        for p in reversed(self.patchers):
            p.stop()
        self.temp.cleanup()

    def run_gate(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                gate.main()
            except SystemExit as exc:
                return exc.code, stdout.getvalue(), stderr.getvalue()
        return 0, stdout.getvalue(), stderr.getvalue()

    def test_empty_payload_is_blocked(self):
        code, _, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("contains no installable", err)

    def test_original_payload_and_verified_metadata_pass(self):
        (self.payload / "custom_hud.dat").write_text("original asset", encoding="utf-8")
        code, out, _ = self.run_gate()
        self.assertEqual(code, 0)
        self.assertIn("1 original/licensed payload files", out)

    def test_wrong_title_id_is_blocked(self):
        self.compatibility["title_id"] = "OTHER"
        (self.integration / "COMPATIBILITY.json").write_text(
            json.dumps(self.compatibility), encoding="utf-8"
        )
        (self.payload / "custom_hud.dat").write_text("asset", encoding="utf-8")
        code, _, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("title_id must be", err)

    def test_unverified_hardware_test_is_blocked(self):
        self.compatibility["hardware_test"] = "not_tested"
        (self.integration / "COMPATIBILITY.json").write_text(
            json.dumps(self.compatibility), encoding="utf-8"
        )
        (self.payload / "custom_hud.dat").write_text("asset", encoding="utf-8")
        code, _, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("hardware_test must be", err)

    def test_retail_archive_is_blocked(self):
        (self.payload / "update.rpf").write_text("not allowed", encoding="utf-8")
        code, _, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("forbidden", err)

    def test_symlink_is_blocked(self):
        outside = self.root / "outside.dat"
        outside.write_text("outside", encoding="utf-8")
        (self.payload / "linked.dat").symlink_to(outside)
        code, _, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("symlinks are not allowed", err)

    def test_missing_pkg_target_is_blocked(self):
        (self.integration / "Makefile").write_text("all:\n\t@echo no package\n", encoding="utf-8")
        (self.payload / "custom_hud.dat").write_text("asset", encoding="utf-8")
        code, _, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("must define a pkg target", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
