#!/usr/bin/env bash
set -euo pipefail

platform="${1:-all}"
case "$platform" in
  grok|claude|cursor|all) ;;
  *)
    echo "usage: $0 [grok|claude|cursor|all]" >&2
    exit 2
    ;;
esac

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
skill_src="$repo_root/SKILL.md"
readme_src="$repo_root/README.md"
helper_src="$repo_root/scripts/review-log.py"
if [[ ! -f "$skill_src" ]]; then
    echo "SKILL.md not found at $skill_src" >&2
    exit 1
fi
if [[ ! -f "$helper_src" ]]; then
    echo "scripts/review-log.py not found at $helper_src" >&2
    exit 1
fi

dest_for() {
  local name="$1"
  local home="${HOME}"
  case "$name" in
    grok)
      local root="${GROK_HOME:-$home/.grok}"
      printf '%s\n' "$root/skills/local-review-loop"
      ;;
    claude) printf '%s\n' "$home/.claude/skills/local-review-loop" ;;
    cursor) printf '%s\n' "$home/.cursor/skills/local-review-loop" ;;
    *)
      echo "Unknown platform $name" >&2
      return 1
      ;;
  esac
}

install_to() {
  local name="$1"
  local dest
  dest="$(dest_for "$name")"
  mkdir -p "$dest/scripts"
  cp "$skill_src" "$dest/SKILL.md"
  if [[ -f "$readme_src" ]]; then
    cp "$readme_src" "$dest/README.md"
  fi
  cp "$helper_src" "$dest/scripts/review-log.py"
  echo "Installed $name -> $dest"
}

if [[ "$platform" == "all" ]]; then
  for t in grok claude cursor; do
    install_to "$t"
  done
else
  install_to "$platform"
fi
