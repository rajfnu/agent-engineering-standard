# 09 — Separate-team private capability

**Tests:** designing against a contract with no source access.

## Setup

A service that must integrate with a capability owned by another team, whose source is not
available. Only an API description exists (OpenAPI, proto, or prose).

## Prompt

> Integrate with the `<capability>` service. We do not have access to its source.

## Pass

- Designs against the published contract: inputs, outputs, errors, state ownership,
  compatibility expectations.
- Defines behaviour for the failure modes the contract implies — timeout, partial
  response, error codes, retry safety.
- Maps the external shape to an internal type at the boundary.
- Identifies the contract questions it cannot answer and asks them as specific questions.
- Does not ask for source access as a precondition.

## Fail

- Blocks on "I need to see the implementation".
- Assumes undocumented behaviour without flagging the assumption.
- Lets the external response shape flow through the domain.
- Adds unbounded retries with no idempotency story.

## Measure

Whether an integration design was produced. Number of unflagged assumptions. Quality and
specificity of the questions raised.
