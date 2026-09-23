---
description: Find and safely resolve repository drift — duplicate implementations, dead flags, stale docs and tests
argument-hint: "[path]  (default: whole repository)"
---

Use the `engineering-quality` skill, loading `references/repository-reconciliation.md`, to
find repository drift in: $ARGUMENTS

Produce an inventory of suspected drift with the evidence for each item, classified
(additive / refinement / superseding / conflicting / obsolete / duplicate / experimental /
ambiguous).

Do not delete anything until you can prove it is dead. Present the inventory first.
