# gentle-grill-me

Same stress-test as grilling. Different manners.

This skill walks a design tree with you until nothing important is silently assumed. It still gives a recommended answer on every question. It does not treat your current choice as evidence that you are a fool.

Works as a Grok skill. The same `SKILL.md` copies onto Claude and Cursor.

The stance is designed from **psychology** — psychological reactance, autonomy support, premortem / prospective hindsight, and task-focused feedback — then mapped into executable rules. See the [rule-to-citation mapping](#rule-to-citation-mapping). That is a design mapping, not an empirical study of this skill.

## Quick start

Say one of:

- `gentle grill me`
- `/gentle-grill-me`

Then install from a clone:

```powershell
.\scripts\install.ps1 grok
```

```bash
./scripts/install.sh grok
```

Use `claude`, `cursor`, or `all` instead of `grok` to copy the same file into those tools.

## When to call this vs grilling

This skill coexists with original `grilling`. It does not steal `grill me`.

Call **gentle-grill-me** when you want a pressure test and you do not want to be treated as stupid for the option you currently hold.

Call original **grilling** when you want the relentless wording, or when you only say `grill me`.

A round looks like this — default one card, then it waits. On Grok and Claude the options are a selectable question card, not transcript bullets.

```text
### Q1 · Cost of being wrong
If this call turns out wrong, what is the costly part?
- time
- money
- reputation
- having to reverse something already said
- low-stakes — skip this
➡️ My bet: reputation. Reject if it doesn't fit.
```

Skip is allowed. Skip parks the node; it does not delete it.

## Vs original

| | Original grilling | gentle-grill-me |
| --- | --- | --- |
| Product | `grilling` / `grill-me` | `gentle-grill-me` |
| Triggers | Grill-family phrases, including bare `grill me` | `gentle grill me` and `/gentle-grill-me` only |
| Coexistence | Unchanged | Coexists; does not steal bare `grill me` |
| Mechanics | Design tree, frontier rounds, ❓ / ➡️ recommended answers, agent finds facts, no action before confirmation | Design tree, host question card with options (markdown ### Q list fallback), ➡️, default one card per round, batch opt-in at most 3, persist until one, most-unblock selection, agent finds facts, no action before confirmation |
| Stance | None | Opening, appraisal, silent calibration, wording contract on questions and recommended answers, skip as deferred, intensity as cadence only, premortem, decision-log close |
| Default cadence | Whole frontier per round | One card per round. Batch opt-in at most 3; persists until one |
| Intensity | Relentless wording allowed | Changes cadence only. Raising intensity does not restore competence-threatening wording |
| Skip | Unspecified | Explicitly deferred; stays on the frontier; listed as an open assumption at close; do not drop skipped nodes to close |
| Close | Empty frontier, then confirmation | Decision log rendered from `.gentle-grill/grill-log.jsonl` (settled, deferred, open assumptions, rejected bets), then confirmation. This session does not implement. |

## Install

One `SKILL.md` in this repository is the only protocol source. Install copies that file and `scripts/grill-log.py`; it does not create a second master.

| Platform | Skill root |
| --- | --- |
| grok | `~/.grok/skills/gentle-grill-me/` |
| claude | `~/.claude/skills/gentle-grill-me/` |
| cursor | `~/.cursor/skills/gentle-grill-me/` |

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

Manual copy (same result): create the skill-root directory for that platform and copy `SKILL.md` plus `scripts/grill-log.py` (and optionally `README.md`) into it.

If `GROK_HOME` is set, the grok target is `$GROK_HOME/skills/gentle-grill-me/` instead of `~/.grok/skills/gentle-grill-me/`.

Installing this skill does not replace original `grilling`.

## How it works

**Mechanics** are the grilling design tree. They are not paper-derived. Cadence and card shape differ from original grilling: default one card per round (host question tool with options, markdown `### Q` list fallback, `➡️`), batch at most 3 of the most-unblocking frontier, facts found without dumping leftover frontier, and no action until the user confirms shared understanding.

**Stance** is the overlay in `SKILL.md` after Mechanics: how the agent opens, appraises stakes, calibrates silently, words questions and recommended answers (meanings, paraphrases, and equivalents in the user's language), treats skip, changes intensity, runs a premortem, and closes. Stance does not drop recommended answers and does not shrink tree coverage.

Research mapping lives here, not in `SKILL.md`.

## Feedback

If a session still feels like an attack, too soft to be useful, or too easy to forget to invoke, open a GitHub issue: [https://github.com/EndeavorYen/gentle-grill-me/issues](https://github.com/EndeavorYen/gentle-grill-me/issues)

Named contacts can also send feedback directly. There is no session quota and no scorecard.

## Rule-to-citation mapping

| SKILL.md rule | Citation |
| --- | --- |
| Opening rationale; not to catch the user out; wording bans on controlling language | Brehm, 1966; Dillard & Shen, 2005 |
| Acknowledgment that being examined is a side effect | Deci, Eghrari, Patrick, & Leone, 1994; Miller, Lane, Deatrick, Young, & Potts, 2007 |
| Choice/restoration: skip, ask a batch, throw out recommended answers; default is one question | Ryan & Deci, 2000; Miller & Rollnick (E-P-E shape and autonomy only, not as therapy) |
| Critique the plan not the person; raising intensity must not restore competence-threatening wording | Kluger & DeNisi, 1996 |
| Treat the user's current choice as a live hypothesis | Argyris & Schön, 1974/1996 |
| Later answer contradicts a settled node: one frontier question, do not keep both | Argyris & Schön, 1974/1996 |
| After two rejections of the same recommendation class, stop offering that class | Ryan & Deci, 2000; Miller & Rollnick (E-P-E shape and autonomy only, not as therapy) |
| Premortem in past tense on the failed plan; 2–3 likely causes | Klein, 2007 (HBR premortem); Mitchell, Russo, & Pennington, 1989; Kahneman & Klein, 2009 |
| Silent calibration; never announce inferred emotion | Lerner & Keltner, 2000; Lerner & Keltner, 2001; Schwarz & Clore, 1983; Lerner et al., 2015 (ATF) |

## References

References used in the skill (only citations a `SKILL.md` rule uses):

- Argyris, C., & Schön, D. A. (1974). *Theory in practice: Increasing professional effectiveness*. Jossey-Bass. See also Argyris, C., & Schön, D. A. (1996). *Organizational learning II*. Addison-Wesley.
- Brehm, J. W. (1966). *A theory of psychological reactance*. Academic Press.
- Deci, E. L., Eghrari, H., Patrick, B. C., & Leone, D. R. (1994). Facilitating internalization: The self-determination theory perspective. *Journal of Personality*, 62(1), 119–142.
- Dillard, J. P., & Shen, L. (2005). On the nature of reactance and its role in persuasive health communication. *Communication Monographs*, 72(2), 144–168.
- Kahneman, D., & Klein, G. (2009). Conditions for intuitive expertise: A failure to disagree. *American Psychologist*, 64(6), 515–526.
- Klein, G. (2007). Performing a project premortem. *Harvard Business Review*, 85(9), 18–21.
- Kluger, A. N., & DeNisi, A. (1996). The effects of feedback interventions on performance: A historical review, a meta-analysis, and a preliminary feedback intervention theory. *Psychological Bulletin*, 119(2), 254–284.
- Lerner, J. S., & Keltner, D. (2000). Beyond valence: Toward a model of emotion-specific influences on judgement and choice. *Cognition and Emotion*, 14(4), 473–493.
- Lerner, J. S., & Keltner, D. (2001). Fear, anger, and risk. *Journal of Personality and Social Psychology*, 81(1), 146–159.
- Lerner, J. S., Li, Y., Valdesolo, P., & Kassam, K. S. (2015). Emotion and decision making. *Annual Review of Psychology*, 66, 799–823. Appraisal Tendency Framework (ATF) entry.
- Miller, C. H., Lane, L. T., Deatrick, L. M., Young, A. M., & Potts, K. A. (2007). Psychological reactance and promotional health messages: The effects of controlling language, lexical concreteness, and the restoration of freedom. *Human Communication Research*, 33(2), 219–240.
- Miller, W. R., & Rollnick, S. Motivational interviewing. Used only for elicit–provide–elicit (E-P-E) shape and autonomy, not as therapy.
- Mitchell, D. J., Russo, J. E., & Pennington, N. (1989). Back to the future: Temporal perspective in the explanation of events. *Journal of Behavioral Decision Making*, 2(1), 25–38.
- Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist*, 55(1), 68–78.
- Schwarz, N., & Clore, G. L. (1983). Mood, misattribution, and judgments of well-being: Informative and directive functions of affective states. *Journal of Personality and Social Psychology*, 45(3), 513–523.

## License

MIT. See [LICENSE](LICENSE).
