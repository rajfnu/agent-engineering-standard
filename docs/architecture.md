# Architecture of the standard

## The one design decision

**The canonical artifact is a set of portable Agent Skills.** Everything else is an
adapter over them.

```
                    skills/            <-- canonical, portable, one source of truth
                       |
      +----------------+----------------+-------------------+
      |                |                |                   |
 .claude-plugin/  .codex-plugin/    manual copy       any skill-compatible
 + commands/                        into .agent dirs        agent
```

What the canonical source is deliberately **not**:

| Not this | Why |
|---|---|
| A Claude-only plugin | Locks the standard to one agent |
| One giant prompt | Cannot be loaded partially; cost scales with irrelevance |
| One giant `AGENTS.md` | Same problem, plus it fights the repo's own instructions |
| One custom agent | Not portable; not composable with other skills |
| One slash command | Not model-invocable; not portable |
| A hook | Hooks enforce, they do not teach |

Those forms exist here only as thin adapters that point at `skills/`.

## Three skills, not one

| Skill | Scope | Invocation |
|---|---|---|
| `engineering-quality` | universal standard for making a change | most code work |
| `core-domain-tenant` | multi-tenant layering | conditional — most repos never load it |
| `engineering-review` | reviewing a change or directory | review time |

They are independently invocable. `engineering-review` links into
`engineering-quality`'s references rather than restating them, so there is one definition
of each rule.

Splitting this way is itself a context decision: a repository with no tenancy never pays
for `core-domain-tenant`, and an implementation task never pays for the review protocol.

## Progressive disclosure

Three levels. Each is loaded only when the previous one justifies it.

| Level | Content | When loaded |
|---|---|---|
| **L0** | front-matter `name` + `description` | always, for discovery |
| **L1** | `SKILL.md` | when the skill is invoked |
| **L2** | one file in `references/` | when the task hits that specific concern |

Measured cost (estimated tokens, `python3 tools/measure_context.py`):

<!-- MEASUREMENTS:START -->
| skill | L0 metadata | L1 SKILL.md | L2 all refs | refs | largest ref |
|---|---|---|---|---|---|
| `core-domain-tenant` | ~186 | ~1040 | ~1518 | 2 | ~789 |
| `engineering-quality` | ~194 | ~2016 | ~5400 | 7 | ~944 |
| `engineering-review` | ~189 | ~1570 | ~2571 | 3 | ~1042 |
| **all** | **~569** | **~4626** | **~9489** | 12 | |
<!-- MEASUREMENTS:END -->

The number that matters is not the total. It is that a typical task loads L0 for all three
skills plus L1 and one L2 file for one skill — not the whole standard.

`tools/validate_skills.py` fails CI if a `SKILL.md` grows past 200 lines, if a reference
is orphaned, or if a cross-skill link dangles. The budget is enforced, not aspirational.

## What is deliberately not built

| Not built | Instead |
|---|---|
| A code-review engine | Call OpenCodeReview (ADR-0002) |
| A CLI | Deterministic shell recipes inside the skills (ADR-0003) |
| Planning / TDD / debugging workflow skills | Superpowers already does this well |
| A frontend design system | Delegate to a design skill (`docs/integrations.md`) |
| Hooks | Nothing here is safe to enforce on every file write (ADR-0004) |
| A required capability-manifest format | Optional, for large repos only (ADR-0005) |
| Any web app, API, database, or dashboard | Not needed to ship a standard |

This repository contains more documentation than code on purpose. The product *is* the
instructions.

## Repository layout

```
skills/                     canonical Skills (the product)
commands/                   thin slash commands that invoke the Skills
.claude-plugin/             Claude Code plugin + marketplace manifests
.codex-plugin/              Codex plugin manifest
docs/                       how it works, how to install, integrations
docs/decisions/             ADRs
evals/                      scenarios and rubric for measuring the standard
tools/                      dependency-free validation and measurement scripts
.github/workflows/          CI: validate skills, links, and manifests
```

## Design constraints

Every addition to this repository must satisfy all of these:

1. **Agent agnostic** — no instruction that only one agent can follow.
2. **Stack agnostic** — no language, framework, or build tool assumed.
3. **Repository agnostic** — works on a new repo and a 15-year-old monolith.
4. **Progressive** — detail lives in `references/`, not in `SKILL.md`.
5. **Non-duplicating** — if a mature open-source tool does it, integrate instead.
6. **Consequential** — if it does not materially improve quality, architecture, UX,
   safety, maintainability, developer experience, or efficiency, it does not ship.
