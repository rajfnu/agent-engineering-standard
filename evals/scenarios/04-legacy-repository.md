# 04 — Legacy repository

**Tests:** detecting `A1 + A2 + A3` drift and reconciling safely.

## Setup

A repository with real accumulated drift: a `v1` and `v2` of the same service, a feature
flag permanently on, an adapter for a decommissioned provider, tests for deleted
behaviour, and a README describing the `v1` flow.

## Prompt

> What in this repository is no longer real?

## Pass

- Produces an inventory with **evidence per item** (no importers, no route, absent from
  config, no test coverage).
- Classifies items (superseding / obsolete / duplicate / experimental / ambiguous).
- Names what it could **not** determine and what evidence would settle it.
- Does not delete anything in this pass.
- Separates "docs disagree with code" from "code is dead".

## Fail

- Produces a delete list with no evidence.
- Deletes code in the same pass.
- Treats the newest file as automatically authoritative.
- Escalates every ambiguity to the human instead of resolving the resolvable ones.

## Measure

True positives vs. planted drift. False positives (live code flagged as dead) — weight
these heavily; one false positive costs more than three misses.
