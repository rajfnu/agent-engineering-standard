# Placement: worked examples

## Sorting signals

| Signal | Layer |
|---|---|
| Names a customer, their systems, or their terminology | Tenant |
| Encodes a rule from a regulation/practice shared by an industry or function | Domain |
| Would be a reasonable open-source library on its own | Core |
| Changes when a customer's contract changes | Tenant |
| Changes when the problem space's rules change | Domain |
| Changes when the platform's own architecture changes | Core |
| Has exactly one consumer today and no credible second | Tenant (wait) |

"Would be a reasonable standalone library" is the sharpest Core test. Auth, retries,
queueing, storage abstraction, tracing, feature flags, templating — plausible libraries.
"Claim triage workflow" is not.

## Examples

| Behaviour | Layer | Why |
|---|---|---|
| Retry/backoff helper | Core | Universal; useful with no domain at all |
| Model-provider abstraction | Core | Universal infrastructure concern |
| Audit log writer | Core | Every domain and tenant needs it identically |
| "Claim" entity and its lifecycle states | Domain (insurance) | Every insurer has claims; no insurer defines them alone |
| Prompt template for summarising a clinical note | Domain (healthcare) | Reused by any customer in that space |
| Regulatory retention policy for a jurisdiction | Domain | Shared by everyone operating there |
| Mapping Acme's `CUST_REF` field to `customerId` | Tenant | Acme's schema, nobody else's |
| Acme's SSO configuration | Tenant | Pure configuration |
| Acme's brand palette and logo | Tenant | Branding |
| An export format three customers asked for | Domain, after the third | Promote once the shape is proven |

## Ambiguous cases

**"Two tenants need the same thing."** Two is weak evidence. Duplicate in both Tenants,
note the duplication, and promote at the third — or at the second if they arrived at an
identical shape independently, which is strong evidence.

**"It is universal but only one domain uses it."** Core, if it genuinely has no domain
knowledge and would be a sane library. Keeping a small, clean, domain-free utility in Core
costs little. Moving domain knowledge into Core costs a lot.

**"Core needs to know about a domain concept."** It does not. Invert the dependency: Core
exposes an extension point or interface; Domain supplies the concept. If that feels
awkward, the behaviour probably belongs in Domain.

**"The tenant needs different behaviour, not just config."** Give Domain an explicit
extension point (strategy, hook, policy object) and let Tenant implement it. Never a
branch on customer identity inside Domain.

**"This tenant is our only real customer."** Then most things are Tenant, and Core/Domain
stay thin. That is correct, not a gap to be filled.

## Anti-patterns

- `if (tenant === 'acme')` anywhere in Core or Domain.
- Core importing a Domain type "just for the enum".
- A Domain layer that is an empty pass-through to Core, existing only for symmetry.
- Promoting to Core on first reuse, then fighting the abstraction for a year.
- A `common/` or `shared/` directory that is actually a fourth, unlabelled layer where
  everything lands.
