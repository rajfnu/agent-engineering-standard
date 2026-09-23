# 07 — Core / Domain / Tenant project

**Tests:** correct placement in a genuinely three-layer product.

## Setup

A product with `core/`, `domain/<space>/`, and `tenant/<customer>/`, at least two tenants
sharing a domain.

## Prompt

Run all four:

> Where should a retry-with-backoff helper live?
> Where should the claim-lifecycle state machine live?
> Where should Acme's field mapping from `CUST_REF` to `customerId` live?
> Two tenants now need the same CSV export. What should we do?

## Pass

- Core / Domain / Tenant / "duplicate for now, promote at the third — or at the second if
  the shapes arrived identical".
- Gives the reasoning, not just the answer.
- On promotion: says *move, not copy*, and to strip customer-specific knowledge.
- Mentions enforcing the layer rules with a check.

## Fail

- Puts the retry helper in Domain "because that is where it is used".
- Puts anything customer-named in Core or Domain.
- Proposes `if (tenant === 'acme')` inside shared code.
- Promotes to Core on first reuse.

## Measure

Correct answers / 4. Whether reasoning cites the placement questions or is post-hoc.
