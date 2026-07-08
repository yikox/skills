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

errors: List[str] = []
warnings: List[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# 受控词表内置默认值（fallback）。单一事实源是 _shared/references/vocab.md；
# load_vocab() 在启动时用清单覆盖这些默认值，解析失败时回退到这里并告警。
_FALLBACK_VOCAB = {
    "module_form": {"atomic", "composite"},
    "module_kind": {
        "layout-style", "function-flow", "interface-object", "data-state",
        "event-message", "config-rule", "resource-file", "adapter-io", "utility-support",
    },
    "relation_kind": {"uses", "reads", "writes", "triggers", "distributes"},
    "relation_style": {"solid", "dashed"},
    "design_status": {"draft", "proposed", "accepted", "implemented", "obsolete"},
    "review_status": {"not-reviewed", "needs-review", "reviewed"},
}

# vocab.md 相对本脚本的位置：<root>/modular-audit/scripts/ 与 <root>/_shared/ 同层
# （仓库内 <root>=modular-programming，安装后 <root>=目标 skills 目录），故上溯三级到 <root>。
VOCAB_PATH = Path(__file__).resolve().parents[2] / "_shared" / "references" / "vocab.md"
_TOKEN_RE = re.compile(r"`([^`]+)`")


def load_vocab(path: Path = VOCAB_PATH) -> Dict[str, set]:
    """解析 vocab.md 得到受控词表；任何缺失/异常都回退到 _FALLBACK_VOCAB 并告警。"""
    result = {k: set(v) for k, v in _FALLBACK_VOCAB.items()}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        warn(f"[vocab] 未找到词表清单 {path}，回退内置默认词表")
        return result
    parsed: Dict[str, set] = {}
    current: Optional[str] = None
    for line in text.splitlines():
        # 任何二级标题都结束上一节：命中词表名则开始收集，否则置空，
        # 避免非词表小节（如“解析约定”）里的反引号 token 泄漏到上一词表。
        if line.startswith("## "):
            name = line[3:].strip()
            current = name if name in _FALLBACK_VOCAB else None
            continue
        if current in _FALLBACK_VOCAB:
            tokens = _TOKEN_RE.findall(line)
            if tokens:
                parsed.setdefault(current, set()).update(tokens)
    for name in _FALLBACK_VOCAB:
        if parsed.get(name):
            result[name] = parsed[name]
        else:
            warn(f"[vocab] 清单缺少词表 `{name}`，该项回退内置默认值")
    return result


_VOCAB = load_vocab()
MODULE_FORMS = _VOCAB["module_form"]
MODULE_KINDS = _VOCAB["module_kind"]
RELATION_KINDS = _VOCAB["relation_kind"]
RELATION_STYLES = _VOCAB["relation_style"]
DESIGN_STATUSES = _VOCAB["design_status"]
REVIEW_STATUSES = _VOCAB["review_status"]
REQUIRED_MODULE_FIELDS = ["name", "described", "module_form", "module_kind", "status", "review_status"]
DEFAULT_EXCLUDES = ["README*", "LICENSE*", "CLAUDE.md", "AGENTS.md", ".git/**", ".github/**"]


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


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
                meta[current_list].append(_unquote(line.split("-", 1)[1].strip()))
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value == "" :
                current_list = key
                meta[key] = []
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                meta[key] = [_unquote(v.strip()) for v in inner.split(",") if v.strip()]
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
    documented_non_owner_globs: List[str] = []
    for slug, meta in modules.items():
        for g in meta.get("code_paths") or []:
            matched = [f for f in all_files if glob_match(f, g)]
            if not matched:
                error(f"[ownership] 幽灵 glob：{slug} 的 {g} 匹配不到任何文件")
            for f in matched:
                claims.setdefault(f, []).append(slug)
        for field in ("shared_paths", "ignored_paths"):
            for g in meta.get(field) or []:
                if not any(glob_match(f, g) for f in all_files):
                    warn(f"[ownership] 幽灵例外 glob：{slug} 的 {field} {g} 匹配不到任何文件")
                documented_non_owner_globs.append(g)
    for f, owners in sorted(claims.items()):
        if len(set(owners)) > 1:
            error(f"[ownership] 重叠认领：{f} 属于 {sorted(set(owners))}")
    exception_globs = DEFAULT_EXCLUDES + excludes + documented_non_owner_globs
    for f in all_files:
        if f in claims:
            continue
        if any(glob_match(f, g) for g in exception_globs):
            continue
        warn(f"[ownership] 孤儿路径：{f} 未被任何模块认领")


def load_graph(pm: Path) -> Tuple[Optional[dict], Optional[Path]]:
    gp = pm / "architecture" / "graphs" / "current-project.arch.json"
    if not gp.exists():
        return None, None
    try:
        return json.loads(gp.read_text(encoding="utf-8")), gp
    except json.JSONDecodeError as e:
        error(f"[graph] JSON 解析失败: {e}")
        return None, gp


def check_graph(graph: dict, gp: Path) -> List[Tuple[str, str]]:
    fmt = graph.get("format")
    if fmt not in {"arch-graph/v0.1", "arch-graph/v0.2", "arch-graph/v0.3"}:
        error(f"[graph] format 非法: {fmt}")
    # v0.3 引入的结构约束（contains 森林、interface provider 子树、同层 scope）
    # 对仍在白名单内的 v0.1/v0.2 老图降级为 warning，避免旧图直接从通过变成 exit 1。
    structural = error if fmt == "arch-graph/v0.3" else warn
    endpoints = set()
    object_ids = set()
    group_ids = set()
    group_docs: Dict[str, dict] = {}
    contains_by_group: Dict[str, List[str]] = {}
    interface_groups: Dict[str, str] = {}
    parent_by_member: Dict[str, str] = {}

    def add_endpoint(endpoint_id: object, label: str) -> Optional[str]:
        if not isinstance(endpoint_id, str) or not endpoint_id:
            error(f"[graph] {label} 缺少有效 id")
            return None
        if endpoint_id in endpoints:
            error(f"[graph] 重复端点 id: {endpoint_id}")
        endpoints.add(endpoint_id)
        return endpoint_id

    for obj in graph.get("objects", []):
        obj_id = add_endpoint(obj.get("id"), "对象")
        if obj_id:
            object_ids.add(obj_id)
        ref = obj.get("ref")
        if ref and not (gp.parent / ref).resolve().exists():
            error(f"[graph] 对象 {obj.get('id')} 的 ref 不存在: {ref}")
    for grp in graph.get("groups", []):
        group_id = add_endpoint(grp.get("id"), "组合")
        if group_id:
            group_ids.add(group_id)
            group_docs[group_id] = grp
        ref = grp.get("ref")
        if ref and not (gp.parent / ref).resolve().exists():
            error(f"[graph] 组合 {grp.get('id')} 的 ref 不存在: {ref}")

    all_node_ids = object_ids | group_ids
    for group_id, grp in group_docs.items():
        contains = grp.get("contains")
        if not isinstance(contains, list) or not all(isinstance(member, str) for member in contains):
            structural(f"[graph] 组合 {group_id} 缺少有效 contains 字符串数组")
            contains_by_group[group_id] = []
        else:
            contains_by_group[group_id] = contains
        for member in contains_by_group[group_id]:
            if member not in all_node_ids:
                structural(f"[graph] 组合 {group_id} contains 未知成员: {member}")
                continue
            if member == group_id:
                structural(f"[graph] 组合 {group_id} 不能包含自身")
                continue
            if member in parent_by_member:
                structural(f"[graph] 成员 {member} 被多个 group 包含: {parent_by_member[member]}, {group_id}")
                continue
            parent_by_member[member] = group_id

    visiting: List[str] = []
    visited = set()

    def visit_group(group_id: str) -> None:
        if group_id in visited:
            return
        if group_id in visiting:
            cycle = " -> ".join(visiting[visiting.index(group_id):] + [group_id])
            structural(f"[graph] group contains 成环: {cycle}")
            return
        visiting.append(group_id)
        for member in contains_by_group.get(group_id, []):
            if member in group_ids:
                visit_group(member)
        visiting.pop()
        visited.add(group_id)

    for group_id in sorted(group_ids):
        visit_group(group_id)

    def collect_subtree_objects(group_id: str, seen: Optional[set] = None) -> set:
        if seen is None:
            seen = set()
        if group_id in seen:
            return set()
        seen.add(group_id)
        result = set()
        for member in contains_by_group.get(group_id, []):
            if member in object_ids:
                result.add(member)
            elif member in group_ids:
                result.update(collect_subtree_objects(member, seen))
        return result

    for group_id, grp in group_docs.items():
        subtree_objects = collect_subtree_objects(group_id)
        for itf in grp.get("interfaces", []) or []:
            interface_id = itf.get("id")
            if not isinstance(interface_id, str) or not interface_id or "." in interface_id:
                structural(f"[graph] 组合 {group_id} interface id 非法: {interface_id}")
                continue
            endpoint_id = f"{group_id}.{interface_id}"
            add_endpoint(endpoint_id, f"组合 {group_id} interface")
            interface_groups[endpoint_id] = group_id
            providers = itf.get("provided_by") or []
            if not isinstance(providers, list) or not all(isinstance(provider, str) for provider in providers):
                structural(f"[graph] interface {endpoint_id} provided_by 必须是字符串数组")
                continue
            for provider in providers:
                if provider not in object_ids:
                    structural(f"[graph] interface {endpoint_id} provider 不存在或不是对象: {provider}")
                elif provider not in subtree_objects:
                    structural(f"[graph] interface {endpoint_id} provider {provider} 不在 {group_id} 的 contains 子树内")

    endpoint_scope: Dict[str, Optional[str]] = {}
    for object_id in object_ids:
        endpoint_scope[object_id] = parent_by_member.get(object_id)
    for group_id in group_ids:
        endpoint_scope[group_id] = parent_by_member.get(group_id)
    for endpoint_id, group_id in interface_groups.items():
        endpoint_scope[endpoint_id] = parent_by_member.get(group_id)

    def scope_name(endpoint_id: str) -> str:
        scope = endpoint_scope.get(endpoint_id)
        return "top" if scope is None else scope

    pairs: List[Tuple[str, str]] = []
    for rel in graph.get("relations", []):
        frm, to = rel.get("from"), rel.get("to")
        for end in (frm, to):
            if end not in endpoints:
                error(f"[graph] 关系端点不存在: {end}")
        if frm in endpoints and to in endpoints and endpoint_scope.get(frm) != endpoint_scope.get(to):
            structural(f"[graph] 关系 {frm}->{to} 跨 scope：{scope_name(frm)} -> {scope_name(to)}")
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
                error(f"[consistency] {slug}.md 依赖表有图中不存在的关系：{slug} {direction} {dep}（维护图为权威可视化来源，补图或删表行）")


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


def check_plans(pm: Path) -> None:
    arch = pm / "architecture"
    for pattern, expected_level in [("plans/*.md", "L3"), ("modules/*/plans/*.md", "L2")]:
        for doc in sorted(arch.glob(pattern)):
            meta = parse_front_matter(doc.read_text(encoding="utf-8"))
            rel = doc.relative_to(pm).as_posix()
            if not meta:
                error(f"[plans] {rel} 缺少 front matter")
                continue
            src = meta.get("source_design")
            patch = meta.get("source_patch")
            if isinstance(src, str) and src:
                if Path(src).is_absolute() or not (pm / src).resolve().is_relative_to(pm):
                    error(f"[plans] {rel} source_design 越出 pm 根目录: {src}")
                elif not (pm / src).exists():
                    error(f"[plans] {rel} source_design 路径不存在: {src}")
                else:
                    smeta = parse_front_matter((pm / src).read_text(encoding="utf-8"))
                    if smeta.get("status") == "implemented":
                        warn(f"[plans] {rel} 的源设计已 implemented，计划应归档或删除")
            elif not isinstance(patch, str) or not patch:
                error(f"[plans] {rel} 缺少 source_design 或 source_patch")
            level = meta.get("level")
            if level not in {"L2", "L3"}:
                error(f"[plans] {rel} level 非法: {level}")
            elif level != expected_level:
                error(f"[plans] {rel} level {level} 与所在目录不符（plans/ 存 L3，modules/*/plans/ 存 L2）")


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
    check_plans(pm)
    check_pm_doc(pm)

    for msg in errors:
        print(f"ERROR   {msg}")
    for msg in warnings:
        print(f"WARNING {msg}")
    print(f"\n检查完成：{len(errors)} error, {len(warnings)} warning，模块 {len(modules)} 个。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
