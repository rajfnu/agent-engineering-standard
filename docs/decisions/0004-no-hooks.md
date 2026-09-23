# ADR-0004: Ship no hooks

- **Status:** Accepted
- **Date:** 2026-09-23

## Context

The Claude plugin format supports hooks that fire on events such as file writes. A hook
could, in principle, enforce parts of the standard automatically.

## Decision

Ship none.

## Rationale

- Nothing in this standard is safe to enforce on every file write. "Is this boundary
  sound?" and "is this the right test level?" require judgment and the surrounding change.
- Triggering an LLM workflow per file write is exactly the context waste the standard
  exists to prevent.
- The rules that *are* mechanically enforceable — import rules, cycles, types, lint,
  contract tests — are better enforced by the repository's own CI, where they run for
  humans too. The standard tells agents to prefer that (`engineering-quality`, "Prefer
  mechanical enforcement").
- A hook that fires often and blocks occasionally gets disabled, taking the standard with
  it.

## Consequences

- Adoption relies on the agent loading and following the Skills.
- Teams wanting hard gates should wire their own CI checks; the Skills point at the
  per-ecosystem tools for doing so.
