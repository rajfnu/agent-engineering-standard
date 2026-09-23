# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project
follows [Semantic Versioning](VERSIONING.md).

## [Unreleased]

## [0.1.1] — 2026-09-23

### Fixed

- `CLAUDE.md` was a prose pointer (`See AGENTS.md`). Because a `CLAUDE.md` exists, Claude
  Code reads it *instead of* `AGENTS.md`, so contributors got one line rather than the
  repository's instructions. Replaced with an `@AGENTS.md` import, which also covers Claude
  Code before v2.1.277 and sessions that cannot read `AGENTS.md` directly.
- Removed `commands/engineering-review.md`. It collided with the `engineering-review`
  skill — both resolve under the same `/plugin-name:` namespace — and, since skills are
  user-invocable already, it only forwarded to the skill, which ADR-0001 forbids.
  `/engineering-review` still works, as the skill.

### Changed

- Token figures cross-checked against Claude Code's own estimator. `chars/4` under-reads a
  real tokenizer by roughly 25–45%, so it is now presented as a portable **lower bound**
  rather than a measurement, with the first-party numbers published alongside in
  `evals/RESULTS.md`.

## [0.1.0] — 2026-09-23

Initial public release.

### Added

- **`engineering-quality` skill** — the universal standard: the scope→context→understand→
  change→test→reconcile loop, context budgets, capability boundaries and contracts,
  dependency direction, configuration vs. code, reuse without importing debt, size as a
  smell, impact-based testing (L1–L4), mechanical enforcement, security/reliability/
  observability, UX, and source-of-truth resolution. Seven progressive-disclosure
  references.
- **`core-domain-tenant` skill** — conditional layering for genuinely multi-tenant
  products, with an explicit applicability gate, the placement test, promotion/demotion
  procedures, and per-ecosystem enforcement tooling. Two references.
- **`engineering-review` skill** — a seven-step review pipeline that delegates line-level
  defect detection to OpenCodeReview and adds scope, architecture, test impact, repository
  drift, and UX. Three references, including severity definitions and the evidence rule.
- **Adapters** — Claude Code plugin and marketplace manifests, Codex plugin manifest, and
  four slash commands (`/engineering-review`, `/architecture-review`, `/reconcile-repo`,
  `/ux-review`) that invoke the Skills without duplicating their instructions.
- **Documentation** — architecture of the standard, optional integrations with verified
  install commands, optional capability-metadata format, and install guides for Claude
  Code, Codex, and any skill-compatible agent.
- **Six ADRs** — portable Skills as the canonical artifact; integrate OpenCodeReview rather
  than rebuild it; no CLI in v0.1; no hooks; capability metadata optional; Apache-2.0.
- **Evaluation suite** — twelve reproducible scenarios with pass/fail criteria and metrics,
  half of which test that the standard is *not* over-applied.
- **Tooling** — `tools/validate_skills.py` (structure, 200-line `SKILL.md` budget,
  description quality including a mandatory "when not to use" clause, orphaned and dangling
  reference links) and `tools/measure_context.py` (context cost per disclosure level). No
  third-party dependencies.
- **CI** — validates skills, plugin manifests, version consistency, and internal links on
  every push and pull request.
- **Open-source hygiene** — Apache-2.0 licence, NOTICE, CONTRIBUTING, SECURITY,
  CODE_OF_CONDUCT, VERSIONING.

### Known limitations

- The twelve behavioural eval scenarios are **specified but not run**. Context measurements
  are real; behavioural claims are not yet evidenced. See `evals/RESULTS.md`.
- Token figures are `chars/4` estimates, not tokenizer output.
- Full-strength review requires the external `ocr` CLI; without it the line-level pass is
  degraded to a bounded manual review.
- Scope and test-impact selection are heuristic unless a repository brings its own
  affected-graph tooling.

[Unreleased]: https://github.com/rajfnu/agent-engineering-standard/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/rajfnu/agent-engineering-standard/releases/tag/v0.1.1
[0.1.0]: https://github.com/rajfnu/agent-engineering-standard/releases/tag/v0.1.0
