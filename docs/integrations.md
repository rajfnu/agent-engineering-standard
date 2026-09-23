# Optional integrations

All of these are **optional**. Every skill in this standard degrades gracefully when the
tool is absent. Nothing here is vendored or forked; we call tools and cite them.

## OpenCodeReview — line-level review

[alibaba/open-code-review](https://github.com/alibaba/open-code-review) · Apache-2.0

Deterministic file selection, semantic file bundling, rule matching, external comment
positioning, delegation mode, JSON output, CI integrations, MCP support, OpenTelemetry.

```bash
npm install -g @alibaba-group/open-code-review
ocr config provider && ocr config model && ocr llm test
```

`engineering-review` calls it for the line-level pass and adds the architectural reasoning
OCR does not do. Full integration notes, including delegation mode and CI:
`skills/engineering-review/references/open-code-review.md`.

## Superpowers — workflow methodology

[obra/superpowers](https://github.com/obra/superpowers) · MIT

Brainstorming, writing and executing plans, TDD, systematic debugging, dispatching
parallel agents, requesting/receiving code review, verification before completion,
finishing a branch.

```text
/plugin marketplace add obra/superpowers
/plugin install superpowers@superpowers-dev
```

**Complementary, not overlapping.** Superpowers governs *how you work through a task*;
this standard governs *what good engineering looks like in the result*. We deliberately do
not ship planning, TDD, or debugging skills — use theirs.

## Frontend design — visual and design-system work

```bash
npx claude-code-templates@latest --skill creative-design/frontend-design --yes
```

`engineering-quality/references/ux.md` and `engineering-review/references/ux-review.md`
cover UX reasoning, states, and the accessibility floor. For deep visual design and design
systems, delegate to a specialist skill rather than improvising one.

## Code reviewer skill — alternative when OCR is unavailable

```bash
npx claude-code-templates@latest --skill development/code-reviewer --yes
```

Useful where installing a CLI is not possible. Prefer OCR where you can: deterministic
file selection is the part a language-only skill cannot replicate.

## Everything Claude Code — à la carte specialists

[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) · MIT

A large collection of agents, skills, hooks, and per-harness configurations. Install
**selected** capabilities if you want them. Do not install it wholesale alongside this
standard — the combined always-loaded metadata is the thing we are trying to keep small.

## Claude Code Templates — component distribution

[davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) · MIT

```bash
npx claude-code-templates@latest --skill <category>/<name> --yes
npx claude-code-templates@latest --agent <category>/<name> --yes
```

This standard is compatible with that ecosystem but does not depend on it.

## Web research

Current-information lookups (a library's present API, a CVE, a spec revision) belong to a
web-search or research tool such as Exa, the agent's built-in search, or an MCP server.
Ordinary implementation should not need web search — if a task keeps reaching for it, the
repository's own documentation is probably wrong or missing.

## Verify before you script

Third-party CLI flags change. The commands above were verified against each project in
September 2026. Run `--help` for your installed version before committing them into CI.
