# Optional capability metadata

**Skip this unless you have a large repository where scope resolution is genuinely slow.**
Small and medium repositories should use the shell recipes in
`skills/engineering-quality/references/context-economy.md` instead. A manifest that drifts
from reality is worse than no manifest.

## When it earns its keep

All of these should be true:

- the repository is large enough that "which module owns this?" is not obvious from paths;
- ownership, contracts, and test locations do not follow a single convention;
- the same scoping questions are asked repeatedly across many changes;
- someone will actually maintain the file.

## Format

One `capability.yaml` per capability, at the capability root. No schema is imposed; keep
the keys you use and delete the rest.

```yaml
name: payments

owns:
  - src/payments/**

docs:
  - docs/payments/architecture.md

contracts:
  - api/payments/openapi.yaml

tests:
  unit:
    - src/payments/**/*_test.*
  integration:
    - tests/integration/payments/**
  e2e:
    - tests/e2e/checkout.spec.*

allowed_dependencies:
  - platform
  - ledger

forbidden_dependencies:
  - tenant-*
```

## What an agent does with it

| Question | Answered by |
|---|---|
| Which capability owns this changed file? | `owns` |
| What must I read before changing it? | `docs`, `contracts` |
| Which tests are L1 / L2 / L3 here? | `tests` |
| Is this new import legal? | `allowed_dependencies`, `forbidden_dependencies` |

That turns four searches into one lookup, which is the entire justification.

## Keeping it honest

- Generate the dependency rules into whatever import linter the ecosystem already has, so
  CI fails when code and manifest disagree.
- Fail CI if a `owns` glob matches nothing, or if a file is claimed by two capabilities.
- Review the manifest when a capability is split or merged — the same reconciliation
  discipline applies to metadata as to code.

If you cannot commit to those three, do not adopt the format.
