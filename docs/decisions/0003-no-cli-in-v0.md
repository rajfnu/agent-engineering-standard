# ADR-0003: No `aes` CLI in v0.1

- **Status:** Accepted
- **Date:** 2026-09-23

## Context

A CLI (`aes scope`, `aes context`, `aes test`, `aes review`, `aes reconcile`, `aes check`)
would make scope resolution, test-impact mapping, and architecture checks deterministic
and machine-readable.

## Decision

Do not ship one in v0.1. Ship deterministic shell recipes inside the Skills instead, plus
two dependency-free Python scripts used only for this repository's own CI.

## Rationale

- **Most capabilities already exist.** Changed-file detection is `git diff --name-only`.
  Dependency analysis belongs to `dependency-cruiser`, `import-linter`, ArchUnit,
  NetArchTest, `depguard`. Test impact belongs to the repo's runner and to nx/turbo/bazel
  affected graphs. Review belongs to `ocr`.
- **A CLI is a distribution tax.** It needs a runtime, a package registry, releases, and
  cross-platform support, in a project whose value is instructions.
- **It would need to be language-aware to be useful**, which contradicts stack agnosticism —
  or it would shell out to the tools above, which the agent can do directly.
- Meaningful deterministic value would need repository-specific knowledge, which is the
  optional capability manifest (ADR-0005), not a CLI.

## Consequences

- Scope and test selection stay heuristic unless a repository adopts its own tooling.
- Revisit if evals show agents repeatedly mis-scoping in ways a deterministic tool would
  fix, or if the capability-manifest format gets real adoption.
