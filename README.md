# Agent Engineering Standard

**Portable engineering Skills for AI coding agents — architecture, code quality, UX, scoped
testing, repository hygiene, and low-context development.**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-3-informational.svg)](skills/)
[![Agents](https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex%20%7C%20any%20skill--compatible-blueviolet.svg)](docs/install/other-agents.md)

---

## The problem

Coding agents are good at writing code and bad at the decisions around it. The recurring
failures are not syntax:

- **Context bloat.** A one-line fix triggers a repository tour. Cost and latency scale with
  what was read, not with what changed.
- **Test waste.** The full suite runs after every edit, so nobody watches the result.
- **Architecture drift.** Boundaries erode one plausible import at a time.
- **Repository sediment.** `A1 → A2 → A3` becomes `A1 + A2 + A3` all half-alive, and the
  next agent reads all three.
- **Frontend treated as glue.** Business logic in components, no error state, no keyboard
  path.
- **Ceremony.** Interfaces around one implementation, plans that never become code.

The usual fix — a longer prompt — makes the first problem worse.

## The approach

```
SMALL RELEVANT CONTEXT + CLEAR BOUNDARIES + DETERMINISTIC ENFORCEMENT
        + SPECIALIST TOOLS + SCOPED TESTING + REPOSITORY RECONCILIATION
        + AGENT JUDGMENT
        = better software with less waste
```

Three focused Skills, loaded progressively, integrating mature tools instead of
reimplementing them.

## The three Skills

| Skill | What it does | When it loads |
|---|---|---|
| **[`engineering-quality`](skills/engineering-quality/)** | The universal standard: context budgets, capability boundaries and contracts, dependency direction, configuration vs. code, reuse without importing debt, impact-based testing, security and observability, UX, source-of-truth resolution. | Most code work |
| **[`core-domain-tenant`](skills/core-domain-tenant/)** | Placement and layering for products that genuinely have reusable Core + reusable Domain + customer Tenants. | **Conditional** — most repositories never load it |
| **[`engineering-review`](skills/engineering-review/)** | Scoped review: blast radius → boundaries → line-level defects (via OpenCodeReview) → test impact → repository drift → UX → ranked report. | Review time |

Each is independently invocable. `engineering-review` links into `engineering-quality`'s
references instead of restating them, so each rule is defined once.

## Progressive disclosure, measured

Three levels, each loaded only when the previous justifies it.

| Level | Content | Loaded |
|---|---|---|
| **L0** | front-matter `name` + `description` | always, for discovery |
| **L1** | one `SKILL.md` | when that skill is invoked |
| **L2** | one file from `references/` | when the task hits that concern |

Estimated tokens (chars ÷ 4), reproducible with `python3 tools/measure_context.py`:

<!-- MEASUREMENTS:START -->
| skill | L0 metadata | L1 SKILL.md | L2 all refs | refs | largest ref |
|---|---|---|---|---|---|
| `core-domain-tenant` | ~186 | ~1040 | ~1518 | 2 | ~789 |
| `engineering-quality` | ~194 | ~2016 | ~5400 | 7 | ~944 |
| `engineering-review` | ~189 | ~1570 | ~2571 | 3 | ~1042 |
| **all** | **~569** | **~4626** | **~9489** | 12 | |
<!-- MEASUREMENTS:END -->

A typical implementation task pays L0 for all three skills, L1 for one, and one L2 file.
Loading everything would cost roughly 3× that — which is what a single-large-prompt design
pays on *every* request.

Verified against Claude Code's own estimator (`claude plugin details`), which reports
**~817 tokens always-on** for the whole plugin and ~1.2k–2.5k on-invoke per skill. Treat the
`chars/4` table as a portable lower bound: it runs without any agent installed, but it
under-reads a real tokenizer by roughly 25–45%.

CI enforces the budget: `tools/validate_skills.py` fails if a `SKILL.md` exceeds 200 lines,
if a description is under 120 characters or never says when *not* to use the skill, or if a
reference file is orphaned or a reference link dangles.

## Install

### Claude Code

```text
/plugin marketplace add rajfnu/agent-engineering-standard
/plugin install agent-engineering-standard@agent-engineering-standard
```

The three Skills are user-invocable directly (`/engineering-review`), plus three commands
that route into specific references: `/architecture-review`, `/reconcile-repo`, `/ux-review`.
Details and project-local installs: **[docs/install/claude-code.md](docs/install/claude-code.md)**

### Codex

```bash
codex plugin marketplace add rajfnu/agent-engineering-standard
codex
```

Details and manual install: **[docs/install/codex.md](docs/install/codex.md)**

### Any other skill-compatible agent

```bash
git clone --depth 1 https://github.com/rajfnu/agent-engineering-standard /tmp/aes
cp -R /tmp/aes/skills/* <your-agent's-skills-directory>/
```

**[docs/install/other-agents.md](docs/install/other-agents.md)**

### Recommended alongside

```bash
npm install -g @alibaba-group/open-code-review   # engineering-review calls this
```

## Examples

```text
> Fix the off-by-one in formatRange().
  → reads the module and its test, runs L1 tests, fixes it. No repo tour, no plan document.

> This 800-line file is too long, split it.
  → checks whether it has more than one reason to change. If it does not, says so and
    leaves it alone. Size is a smell, not a limit.

> Review this branch.
  → scope → boundaries → `ocr review --format json` → impacted tests → drift → UX →
    findings ranked by consequence, each with a concrete failure scenario.

> How should we structure this single-tenant internal tool?
  → ordinary boundary reasoning. Does not invent Core/Domain/Tenant layers.

> Add a required `currency` field to the Order schema.
  → finds every consumer, escalates to L2/L3, raises backward compatibility before writing
    the migration.
```

## Why another coding-agent project

Most of this ecosystem is either a workflow methodology (how to move through a task) or a
component marketplace (a skill for every framework). Neither says **what good engineering
looks like in the result**, in a way that is portable and cheap to load.

This project is deliberately narrow:

| We build | We do not build |
|---|---|
| Portable engineering Skills | A code-review engine — **OpenCodeReview** does that |
| Context and test-scope discipline | Planning / TDD / debugging workflows — **Superpowers** does those |
| Architecture and boundary reasoning | A design system — delegate to a design skill |
| Repository reconciliation | A CLI, hooks, a web app, or a database ([ADR-0003](docs/decisions/0003-no-cli-in-v0.md), [ADR-0004](docs/decisions/0004-no-hooks.md)) |

### Relationship to OpenCodeReview

[OpenCodeReview](https://github.com/alibaba/open-code-review) (Apache-2.0, Alibaba) does
line-level review with deterministic file selection, semantic bundling, rule matching, and
external comment positioning — reporting higher precision and F1 than a general-purpose
agent on the same model at roughly 1/9 the tokens, with lower recall by design.

`engineering-review` **calls it** and adds what it does not do: scope, architecture,
contract compatibility, test-level selection, repository drift, and UX. Without `ocr`
installed, the skill degrades to a bounded manual pass. Nothing is vendored.
[ADR-0002](docs/decisions/0002-integrate-opencodereview.md) ·
[integration notes](skills/engineering-review/references/open-code-review.md)

### Relationship to specialist skills

| Tool | Role |
|---|---|
| [Superpowers](https://github.com/obra/superpowers) (MIT) | Workflow: brainstorming, plans, TDD, debugging, parallel agents. Complementary — we ship none of this. |
| [Claude Code Templates](https://github.com/davila7/claude-code-templates) (MIT) | `--skill creative-design/frontend-design` for deep visual design work. |
| [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) (MIT) | À-la-carte specialists. Install selectively, not wholesale. |

Full table: **[docs/integrations.md](docs/integrations.md)**

## Design constraints

Every addition must satisfy all six:

1. **Agent agnostic** — no instruction only one agent can follow.
2. **Stack agnostic** — no language, framework, or build tool assumed.
3. **Repository agnostic** — a new repo and a 15-year-old monolith.
4. **Progressive** — detail lives in `references/`, not `SKILL.md`.
5. **Non-duplicating** — if a mature tool does it, integrate.
6. **Consequential** — if it does not materially improve quality, architecture, UX, safety,
   maintainability, developer experience, or efficiency, it does not ship.

## Evaluation

Twelve reproducible scenarios in **[`evals/`](evals/)**. Half test that the agent *does*
something; half test that it *does not* — no repository tour for a one-line fix, no 5,000
tests for a local change, no manufactured Core/Domain/Tenant layers, no splitting a
cohesive file to hit a line count.

**Honest status:** the twelve behavioural scenarios are **specified but not yet run**. The
context measurements above are real and reproducible; the behavioural claims are not yet
evidence. See **[evals/RESULTS.md](evals/RESULTS.md)**. Results — including negative ones —
are welcome as pull requests.

## Repository layout

```
skills/              canonical Skills — the product
commands/            thin slash commands that invoke the Skills
.claude-plugin/      Claude Code plugin + marketplace manifests
.codex-plugin/       Codex plugin manifest
docs/                architecture, integrations, install guides
docs/decisions/      ADRs
evals/               scenarios, rubric, results
tools/               dependency-free validation and measurement
```

More documentation than code, on purpose — the product *is* the instructions.
**[docs/architecture.md](docs/architecture.md)**

## Contributing

Small, evidence-backed changes. A new rule needs a failure it prevents; a new reference
needs a task that needs it; a new skill needs a reason the existing three cannot hold it.
**[CONTRIBUTING.md](CONTRIBUTING.md)** · **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** ·
**[SECURITY.md](SECURITY.md)**

## Roadmap

- **v0.1** — three Skills, adapters, integration docs, eval scenarios. *(current)*
- **Next** — run the eval suite on real repositories and publish baseline-vs-treatment
  numbers; act on the failures.
- **Later** — revisit the CLI only if evals show deterministic tooling fixes a real,
  repeated mis-scoping ([ADR-0003](docs/decisions/0003-no-cli-in-v0.md)); capability
  metadata only if it gets real adoption ([ADR-0005](docs/decisions/0005-capability-metadata-optional.md)).

Roadmap items are candidates, not commitments.

## Licence

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
All content is original; no third-party code or text is vendored.

---

> **No engineering theatre.** If a rule does not materially improve code quality,
> architecture, UX, safety, maintainability, developer experience, or efficiency, it does
> not belong here.
