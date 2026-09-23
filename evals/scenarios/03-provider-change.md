# 03 — Provider change

**Tests:** configuration vs. code, abstraction judgment, no hard-coded vendor leakage.

## Setup

A codebase calling one external provider (model API, payment processor, storage, email)
with the vendor's SDK types used directly in domain code, and the endpoint or model name
hard-coded.

## Prompt

> We need to support a second provider alongside the current one.

## Pass

- Finds every place the vendor leaks into domain code, including types in signatures.
- Distinguishes intentional variability (provider, model, endpoint, timeout → config) from
  invariants (the business rule → code).
- Proposes an interface owned by the domain, with the vendor behind an adapter — and says
  what the interface is *for*, not just that interfaces are good.
- Maps the vendor response to an internal type at the boundary.

## Fail

- Wraps the existing SDK one-to-one and calls it an abstraction.
- Adds `if (provider === 'x')` branches through the domain.
- Leaves the model name or endpoint hard-coded.
- Makes everything configurable, including things that never vary.

## Measure

Vendor leak sites found vs. actual. Whether the proposed interface reflects the domain's
needs or the vendor's API shape.
