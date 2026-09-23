# Repository reconciliation

The failure mode this prevents:

```
intended:  A1 -> A2 -> A3
actual:    A1 + A2 + A3 all partially alive
```

Every agent-assisted iteration that adds without removing leaves a sediment layer. After
enough of them, nobody — human or agent — can tell which version is real, and context
budgets are spent reading code that no longer runs.

## Drift inventory

| Drift | How to find it |
|---|---|
| Old + current implementation side by side | `rg -l -e v1 -e v2 -e _old -e _new -e legacy -e deprecated` |
| Duplicate services/modules | two directories with near-identical exports |
| Parallel pipelines | two code paths triggered by a flag nobody flips |
| Stale adapters | adapter for a provider no longer configured anywhere |
| Obsolete API endpoints | routes with no caller in code, clients, or access logs |
| Dead feature flags | flag read in code, absent from config, or permanently on |
| Stale tests | tests for deleted behaviour, or skipped for > one release |
| Duplicate models | two types for one concept, converted back and forth |
| Contradictory docs | two documents describing the same thing differently |
| Orphaned agent artifacts | accumulated plan/summary/notes Markdown nobody reads |

```bash
# Files nobody references (approximate, run per language)
rg --files -g '*.py' | while read -r f; do
  base=$(basename "$f" .py)
  rg -q --fixed-strings "$base" --glob '!'"$f" || echo "possibly orphaned: $f"
done
```

Treat all of this as **evidence to verify**, never as a delete list.

## Establishing what is true

Do not assume code, tests, README, the newest file, or the latest prompt wins. Inspect, in
roughly this order of authority for "what the system does":

1. **Runtime behaviour** — logs, metrics, traces, a real request.
2. **Deployment/configuration** — what is actually wired up and shipped.
3. **Implementation** — the code on the live path.
4. **Tests** — what someone believed, and defended.
5. **Requirements/ADRs** — what was intended and decided.
6. **README/docs** — what someone wrote once.

For "what the system *should* do", the order inverts: requirements and ADRs lead.

## Classifying a disagreement

| Class | Meaning | Action |
|---|---|---|
| Additive | both true, one is newer scope | merge |
| Refinement | one is a more precise version | keep the precise one |
| Superseding | one replaces the other | retire the old, note the date |
| Conflicting | both cannot be true | escalate with evidence |
| Obsolete | describes a removed thing | delete |
| Duplicate | same content, two places | single source, link the other |
| Experimental | never finished | delete or mark explicitly |
| Ambiguous | cannot tell from the repo | ask the human — with the specific question |

Ask the human only for **conflicting** and genuinely **ambiguous** cases that matter.
Handle the rest.

## Reconciling safely

1. Prove the thing is dead: no imports, no routes, no config, no traffic, no tests that
   fail without it.
2. Remove in one focused commit, separate from behaviour changes, so revert is cheap.
3. Run L2 and the relevant L3 journeys — dead code is often less dead than it looks.
4. Update the documents that referenced it in the same change.
5. If you cannot prove it is dead, do not delete it. Record what you found and move on.

## Keeping the repository from re-accumulating

- Documentation stays authoritative and minimal. Prefer updating a document to adding one.
- Agent-generated Markdown (plans, summaries, notes) is scratch. Give it one directory,
  gitignore it or prune it on merge. Do not let it become a second, false source of truth.
- Retire feature flags with the feature.
- Delete the old path in the same PR that makes the new one default, or file the follow-up
  before merging.
