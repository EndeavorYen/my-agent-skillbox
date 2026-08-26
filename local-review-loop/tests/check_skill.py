#!/usr/bin/env python3
"""Structural acceptance checks for local-review-loop. Run from the skill root."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
README_PATH = ROOT / "README.md"


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    rest = text[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    match = re.search(r"\n---\s*(?:\n|$)", rest)
    if not match:
        return "", text
    return rest[: match.start()], rest[match.end() :]


def main() -> int:
    skill = read_text(SKILL_PATH) or ""
    readme = read_text(README_PATH) or ""
    fm, body = split_frontmatter(skill)
    checks: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    check("SKILL.md frontmatter name local-review-loop", bool(re.search(r"(?m)^name:\s*local-review-loop\s*$", fm)))
    check("description contains 提出 10 個質疑", "提出 10 個質疑" in fm)
    check("description contains /local-review-loop", "/local-review-loop" in fm)
    check("round hunts for 10 new real challenges", "10 new real challenges" in body)
    check("challenge needs path or command result", "path or a command result" in body)
    check("padding forbidden", "Padding" in body)
    check("fix in this round or blocked", "fix in this round" in body and "blocked" in body)
    check("verify with a command", "Verify every fix with a command" in body)
    check("stop at 0 new real challenges", "0** new real challenges" in body or "0 new real challenges" in body)
    check("do not stop because ten fixes felt like enough", "ten fixes felt like enough" in body)
    check("close from review-log.jsonl", "review-log.jsonl" in body)
    check("append before next round", "before the next round" in body)
    check("scripts/review-log.py exists", (ROOT / "scripts" / "review-log.py").is_file())
    check("scripts/install.ps1 exists", (ROOT / "scripts" / "install.ps1").is_file())
    check("scripts/install.sh exists", (ROOT / "scripts" / "install.sh").is_file())
    check("README install path", "~/.grok/skills/local-review-loop/" in readme)

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "dest"
        dest.mkdir()
        env = {**dict(**{k: v for k, v in __import__("os").environ.items()}), "USERPROFILE": str(dest), "HOME": str(dest)}
        env.pop("GROK_HOME", None)
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-File", str(ROOT / "scripts" / "install.ps1"), "grok"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env=env,
        )
        installed = dest / ".grok" / "skills" / "local-review-loop" / "SKILL.md"
        check("install.ps1 grok copies SKILL.md", proc.returncode == 0 and installed.is_file())

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
