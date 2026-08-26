---
name: local-review-loop
description: >
  Run a local review loop on the current project: raise up to 10
  evidence-backed challenges, fix or record blockers, then repeat rounds
  until a round finds no new real challenges. Close with an inventory of
  unsolved items. Use when the user says 提出 10 個質疑, local review loop,
  不可放水, 繼續 n 輪, or runs /local-review-loop.
---

Speak in the user's language.

## Round

Scope is the current repository unless the user names a path.

Each round, hunt until you hold **10 new real challenges** or the hunt is exhausted. A challenge is real only if it cites a path or a command result from this round. Padding, restating a closed id, and style-only remarks that do not change behavior are forbidden.

Hunt coverage for every round, including the last:

- failing or missing tests for claimed behavior
- docs or README that disagree with the code
- error paths, empty input, and permission failures
- security or data-loss risk
- regressions from fixes already made this session

For each challenge: **fix in this round**, or mark **blocked** with the exact missing input or constraint. Verify every fix with a command. Do not claim fixed without that command's actual output.

Then start the next round. Closed ids stay closed. A regression is a new id that points at the old one.

## Stop

Stop after a round that produced 0 new real challenges. If a round produced 1–9, resolve those, then run one more hunt. Only 0 new real challenges ends the loop.

Do not stop because ten fixes felt like enough. Do not soften findings. Do not expand the project into a new product.

## Close

Render the unsolved inventory from `.local-review-loop/review-log.jsonl` via `python3 scripts/review-log.py render`: every item still `blocked`. Do not invent leftover issues to fill the inventory. If the file is empty of blockers, say so.

## Persist

After each challenge is fixed or blocked, append one JSONL record with `python3 scripts/review-log.py append` **before the next round**. The file is append-only. If append fails, do not start the next round.

Minimum fields: id, round, challenge, evidence, status (`fixed` | `blocked`), blocker (if blocked).
