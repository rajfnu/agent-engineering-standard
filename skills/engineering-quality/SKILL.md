---
name: engineering-quality
description: Universal engineering standard for making changes to a codebase — decide how much context to load, keep capability boundaries and dependency direction sound, reuse proven behaviour without importing technical debt, choose the right test scope, and treat frontend UX as engineering quality. Use when implementing, refactoring, extending, or reviewing a change in any language, framework, or repository, and when deciding how much of a repository to read before changing it. Do NOT use for pure Q&A about a codebase, for generating documentation with no code change, or as a substitute for running the repository's own linters, type checkers, and tests.
license: Apache-2.0
metadata:
  standard: agent-engineering-standard
  version: 0.1.1
---

# Engineering Quality

An engineering standard for coding agents. Language, framework, and agent agnostic.

## Core principle

> Preserve proven **behaviour**. Reuse proven **implementation** intelligently.
> Do not preserve unnecessary complexity or technical debt.

Existing code is evidence that some behaviour works. It is **not** evidence that the
architecture, design, tests, documentation, UX, or dependency structure are good.
Everything relevant stays reviewable.

## The loop

Run this for every change. Stop at the first step that answers the question.

1. **Scope** — name the capability being changed and the blast radius.
2. **Context** — load the smallest context that covers that scope (`references/context-economy.md`).
3. **Understand** — responsibility, public contracts, relevant tests and docs, runtime paths.
4. **Change** — smallest coherent change that leaves the boundary sound.
5. **Test** — the impacted level, not every level (`references/testing.md`).
6. **Reconcile** — leave no second live version of the thing you changed
   (`references/repository-reconciliation.md`).

Keep each step proportional. A one-line fix does not get an architecture review.

## Context economy

Context is a first-class engineering budget, not a free resource.

```
identify scope -> load global rules -> load the owning capability
               -> pull adjacent context only when a question demands it
```

Never: *small change -> read whole repo -> read all docs -> run all tests*.

Default budgets, override only with a reason:

| Change size | Files read | Test level |
|---|---|---|
| Local fix inside one module | the module + its tests | L1 |
| New behaviour in one capability | the capability + its contract + callers of the contract | L1–L2 |
| Contract or schema change | the contract + every consumer | L2–L3 |
| Cross-cutting / release | as needed | L4 |

Details: `references/context-economy.md`.

## Boundaries and dependency direction

Derive module boundaries from **coherent responsibility, ownership, independent
evolution, state ownership, explicit contract, independent testability, and blast
radius** — not from folder layout and not from a fixed module count.

A meaningful capability exposes a contract: responsibility, inputs, outputs, errors,
state ownership, allowed dependencies, compatibility expectations. Callers depend on the
contract, never on internals.

Keep domain logic away from volatile infrastructure (DB drivers, cloud SDKs, model
providers, external APIs, UI frameworks). Use a port/adapter **only where it buys real
isolation** — a wrapper that mirrors one vendor's API one-to-one buys nothing.

Details: `references/architecture.md`.

## Configuration vs. code

```
intentional variability  -> configuration
fundamental invariant    -> code / domain rule
```

Known-variable things (providers, models, endpoints, environments, flags, timeouts,
retries, concurrency, limits) should not be hard-coded. Everything else should not be
configurable.

## Code quality

Apply SRP, separation of concerns, SOLID, KISS, DRY, YAGNI, high cohesion, low coupling,
composition, explicit dependencies, testability, failure isolation, idempotency,
determinism where practical, structured logging, clean error handling — **as tools, in
proportion**. Patterns are not goals.

**Size is a smell, not a limit.** Around 300 substantive lines, ask whether the unit has
several reasons to change, or mixes orchestration with persistence, domain with
infrastructure, or configuration with execution. If it does not, leave it alone. Never
split a file to satisfy a number.

Details: `references/code-quality.md`.

## Reuse without importing debt

Before copying code from another repo or module, answer four questions:
**Do we need it? Is it clean enough? Does it belong here? What dependencies come with it?**

Do not carry over obsolete compatibility layers, dead utilities, customer-specific
assumptions, old experiments, stale prompts, generated artifacts, or unrelated docs.

## Testing

Impact-based, four levels:

| Level | Scope | When |
|---|---|---|
| L1 | affected unit / module | every change |
| L2 | affected contract / integration | contract, schema, or cross-module change |
| L3 | affected end-to-end journey | user-visible flow changed |
| L4 | full regression | release, or broad/unclear blast radius |

Do not run L4 after every edit. Test count is not a quality metric — every test must
protect a real behaviour, invariant, contract, regression, security boundary, or
architecture boundary. Details: `references/testing.md`.

## Prefer mechanical enforcement

If a tool can enforce a rule reliably, use the tool instead of repeating the rule in
prose: import/dependency rules, architecture tests, cycle detection, linting, type
checking, contract tests, schema-compatibility checks, scoped test commands.

## Security, reliability, observability

Proportional, not ceremonial: least privilege, secret management, input validation,
authz/authn boundaries, dependency risk, sensitive-data handling, secure configuration,
safe error messages, auditability. Production paths need logs, traces, metrics,
correlation IDs, latency and dependency-failure visibility. Never log secrets.
Details: `references/security-reliability.md`.

## Frontend and UX

Frontend quality is engineering quality, not disposable glue. Before visual polish ask:
**who is the user, what are they doing, where are they, what do they need to know, what
is the next obvious action?** Then review journey, information architecture, navigation,
terminology, progressive disclosure, forms, dialogs, empty states, errors, loading, and
accessibility. Then style. Details: `references/ux.md`.

## Source of truth

Never assume code, tests, README, the newest file, or the latest prompt is automatically
correct. When they disagree, inspect runtime behaviour, implementation, requirements,
ADRs, configuration, tests, and deployment; classify the disagreement (additive,
refinement, superseding, conflicting, obsolete, duplicate, experimental, ambiguous) and
resolve it. Ask the human only when consequential ambiguity genuinely remains.

## No engineering theatre

Avoid microservices everywhere, containers everywhere, interfaces everywhere, factories
everywhere, thousands of shallow tests, full-suite runs after local edits, giant prompts,
sprawling documentation, unnecessary approval gates, and planning that never becomes
implementation. If a rule does not materially improve quality, architecture, UX, safety,
maintainability, developer experience, or efficiency, drop it.

## References

Load only what the current task needs.

| File | Load when |
|---|---|
| `references/context-economy.md` | deciding what to read, or the repo is large/unfamiliar |
| `references/architecture.md` | boundaries, contracts, dependency direction, ports/adapters |
| `references/code-quality.md` | refactoring, large files, design-principle calls |
| `references/testing.md` | choosing test scope, writing or pruning tests |
| `references/security-reliability.md` | auth, secrets, external input, production paths |
| `references/ux.md` | any frontend or user-facing change |
| `references/repository-reconciliation.md` | duplicate/legacy versions, drifted docs, v1/v2/v3 |
