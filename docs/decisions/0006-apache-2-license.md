# ADR-0006: Apache-2.0 licence

- **Status:** Accepted
- **Date:** 2026-09-23

## Context

The project must be permissively licensed for public adoption, and must be compatible with
the projects it integrates with.

## Decision

Apache-2.0.

## Rationale

- Permissive, and widely accepted in corporate environments.
- Includes an express patent grant, which MIT does not — relevant for a standard intended
  for commercial adoption.
- Matches OpenCodeReview (Apache-2.0), the project we integrate most closely with.
- Compatible with the MIT-licensed projects we reference (Superpowers, Everything Claude
  Code, Claude Code Templates).

## Licence review of integrated projects

| Project | Licence | Our use |
|---|---|---|
| alibaba/open-code-review | Apache-2.0 | called as a CLI; no code copied |
| obra/superpowers | MIT | referenced and recommended; no code copied |
| affaan-m/everything-claude-code | MIT | referenced; no code copied |
| davila7/claude-code-templates | MIT | install commands documented; no code copied |

No source, prompt text, or documentation from any of these projects is vendored into this
repository. All content here is original. If that ever changes, the relevant notice and
attribution requirements must be honoured in `NOTICE`.

## Consequences

- Contributions are Apache-2.0; `CONTRIBUTING.md` states this.
- Each Skill carries `license: Apache-2.0` in its front matter, so a copied-out skill file
  keeps its licence.
