# Impact-based testing

## The four levels

| Level | Scope | Typical runtime | Run when |
|---|---|---|---|
| **L1** | affected unit / module | seconds | every change |
| **L2** | affected contract / integration | seconds–minutes | contract, schema, cross-module, or IO change |
| **L3** | affected end-to-end journey | minutes | a user-visible flow changed |
| **L4** | full regression suite | long | release, risky refactor, or blast radius genuinely unclear |

Running L4 after every edit is not rigour. It is slow, expensive, and it trains everyone
to ignore the result.

## Choosing the level

```
Did a public contract, schema, wire format, or shared type change?
  yes -> L2, plus L3 for the journeys that cross it
  no  -> did behaviour visible to a user change?
           yes -> L1 + the one L3 journey that covers it
           no  -> L1
Is the blast radius genuinely unclear after scoping?
  yes -> widen one level, and say why
```

Broaden for: shared contracts, auth and permissions, data migrations, money, concurrency
primitives, and anything with a security boundary.

## Selecting the tests to run

```bash
# Files changed
git diff --name-only origin/main...HEAD

# Tests co-located with those files (most repos)
git diff --name-only origin/main...HEAD | sed 's#/[^/]*$##' | sort -u

# Many runners support path/pattern selection directly:
#   pytest <paths>            jest --findRelatedTests <files>
#   go test ./pkg/...         cargo test -p <crate>
#   mvn -pl <module> test     dotnet test <project>
#   vitest related <files>
```

If the repository already defines scoped test commands (Makefile targets, nx/turbo
affected graphs, bazel query), use those — they are more accurate than heuristics.

## What deserves a test

Every test should protect one of:

- a **behaviour** a user or caller depends on,
- an **invariant** that must hold,
- a **contract** between capabilities,
- a **regression** that actually happened,
- a **security boundary**,
- an **architecture boundary** (import rules, layering, cycles).

Test count is not a quality metric. A suite of 5,000 assertions on getters protects
nothing and slows every change.

## Tests worth deleting

- Asserting on implementation details that change with every refactor.
- Duplicates of another test at a cheaper level.
- Tests for deleted or unreachable behaviour.
- Snapshot tests nobody reads, regenerated on every failure.
- Tests that pass with the implementation commented out.

Deleting a bad test is a quality improvement. Say so in the change description.

## Test quality

Deterministic — no wall-clock, no network, no shared mutable fixture, no ordering
dependency. Named for the behaviour, not the function. One reason to fail. Fast enough
that L1 is run without thinking about it.
