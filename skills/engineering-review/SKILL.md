---
name: engineering-review
description: Runs a scoped engineering review of a change or directory — establishes blast radius, checks architecture and capability boundaries, delegates line-level defect detection to OpenCodeReview (`ocr`) when installed, selects the impacted test level, checks for repository drift, and reviews UX when the frontend changed, then reports findings ranked by severity. Use when asked to review a diff, branch, or pull request, before merging a substantial change, or to audit an unfamiliar directory. Do NOT use as a line-level linter substitute, for reviewing your own uncommitted scratch work mid-implementation, or when no code has changed.
license: Apache-2.0
metadata:
  standard: agent-engineering-standard
  version: 0.1.1
---

# Engineering Review

This skill **coordinates** a review. It does not reimplement line-level defect detection —
that is [OpenCodeReview](https://github.com/alibaba/open-code-review)'s job, and it does it
better than a general-purpose agent (deterministic file selection, bundling, external
positioning, ~1/9 the tokens of an agent doing the same review by hand).

What this skill adds on top is the reasoning OCR does not do: **scope, architecture,
boundaries, test impact, repository drift, and UX.**

## Pipeline

```
1  scope and change impact
2  architecture and boundary checks
3  line-level review        -> OpenCodeReview if available, else bounded manual pass
4  test impact
5  repository consistency
6  UX review                -> only if the frontend changed
7  final assessment
```

Steps 2–6 are independent. Do not let a later step re-read what an earlier step
established.

## 1. Scope

```bash
git diff --name-only origin/main...HEAD
git diff --stat      origin/main...HEAD
```

Write down, before reading any file in depth:

- the capability or capabilities touched,
- whether any **public contract** (API, schema, wire format, shared type, CLI, DB) changed,
- the blast radius: who calls this,
- whether the frontend is involved.

That determines how much of the rest of the pipeline runs. A typo fix in a comment needs
step 3 and nothing else.

## 2. Architecture and boundaries

Against the scope from step 1:

- new imports crossing a capability boundary, or reaching into another module's internals;
- domain/business logic newly depending on a volatile dependency (driver, SDK, provider,
  UI framework);
- responsibility leaking into the wrong unit (persistence in a handler, domain rules in a
  component);
- a second implementation of something that already exists;
- a contract changed without its consumers, or without a compatibility story;
- configuration hard-coded where it is known to vary; or new configuration for an
  invariant;
- if the repo runs Core/Domain/Tenant, layer violations — see the `core-domain-tenant`
  skill. Do not apply that model to repositories that do not use it.

Background: `engineering-quality/references/architecture.md`.

## 3. Line-level review

**If `ocr` is installed**, use it — do not hand-scan the diff in parallel:

```bash
ocr review --from main --to HEAD --format json --output .aes/ocr.json
```

Then read the JSON and fold its findings into your report. If the host agent should do
the reviewing itself (no OCR model configured), use delegation mode, which still gives you
OCR's deterministic file selection and rule matching:

```bash
ocr delegate preview                       # which files, which bundles
ocr delegate rule <file> [<file> ...]      # the rules that apply to those files
```

**If `ocr` is not installed**, do a bounded manual pass over the changed hunks only:
correctness, error handling, resource lifetime, concurrency, input validation, injection,
and obvious performance traps. Do not read unchanged files hunting for unrelated defects.

Setup, flags, CI wiring, and what to do with the JSON: `references/open-code-review.md`.

## 4. Test impact

Determine the level the change deserves (L1–L4), run it, and report what you ran:

| Trigger | Level |
|---|---|
| local change inside one module | L1 |
| contract/schema/cross-module change | L2 (+ L3 for crossing journeys) |
| user-visible flow changed | L1 + relevant L3 |
| release, or blast radius unclear | L4 |

Also review the tests **in** the diff: does each one protect a real behaviour, invariant,
contract, regression, or boundary? Flag tests that assert implementation details, and
behaviour changes that arrived with no test at all.

Background: `engineering-quality/references/testing.md`.

## 5. Repository consistency

Cheap checks, high value:

- Did this change leave two live versions of the same thing (old path not removed, flag
  not retired, adapter orphaned)?
- Do the documents that describe the changed behaviour still match it?
- Were stale tests left behind for removed behaviour?
- Did the change add agent-generated Markdown that will rot?

Background: `engineering-quality/references/repository-reconciliation.md`.

## 6. UX review — only if the frontend changed

Journey and information architecture first, then states (loading, empty, error), then
accessibility, then visuals. A change that only touches styles still needs the
accessibility floor checked. `references/ux-review.md`.

## 7. Final assessment

Report findings ranked most-severe first. For each: **file:line — what is wrong — the
concrete failure it causes — the smallest fix.** Then state, in two or three lines:

- what you reviewed and what you deliberately did not,
- which tests you ran and their result,
- the one thing that would most improve this change.

Rules for the report:

- Severity is about consequence, not about how much you want the change.
- No finding without a concrete failure scenario. Speculation is noise.
- Do not report style the repository's own formatter or linter already governs.
- Say plainly when the change is fine. "No blocking findings" is a valid review.

Full protocol, severity definitions, and report format: `references/review-protocol.md`.

## References

| File | Load when |
|---|---|
| `references/review-protocol.md` | running the full pipeline, or writing the report |
| `references/open-code-review.md` | installing, configuring, or wiring `ocr`, incl. CI |
| `references/ux-review.md` | the change touches the frontend |
