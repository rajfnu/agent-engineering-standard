# Context economy

Loading context costs money, latency, and attention. An agent that reads 200 files to
change one function is not being thorough, it is being wasteful — and the signal it needs
gets buried in the noise it loaded.

## The selection order

1. **Changed surface.** What did the human actually ask to change? Name it in one sentence.
2. **Owning capability.** Which directory/module owns that behaviour? Read it.
3. **Contract.** What does that capability expose, and who calls it?
4. **Adjacent context, on demand only.** Pull a file when a specific unanswered question
   requires it — not "in case it is relevant".

Stop as soon as you can state: *what changes, what it touches, what could break.*

## Deterministic scoping recipes

These are language- and agent-agnostic. Prefer them to guessing.

```bash
# What actually changed
git diff --name-only origin/main...HEAD
git diff --stat origin/main...HEAD

# Who imports/references the thing you are changing (ripgrep, any language)
rg -n --fixed-strings 'SymbolName' -g '!**/{node_modules,dist,build,vendor,target}/**'

# Which tests sit closest to the changed files
git diff --name-only origin/main...HEAD | sed 's#/[^/]*$##' | sort -u

# Public contract surface near the change
rg -n --files-with-matches 'openapi|\.proto$|schema' <capability-dir>
```

If the repository ships a capability manifest (see `docs/capability-metadata.md` in the
standard), use it — it turns all of the above into a lookup.

## Budgets

| Change | Read | Tests |
|---|---|---|
| Local fix in one module | that module + its tests | L1 |
| New behaviour in one capability | capability + contract + contract callers | L1–L2 |
| Contract/schema change | contract + every consumer | L2–L3 |
| Cross-cutting or release | as needed | L4 |

Exceeding a budget is fine when you can say **why**. Exceeding it by default is not.

## Anti-patterns

- Reading the whole repository tree "to orient" before a one-line change.
- Loading every `*.md` in `docs/` when one document owns the answer.
- Re-reading a file you already read this session.
- Reading generated output, lockfiles, vendored dependencies, or build artifacts.
- Loading all four reference files of this skill when the task touches one concern.
- Summarising files you did not need, which then occupy context for the rest of the task.

## Signals you loaded too little

- You cannot name the callers of the function you changed.
- You do not know whether the behaviour is covered by a test.
- You are guessing at a type, a field name, or an error contract.

Those are the cases to spend context on. Spend it there, not everywhere.
