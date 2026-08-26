#!/usr/bin/env python3
"""Append-only local review-loop log. Run from the working directory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_REL = Path(".local-review-loop") / "review-log.jsonl"
REQUIRED = ("id", "round", "challenge", "evidence", "status")
STATUSES = frozenset({"fixed", "blocked"})


def log_path(explicit: str | None) -> Path:
    return Path(explicit) if explicit else Path.cwd() / DEFAULT_REL


def load_record(raw: str) -> dict:
    try:
        record = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"append: invalid JSON: {exc}") from exc
    if not isinstance(record, dict):
        raise SystemExit("append: record must be a JSON object")
    missing = [key for key in REQUIRED if key not in record]
    if missing:
        raise SystemExit(f"append: missing fields: {', '.join(missing)}")
    if record["status"] not in STATUSES:
        raise SystemExit(
            f"append: status must be one of {', '.join(sorted(STATUSES))}"
        )
    if record["status"] == "blocked" and not record.get("blocker"):
        raise SystemExit("append: blocked records need blocker")
    return record


def append_record(record: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    try:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError as exc:
        raise SystemExit(f"append: failed to write {path}: {exc}") from exc


def read_records(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    records: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"render: failed to read {path}: {exc}") from exc
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"render: bad JSON on line {lineno}: {exc}") from exc
        if isinstance(item, dict):
            records.append(item)
    return records


def render_records(records: list[dict]) -> str:
    blocked = [rec for rec in records if rec.get("status") == "blocked"]
    if not blocked:
        return "Unsolved inventory: none."
    lines = ["Unsolved inventory:"]
    for rec in blocked:
        ident = rec.get("id", "?")
        challenge = rec.get("challenge", "")
        blocker = rec.get("blocker", "")
        lines.append(f"- {ident}: {challenge} | blocker: {blocker}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="review-log.py")
    parser.add_argument("--path", default=None)
    sub = parser.add_subparsers(dest="cmd", required=True)
    append_p = sub.add_parser("append")
    append_p.add_argument("record")
    sub.add_parser("render")
    args = parser.parse_args(argv)
    path = log_path(args.path)
    if args.cmd == "append":
        append_record(load_record(args.record), path)
        return 0
    print(render_records(read_records(path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
