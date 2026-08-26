#!/usr/bin/env python3
"""Layout and independence checks for this skillbox. Run from the repository root."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
CLAUDE = ROOT / "CLAUDE.md"
SKIP_DIR_NAMES = {".git", ".agent_plan", "__pycache__", ".pytest_cache", ".venv", "tools"}
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".ps1",
    ".sh",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".mjs",
}
UNIT_HEADING = re.compile(r"(?m)^### \[([^\]]+)\]\(([^)]+)\)\s*$")


def skill_dirs() -> list[Path]:
    found: list[Path] = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_dir() or path.name in SKIP_DIR_NAMES:
            continue
        if any(path.rglob("SKILL.md")):
            found.append(path)
    return found


def heading_names(readme: str) -> list[str]:
    names: list[str] = []
    for match in UNIT_HEADING.finditer(readme):
        name, target = match.group(1), match.group(2).rstrip("/")
        if name != target:
            names.append(f"{name} -> {match.group(2)}")
        else:
            names.append(name)
    return names


def catalog_ok(readme: str, names: list[str]) -> list[str]:
    errors: list[str] = []
    headings = heading_names(readme)
    mismatched = [item for item in headings if " -> " in item]
    for item in mismatched:
        errors.append(f"README.md heading link target does not match folder name: {item}")
    heading_set = {item for item in headings if " -> " not in item}
    name_set = set(names)
    for name in names:
        if name not in heading_set:
            errors.append(f"README.md has no ### [{name}]({name}/) heading")
        if f"cd {name}" not in readme:
            errors.append(f"README.md does not install from inside {name}")
    for heading in sorted(heading_set - name_set):
        errors.append(f"README.md heading ### [{heading}]({heading}/) has no first-level SKILL.md folder")
    if "AGENTS.md" not in readme:
        errors.append("README.md does not point to AGENTS.md")
    return errors


def relative_path_hits(text: str, other: str) -> bool:
    pattern = rf"(?:^|[\\/])\.\.(?:[\\/]){re.escape(other)}(?:[\\/]|$)"
    return re.search(pattern, text) is not None


def independence_errors(dirs: list[Path]) -> list[str]:
    names = [d.name for d in dirs]
    errors: list[str] = []
    for skill in dirs:
        others = [n for n in names if n != skill.name]
        for path in skill.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            for other in others:
                if relative_path_hits(text, other):
                    errors.append(f"{rel} has a relative path into {other}")
                if f"from {other.replace('-', '_')} " in text:
                    errors.append(f"{rel} imports {other}")
    return errors


def main() -> int:
    dirs = skill_dirs()
    names = [d.name for d in dirs]
    errors: list[str] = []

    if not AGENTS.is_file():
        errors.append("AGENTS.md is missing")
    if not CLAUDE.is_file():
        errors.append("CLAUDE.md is missing")
    elif "AGENTS.md" not in CLAUDE.read_text(encoding="utf-8"):
        errors.append("CLAUDE.md does not point to AGENTS.md")
    if not README.is_file():
        errors.append("README.md is missing")
        readme = ""
    else:
        readme = README.read_text(encoding="utf-8")

    if not names:
        errors.append("no first-level folders that contain SKILL.md")
    else:
        errors.extend(catalog_ok(readme, names))
        errors.extend(independence_errors(dirs))

    print(f"skill folders: {', '.join(names) if names else '(none)'}")
    if errors:
        print("FAIL")
        for item in errors:
            print(f"- {item}")
        return 1
    print("PASS")
    print("- AGENTS.md exists")
    print("- each unit is a first-level folder that contains SKILL.md")
    print("- root README has ### [name](name/) and cd <name> for every unit")
    print("- no unit uses a relative path or import into another first-level folder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
