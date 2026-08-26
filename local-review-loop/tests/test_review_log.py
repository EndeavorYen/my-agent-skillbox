#!/usr/bin/env python3
"""Tests for scripts/review-log.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "review-log.py"


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def test_append_and_render_blocked(tmp_path: Path) -> None:
    record = {
        "id": "C1",
        "round": 1,
        "challenge": "missing test",
        "evidence": "tests/foo.py",
        "status": "blocked",
        "blocker": "no fixture",
    }
    result = run(["append", json.dumps(record)], tmp_path)
    assert result.returncode == 0, result.stderr
    rendered = run(["render"], tmp_path)
    assert rendered.returncode == 0
    assert "C1" in rendered.stdout
    assert "no fixture" in rendered.stdout


def test_render_none_when_only_fixed(tmp_path: Path) -> None:
    record = {
        "id": "C1",
        "round": 1,
        "challenge": "missing test",
        "evidence": "tests/foo.py",
        "status": "fixed",
    }
    assert run(["append", json.dumps(record)], tmp_path).returncode == 0
    rendered = run(["render"], tmp_path)
    assert rendered.returncode == 0
    assert "none" in rendered.stdout.lower()
