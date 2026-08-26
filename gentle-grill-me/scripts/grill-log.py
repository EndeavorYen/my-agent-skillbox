#!/usr/bin/env python3
"""Append-only grill decision log. Run from the working directory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_REL = Path(".gentle-grill") / "grill-log.jsonl"
REQUIRED = ("id", "question", "options", "chosen", "rejected", "status")
STATUSES = frozenset({"settled", "skipped", "superseded"})


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


def _join(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(part) for part in value if part not in (None, ""))
    return str(value)


def render_records(records: list[dict]) -> str:
    buckets = {"settled": [], "skipped": [], "superseded": []}
    for rec in records:
        status = rec.get("status")
        if status in buckets:
            buckets[status].append(rec)

    lines = ["# Decision log", ""]

    def emit(title: str, items: list[dict]) -> None:
        lines.append(f"## {title}")
        if not items:
            lines.append("- (none)")
        else:
            for rec in items:
                ident = rec.get("id", "")
                question = rec.get("question", "")
                chosen = _join(rec.get("chosen"))
                rejected = _join(rec.get("rejected"))
                supersedes = _join(rec.get("supersedes"))
                head = f"- [{ident}] {question}"
                if chosen:
                    head += f" → {chosen}"
                lines.append(head)
                extras = []
                if rejected:
                    extras.append(f"rejected: {rejected}")
                if supersedes:
                    extras.append(f"supersedes: {supersedes}")
                if extras:
                    lines.append(f"  {'; '.join(extras)}")
        lines.append("")

    emit("Settled", buckets["settled"])
    emit("Deferred (skipped)", buckets["skipped"])
    emit("Superseded", buckets["superseded"])
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grill-log.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    append_p = sub.add_parser("append", help="append one JSONL record")
    append_p.add_argument("--json", dest="json_text", help="record JSON")
    append_p.add_argument("--path", help="log path (default .gentle-grill/grill-log.jsonl)")

    render_p = sub.add_parser("render", help="render the decision log from the file only")
    render_p.add_argument("--path", help="log path (default .gentle-grill/grill-log.jsonl)")
    render_p.add_argument(
        "--summary",
        help="ignored; close log is rendered from the file only",
    )

    args = parser.parse_args(argv)
    if args.cmd == "append":
        raw = args.json_text if args.json_text is not None else sys.stdin.read()
        if not raw.strip():
            raise SystemExit("append: empty record")
        append_record(load_record(raw), log_path(args.path))
        return 0
    if args.cmd == "render":
        sys.stdout.write(render_records(read_records(log_path(args.path))))
        return 0
    raise SystemExit(f"unknown command: {args.cmd}")


if __name__ == "__main__":
    sys.exit(main())
