# 10 — Small change, 5,000 tests

**Tests:** impacted tests first, not the full suite. The headline efficiency claim.

## Setup

A repository with a large suite (thousands of tests, multi-minute runtime). Make a
one-function change with no contract impact.

## Prompt

> Change `<function>` so it returns an empty list instead of null when there are no
> results, and make sure nothing broke.

Note the prompt's "make sure nothing broke" — it invites a full run. The standard should
resist it.

## Pass

- Runs the module's tests plus tests of the direct callers (L1, arguably L2).
- Explains why that scope is sufficient: the change is internal, the contract is unchanged.
- Offers a full run as an explicit option for pre-merge, without doing it unasked.
- Notices if returning `[]` instead of `null` is in fact a contract change for callers, and
  broadens if so — that judgment is the point.

## Fail

- Runs all 5,000 tests by default.
- Runs only the single changed file's test and ignores callers.
- Claims "nothing broke" without running anything.

## Measure

Tests run vs. total. Wall-clock vs. baseline. Whether the caller analysis happened at all.
