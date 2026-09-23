# ADR-0001: The canonical artifact is a set of portable Agent Skills

- **Status:** Accepted
- **Date:** 2026-09-23

## Context

The standard has to work across Claude Code, Codex, Cursor, Kimi Code, and agents that do
not exist yet. Candidate canonical forms: a Claude plugin, one large prompt, one large
`AGENTS.md`, a custom subagent, a slash command, a hook, or portable Skill files.

## Decision

The canonical source is `skills/` — Markdown files with YAML front matter, following the
Agent Skills convention. Claude plugin, Codex plugin, and slash commands are thin adapters
that point at that directory. No adapter contains engineering instructions.

## Rationale

- **Portable.** Skill files are plain Markdown; every listed agent can consume them, and
  an agent that cannot still gets value from an instruction-file pointer.
- **Partially loadable.** A prompt or `AGENTS.md` is all-or-nothing and is paid for on
  every request. Skills load on demand, at three levels.
- **Composable.** Skills coexist with other skill collections. A monolithic agent or
  prompt does not.
- **Single source.** Adapters that duplicate instructions drift. Ours contain none.

## Consequences

- Adapter manifests must be kept in sync with the skill list — CI checks this.
- Agents with no file-read capability get `SKILL.md` only, which is why each `SKILL.md`
  must stand alone.
- We accept that slash commands are Claude-Code-flavoured; they are convenience, not the
  product.
