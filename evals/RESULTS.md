# Evaluation results

## Status

**Behavioural scenarios 01–12: not run.**

They are specified in `scenarios/` and reproducible by anyone, but they have not been
executed against a model on real repositories. Publishing unverified pass marks would
break the project's own rule against unverifiable claims, so nothing is claimed for them.

What *has* been measured is the context cost of the Skills themselves, below. That is a
property of this repository and is reproducible with one command.

## Measured: context cost

```bash
python3 tools/measure_context.py skills --markdown
```

Estimated tokens (characters ÷ 4 — an approximation, not a tokenizer), as of v0.1.0:

<!-- MEASUREMENTS:START -->
| skill | L0 metadata | L1 SKILL.md | L2 all refs | refs | largest ref |
|---|---|---|---|---|---|
| `core-domain-tenant` | ~186 | ~1040 | ~1518 | 2 | ~789 |
| `engineering-quality` | ~194 | ~2016 | ~5400 | 7 | ~944 |
| `engineering-review` | ~189 | ~1570 | ~2571 | 3 | ~1042 |
| **all** | **~569** | **~4626** | **~9489** | 12 | |
<!-- MEASUREMENTS:END -->

### Reading the table

| Level | Content | Loaded |
|---|---|---|
| L0 | front matter of all three skills | always, for discovery |
| L1 | one `SKILL.md` | when that skill is invoked |
| L2 | one `references/` file | when the task hits that concern |

A typical task pays **L0 for all three skills + L1 for one skill + one L2 file**. Loading the
entire standard — every skill and every reference — costs roughly 3× that, which is what a
single-large-prompt design would pay on every request.

The ratio is the design working. The absolute number is small enough not to matter much;
the point is that it does not grow with the parts of the standard a task does not use.

### Cross-checked against a real tokenizer

`chars/4` is a portable approximation, so it was checked against Claude Code's own estimator
on the installed plugin (`claude plugin details agent-engineering-standard`):

| | this tool (`chars/4`) | Claude Code estimator |
|---|---|---|
| always-on (all components) | ~569 | ~817 |
| `engineering-quality` on-invoke | ~2,016 | ~2,500 |
| `engineering-review` on-invoke | ~1,570 | ~1,900 |
| `core-domain-tenant` on-invoke | ~1,040 | ~1,200 |

`chars/4` under-reads by roughly 25–45%. It is kept as the CI check because it is
agent-agnostic and needs nothing installed — but it is a **lower bound**, not a measurement,
and the tables above should be read that way.

### What this does not show

It does not show that the Skills change agent behaviour, reduce *task* context, or improve
code. Those are scenarios 01–12, and they are unrun. A cheap standard that does not work is
not an achievement.

## Enforced budgets

`tools/validate_skills.py` runs in CI and fails on:

- a `SKILL.md` over 200 lines (progressive-disclosure budget),
- a `description` under 120 characters or that never says when **not** to use the skill,
- an orphaned reference file, or a dangling reference link,
- a skill `name` that does not match its directory.

Current: 3 skills, 0 errors, 0 warnings.

## Contributing results

Run a scenario, fill in this template, and open a PR:

```markdown
### Scenario NN — <name>
- Agent / model:
- Repository:
- Baseline (standard not installed): files read, tokens, tests run, outcome
- Treatment (standard installed):    files read, tokens, tests run, outcome
- Verdict: pass / partial / fail
- Notes:
```

Negative results are as welcome as positive ones and will be published as-is. A scenario
the standard fails is a bug in the standard.
