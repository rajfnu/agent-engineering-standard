# 12 — Review pipeline

**Tests:** the `engineering-review` pipeline end to end, including OCR integration and
report discipline.

## Setup

A branch with a mixed diff: one real logic bug, one boundary violation, one missing test,
one stale document, and one purely cosmetic change. Run twice — once with `ocr` installed
and configured, once without.

## Prompt

> Review this branch.

## Pass

- Establishes scope before reading files in depth.
- **With `ocr`:** calls it for the line-level pass and does not hand-scan the same hunks
  for the same defect classes.
- **Without `ocr`:** does a bounded manual pass over changed hunks only, and says the
  line-level pass was degraded.
- Finds the boundary violation and the stale document — the things OCR does not look for.
- Every finding carries a concrete failure scenario.
- Findings ranked by consequence; the cosmetic change is not reported as a defect.
- States what was reviewed, what was not, which tests ran, and their result.

## Fail

- Reports formatter-governed style as findings.
- Duplicates OCR findings in its own words.
- Ranks by ease of fix rather than consequence.
- Reads the whole repository.
- Pads a clean area with speculative findings.

## Measure

Planted issues found / 5. False positives. Context tokens with vs. without OCR — the token
delta is the clearest evidence for ADR-0002.
