#!/usr/bin/env python3
"""Validate the canonical Skills in skills/.

Checks structure and metadata quality that a reader cannot be trusted to keep consistent
by hand. No third-party dependencies: it runs anywhere python3 does, which is the point.

Usage: python3 tools/validate_skills.py [skills_dir]
Exit code 0 = valid, 1 = errors found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_SKILL_LINES = 200
MIN_DESCRIPTION_CHARS = 120
MAX_DESCRIPTION_CHARS = 1024
VAGUE = ("helps with", "useful for", "various", "etc.", "and more")

errors: list[str] = []
warnings: list[str] = []


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Minimal YAML front-matter reader: top-level `key: value` scalars only."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("#") or line[0].isspace():
            continue
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def check_skill(skill_dir: Path) -> None:
    rel = skill_dir.name
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        errors.append(f"{rel}: missing SKILL.md")
        return

    text = md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{rel}/SKILL.md: missing or malformed YAML front matter")
        return

    name = fm.get("name", "")
    if not name:
        errors.append(f"{rel}/SKILL.md: front matter has no `name`")
    elif name != rel:
        errors.append(f"{rel}/SKILL.md: name '{name}' does not match directory '{rel}'")
    elif not NAME_RE.match(name):
        errors.append(f"{rel}/SKILL.md: name '{name}' is not lowercase-kebab-case")

    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{rel}/SKILL.md: front matter has no `description`")
    else:
        if len(desc) < MIN_DESCRIPTION_CHARS:
            errors.append(
                f"{rel}/SKILL.md: description is {len(desc)} chars; needs >= "
                f"{MIN_DESCRIPTION_CHARS} to state what it does AND when to use it"
            )
        if len(desc) > MAX_DESCRIPTION_CHARS:
            errors.append(f"{rel}/SKILL.md: description exceeds {MAX_DESCRIPTION_CHARS} chars")
        lowered = desc.lower()
        if "not use" not in lowered and "not for" not in lowered:
            errors.append(
                f"{rel}/SKILL.md: description does not say when NOT to use the skill"
            )
        for phrase in VAGUE:
            if phrase in lowered:
                warnings.append(f"{rel}/SKILL.md: description contains vague phrase '{phrase}'")

    if not fm.get("license"):
        warnings.append(f"{rel}/SKILL.md: no `license` field")

    body_lines = text.count("\n")
    if body_lines > MAX_SKILL_LINES:
        errors.append(
            f"{rel}/SKILL.md: {body_lines} lines exceeds the progressive-disclosure budget "
            f"of {MAX_SKILL_LINES}; move detail into references/"
        )

    # Every reference must be reachable from SKILL.md, and every link must resolve.
    ref_dir = skill_dir / "references"
    on_disk = {p.name for p in ref_dir.glob("*.md")} if ref_dir.is_dir() else set()
    linked = set(re.findall(r"(?<![\w/.-])references/([A-Za-z0-9._-]+\.md)", text))
    for missing in sorted(linked - on_disk):
        errors.append(f"{rel}/SKILL.md: links to references/{missing}, which does not exist")
    for orphan in sorted(on_disk - linked):
        errors.append(f"{rel}/references/{orphan}: never referenced from SKILL.md")

    # Cross-skill pointers must resolve too, so renames cannot silently break routing.
    for other, ref in re.findall(r"([a-z0-9-]+)/references/([A-Za-z0-9._-]+\.md)", text):
        if not (skill_dir.parent / other / "references" / ref).is_file():
            errors.append(f"{rel}/SKILL.md: dangling cross-skill link {other}/references/{ref}")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "skills")
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 1

    skills = sorted(p for p in root.iterdir() if p.is_dir())
    if not skills:
        print(f"error: no skills found in {root}", file=sys.stderr)
        return 1

    for skill in skills:
        check_skill(skill)

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")

    print(f"\n{len(skills)} skill(s) checked, {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
