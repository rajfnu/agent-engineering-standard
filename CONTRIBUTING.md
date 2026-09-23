# Contributing

Thanks for considering a contribution. This project is small on purpose, and the main way
to help it is to keep it that way while making it more accurate.

## The bar

Every change must pass the project's own six constraints:

1. **Agent agnostic** — no instruction only one agent can follow.
2. **Stack agnostic** — no language, framework, or build tool assumed.
3. **Repository agnostic** — works on a new repo and a 15-year-old monolith.
4. **Progressive** — detail goes in `references/`, not `SKILL.md`.
5. **Non-duplicating** — if a mature open-source tool does it, integrate instead.
6. **Consequential** — if it does not materially improve quality, architecture, UX, safety,
   maintainability, developer experience, or efficiency, it does not ship.

Concretely:

| Adding | Must include |
|---|---|
| A rule | The failure it prevents, stated as a concrete scenario |
| A reference file | The task that needs it, and a link from the owning `SKILL.md` |
| A skill | Why none of the existing three can hold it |
| An integration | Licence, verified install command, and how things degrade without it |
| An eval scenario | Pass criteria, fail criteria, and what to measure |

The most valuable contributions are usually **deletions** and **eval results**.

## What we will decline

- Language- or framework-specific guidance ("in React, …"). Put it in your own skill.
- Restating a rule that already exists elsewhere in the repository.
- Growing a `SKILL.md` past its budget. Move the detail to `references/`.
- Vague descriptions. Skill discovery depends entirely on description quality.
- New rules with no failure behind them.
- Vendoring third-party code or text.

## Before opening a PR

```bash
python3 tools/validate_skills.py skills        # structure, budgets, descriptions, links
python3 tools/validate_repo.py                 # versions, manifests, links, measurements
python3 tools/measure_context.py skills --write  # refresh the published tables
```

All three run in CI (the third as a staleness check). If your change alters skill sizes,
`--write` updates the measurement tables in `README.md`, `docs/architecture.md`, and
`evals/RESULTS.md` for you — commit the result. Prose that quotes a number from those
tables is not updated automatically; check it by hand.

## Skill writing guide

**Front matter.** `name` matches the directory. `description` says what the skill does,
when to use it, and **when not to** — that last clause is what stops a conditional skill
from being loaded unconditionally. Minimum 120 characters; CI checks it.

**`SKILL.md`.** Under 200 lines, CI-enforced. Self-contained: an agent that cannot read
files on demand should still get correct guidance from it alone. End with a table routing
to `references/`, with a "load when" column.

**References.** One concern per file. Written for an agent that has already loaded
`SKILL.md` — do not re-establish context. Concrete over abstract: tables, commands,
examples, anti-patterns. Cross-skill links use the full path
(`engineering-quality/references/testing.md`); CI checks they resolve.

**Tone.** Direct. Prefer "do X" to "consider possibly doing X". Say when a rule does not
apply — that is what keeps it from being applied everywhere.

## Eval results

The most useful PR is a filled-in scenario result, positive or negative. Template in
[`evals/RESULTS.md`](evals/RESULTS.md). Always include the baseline run with the standard
uninstalled — a number without a baseline is not a result. Negative results are published
as-is; a scenario the standard fails is a bug in the standard.

## Commits and PRs

Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`). One concern per PR. In the
description, say what failure the change prevents.

## Licence

Contributions are licensed under Apache-2.0. By opening a PR you confirm the content is
your original work and that you have the right to contribute it under that licence.
