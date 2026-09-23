#!/usr/bin/env python3
"""Report the context cost of the Skills, per progressive-disclosure level.

Token counts are estimates (chars/4), not a tokenizer. They are here so the project's
token-efficiency claims are measurable and reproducible rather than asserted.

Usage:
  python3 tools/measure_context.py [skills_dir]             plain table
  python3 tools/measure_context.py [skills_dir] --markdown  markdown table
  python3 tools/measure_context.py [skills_dir] --write     update the published tables
"""
from __future__ import annotations

import sys
from pathlib import Path


def est_tokens(path: Path) -> int:
    return round(len(path.read_text(encoding="utf-8")) / 4)


def frontmatter_len(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return 0
    end = text.find("\n---\n", 3)
    return round(len(text[4:end]) / 4) if end != -1 else 0


# Files carrying a published measurement table, between MEASUREMENTS markers.
PUBLISHED = ("README.md", "docs/architecture.md", "evals/RESULTS.md")
START, END = "<!-- MEASUREMENTS:START -->", "<!-- MEASUREMENTS:END -->"


def write_published(table: str) -> None:
    """Keep the published tables in sync so they cannot silently drift."""
    root = Path(__file__).resolve().parent.parent
    for name in PUBLISHED:
        path = root / name
        text = path.read_text(encoding="utf-8")
        if START not in text or END not in text:
            print(f"skipped {name}: no MEASUREMENTS markers")
            continue
        i, j = text.index(START) + len(START), text.index(END)
        updated = text[:i] + "\n" + table + "\n" + text[j:]
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {name}")
        else:
            print(f"unchanged {name}")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    markdown = "--markdown" in sys.argv or write
    root = Path(args[0] if args else "skills")

    rows = []
    for skill in sorted(p for p in root.iterdir() if p.is_dir()):
        md = skill / "SKILL.md"
        if not md.is_file():
            continue
        refs = sorted((skill / "references").glob("*.md"))
        rows.append(
            {
                "name": skill.name,
                "l0": frontmatter_len(md),
                "l1": est_tokens(md),
                "l2": sum(est_tokens(r) for r in refs),
                "refs": len(refs),
                "largest_ref": max((est_tokens(r) for r in refs), default=0),
            }
        )

    header = ("skill", "L0 metadata", "L1 SKILL.md", "L2 all refs", "refs", "largest ref")
    if markdown:
        lines = ["| " + " | ".join(header) + " |",
                 "|" + "|".join(["---"] * len(header)) + "|"]
        for r in rows:
            lines.append(
                f"| `{r['name']}` | ~{r['l0']} | ~{r['l1']} | ~{r['l2']} | "
                f"{r['refs']} | ~{r['largest_ref']} |"
            )
        lines.append(
            f"| **all** | **~{sum(r['l0'] for r in rows)}** | **~{sum(r['l1'] for r in rows)}** "
            f"| **~{sum(r['l2'] for r in rows)}** | {sum(r['refs'] for r in rows)} | |"
        )
        table = "\n".join(lines)
        if write:
            write_published(table)
        else:
            print(table)
    else:
        w = max(len(r["name"]) for r in rows) + 2
        print(f"{'skill':<{w}}{'L0':>8}{'L1':>10}{'L2':>10}{'refs':>7}")
        for r in rows:
            print(f"{r['name']:<{w}}{r['l0']:>8}{r['l1']:>10}{r['l2']:>10}{r['refs']:>7}")
        print(f"\n{'TOTAL':<{w}}{sum(r['l0'] for r in rows):>8}"
              f"{sum(r['l1'] for r in rows):>10}{sum(r['l2'] for r in rows):>10}")
        print("\nestimated tokens (chars/4). L0 = always loaded, L1 = on invocation, "
              "L2 = only the reference the task needs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
