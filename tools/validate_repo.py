#!/usr/bin/env python3
"""Repository-level checks: version consistency, internal links, measurement freshness.

These are exactly the drift the standard tells other repositories to prevent, so this
project enforces them on itself. No third-party dependencies.

Usage: python3 tools/validate_repo.py
Exit code 0 = valid, 1 = errors found.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []

SKIP_DIRS = {".git", ".aes", "__pycache__", ".github"}
MEASURED = ("README.md", "docs/architecture.md", "evals/RESULTS.md")


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def check_versions() -> None:
    """Every manifest and skill must declare the same version."""
    found: dict[str, str] = {}

    for path, keys in (
        (".claude-plugin/plugin.json", ("version",)),
        (".codex-plugin/plugin.json", ("version",)),
    ):
        data = json.loads((ROOT / path).read_text(encoding="utf-8"))
        for key in keys:
            found[f"{path}:{key}"] = data[key]

    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    found[".claude-plugin/marketplace.json:plugins[0].version"] = market["plugins"][0]["version"]

    for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
        m = re.search(r"^\s+version:\s*(\S+)\s*$", skill_md.read_text(encoding="utf-8"), re.M)
        if m:
            found[f"{rel(skill_md)}:metadata.version"] = m.group(1)
        else:
            errors.append(f"{rel(skill_md)}: no metadata.version")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.M)
    if m:
        found["CHANGELOG.md:latest release"] = m.group(1)
    else:
        errors.append("CHANGELOG.md: no released version heading found")

    distinct = set(found.values())
    if len(distinct) > 1:
        errors.append("version mismatch across declarations:")
        for where, value in sorted(found.items()):
            errors.append(f"    {value}  <- {where}")


def check_manifest_targets() -> None:
    """Adapter manifests must point at directories that exist."""
    for path in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        data = json.loads((ROOT / path).read_text(encoding="utf-8"))
        for key in ("skills", "commands"):
            target = data.get(key)
            if target and not (ROOT / target.lstrip("./")).is_dir():
                errors.append(f"{path}: `{key}` points at missing directory {target}")


def check_links() -> None:
    """Relative Markdown links must resolve."""
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for md in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in md.parts):
            continue
        for target in pattern.findall(md.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (md.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                errors.append(f"{rel(md)}: broken link -> {target}")


def check_measurements() -> None:
    """The published measurement tables must match what the tool reports now."""
    current = subprocess.run(
        [sys.executable, str(ROOT / "tools/measure_context.py"), str(ROOT / "skills"), "--markdown"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    for name in MEASURED:
        text = (ROOT / name).read_text(encoding="utf-8")
        start, end = "<!-- MEASUREMENTS:START -->", "<!-- MEASUREMENTS:END -->"
        if start not in text or end not in text:
            errors.append(f"{name}: missing MEASUREMENTS markers")
            continue
        block = text[text.index(start) + len(start):text.index(end)].strip()
        if block != current:
            errors.append(
                f"{name}: measurement table is stale; regenerate with "
                f"`python3 tools/measure_context.py skills --markdown`"
            )


def main() -> int:
    check_versions()
    check_manifest_targets()
    check_links()
    check_measurements()

    for e in errors:
        print(f"error: {e}" if not e.startswith("    ") else e)
    print(f"\nrepository checks: {len([e for e in errors if not e.startswith('    ')])} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
