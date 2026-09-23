# Working on this repository

Instructions for agents contributing to the Agent Engineering Standard itself. For the
standard's guidance on writing software generally, see `skills/`.

## What this repository is

A collection of portable Agent Skills. The product is instructions, not code. There is
more Markdown here than source, and that is correct — do not "add an implementation".

## Rules

1. **`skills/` is the single source of truth.** Adapters (`.claude-plugin/`,
   `.codex-plugin/`, `commands/`) point at it and must never contain engineering
   instructions. If you find yourself copying a rule into a command, stop.
2. **Respect the budgets.** `SKILL.md` stays under 200 lines; detail goes to
   `references/`. CI enforces this.
3. **No rule without a failure.** Every rule must name the concrete failure it prevents.
   If you cannot state it, do not add it.
4. **Do not duplicate integrated tools.** OpenCodeReview owns line-level review;
   Superpowers owns workflow methodology. See `docs/decisions/`.
5. **Stay agnostic.** No language, framework, build tool, or single agent assumed.
6. **Verify external commands** against upstream before documenting them. They change.

## Before finishing

```bash
python3 tools/validate_skills.py skills
python3 tools/validate_repo.py
```

If skill sizes changed, refresh the published measurement tables:

```bash
python3 tools/measure_context.py skills --write
```

That rewrites the tables between the `<!-- MEASUREMENTS:START -->` / `<!-- MEASUREMENTS:END -->`
markers in `README.md`, `docs/architecture.md`, and `evals/RESULTS.md`. `validate_repo.py`
fails if they are stale, so this is not optional.

## Scratch space

Working notes and OpenCodeReview output go in `.aes/` (gitignored). Do not commit
agent-generated plan or summary Markdown into the repository — that is precisely the
sediment `repository-reconciliation.md` warns about.

## Decisions

Architectural decisions live in `docs/decisions/`. If you are about to reverse one (build a
CLI, add hooks, vendor third-party code), write an ADR superseding the existing one rather
than quietly changing course.
