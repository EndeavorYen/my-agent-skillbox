# local-review-loop

A local review loop. Each round hunts for up to 10 evidence-backed challenges, fixes them or records blockers, then repeats until a round finds no new real challenges. Close with the unsolved inventory.

Works as a Grok skill. The same `SKILL.md` copies onto Claude and Cursor.

## Quick start

Say one of:

- `提出 10 個質疑`
- `local review loop`
- `/local-review-loop`

Then install from a clone:

```powershell
.\scripts\install.ps1 grok
```

```bash
./scripts/install.sh grok
```

Use `claude`, `cursor`, or `all` instead of `grok`.

## Install

| Platform | Skill root |
| --- | --- |
| grok | `~/.grok/skills/local-review-loop/` |
| claude | `~/.claude/skills/local-review-loop/` |
| cursor | `~/.cursor/skills/local-review-loop/` |

```text
# Windows
.\scripts\install.ps1 grok
.\scripts\install.ps1 claude
.\scripts\install.ps1 cursor
.\scripts\install.ps1 all

# Unix
./scripts/install.sh grok
./scripts/install.sh claude
./scripts/install.sh cursor
./scripts/install.sh all
```

If `GROK_HOME` is set, the grok target is `$GROK_HOME/skills/local-review-loop/`.

## How it works

Each round must hunt until it holds 10 new real challenges or the hunt is exhausted. A challenge is real only with a path or command result. Padding is forbidden. Fixes run in the same round and need a verification command. The loop ends only after a round with 0 new real challenges. Close lists every still-blocked item from `.local-review-loop/review-log.jsonl`.
