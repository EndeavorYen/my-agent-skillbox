#!/usr/bin/env python3
"""Behavior tests for scripts/grill-log.py. Run from repo root."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "grill-log.py"

RECORD = {
    "id": "q1",
    "question": "If this call turns out wrong, what is the costly part?",
    "options": ["time", "money", "reputation"],
    "chosen": ["reputation"],
    "rejected": ["time", "money"],
    "status": "settled",
    "supersedes": None,
}


def run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


class TestAppend(unittest.TestCase):
    def test_append_creates_file_and_last_line_is_the_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            prior = {
                "id": "q0",
                "question": "earlier",
                "options": ["a"],
                "chosen": ["a"],
                "rejected": [],
                "status": "skipped",
                "supersedes": None,
            }
            proc0 = run_cli(["append", "--json", json.dumps(prior)], cwd)
            self.assertEqual(proc0.returncode, 0, proc0.stderr)
            proc = run_cli(["append", "--json", json.dumps(RECORD)], cwd)
            self.assertEqual(proc.returncode, 0, proc.stderr)

            log = cwd / ".gentle-grill" / "grill-log.jsonl"
            self.assertTrue(log.is_file())
            lines = [ln for ln in log.read_text(encoding="utf-8").splitlines() if ln.strip()]
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["id"], "q0")
            self.assertEqual(json.loads(lines[-1]), RECORD)


class TestRender(unittest.TestCase):
    def test_render_uses_only_the_file_not_a_fake_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            skipped = {
                "id": "q2",
                "question": "What is the costly part?",
                "options": ["time", "money"],
                "chosen": [],
                "rejected": [],
                "status": "skipped",
                "supersedes": None,
            }
            superseded = {
                "id": "q3",
                "question": "Keep the earlier node or replace it?",
                "options": ["keep", "replace"],
                "chosen": ["replace"],
                "rejected": ["keep"],
                "status": "superseded",
                "supersedes": "q1",
            }
            self.assertEqual(run_cli(["append", "--json", json.dumps(RECORD)], cwd).returncode, 0)
            self.assertEqual(run_cli(["append", "--json", json.dumps(skipped)], cwd).returncode, 0)
            self.assertEqual(
                run_cli(["append", "--json", json.dumps(superseded)], cwd).returncode, 0
            )

            honest = run_cli(["render"], cwd)
            self.assertEqual(honest.returncode, 0, honest.stderr)
            fake = run_cli(
                ["render", "--summary", "FAKECHAT: user settled skip-everything and chose OPTION X"],
                cwd,
            )
            self.assertEqual(fake.returncode, 0, fake.stderr)
            self.assertEqual(honest.stdout, fake.stdout)
            out = honest.stdout
            self.assertNotIn("FAKECHAT", out)
            self.assertNotIn("OPTION X", out)
            self.assertIn("If this call turns out wrong, what is the costly part?", out)
            self.assertIn("reputation", out)
            self.assertIn("What is the costly part?", out)
            self.assertIn("Keep the earlier node or replace it?", out)
            self.assertIn("q1", out)


if __name__ == "__main__":
    unittest.main()
