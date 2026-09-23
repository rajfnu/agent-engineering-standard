# Evaluation suite

Twelve scenarios that check whether the standard changes agent behaviour in the ways it
claims to. They are behavioural evals, not unit tests: each defines a situation, the
behaviour that counts as a pass, and the failure modes to watch for.

## Why these twelve

Half of them test that the agent **does** something (scope correctly, reason about
architecture, find drift). Half test that it **does not** — does not read the whole repo,
does not run 5,000 tests, does not manufacture Core/Domain/Tenant layers, does not split
files to hit a line count. Over-application is the more likely failure for a standard
written as instructions, so it is tested at least as hard as under-application.

## Running one

1. Pick a repository matching the scenario's **Setup** (your own, or a public one).
2. Start a clean session with the standard installed.
3. Give the agent the scenario's **Prompt**, verbatim, and nothing else.
4. Record the metrics below.
5. Score against **Pass** and **Fail**.
6. Re-run with the standard *uninstalled* for a baseline. The delta is the result; an
   absolute number on its own says nothing.

## Metrics

| Metric | How to capture |
|---|---|
| Context tokens | the agent's own token/usage report for the session |
| Files read | count distinct file-read tool calls |
| Tests run | count, and which level (L1–L4) |
| Wall-clock | session duration |
| False positives | findings with no real defect behind them |
| Real issues found | architecture/boundary/drift issues confirmed by a human |
| Unnecessary work | files rewritten, docs generated, refactors nobody asked for |

## Scoring

Each scenario is **pass**, **partial**, or **fail** against its criteria, with a one-line
justification. A scenario that passes while burning 4× the baseline context is a partial —
efficiency is part of the claim, not a bonus.

## Honesty rules

- Report baseline and treatment. A number without a baseline is not a result.
- Report the model and agent used; results are not transferable between them.
- Do not tune a scenario's prompt until the standard passes it. Fix the standard, or record
  the failure.
- Record scenarios you did not run as *not run*, never as pass.

Results go in `RESULTS.md`.

## Scenarios

| # | File | Tests |
|---|---|---|
| 01 | `scenarios/01-small-isolated-change.md` | minimal context, scoped tests, no ceremony |
| 02 | `scenarios/02-large-existing-service.md` | responsibility review, not line-count splitting |
| 03 | `scenarios/03-provider-change.md` | configuration and abstraction, no vendor leakage |
| 04 | `scenarios/04-legacy-repository.md` | A1/A2/A3 detection and reconciliation |
| 05 | `scenarios/05-frontend-flow.md` | UX reasoning before cosmetics |
| 06 | `scenarios/06-boundary-violation.md` | detecting improper dependencies |
| 07 | `scenarios/07-core-domain-tenant.md` | correct layer placement |
| 08 | `scenarios/08-not-core-domain-tenant.md` | **not** manufacturing those layers |
| 09 | `scenarios/09-private-capability-contract.md` | contract without source access |
| 10 | `scenarios/10-five-thousand-tests.md` | impacted tests first, not all 5,000 |
| 11 | `scenarios/11-shared-contract-change.md` | correctly broadening regression scope |
| 12 | `scenarios/12-review-pipeline.md` | review pipeline, OCR delegation, ranked report |
