# Versioning and releases

## Scheme

[Semantic Versioning](https://semver.org). The public interface of this project is **the
behaviour the Skills produce**, plus the names and file paths adopters depend on.

| Bump | Means | Examples |
|---|---|---|
| **Major** | An adopter must change something, or the guidance now materially contradicts the previous version. | Renaming or removing a skill; moving `skills/`; reversing a rule; changing plugin manifest paths. |
| **Minor** | New capability, backward compatible. | A new skill; a new reference file; a new integration; a new eval scenario; a substantive new rule. |
| **Patch** | No behavioural change for adopters. | Clarifications, typos, corrected external commands, tightened wording, tooling fixes, eval results. |

Renaming a `references/` file is a **minor** bump if `SKILL.md` still routes correctly, and
**major** if adopters could be linking to it directly.

Pre-1.0: the eval suite has not been run, so guidance may change on evidence. Minor
versions may carry more change than they would after 1.0. Pin a tag if that matters to you.

## Version locations

Kept in sync; CI checks them:

- `.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → `plugins[0].version`
- `.codex-plugin/plugin.json` → `version`
- each `skills/*/SKILL.md` → `metadata.version`
- `CHANGELOG.md` → the release heading

## Release process

1. Update `CHANGELOG.md` (move `Unreleased` into a dated version heading).
2. Bump the version in every location above.
3. `python3 tools/validate_skills.py` and `python3 tools/measure_context.py`.
4. Refresh the measurement tables in `README.md`, `docs/architecture.md`, and
   `evals/RESULTS.md` if skill sizes changed.
5. Tag `vX.Y.Z` and push; create a GitHub release with the changelog section as its body.

## What reaching 1.0 requires

1. The twelve eval scenarios run against at least two agents, with published
   baseline-vs-treatment numbers.
2. Failures found by those evals fixed, or documented as accepted limitations.
3. Real adoption feedback from repositories the maintainers did not write.

Until then the project is pre-1.0 and says so.

## Deprecation

Announce in `CHANGELOG.md` one minor version before removal, keep the old path working for
that version where feasible, and state the replacement. Practise the reconciliation the
standard preaches: remove the old thing rather than leaving both alive.
