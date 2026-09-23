# Code quality

## Principles, applied in proportion

| Principle | Real use | Failure mode when overdone |
|---|---|---|
| SRP | one reason to change | a file per function |
| Separation of concerns | keep IO, domain, presentation apart | ceremonial layering |
| Open/closed | extend without editing stable code | speculative plugin points |
| Liskov | substitutes really substitute | inheritance gymnastics |
| Interface segregation | narrow, honest interfaces | one-method interface per call site |
| Dependency inversion | domain owns its interfaces | wrappers around wrappers |
| KISS | boring, readable solution | cleverness contests |
| DRY | one source of truth for a *rule* | coupling unrelated code that merely looks alike |
| YAGNI | build what is needed | frameworks for one use case |

DRY applies to knowledge, not to character sequences. Two functions that look identical
but change for different reasons should stay separate.

## Size as a smell

At roughly **300 substantive lines** (excluding imports, generated code, data tables),
pause and ask:

- Does it have more than one reason to change?
- Does it mix orchestration with persistence?
- Does it mix domain rules with infrastructure?
- Does it mix configuration with execution?
- Does it mix concepts that a reader has to hold simultaneously?
- Is any part of it hard to test without the rest?

Yes to several → split along the concept boundary you just named.
No to all → it is a long file that is fine. Leave it.

Never split to satisfy a line count. A 400-line state machine with one responsibility is
healthier than four 100-line files that must be read together.

## Functions

Prefer explicit dependencies over ambient ones (globals, singletons, implicit context).
Prefer returning values over mutating arguments. Prefer total functions over ones that
throw for ordinary inputs. Keep the happy path at the lowest indentation level.

## Errors

- Fail fast on programmer error; degrade deliberately on operational error.
- Errors carry enough structure to be handled (type/code), not just printed.
- Do not swallow errors to make a test pass.
- Do not leak internals (stack traces, SQL, provider payloads) to end users.
- Retries need a bound, a backoff, and an idempotency story.

## Logging

Structured, keyed, and leveled. Log decisions and boundaries, not every line. Include a
correlation ID on anything crossing a process. Never log secrets, tokens, credentials,
PII, or full request bodies from untrusted sources.

## Reuse without importing debt

Before copying anything in from another repo or module:

1. **Do we need it?** — not "might we".
2. **Is it clean enough?** — would you write it this way today?
3. **Does it belong here?** — does it fit this capability's responsibility?
4. **What comes with it?** — transitive dependencies, config, assumptions, build steps.

Never bulk-copy: directories, obsolete compatibility shims, dead utilities,
customer-specific branches, old experiments, historical context files, stale prompts,
generated artifacts, unrelated documentation, or dependencies you will not use.

## Comments

Comment *why*, and non-obvious constraints. Do not narrate *what* the line does. Delete
commented-out code — version control already has it.
