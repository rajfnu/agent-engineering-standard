# Install for Codex

The Skills are portable — there is no Codex-specific fork of the engineering rules. The
canonical `skills/` directory is what Codex loads, byte for byte the same files Claude
Code loads.

## Plugin marketplace

```bash
codex plugin marketplace add rajfnu/agent-engineering-standard
codex
```

Then open `/plugins`, install and enable **agent-engineering-standard**, and start a new
task. The repository ships `.codex-plugin/plugin.json` pointing at `./skills/`.

## Manual install

```bash
git clone --depth 1 https://github.com/rajfnu/agent-engineering-standard /tmp/aes
mkdir -p ~/.codex/skills
cp -R /tmp/aes/skills/* ~/.codex/skills/
```

For a single project, copy into the project's skills directory instead of the home one.

## Referencing from AGENTS.md

If your Codex setup drives behaviour from `AGENTS.md`, point at the Skills rather than
inlining them — inlining defeats progressive disclosure and puts the full text in every
request:

```markdown
## Engineering standard

Before substantial changes, load `skills/engineering-quality/SKILL.md` and follow it.
Load a file from its `references/` only when the task hits that concern.
Reviews: `skills/engineering-review/SKILL.md`.
```

## Slash commands

The `commands/` directory is a Claude Code convention. Under Codex, invoke the Skills by
name in the prompt:

```text
Use the engineering-review skill to review my current changes against main.
```

## Recommended alongside

```bash
npm install -g @alibaba-group/open-code-review
codex plugin marketplace add alibaba/open-code-review
```

## Verify the flags

Codex's plugin CLI is evolving. If `codex plugin marketplace add` is unavailable in your
version, use the manual install above — it works regardless.
