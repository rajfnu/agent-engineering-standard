# Install for Claude Code

## Plugin (recommended)

```text
/plugin marketplace add rajfnu/agent-engineering-standard
/plugin install agent-engineering-standard@agent-engineering-standard
```

This registers the three Skills plus four slash commands:

| Command | Does |
|---|---|
| `/engineering-review [target]` | full review pipeline on a branch, PR, or path |
| `/architecture-review [target]` | boundaries, contracts, dependency direction only |
| `/reconcile-repo [path]` | inventory repository drift with evidence |
| `/ux-review [target]` | frontend journey, states, accessibility, component quality |

Verify with `/plugin` (the plugin should be listed and enabled).

## Project skills (no plugin)

Vendor the skills into the repository so everyone working on it gets them:

```bash
git clone --depth 1 https://github.com/rajfnu/agent-engineering-standard /tmp/aes
mkdir -p .claude/skills
cp -R /tmp/aes/skills/* .claude/skills/
git add .claude/skills && git commit -m "chore: add agent engineering standard skills"
```

## Personal skills (all your projects)

```bash
git clone --depth 1 https://github.com/rajfnu/agent-engineering-standard /tmp/aes
mkdir -p ~/.claude/skills
cp -R /tmp/aes/skills/* ~/.claude/skills/
```

## Monorepos

Place a copy under the subtree that should get it:

```
packages/web/.claude/skills/engineering-quality/SKILL.md
```

It loads for sessions started in or below that directory. Prefer one repository-root copy
unless different subtrees genuinely need different standards.

## Using it

The Skills are model-invocable: describe the work and the agent loads what fits
("review this branch", "refactor this 800-line service"). To force one:

```text
Use the engineering-quality skill and refactor src/billing/invoice.ts
```

Only load `core-domain-tenant` in repositories that actually have those layers.

## Recommended alongside

```bash
npm install -g @alibaba-group/open-code-review   # engineering-review calls this
```

```text
/plugin marketplace add obra/superpowers          # workflow methodology, complementary
```

## Keeping it updated

Plugin installs update through `/plugin`. Vendored copies need a re-copy; pin the version
you vendored in your own `CHANGELOG` so you can tell what you have.
