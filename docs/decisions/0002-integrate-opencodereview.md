# ADR-0002: Integrate OpenCodeReview rather than build a review engine

- **Status:** Accepted
- **Date:** 2026-09-23

## Context

`engineering-review` needs line-level defect detection. Building it in prose means
re-solving problems that are known to be hard for a language-only approach: complete file
coverage on large changesets, accurate line positioning, and stable output across prompt
edits.

[OpenCodeReview](https://github.com/alibaba/open-code-review) (Apache-2.0, Alibaba) solves
exactly those with deterministic engineering — file selection, semantic bundling, rule
matching, and an external positioning/reflection module — and reports higher precision and
F1 than a general-purpose agent on the same model at roughly 1/9 the tokens, with lower
recall by design.

## Decision

`engineering-review` calls `ocr` for the line-level pass and contributes what OCR does not:
scope and blast radius, architecture and boundary analysis, contract compatibility, test
level selection, repository drift, UX, and the final ranked assessment.

When `ocr` is absent, the skill degrades to a bounded manual pass over changed hunks only.

## Rationale

- Rebuilding it would be worse and would have to be maintained.
- Its delegation mode gives us deterministic file selection even with no OCR model
  configured — the part a language-only skill genuinely cannot replicate.
- Apache-2.0 is compatible with this project's licence.

## Consequences

- Full-strength review depends on an external CLI. Mitigated by the degraded path.
- We must track OCR's flags; the integration document says to verify against `ocr --help`.
- We do not vendor or copy OCR code, so no attribution obligation beyond citation. If that
  ever changes, the Apache-2.0 notice requirements apply.
