# 08 — Non Core/Domain/Tenant project

**Tests:** **not** manufacturing layers that do not apply. This is the over-application
guard for `core-domain-tenant`.

## Setup

A single-tenant internal tool, or an open-source library. No tenancy, no customers, one
problem space.

## Prompt

> How should we structure this as it grows?

## Pass

- Does not mention Core/Domain/Tenant, or explicitly says it does not apply here and why.
- Answers with ordinary boundary reasoning: responsibility, contracts, dependency
  direction, blast radius.
- Proposes the smallest structure that fits the current size.

## Fail

- Introduces the three layers anyway.
- Creates `core/`, `domain/`, `tenant/` directories.
- Recommends the layering "for future flexibility".

## Measure

Binary. Any unsolicited Core/Domain/Tenant structure is a fail. This scenario is the main
defence against a conditional skill becoming an unconditional one.
