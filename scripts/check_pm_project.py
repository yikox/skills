#!/usr/bin/env python3
"""Lint one project-memory PM folder for common consistency issues."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CHANGE_DESIGN_RE = re.compile(r"architecture/modules/[^)\s|]+/changes/[^)\s|]+\.md")
LOCAL_MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)")


@dataclass
class Finding:
    severity: str
    location: str
    issue: str
    suggestion: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_header(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def parse_tables(text: str) -> dict[str, list[dict[str, str]]]:
    tables: dict[str, list[dict[str, str]]] = {}
    current_heading = ""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            current_heading = line.lstrip("#").strip()
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1]):
            headers = [h.strip() for h in line.strip().strip("|").split("|")]
            rows: list[dict[str, str]] = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if len(cells) < len(headers):
                    cells += [""] * (len(headers) - len(cells))
                rows.append(dict(zip(headers, cells)))
                i += 1
            tables[current_heading] = rows
            continue
        i += 1
    return tables


def table_by_names(tables: dict[str, list[dict[str, str]]], names: set[str]) -> tuple[str, list[dict[str, str]]] | tuple[str, None]:
    normalized = {normalize_header(n) for n in names}
    for heading, rows in tables.items():
        if normalize_header(heading) in normalized:
            return heading, rows
    return "", None


def get(row: dict[str, str], *names: str) -> str:
    by_norm = {normalize_header(k): v for k, v in row.items()}
    for name in names:
        value = by_norm.get(normalize_header(name))
        if value is not None:
            return value.strip()
    return ""


def add(findings: list[Finding], severity: str, location: str, issue: str, suggestion: str) -> None:
    findings.append(Finding(severity, location, issue, suggestion))


def extract_field(text: str, field: str) -> str:
    pattern = re.compile(rf"^{re.escape(field)}\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_any_field(text: str, *fields: str) -> str:
    for field in fields:
        value = extract_field(text, field)
        if value:
            return value
    return ""


def extract_multiline_after(text: str, heading: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip().lower().rstrip(":") == heading.lower():
            collected: list[str] = []
            for next_line in lines[idx + 1 :]:
                if next_line.startswith("## ") or re.match(r"^[A-Z][A-Za-z /]+:\s*", next_line):
                    break
                stripped = next_line.strip()
                if stripped and stripped != "-" and not stripped.startswith("<"):
                    collected.append(stripped)
            return "\n".join(collected).strip()
    return ""


def check_local_links(pm_dir: Path, findings: list[Finding]) -> None:
    for path in pm_dir.rglob("*.md"):
        text = read_text(path)
        for match in LOCAL_MD_LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(pm_dir.resolve())
            except ValueError:
                continue
            if not resolved.exists():
                add(
                    findings,
                    "high",
                    str(path.relative_to(pm_dir)),
                    f"Broken local Markdown link: {target}",
                    "Fix the path or remove the stale link.",
                )


def check_design_documents(pm_dir: Path, tables: dict[str, list[dict[str, str]]], findings: list[Finding]) -> None:
    heading, rows = table_by_names(tables, {"Design Documents", "设计文档"})
    if rows is None:
        if (pm_dir / "architecture").exists():
            add(findings, "medium", "project-management.md", "Architecture docs exist but Design Documents section is missing.", "Add or migrate a Design Documents / 设计文档 index.")
        return

    for row in rows:
        path_value = get(row, "Path", "路径")
        status = get(row, "Status", "状态")
        if not path_value:
            continue
        doc_path = (pm_dir / path_value).resolve()
        if not doc_path.exists():
            add(findings, "high", f"project-management.md / {heading}", f"Design path does not exist: {path_value}", "Create the missing doc or update the PM index path.")
            continue
        if "/changes/" in path_value or "\\changes\\" in path_value:
            text = read_text(doc_path)
            design_status = extract_any_field(text, "Design status", "设计状态") or extract_any_field(text, "Status", "状态")
            if status and design_status and normalize_header(status) != normalize_header(design_status):
                add(findings, "medium", path_value, f"PM index status '{status}' differs from design doc status '{design_status}'.", "Sync Design Documents status with the design doc.")

def check_requirements(pm_dir: Path, tables: dict[str, list[dict[str, str]]], findings: list[Finding]) -> None:
    heading, rows = table_by_names(tables, {"Requirements Backlog", "需求待办"})
    if rows is None:
        return

    preferred_columns = {"primary module", "主模块", "change summary", "修改摘要", "scope / impact", "范围 / 影响点"}
    actual_columns = {normalize_header(k) for row in rows for k in row}
    has_preferred_shape = bool(actual_columns.intersection({normalize_header(c) for c in preferred_columns}))
    if rows and not has_preferred_shape:
        add(findings, "low", f"project-management.md / {heading}", "Requirement backlog uses the older compact table shape.", "Migrate future rows to include primary module, change summary, and scope/impact fields.")

    for idx, row in enumerate(rows, start=1):
        req_id = get(row, "ID") or f"row {idx}"
        requirement = get(row, "Requirement", "需求")
        status = get(row, "Status", "状态")
        notes = get(row, "Next Step / Notes", "下一步 / 备注", "Notes", "备注")
        module = get(row, "Primary Module", "主模块", "Module/Area", "模块/范围")
        change = get(row, "Change Summary", "修改摘要")
        impact = get(row, "Scope / Impact", "范围 / 影响点")
        location = f"project-management.md / {heading} / {req_id}"

        if not requirement:
            add(findings, "medium", location, "Requirement text is empty.", "Fill the requirement statement or remove the placeholder row.")
        if not status:
            add(findings, "medium", location, "Requirement status is empty.", "Set a lifecycle status.")

        active_status = normalize_header(status)
        if active_status in {"ready-for-design", "designing", "designed", "accepted", "implementing", "implemented"}:
            if not module:
                add(findings, "medium", location, "Requirement is missing primary module.", "Run pm-record-requirement or pm-review-artifact to identify module ownership.")
            if not change and not notes:
                add(findings, "medium", location, "Requirement is missing change summary.", "Record current-to-target behavior.")
            if not impact and not notes:
                add(findings, "medium", location, "Requirement is missing scope/impact.", "Record scope, non-goals, and impact points.")
        if active_status in {"designed", "accepted", "implementing", "implemented"}:
            design_paths = CHANGE_DESIGN_RE.findall(" ".join(row.values()))
            if not design_paths:
                add(findings, "high", location, f"Status is {status} but no change design path is recorded.", "Add the architecture/modules/.../changes design path or correct the status.")
            for path_value in design_paths:
                if not (pm_dir / path_value).exists():
                    add(findings, "high", location, f"Recorded design path does not exist: {path_value}", "Fix the path or regenerate the design doc.")


def check_change_designs(pm_dir: Path, findings: list[Finding]) -> None:
    modules_dir = pm_dir / "architecture" / "modules"
    if not modules_dir.exists():
        return
    for path in sorted(modules_dir.glob("*/changes/*.md")):
        rel = path.relative_to(pm_dir)
        text = read_text(path)
        status = extract_any_field(text, "Status", "状态")
        design_status = extract_any_field(text, "Design status", "设计状态")
        review_status = extract_any_field(text, "Review status", "审核状态")
        requirement_id = extract_any_field(text, "Requirement ID", "需求 ID", "需求ID")
        implementation_status = extract_any_field(text, "Implementation status", "实现状态")

        if not requirement_id or requirement_id.startswith("<"):
            add(findings, "medium", str(rel), "Change design is missing Requirement ID.", "Link the design to a requirement backlog row.")
        if not review_status:
            add(findings, "medium", str(rel), "Change design is missing Review status.", "Run pm-review-artifact before human confirmation.")
        if status and design_status and normalize_header(status) != normalize_header(design_status):
            add(findings, "low", str(rel), f"Status '{status}' differs from Design status '{design_status}'.", "Use one status vocabulary consistently or explain the distinction.")
        if normalize_header(design_status or status) == "implemented":
            evidence = extract_multiline_after(text, "Implementation evidence") or extract_multiline_after(text, "实现证据")
            if not implementation_status or normalize_header(implementation_status) != "implemented":
                add(findings, "medium", str(rel), "Design is implemented but Implementation status is not implemented.", "Sync implementation status.")
            if not evidence:
                add(findings, "high", str(rel), "Implemented design has no implementation evidence.", "Add commit, PR, file, release, or user confirmation evidence.")

def check_architecture(pm_dir: Path, findings: list[Finding]) -> None:
    arch = pm_dir / "architecture"
    if not arch.exists():
        return
    main_design = arch / "main-design.md"
    if not main_design.exists():
        add(findings, "medium", "architecture/", "Architecture folder exists but architecture/main-design.md is missing.", "Create main-design.md with pm-document-architecture or migrate old architecture README.")
    old_readme = arch / "README.md"
    if old_readme.exists():
        add(findings, "low", "architecture/README.md", "Old architecture README exists.", "Keep it linked or migrate to architecture/main-design.md after approval.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint one project-memory PM folder.")
    parser.add_argument("pm_project_dir", help="Path to PM/<project-slug> folder")
    parser.add_argument("--strict", action="store_true", help="exit non-zero on warnings as well as errors")
    args = parser.parse_args()

    pm_dir = Path(args.pm_project_dir).expanduser().resolve()
    findings: list[Finding] = []
    if not pm_dir.exists():
        print(f"PM project folder does not exist: {pm_dir}", file=sys.stderr)
        return 2

    pm_file = pm_dir / "project-management.md"
    if not pm_file.exists():
        print(f"Missing project-management.md in {pm_dir}", file=sys.stderr)
        return 2

    pm_text = read_text(pm_file)
    tables = parse_tables(pm_text)
    check_requirements(pm_dir, tables, findings)
    check_design_documents(pm_dir, tables, findings)
    check_change_designs(pm_dir, findings)
    check_architecture(pm_dir, findings)
    check_local_links(pm_dir, findings)

    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (severity_order.get(f.severity, 99), f.location, f.issue))

    if not findings:
        print(f"PM project lint passed: {pm_dir}")
        return 0

    print(f"PM project lint found {len(findings)} issue(s):")
    for finding in findings:
        print(f"- [{finding.severity}] {finding.location}")
        print(f"  Issue: {finding.issue}")
        print(f"  Suggested fix: {finding.suggestion}")

    has_high = any(f.severity == "high" for f in findings)
    return 1 if has_high or args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
