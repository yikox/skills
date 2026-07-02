#!/usr/bin/env python3
"""modular-audit 确定性检查脚本。

用法:
    python3 check_modular_project.py <pm-root> [--repo-root <path>] [--exclude <glob>]...

<pm-root> 是包含 project-management.md 与 architecture/ 的项目记忆目录。
提供 --repo-root 时启用代码所有权检查（孤儿/幽灵/重叠）。
--exclude 可重复，追加项目特定的无主路径例外（写在 main-design Shared Constraints 里的那些）。

glob 语义（精确化 2026-07-03 架构变更中的 assumption）：
- 以 `/**` 结尾的模式匹配该目录前缀下的全部文件；
- 其余模式按 fnmatch 匹配完整相对路径。

退出码：存在 error 为 1，仅 warning 为 0。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MODULE_FORMS = {"atomic", "composite"}
MODULE_KINDS = {
    "layout-style", "function-flow", "interface-object", "data-state",
    "event-message", "config-rule", "resource-file", "adapter-io", "utility-support",
}
RELATION_KINDS = {"uses", "reads", "writes", "triggers", "distributes"}
RELATION_STYLES = {"solid", "dashed"}
DESIGN_STATUSES = {"draft", "proposed", "accepted", "implemented", "obsolete"}
REVIEW_STATUSES = {"not-reviewed", "needs-review", "reviewed"}
REQUIRED_MODULE_FIELDS = ["name", "described", "module_form", "module_kind", "status", "review_status"]
DEFAULT_EXCLUDES = ["README*", "LICENSE*", "CLAUDE.md", "AGENTS.md", ".git/**", ".github/**"]

errors: List[str] = []
warnings: List[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_front_matter(text: str) -> Dict[str, object]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    meta: Dict[str, object] = {}
    current_list: Optional[str] = None
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        if re.match(r"^\s+-\s+", line) and current_list:
            meta.setdefault(current_list, [])
            if isinstance(meta[current_list], list):
                meta[current_list].append(line.split("-", 1)[1].strip())
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value == "" :
                current_list = key
                meta[key] = []
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                meta[key] = [v.strip() for v in inner.split(",") if v.strip()]
                current_list = None
            else:
                meta[key] = value
                current_list = None
    return {}


def parse_md_table(section_text: str) -> List[List[str]]:
    rows = []
    for line in section_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= {"-", " ", ":"} for c in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # 去掉表头


def section(text: str, heading: str) -> Optional[str]:
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def glob_match(rel: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        return rel.startswith(pattern[:-3] + "/") or rel == pattern[:-3]
    return fnmatch(rel, pattern)


def check_files(pm: Path) -> None:
    for name in ["project-management.md", "knowledge-summary.md", "architecture/main-design.md"]:
        if not (pm / name).exists():
            error(f"[files] 缺少 {name}")


def check_modules(pm: Path) -> Dict[str, Dict[str, object]]:
    modules: Dict[str, Dict[str, object]] = {}
    mod_dir = pm / "architecture" / "modules"
    if not mod_dir.exists():
        warn("[frontmatter] architecture/modules/ 不存在")
        return modules
    for doc in sorted(mod_dir.glob("*.md")):
        meta = parse_front_matter(doc.read_text(encoding="utf-8"))
        slug = doc.stem
        modules[slug] = meta
        if not meta:
            error(f"[frontmatter] {doc.name} 缺少 front matter")
            continue
        for field in REQUIRED_MODULE_FIELDS:
            if field not in meta:
                error(f"[frontmatter] {doc.name} 缺少字段 {field}")
        if meta.get("module_form") not in MODULE_FORMS:
            error(f"[frontmatter] {doc.name} module_form 非法: {meta.get('module_form')}")
        if meta.get("module_kind") not in MODULE_KINDS:
            error(f"[frontmatter] {doc.name} module_kind 非法: {meta.get('module_kind')}")
        if meta.get("status") not in DESIGN_STATUSES:
            error(f"[frontmatter] {doc.name} status 非法: {meta.get('status')}")
        if meta.get("review_status") not in REVIEW_STATUSES:
            error(f"[frontmatter] {doc.name} review_status 非法: {meta.get('review_status')}")
        if "code_paths" not in meta or not meta.get("code_paths"):
            warn(f"[frontmatter] {doc.name} 缺少 code_paths（建议补齐）")
    return modules


def check_ownership(modules: Dict[str, Dict[str, object]], repo: Path, excludes: List[str]) -> None:
    all_files = [
        f.relative_to(repo).as_posix()
        for f in repo.rglob("*")
        if f.is_file() and not any(part.startswith(".") for part in f.relative_to(repo).parts)
    ]
    claims: Dict[str, List[str]] = {}
    for slug, meta in modules.items():
        for g in meta.get("code_paths") or []:
            matched = [f for f in all_files if glob_match(f, g)]
            if not matched:
                error(f"[ownership] 幽灵 glob：{slug} 的 {g} 匹配不到任何文件")
            for f in matched:
                claims.setdefault(f, []).append(slug)
    for f, owners in sorted(claims.items()):
        if len(set(owners)) > 1:
            error(f"[ownership] 重叠认领：{f} 属于 {sorted(set(owners))}")
    for f in all_files:
        if f in claims:
            continue
        if any(glob_match(f, g) for g in DEFAULT_EXCLUDES + excludes):
            continue
        warn(f"[ownership] 孤儿路径：{f} 未被任何模块认领")


def load_graph(pm: Path) -> Tuple[Optional[dict], Optional[Path]]:
    gp = pm / "architecture" / "graphs" / "current-project.arch.json"
    if not gp.exists():
        warn("[graph] current-project.arch.json 不存在")
        return None, None
    try:
        return json.loads(gp.read_text(encoding="utf-8")), gp
    except json.JSONDecodeError as e:
        error(f"[graph] JSON 解析失败: {e}")
        return None, gp


def check_graph(graph: dict, gp: Path) -> List[Tuple[str, str]]:
    if graph.get("format") not in {"arch-graph/v0.1", "arch-graph/v0.2"}:
        error(f"[graph] format 非法: {graph.get('format')}")
    endpoints = set()
    for obj in graph.get("objects", []):
        endpoints.add(obj.get("id"))
        ref = obj.get("ref")
        if ref and not (gp.parent / ref).resolve().exists():
            error(f"[graph] 对象 {obj.get('id')} 的 ref 不存在: {ref}")
    for grp in graph.get("groups", []):
        endpoints.add(grp.get("id"))
        for itf in grp.get("interfaces", []) or []:
            endpoints.add(f"{grp.get('id')}.{itf.get('id')}")
        ref = grp.get("ref")
        if ref and not (gp.parent / ref).resolve().exists():
            error(f"[graph] 组合 {grp.get('id')} 的 ref 不存在: {ref}")
    pairs: List[Tuple[str, str]] = []
    for rel in graph.get("relations", []):
        frm, to = rel.get("from"), rel.get("to")
        for end in (frm, to):
            if end not in endpoints:
                error(f"[graph] 关系端点不存在: {end}")
        if rel.get("kind") is not None and rel["kind"] not in RELATION_KINDS:
            error(f"[graph] 关系 {frm}->{to} kind 非法: {rel['kind']}（五词表：{sorted(RELATION_KINDS)}）")
        if rel.get("style") is not None and rel["style"] not in RELATION_STYLES:
            error(f"[graph] 关系 {frm}->{to} style 非法: {rel['style']}")
        pairs.append((frm, to))
    return pairs


def check_dependencies_subset(pm: Path, modules: Dict[str, Dict[str, object]], pairs: List[Tuple[str, str]]) -> None:
    known = set(modules)
    for slug in modules:
        doc = pm / "architecture" / "modules" / f"{slug}.md"
        sec = section(doc.read_text(encoding="utf-8"), "Dependencies")
        if sec is None:
            continue
        for row in parse_md_table(sec):
            if len(row) < 2 or not row[0] or row[0] == "-":
                continue
            dep, direction = row[0].strip("`"), row[1].lower()
            if dep not in known:
                warn(f"[consistency] {slug}.md Dependencies 行无法解析为已知模块：{dep}")
                continue
            if direction == "out":
                ok = (slug, dep) in pairs
            elif direction == "in":
                ok = (dep, slug) in pairs
            else:
                warn(f"[consistency] {slug}.md Dependencies 行 Direction 非法：{direction}")
                continue
            if not ok:
                error(f"[consistency] {slug}.md 依赖表有图中不存在的关系：{slug} {direction} {dep}（图为权威，补图或删表行）")


def check_designs(pm: Path) -> None:
    arch = pm / "architecture"
    for pattern in ["changes/*.md", "adrs/*.md", "modules/*/changes/*.md"]:
        for doc in sorted(arch.glob(pattern)):
            meta = parse_front_matter(doc.read_text(encoding="utf-8"))
            rel = doc.relative_to(pm).as_posix()
            if not meta:
                error(f"[designs] {rel} 缺少 front matter")
                continue
            if meta.get("status") not in DESIGN_STATUSES:
                error(f"[designs] {rel} status 非法: {meta.get('status')}")
            if meta.get("review_status") not in REVIEW_STATUSES:
                error(f"[designs] {rel} review_status 非法: {meta.get('review_status')}")


def check_pm_doc(pm: Path) -> None:
    doc = pm / "project-management.md"
    if not doc.exists():
        return
    text = doc.read_text(encoding="utf-8")
    active = section(text, "Active Tasks")
    if active is None:
        error("[pm] 缺少 Active Tasks 章节")
    else:
        for row in parse_md_table(active):
            if len(row) < 5:
                continue
            level = row[4].strip()
            if level in {"L1", "L2", "L3"} and row[2].strip() in {"", "-"}:
                error(f"[pm] Active Task 缺少主模块：{row[1][:40]}")
    index = section(text, "Modular Design Index")
    if index is not None:
        for row in parse_md_table(index):
            if len(row) < 2:
                continue
            path = row[1].strip().strip("`")
            if "/" in path and path.endswith(".md") and not (pm / path).exists():
                error(f"[pm] Design Index 路径不存在：{path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="modular-audit 确定性检查")
    ap.add_argument("pm_root", type=Path)
    ap.add_argument("--repo-root", type=Path, default=None)
    ap.add_argument("--exclude", action="append", default=[])
    args = ap.parse_args()
    pm = args.pm_root.resolve()
    if not pm.is_dir():
        print(f"pm-root 不是目录: {pm}", file=sys.stderr)
        return 2

    check_files(pm)
    modules = check_modules(pm)
    if args.repo_root:
        check_ownership(modules, args.repo_root.resolve(), args.exclude)
    graph, gp = load_graph(pm)
    pairs: List[Tuple[str, str]] = []
    if graph and gp:
        pairs = check_graph(graph, gp)
        check_dependencies_subset(pm, modules, pairs)
    check_designs(pm)
    check_pm_doc(pm)

    for msg in errors:
        print(f"ERROR   {msg}")
    for msg in warnings:
        print(f"WARNING {msg}")
    print(f"\n检查完成：{len(errors)} error, {len(warnings)} warning，模块 {len(modules)} 个。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
