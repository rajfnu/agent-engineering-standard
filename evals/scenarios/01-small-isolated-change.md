# 01 — Small isolated change

**Tests:** minimal context, scoped tests, no unnecessary architecture work.

## Setup

Any repository with at least 200 source files and a test suite. Pick a pure utility
function with local callers only (a formatter, a validator, a parser helper).

## Prompt

> Fix the off-by-one in `<function>` in `<file>` — it drops the last element.

## Pass

- Reads the target file, its test file, and at most a couple of call sites.
- Runs only the tests for that module (L1).
- Fixes the bug and adds or extends one test.
- Produces no architecture commentary, no plan document, no refactor.

## Fail

- Reads the repository tree or `docs/` to "get oriented".
- Runs the full suite.
- Proposes restructuring the module.
- Writes a summary Markdown file nobody asked for.

## Measure

Files read (target: ≤ 5), context tokens, test level (target: L1), wall-clock.
Compare to baseline: this scenario is where the standard should *save*, not add.
