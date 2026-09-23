# 11 — Shared contract modification

**Tests:** broadening regression scope when it is actually warranted. The counterpart to
scenario 10 — narrow scoping must not become a reflex.

## Setup

The same large repository. This time change a shared type, API schema, or wire format with
multiple consumers.

## Prompt

> Add a required `currency` field to the `Order` schema.

## Pass

- Identifies every consumer — including ones outside this repository, if any.
- Escalates to L2 for contract tests and L3 for the journeys that cross the boundary.
- Raises compatibility: required field on an existing schema breaks old clients; proposes
  optional-with-default, versioning, or a migration sequence.
- Considers stored data, not just in-flight messages.
- States explicitly that this change deserves broader testing, and why.

## Fail

- Runs only L1 because "it is a small diff".
- Misses a consumer.
- Adds a required field with no compatibility discussion.
- Jumps straight to L4 without identifying consumers — right answer, no reasoning, and it
  will not generalise.

## Measure

Consumers found / actual. Test level chosen. Whether backward compatibility was raised
before implementation.
