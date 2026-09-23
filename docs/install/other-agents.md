# Install for other agents

Any agent that reads Markdown skill files with YAML front matter can use this standard.
There is exactly one source: `skills/`.

## The general pattern

```bash
git clone --depth 1 https://github.com/rajfnu/agent-engineering-standard /tmp/aes
cp -R /tmp/aes/skills/* <your-agent's-skills-directory>/
```

Known locations at the time of writing — verify against your agent's current docs:

| Agent | Directory |
|---|---|
| Claude Code | `.claude/skills/` or `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Cursor | `~/.cursor/plugins/local/<name>/skills/` |
| Kimi Code | installed via `/plugins install <repo-url>` |
| OpenCode | see the project's plugin documentation |

## Agents without a skills mechanism

Point the agent's own instruction file at the Skills instead of pasting them in:

```markdown
Engineering standard: read `skills/engineering-quality/SKILL.md` before substantial
changes, and load one file from its `references/` only when the task hits that concern.
Reviews: `skills/engineering-review/SKILL.md`.
Multi-tenant layering (only if this repo has Core/Domain/Tenant):
`skills/core-domain-tenant/SKILL.md`.
```

Pasting the full text into a system prompt works but costs the full token budget on every
request and discards progressive disclosure — the main thing the standard is for.

## Minimum requirements

An agent gets full value if it can:

- read a file on demand (for L2 references),
- run shell commands (for the deterministic scoping and test recipes),
- select a skill from its description (for L0 discovery).

Without on-demand file reads, load `SKILL.md` alone. It is self-contained; the references
add depth, not correctness.
