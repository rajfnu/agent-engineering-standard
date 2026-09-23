# OpenCodeReview integration

[OpenCodeReview](https://github.com/alibaba/open-code-review) (`ocr`) is an Apache-2.0
code-review CLI from Alibaba. It combines deterministic pipelines (file selection, file
bundling, rule matching, comment positioning) with an LLM agent. Per its published
benchmark it reaches higher precision and F1 than a general-purpose agent on the same
model while using roughly **1/9 the tokens**, with lower recall — a deliberate trade
against noise.

This standard **integrates** it rather than reimplementing it. Everything below is
optional: the `engineering-review` skill degrades to a bounded manual pass when `ocr` is
absent.

## Install

```bash
npm install -g @alibaba-group/open-code-review   # requires Git >= 2.41
ocr config provider     # pick/add a provider, enter the API key
ocr config model        # pick a model
ocr llm test            # verify connectivity
```

Other install methods (script, release binary, source) are in the project's docs.

## Commands this standard uses

```bash
# Review a branch against its merge base, JSON for the agent to consume
ocr review --from main --to HEAD --format json --output .aes/ocr.json

# Review uncommitted work (staged + unstaged + untracked)
ocr review

# Review a single commit
ocr review --commit <sha>

# Resume an interrupted review
ocr session list
ocr review --from main --to HEAD --resume <session-id>

# Audit a directory with no meaningful diff
ocr scan --path <dir>

# Delegation mode: OCR picks files and rules, your agent does the reading.
# No OCR model endpoint needed.
ocr delegate preview
ocr delegate rule <file> [<file> ...]
```

Verify flags against `ocr --help` for your installed version before scripting them.

## Division of labour

| Concern | Owner |
|---|---|
| Which files to review, which to filter | OCR (deterministic) |
| Grouping related files into review units | OCR |
| Matching review rules to file characteristics | OCR |
| Line-level defects: NPE, concurrency, injection, XSS, resource leaks | OCR |
| Accurate comment positioning | OCR |
| Capability scope and blast radius | this standard |
| Architecture and boundary violations | this standard |
| Contract compatibility | this standard |
| Test level selection and test quality | this standard |
| Repository drift and duplicate implementations | this standard |
| UX and accessibility | this standard |
| Final ranked assessment | this standard |

Do not duplicate the left column. If OCR reported it, cite it; do not re-derive it.

## Consuming the JSON

`--format json --output <path>` is the recommended shape for a host agent: read the file,
fold its findings into your report, and drop the ones your architecture analysis shows to
be false positives — saying why. Do not paste the raw JSON into your report.

Write OCR output under a gitignored scratch directory (`.aes/`), not into the repository.

## CI

OCR documents GitHub Actions, GitLab CI, GitFlic CI, and Gerrit integrations. A minimal
gate:

```yaml
# fetch-depth: 0 matters — OCR needs the base branch in the clone to compute a merge base.
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
- run: npm install -g @alibaba-group/open-code-review
- run: ocr review --from "origin/${{ github.base_ref }}" --to HEAD --format json --output ocr.json
  env:
    # provider key from repository secrets
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

Gate on blockers only. A review that fails the build on style findings gets disabled
within a week.

## Agent-native integrations

OCR ships its own plugins, which you may install alongside this standard:

```text
# Claude Code
/plugin marketplace add alibaba/open-code-review
/plugin install open-code-review@open-code-review
```

```bash
# Codex
codex plugin marketplace add alibaba/open-code-review
```

Cursor, Kimi Code, OpenCode, and other skill-compatible agents are covered in the OCR
repository's `plugins/open-code-review/README.md`.

## Licence and attribution

OCR is Apache-2.0. This standard does not vendor or copy OCR code — it calls the CLI and
reads its output. Keep it that way; if you ever do copy code, preserve the licence header
and attribution.
