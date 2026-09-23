# ADR-0005: Capability metadata is optional and unenforced

- **Status:** Accepted
- **Date:** 2026-09-23

## Context

A per-capability manifest (`owns`, `docs`, `contracts`, `tests`, `allowed_dependencies`)
would turn scope, context, and test-impact resolution into a lookup instead of a search.
It could also be required, giving the standard a deterministic backbone.

## Decision

Document the format in `docs/capability-metadata.md` as an optional adoption for large
repositories. Do not require it, do not validate it here, and do not make any Skill depend
on its presence.

## Rationale

- Requiring it would break "works on a new repo and on a 15-year-old monolith". Most
  repositories would never write it.
- An unmaintained manifest is actively harmful: agents would trust stale ownership, stale
  test paths, and stale dependency rules.
- The shell recipes in `context-economy.md` get most of the benefit at zero adoption cost.

## Consequences

- Scope resolution stays heuristic by default.
- Repositories that do adopt it must generate their dependency rules into a real import
  linter, so CI fails when code and manifest disagree. The document says so explicitly.
