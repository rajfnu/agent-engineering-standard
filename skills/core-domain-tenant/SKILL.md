---
name: core-domain-tenant
description: Placement and layering rules for multi-tenant products that genuinely have a reusable Core, a reusable Domain specialization, and customer-specific Tenant implementations — decides which layer new behaviour belongs in, keeps Core free of customer knowledge, and enforces the Tenant→Domain→Core dependency direction. Use only when the repository already has (or is deliberately building) all three layers, or when behaviour is being duplicated across customers. Do NOT use for single-tenant products, libraries, internal tools, or as a reason to invent Core/Domain/Tenant layers in a repository that does not have them.
license: Apache-2.0
metadata:
  standard: agent-engineering-standard
  version: 0.1.0
---

# Core / Domain / Tenant

**This skill is conditional. Most repositories should not use it.**

## Applicability gate

Use it only if the product genuinely has all three of:

1. a **Core** that is useful regardless of problem space or customer,
2. a **Domain** specialization reused by multiple customers solving the same kind of
   problem,
3. **Tenant** implementations for specific customers.

If the repository has one customer, one problem space, or is a library/tool/service with
no tenancy, **stop here**. Manufacturing these layers is overengineering. Use
`engineering-quality` instead.

Not sure? Ask: *do at least two tenants exist or are two credibly planned, and do they
share behaviour that is not universal?* If no, stop.

## The model

```
CORE     universal capability, no domain or customer knowledge
  ^
  |
DOMAIN   reusable specialization for one coherent problem space
  ^
  |
TENANT   one customer's implementation
```

Dependency rules, non-negotiable:

- Tenant **may** depend on Domain and Core.
- Domain **may** depend on Core.
- Core **must not** depend on Domain or Tenant.
- Domain **must not** depend on Tenant.

## Core

> If every current domain and customer disappeared tomorrow, would this still belong in
> the product?

Yes → Core. Core must not know customer names, tenant workflows, customer prompts, one-off
integrations, or domain concepts that are not genuinely universal.

Keep Core intentionally small. Premature generalisation into Core is harder to undo than
duplication in Tenant — Core changes affect everyone.

## Domain

The reusable specialization for a coherent problem space. A Domain may be an industry, a
profession, a business function, or a problem category — **do not assume it means
industry**.

A Domain may own vocabulary, business rules, workflows, prompts, skills, templates,
entities, policies, tools, artifact types, and domain UX.

> Would multiple customers solving this same kind of problem reuse this behaviour?

Yes → Domain.

## Tenant

One customer. Normally mostly configuration, integrations, mappings, branding,
customer-specific terminology, enabled capabilities, and bounded extensions.

Never put `if customer == "X"` inside Core or Domain. When several tenants grow the same
behaviour, promote it into Domain — but only after the second or third repetition shows
the shared shape, not on the first.

## Placement test

For any substantial behaviour, in order:

1. Needed across fundamentally different problem spaces? → consider **Core**.
2. Reused by multiple customers with the same kind of problem? → consider **Domain**.
3. Unique to one customer? → **Tenant**.

Apply with judgment, not mechanically. Worked examples and the ambiguous cases:
`references/placement.md`.

## Enforcement

Encode the dependency rules as a check, not a reminder — a layering rule that is only in
prose will be violated. Tooling per ecosystem, promotion and demotion procedures:
`references/enforcement.md`.

## UX across layers

Prefer one frontend composed as **Core UX + Domain UX/configuration + Tenant
branding/configuration** over a per-customer frontend fork. Forks diverge, and every fix
then has to be applied N times.

## References

| File | Load when |
|---|---|
| `references/placement.md` | deciding where behaviour goes, or a case is ambiguous |
| `references/enforcement.md` | wiring up layer checks, promoting or demoting code |
