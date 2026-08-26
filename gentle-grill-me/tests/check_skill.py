#!/usr/bin/env python3
"""Structural acceptance checks for gentle-grill-me. Run from repo root."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
README_PATH = ROOT / "README.md"

OPENING_TEMPLATE = (
    "I'll pressure-test this plan with you so the weak joints show up before "
    "they cost you — not to catch you out. Being examined is a common side "
    "effect; that isn't the job. Skip a question, ask a batch, or throw out "
    "my recommended answers; those are bets, not verdicts. Default is one "
    "question. Your call."
)

APPRAISAL = "If this call turns out wrong, what is the costly part?"


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


def folded(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def has_heading_table(text: str, heading: re.Pattern[str]) -> bool:
    match = heading.search(text)
    if not match:
        return False
    rest = text[match.end() :]
    next_heading = re.search(r"\n##\s", rest)
    chunk = rest[: next_heading.start()] if next_heading else rest
    return bool(re.search(r"^\|.+\|", chunk, re.M))


def contains_all(haystack: str, needles: tuple[str, ...]) -> bool:
    return all(n in haystack for n in needles)


def main() -> int:
    skill = read_text(SKILL_PATH)
    readme = read_text(README_PATH)
    fm, body = split_frontmatter(skill or "")
    skill_l = (skill or "").lower()
    body_l = body.lower()
    fm_folded = folded(fm)
    fm_l = fm_folded.lower()
    skill_folded = folded(skill or "")
    readme_text = readme or ""

    checks: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    check(
        "SKILL.md frontmatter name gentle-grill-me",
        bool(re.search(r"(?m)^name:\s*gentle-grill-me\s*$", fm)),
    )
    check("description contains gentle grill me", "gentle grill me" in fm_l)
    check("description contains /gentle-grill-me", "/gentle-grill-me" in fm)
    check(
        "description does not take over bare grill me",
        "do not use when the user only says grill me" in fm_l,
    )
    check("mechanics: design tree", "design tree" in body_l)
    check("mechanics: frontier", "frontier" in body_l)
    check("mechanics: recommended answers", "recommended answer" in body_l)
    check("mechanics: card heading ### Q", "### Q" in body)
    check("mechanics: ➡️", "➡️" in body)
    check(
        "mechanics: host question tool ask_user_question / AskUserQuestion",
        "ask_user_question" in body and "AskUserQuestion" in body,
    )
    check(
        "mechanics: options go in the question tool not transcript bullets",
        "options go in that tool" in body_l and "transcript bullets" in body_l,
    )
    check(
        "mechanics: do not leave the options list empty",
        "do not leave the options list empty" in body_l,
    )
    check(
        "mechanics: markdown list is fallback only",
        "fallback only" in body_l and "### Q" in body,
    )
    check(
        "mechanics: recommended option first marked (Recommended)",
        "recommended option first" in body_l and "(Recommended)" in body,
    )
    check(
        "mechanics: default one card/one question",
        "default" in body_l
        and ("one card" in body_l or "one question" in body_l),
    )
    check(
        "mechanics: batch at most 3",
        "batch" in body_l and "at most 3" in body_l,
    )
    check("mechanics: batch mode", "batch" in body_l and "batch mode" in body_l)
    check("mechanics: one-card mode", "one-card mode" in body_l)
    check("mechanics: persist", "persist" in body_l)
    check("mechanics: most unblock", "most unblock" in body_l)
    check(
        "mechanics: body allow/ban decision/options vs background/recap",
        "decision" in body_l
        and "option" in body_l
        and "background" in body_l
        and "recap" in body_l,
    )
    check(
        "mechanics: facts are the agent's job",
        "facts" in body_l
        and ("your job" in body_l or "agent's job" in body_l)
        and "never the user's" in body_l,
    )
    check(
        "mechanics: do not act until confirmation",
        "do not act" in body_l and "confirm" in body_l,
    )
    check("opening template present", folded(OPENING_TEMPLATE) in skill_folded)
    check("appraisal costly-part question present", APPRAISAL in (skill or ""))
    check("My bet present", "My bet" in (skill or ""))
    check(
        "premortem past-tense failed-plan present",
        "premortem" in body_l and "has already failed" in body_l,
    )
    check(
        "skip is deferred",
        "skip" in body_l and "deferred" in body_l and "not settled" in body_l,
    )
    check(
        "wording bans paraphrases and equivalents in the user's language",
        "paraphrase" in body_l
        and "equivalent" in body_l
        and "user's language" in body_l,
    )
    check(
        "wording applies to ➡️ recommended answers",
        "➡️" in body
        and "recommended answer" in body_l
        and (
            "questions and recommended answers" in body_l
            or "applies to" in body_l
        ),
    )
    check(
        "skip does not drop nodes to empty the frontier",
        "do not drop" in body_l
        and "skip" in body_l
        and "frontier" in body_l
        and "non-deferred" in body_l,
    )
    check(
        "intensity default one-card cadence",
        "cadence" in body_l
        and ("one card" in body_l or "one question" in body_l),
    )
    check("close is a decision log", "decision log" in body_l)
    check(
        "skill requires append-before-next-question",
        "grill-log.jsonl" in body_l
        and "append" in body_l
        and "before asking the next question" in body_l
        and "if append fails, do not ask the next question" in body_l,
    )
    check(
        "skill forbids same-session implement after close confirm",
        "this session must not implement" in body_l
        and "new session" in body_l
        and "reads the file first" in body_l,
    )
    check(
        "close log is rendered from the file",
        "scripts/grill-log.py" in body
        and "render" in body_l
        and "do not invent the close log from chat memory" in body_l,
    )
    check(
        "conflicts: later answer vs settled node",
        "contradict" in body_l and "settled" in body_l,
    )
    check(
        "stop a twice-rejected recommendation class",
        "twice" in body_l and "class" in body_l,
    )
    check(
        "premortem one primary cause is enough",
        "primary cause" in body_l,
    )
    check("close records superseded nodes", "superseded" in body_l)
    check(
        "partial answers settle only what was named",
        "named" in body_l and "missed homework" in body_l,
    )
    check(
        "SKILL.md does not title itself Collaborative Inquiry",
        "collaborative inquiry" not in skill_l,
    )
    check(
        "README vs-original table",
        has_heading_table(readme_text, re.compile(r"^##\s+Vs original\s*$", re.M | re.I)),
    )
    check(
        "README mapping table",
        has_heading_table(
            readme_text,
            re.compile(r"^##\s+Rule-to-citation mapping\s*$", re.M | re.I),
        ),
    )
    check(
        "README install path",
        "~/.grok/skills/gentle-grill-me/" in readme_text,
    )
    check(
        "README literature claim is a design mapping",
        "design mapping" in readme_text.lower()
        and "not an empirical study" in readme_text.lower()
        and "**psychology**" in readme_text,
    )
    check(
        "README when to call this vs grilling",
        has_heading_table(
            readme_text,
            re.compile(r"^##\s+When to call this vs grilling\s*$", re.M | re.I),
        )
        or (
            "When to call this vs grilling" in readme_text
            and "grill me" in readme_text
            and "/gentle-grill-me" in readme_text
        ),
    )
    check(
        "README does not steal grill me",
        "does not steal" in readme_text.lower()
        and "grill me" in readme_text,
    )
    check(
        "README feedback issues URL",
        "github.com/EndeavorYen/gentle-grill-me/issues" in readme_text,
    )
    check(
        "README claude skill root",
        "~/.claude/skills/gentle-grill-me/" in readme_text,
    )
    check(
        "README cursor skill root",
        "~/.cursor/skills/gentle-grill-me/" in readme_text,
    )
    check(
        "README platform table grok claude cursor",
        has_heading_table(readme_text, re.compile(r"^##\s+Install\s*$", re.M))
        and "| grok |" in readme_text
        and "| claude |" in readme_text
        and "| cursor |" in readme_text,
    )
    ps1 = read_text(ROOT / "scripts" / "install.ps1") or ""
    sh = read_text(ROOT / "scripts" / "install.sh") or ""
    check("scripts/install.ps1 exists", bool(ps1))
    check("scripts/install.sh exists", bool(sh))
    check(
        "install.ps1 platforms grok claude cursor",
        "grok" in ps1 and "claude" in ps1 and "cursor" in ps1,
    )
    check(
        "install.sh platforms grok claude cursor",
        "grok" in sh and "claude" in sh and "cursor" in sh,
    )
    check("scripts/grill-log.py exists", (ROOT / "scripts" / "grill-log.py").is_file())
    check(
        "install.ps1 copies grill-log.py",
        "grill-log.py" in ps1 and "scripts" in ps1,
    )
    check(
        "install.sh copies grill-log.py",
        "grill-log.py" in sh and "scripts" in sh,
    )
    banned = ("aal", "carrera", "ho-forge")
    public = f"{skill or ''}\n{readme_text}"
    public_l = public.lower()
    check(
        "public text has no internal codenames",
        all(token not in public_l for token in banned),
    )
    han = re.compile(r"[\u4e00-\u9fff]")
    check("SKILL.md has no Han characters", not han.search(skill or ""))
    check("README.md has no Han characters", not han.search(readme_text))

    sh_path = ROOT / "scripts" / "install.sh"
    if os.name != "nt" and sh_path.is_file():
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["HOME"] = tmp
            env["GROK_HOME"] = str(Path(tmp) / "fake-grok-home")
            proc = subprocess.run(
                ["bash", str(sh_path), "grok"],
                cwd=str(ROOT),
                env=env,
                capture_output=True,
                text=True,
            )
            dest = (
                Path(tmp)
                / "fake-grok-home"
                / "skills"
                / "gentle-grill-me"
                / "scripts"
                / "grill-log.py"
            )
            check(
                "install.sh grok copies grill-log.py",
                proc.returncode == 0 and dest.is_file(),
            )

    citation_checks = [
        ("README citation: Brehm 1966", ("Brehm", "1966")),
        ("README citation: Dillard & Shen 2005", ("Dillard", "Shen", "2005")),
        ("README citation: Ryan & Deci 2000", ("Ryan", "Deci", "2000")),
        (
            "README citation: Deci Eghrari Patrick Leone 1994",
            ("Deci", "Eghrari", "Patrick", "Leone", "1994"),
        ),
        (
            "README citation: Miller Lane Deatrick Young Potts 2007",
            ("Miller", "Lane", "Deatrick", "Young", "Potts", "2007"),
        ),
        (
            "README citation: Argyris & Schön 1974/1996",
            ("Argyris", "1974/1996"),
        ),
        ("README citation: Kluger & DeNisi 1996", ("Kluger", "DeNisi", "1996")),
        ("README citation: Klein 2007 HBR premortem", ("Klein", "2007", "HBR")),
        (
            "README citation: Mitchell Russo Pennington 1989",
            ("Mitchell", "Russo", "Pennington", "1989"),
        ),
        ("README citation: Kahneman & Klein 2009", ("Kahneman", "Klein", "2009")),
        ("README citation: Miller & Rollnick", ("Miller & Rollnick",)),
        ("README citation: Lerner & Keltner 2000", ("Lerner & Keltner, 2000",)),
        ("README citation: Lerner & Keltner 2001", ("Lerner & Keltner, 2001",)),
        ("README citation: Schwarz & Clore 1983", ("Schwarz", "Clore", "1983")),
        ("README citation: Lerner et al 2015 ATF", ("2015", "ATF")),
    ]
    for name, needles in citation_checks:
        check(name, contains_all(readme_text, needles))

    ps1_path = ROOT / "scripts" / "install.ps1"
    if os.name == "nt" and ps1_path.is_file():
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["USERPROFILE"] = tmp
            env["GROK_HOME"] = str(Path(tmp) / "fake-grok-home")
            proc = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(ps1_path),
                    "grok",
                ],
                cwd=str(ROOT),
                env=env,
                capture_output=True,
                text=True,
            )
            dest = Path(tmp) / "fake-grok-home" / "skills" / "gentle-grill-me" / "SKILL.md"
            check(
                "install.ps1 grok copies SKILL.md",
                proc.returncode == 0 and dest.is_file(),
            )

    failed = 0
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
        if not ok:
            failed += 1
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
