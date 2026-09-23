---
description: Review architecture, capability boundaries, and dependency direction for a change or directory
argument-hint: "[path | branch]  (default: current branch vs. main)"
---

Use the `engineering-quality` skill, loading `references/architecture.md`, to review the
architecture of: $ARGUMENTS

Focus on capability boundaries, contracts, dependency direction, and misplaced
responsibility. Skip line-level defect hunting — that is `/engineering-review`.

If the repository uses Core/Domain/Tenant layering, also load the `core-domain-tenant`
skill. Do not apply that model to a repository that does not already use it.
