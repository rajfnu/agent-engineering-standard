# 06 — Boundary violation

**Tests:** detecting improper dependencies.

## Setup

A repository with clear module boundaries where a recent commit introduces violations: one
module importing another's internal (non-exported-by-convention) helper, a domain class
importing a database driver type, and a new cycle between two modules.

## Prompt

> Review this branch.

## Pass

- Finds all three violations.
- States the consequence of each (what breaks, what can no longer be tested or deployed
  independently), not just "this violates layering".
- Suggests the mechanical check that would have caught it in this ecosystem.
- Does not invent violations in unchanged code.

## Fail

- Reports only the line-level defects and misses the structural ones.
- Flags legitimate cross-module use of a public contract as a violation.
- Recommends a generic architecture overhaul.

## Measure

Violations found / planted. False positives. Whether a mechanical check was proposed.
