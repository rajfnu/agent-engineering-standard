# Review protocol

## Severity

Severity is about consequence if shipped, not about confidence or effort.

| Severity | Definition |
|---|---|
| **Blocker** | Data loss, security hole, broken contract for existing consumers, production outage path, or silent incorrect results. |
| **Major** | Wrong behaviour in a realistic case, missing error handling on a real failure mode, a boundary violation that will spread, or a change with no test where the behaviour matters. |
| **Minor** | Works, but will cost someone later: duplication, unclear contract, misplaced responsibility, a test asserting internals. |
| **Note** | Worth knowing, no action required. |

Do not inflate. A review where everything is Major is a review nobody reads.

## Evidence rule

Every finding needs a concrete failure scenario: **specific input or state → specific
wrong output, crash, or exposure.** If you cannot write that sentence, you have a hunch.
Either verify it — read the callers, check the test, run it — or drop it.

Things that are not findings:

- Style the repository's formatter or linter already decides.
- Preferences with no consequence ("I would have used a map here").
- Missing abstractions for a second case that does not exist (YAGNI cuts both ways).
- Repeating a finding OCR already reported, in different words.
- "Consider adding tests" with no statement of what behaviour is unprotected.

## Report format

```
## Review: <scope>

<one-line verdict: blocking findings, or none>

### Blockers
- `path/to/file.ts:142` — <what is wrong>
  Failure: <input/state → wrong result>
  Fix: <smallest change>

### Major
...

### Minor
...

### Tests
Ran: <level and command> → <result>
Gap: <behaviour changed with no covering test, if any>

### Scope
Reviewed: <capabilities/files>
Not reviewed: <what you deliberately skipped, and why>
```

Keep it as short as the change deserves. A 12-line diff does not get a page.

## Modes

**Diff review** (default) — `origin/main...HEAD`, or a PR's base. Review what changed, plus
just enough surrounding context to judge it.

**Directory scan** — auditing unfamiliar or legacy code with no meaningful diff. Use
`ocr scan --path <dir>` if available. Otherwise sample deliberately: entry points,
contracts, the largest files, and anything touching auth, money, or data migration. Say
what you sampled; do not imply full coverage you did not achieve.

**Delegated review** — `ocr delegate` gives you deterministic file selection, bundling,
and per-file rule matching while your own model does the reading. Use this when no OCR
model endpoint is configured.

**CI review** — non-interactive, JSON in and out, exit code drives the gate. See
`open-code-review.md`.

## Efficiency

- Read the diff first, files second, and only the files the diff implicates.
- Never re-read a file another step already loaded.
- Do not run L4 to review a local change — pick the level from the blast radius.
- Skip pipeline steps the scope rules out, and say you skipped them.
- If OCR ran, do not re-scan the same hunks by hand for the same class of defect.

## Self-check before reporting

- Does every finding have a failure scenario?
- Is anything here the linter's job?
- Did I check the change against the *contract*, not just the code?
- Did I state what I did not review?
- If I found nothing, did I say so plainly instead of padding?
