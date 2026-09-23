# Architecture: boundaries, contracts, dependency direction

## Finding a boundary

A module boundary is real when the code inside it has:

- one coherent responsibility a person can state in a sentence,
- a single owner (team or person) in practice,
- the ability to evolve without lockstep changes elsewhere,
- ownership of its own data/state,
- an explicit contract other code uses,
- tests that run without standing up the rest of the system,
- a plausible independent package/deployment story,
- a bounded blast radius when it breaks.

Fewer than three of those and it is probably a folder, not a capability.

**Do not prescribe a module count.** A capability may contain several modules. A folder
is not an architecture. Directory depth is not layering.

## Contracts

A capability worth naming publishes:

| Element | Question it answers |
|---|---|
| Responsibility | what is this for |
| Inputs | what does it accept, with what validation |
| Outputs | what does it return, in what shape |
| Errors | what can fail, and how is that surfaced |
| State ownership | what data does it own and nobody else writes |
| Allowed dependencies | what may it depend on |
| Compatibility | what may change without breaking callers, and how versions move |

Consumers bind to the contract. Reaching into internals — importing a private module,
querying another capability's tables, depending on its serialisation format — is a
boundary violation even when the language permits it.

## Dependency direction

Domain and business logic should not depend on volatile infrastructure:

```
domain / policy          <-- stable, owns the rules
   ^
   | (interface owned by the domain)
   |
adapter                  <-- volatile: DB driver, cloud SDK, model provider,
                             HTTP client, queue, storage, UI framework
```

Volatility, not category, is the test. A checked-in pure-function date library is not
volatile; a hosted model API with a changing response schema is.

### When a port/adapter is worth it

Worth it when: you have or credibly expect a second implementation; you need to test the
domain without the dependency; the vendor's contract is unstable; or the boundary is a
real compliance/ownership line.

Not worth it when: the interface mirrors one vendor's API method-for-method; there is one
implementation and no test pressure; or the wrapper only renames things. That is a
pointless wrapper — delete it.

## Enforce mechanically where the ecosystem allows

Prefer a check over a reminder. Examples by ecosystem (use what exists; do not add a new
tool just to have one):

- JS/TS — `eslint-plugin-boundaries`, `dependency-cruiser`, `madge` (cycles)
- Java/Kotlin — ArchUnit, Checkstyle import control
- .NET — NetArchTest
- Python — `import-linter`, `pydeps`
- Go — `go-arch-lint`, `depguard`
- Rust — workspace crate graph, `cargo-deny`
- Any — a CI grep/`rg` rule over import statements is better than nothing

## Architecture smells worth reporting

- A capability that owns no state but reads three other capabilities' tables.
- Cycles between modules.
- Domain code importing a driver, SDK, or framework type.
- A contract whose error type is "string".
- Two capabilities that cannot be deployed or tested apart but claim to be separate.
- An "interfaces" or "abstractions" package with exactly one implementer each.
