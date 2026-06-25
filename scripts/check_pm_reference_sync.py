#!/usr/bin/env python3
"""Check consistency of duplicated project-memory skill references."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PM_ROOT = ROOT / "project-memory"

EXACT_BY_FILENAME = {
    "pm-lifecycle-rules.md",
    "pm-design-doc-rules.md",
    "pm-archive-rules.md",
}

SHARED_RULE_PATTERNS = [
    "Read the target file",
    "Preserve user-written",
    "section-level edits",
    "Do not store secrets",
]


def skill_dirs() -> list[Path]:
    return sorted(p for p in PM_ROOT.glob("pm-*") if (p / "SKILL.md").is_file())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_exact(filename: str, verbose: bool) -> list[str]:
    paths = sorted(PM_ROOT.glob(f"pm-*/references/{filename}"))
    if len(paths) < 2:
        return []

    canonical = paths[0]
    canonical_text = read_text(canonical)
    errors: list[str] = []

    for path in paths[1:]:
        text = read_text(path)
        if text == canonical_text:
            continue

        errors.append(f"{filename} drift: {path} differs from {canonical}")
        if verbose:
            diff = difflib.unified_diff(
                canonical_text.splitlines(),
                text.splitlines(),
                fromfile=str(canonical),
                tofile=str(path),
                lineterm="",
            )
            errors.extend(f"  {line}" for line in diff)

    return errors


def check_shared_rules() -> list[str]:
    errors: list[str] = []
    for path in sorted(PM_ROOT.glob("pm-*/references/shared-rules.md")):
        text = read_text(path)
        missing = [pattern for pattern in SHARED_RULE_PATTERNS if pattern not in text]
        if missing:
            errors.append(f"shared-rules baseline missing in {path}: {', '.join(missing)}")
    return errors


def check_frontmatter_name() -> list[str]:
    errors: list[str] = []
    for skill in skill_dirs():
        skill_md = skill / "SKILL.md"
        text = read_text(skill_md)
        expected = f"name: {skill.name}"
        if expected not in text.split("---", 2)[1]:
            errors.append(f"frontmatter name mismatch in {skill_md}; expected {expected}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="print unified diffs for drift")
    args = parser.parse_args()

    errors: list[str] = []
    errors.extend(check_frontmatter_name())
    for filename in sorted(EXACT_BY_FILENAME):
        errors.extend(check_exact(filename, args.verbose))
    errors.extend(check_shared_rules())

    if errors:
        print("PM reference consistency check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("PM reference consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
