# Enforcing the layers

A layering rule that exists only in prose is a layering rule that will be violated. Make
the build fail.

## Rules to encode

```
core   must not import  domain, tenant
domain must not import  tenant
tenant may import       domain, core
```

Plus: no cycles within a layer, and no tenant importing another tenant.

## Tooling

Use what the ecosystem already has; do not introduce a tool solely for this.

| Ecosystem | Tool | Mechanism |
|---|---|---|
| JS/TS | `dependency-cruiser` | `forbidden` rules on path globs |
| JS/TS | `eslint-plugin-boundaries` | element types + allowed-dependency matrix |
| TS monorepo | project references / workspace deps | a layer simply cannot resolve a higher one |
| Python | `import-linter` | `layers` contract, top-down |
| Java/Kotlin | ArchUnit | `layeredArchitecture()` test in the normal suite |
| .NET | NetArchTest | assertion test on assembly references |
| Go | `depguard`, `go-arch-lint` | package-level deny rules |
| Rust | Cargo workspace | crate dependency graph is the enforcement |
| Any | CI grep | `rg` over import lines; crude but real |

Minimal fallback that works anywhere:

```bash
#!/usr/bin/env bash
# Fail the build if core or domain reaches upward. Tune the patterns to your syntax.
fail=0
if rg -n --glob 'core/**' -e '(import|from|require).*(domain|tenant)'; then
  echo "core must not depend on domain or tenant" >&2; fail=1
fi
if rg -n --glob 'domain/**' -e '(import|from|require).*tenant'; then
  echo "domain must not depend on tenant" >&2; fail=1
fi
exit "$fail"
```

Run it in CI, not as a pre-commit hook that people bypass.

## Promotion (Tenant → Domain, Domain → Core)

1. **Confirm the repetition is real** — the same behaviour, not merely similar code.
2. **Find the shared shape** — the union of variations, with differences expressed as
   parameters or extension points.
3. **Move, do not copy.** Leave no old implementation behind; that is exactly the
   `A1 + A2 + A3` drift the standard exists to prevent.
4. **Strip the origin's knowledge** — customer names, field names, hardcoded endpoints.
5. **Add the layer test** so the new home cannot regress.
6. **Migrate every caller in the same change** where feasible; if not, record the
   follow-up before merging.

## Demotion (Core → Domain, Domain → Tenant)

Demote when a Core/Domain item turns out to encode knowledge it should not own. Same
procedure, downward. Demotion is a normal correction, not an admission of failure — it is
cheaper than a wrong abstraction everyone routes around.

## Reviewing a change against the layers

- Which layer do the changed files live in?
- Does the change introduce an import that crosses a rule?
- Does a Core/Domain file now mention a customer, or a Tenant-shaped concept?
- Is there a new `shared/`/`common/` directory acting as an unlabelled layer?
- If behaviour was promoted, was the original actually removed?
