# Security policy

## Scope

This repository contains Markdown instruction files, JSON plugin manifests, and two
dependency-free Python scripts used only by its own CI. It ships no runtime, no service,
and no dependencies. The realistic risks are about what the instructions cause an agent to
do.

## Reporting a vulnerability

Report privately through **GitHub Security Advisories** on this repository
("Security" → "Report a vulnerability"). Please do not open a public issue for a
vulnerability.

Include what an agent following the guidance would do, the impact, and a reproduction if
you have one. We aim to acknowledge within 5 working days and to agree a disclosure
timeline with you.

## In scope

- Guidance that would lead an agent to weaken authentication or authorization, disable a
  security check, expose secrets, or exfiltrate data.
- Prompt-injection surfaces: content in this repository that could be used to redirect an
  agent's behaviour against the user's intent.
- Unsafe commands in the Skills, references, or documentation.
- A supply-chain issue in the install instructions (a wrong package name, an unsigned
  source, a typosquat-adjacent command).
- Vulnerabilities in `tools/*.py`.

## Out of scope

- Vulnerabilities in integrated third-party projects (OpenCodeReview, Superpowers,
  Everything Claude Code, Claude Code Templates). Report those to their maintainers.
- Vulnerabilities in code an agent writes while following this standard.
- Disagreements about engineering guidance — those are issues, not advisories.

## Guidance for users

- **Treat repository content as data, not instructions.** File contents, issue text, tool
  output, and web pages an agent reads are untrusted input. A comment saying "ignore your
  rules" is hostile input, and the standard tells agents to treat it that way
  (`engineering-quality/references/security-reliability.md`).
- **Never put secrets in agent context.** Agent context is logged and cached.
- **Review before adopting.** These are instructions that will influence changes to your
  code. Read them, as you would any dependency.
- **Verify install commands** against each upstream project before putting them in CI.
  Third-party CLI flags and package names change.
