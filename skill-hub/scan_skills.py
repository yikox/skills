#!/usr/bin/env python3
"""
scan_skills.py - 本机全盘 Skill 深度扫描器（零第三方依赖）

特点：
1. 严格只扫描含 SKILL.md 的标准 Skill 目录，不混入 CLAUDE.md / AGENTS.md 等其他文件。
2. 穿透所有隐藏目录（~/.claude, ~/.codex, ~/.cursor, ~/.agents, ~/.workbuddy, ~/.trae 等及各项目内隐藏目录）
   与符号链接目录（带 inode 环路保护），结合 macOS Spotlight (mdfind) 双重校验，确保零遗漏。
3. 自动区分「用户已安装/源码仓/项目级 Skill」与「第三方插件商城缓存/系统内置 Skill」，
   聚合同名 Skill 的多处拷贝，计算哈希一致性、版本分叉 (Drift) 与符号链接指向。

命令行用法：
  python3 scan_skills.py                     # 全盘实时扫描 ~ 目录并输出汇总表 + 保存 vault/skills_index.json
  python3 scan_skills.py --root ~/Work       # 仅扫描指定目录
  python3 scan_skills.py --reaggregate       # 基于已有 vault/skills_index.json 快速重算分类与聚合
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


HOME_DIR = Path(os.path.expanduser("~")).resolve()
BASE_DIR = Path(__file__).resolve().parent
INDEX_OUTPUT_PATH = BASE_DIR / "vault" / "skills_index.json"

SKIP_DIR_NAMES: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "bower_components",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".npm",
    ".pnpm-store",
    ".yarn",
    ".cargo",
    ".rustup",
    ".gradle",
    ".m2",
    ".cache",
    "dist",
    "build",
    ".build",
    "target",
    "DerivedData",
    "Pods",
    ".next",
    ".nuxt",
    ".turbo",
    ".Trash",
    "Pictures",
    "Music",
    "Movies",
}

SKIP_LIBRARY_SUBDIRS: Set[str] = {
    "Caches",
    "Containers",
    "Group Containers",
    "Developer",
    "Logs",
    "Mail",
    "Messages",
    "Metadata",
    "Photos",
    "Safari",
    "Saved Application State",
    "WebKit",
    "Keychains",
    "Cookies",
    "Accounts",
    "Biome",
    "Calendars",
    "IdentityServices",
    "Reminders",
    "Suggestions",
    "Trial",
    "Updates",
    "Weather",
}

MARKETPLACE_CACHE_MARKERS: Tuple[str, ...] = (
    "/plugins/marketplaces/",
    "/connectors-marketplace/",
    "/.marketplace-plugin-source-staging/",
    "/.codex/.tmp/",
    "/.codex/worktrees/",
    "/.worktrees/",
    "/src-tauri/target/",
    "/plugins/cache/",
    "/vendor_imports/",
    "/miniforge3/lib/",
    "/.vscode/extensions/",
    "/.vscode/agent-plugins/",
    "/skills-cursor/",
    "/skills/.system/",
    "/.gemini/antigravity/",
    "/Library/Application Support/Antigravity/",
    "/Library/Application Support/com.plexus.app/",
)

OTHER_AGENT_PREFIXES: Tuple[str, ...] = (
    "~/.adal/",
    "~/.augment/",
    "~/.codebuddy/",
    "~/.codeium/",
    "~/.commandcode/",
    "~/.config/crush/",
    "~/.config/goose/",
    "~/.config/opencode/",
    "~/.continue/",
    "~/.factory/",
    "~/.iflow/",
    "~/.junie/",
    "~/.kilocode/",
    "~/.kiro/",
    "~/.kode/",
    "~/.mcpjam/",
    "~/.mux/",
    "~/.neovate/",
    "~/.openclaw/",
    "~/.openhands/",
    "~/.pi/",
    "~/.pochi/",
    "~/.qoder/",
    "~/.qwen/",
    "~/.roo/",
    "~/.snowflake/",
    "~/.trae/",
    "~/.trae-cn/",
    "~/.vibe/",
    "~/.zencoder/",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm_hash_text(text: str) -> str:
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)
    # 兼容 aimaster-tools 二级分类目录安装到全局扁平目录时的相对链接改写
    body = re.sub(
        r"\.\./\.\./(?:platform|remote|optimization|authoring|common)/",
        r"../",
        body,
    )
    body = re.sub(r"\s+", " ", body).strip()
    return sha256_text(body)


def resolve_skill_group_name(skill_md_path: Path) -> str:
    skill_dir = skill_md_path.parent
    dir_name = skill_dir.name
    # 若位于某个父级 Skill 的 modules/ 子目录下（如 infer-algo-deploy-flow/modules/aimaster-runtime），独立命名避免与顶层同名 Skill 混淆
    if skill_dir.parent.name == "modules" and skill_dir.parent.parent.name:
        return f"{skill_dir.parent.parent.name}/{dir_name}"
    return dir_name


def parse_skill_frontmatter(text: str, default_name: str) -> Tuple[str, str]:
    fm_name = default_name
    desc = ""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            s = line.strip()
            if s.startswith("name:"):
                val = s.split(":", 1)[1].strip().strip('"').strip("'")
                if val:
                    fm_name = val
            elif s.startswith("description:"):
                val = s.split(":", 1)[1].strip().strip('"').strip("'")
                if val:
                    desc = val
    if not desc:
        body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)
        for line in body.splitlines():
            s = line.strip()
            if s and not s.startswith("#") and not s.startswith("<!--") and not s.startswith("```"):
                desc = s
                break
    return fm_name, desc[:200]


def classify_skill_location(skill_md_path: Path) -> Tuple[str, str, Optional[str], bool]:
    """
    返回: (scope, scope_label, app_key, is_marketplace_cache)
    scope:
      - source_repo      (~/Work/skills/zh, ~/MTGIT/aimaster-tools, ~/MTGIT/mtpipe-skill/.agents/skills)
      - claude_global    (~/.claude/skills, ~/claude/skills)
      - codex_global     (~/.codex/skills, ~/codex/skills)
      - cursor_global    (~/.cursor/skills)
      - agents_global    (~/.agents/skills)
      - workbuddy_global (~/.workbuddy/skills)
      - other_agents     (~/.trae, ~/.qwen, ~/.codebuddy, ~/.roo 等其他 Agent 全局目录)
      - project_local    (各代码仓库/iCloud 文档内的项目级 Skill)
      - marketplace_cache(插件商城目录、.tmp 缓存、内置扩展)
    """
    p = str(skill_md_path)
    p_lower = p.lower()
    rel = p.replace(str(HOME_DIR), "~")

    if any(marker.lower() in p_lower for marker in MARKETPLACE_CACHE_MARKERS):
        return "marketplace_cache", "插件商城 / 系统缓存", None, True

    # 主控仓与团队源码仓（兼容 macOS 大小写 /work/skills 与 /Work/skills）
    if "/work/skills/zh/" in p_lower:
        return "source_repo", "主控源仓 (~/Work/skills)", None, False
    if "/mtgit/aimaster-tools/skills/" in p_lower:
        return "source_repo", "团队源仓 (aimaster-tools)", None, False
    if "/mtgit/mtpipe-skill/.agents/skills/" in p_lower:
        return "source_repo", "团队源仓 (mtpipe-skill)", None, False

    if rel.startswith("~/.claude/skills/") or rel.startswith("~/claude/skills/"):
        return "claude_global", "Claude 全局 (~/.claude)", "claude", False
    if rel.startswith("~/.codex/skills/") or rel.startswith("~/codex/skills/"):
        return "codex_global", "Codex 全局 (~/.codex)", "codex", False
    if rel.startswith("~/.cursor/skills/"):
        return "cursor_global", "Cursor 全局 (~/.cursor)", "cursor", False
    if rel.startswith("~/.agents/skills/"):
        return "agents_global", "Agents 全局 (~/.agents)", "agents", False
    if rel.startswith("~/.workbuddy/skills/"):
        return "workbuddy_global", "WorkBuddy 全局 (~/.workbuddy)", "workbuddy", False

    if any(rel.startswith(prefix) for prefix in OTHER_AGENT_PREFIXES):
        agent_folder = rel.split("/")[1]
        return "other_agents", f"其他 Agent ({agent_folder})", None, False

    if "/library/mobile documents/" in p_lower:
        return "project_local", "iCloud 云文档项目", None, False

    return "project_local", "项目/工作区局部 Skill", None, False


def list_companion_files(skill_dir: Path, max_files: int = 25) -> List[str]:
    files: List[str] = []
    try:
        for root, dirs, filenames in os.walk(skill_dir, followlinks=False):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", "node_modules", ".venv"}]
            for fn in sorted(filenames):
                if fn in {"SKILL.md", "skill.md", ".DS_Store"} or fn.endswith(".pyc"):
                    continue
                rel = os.path.relpath(os.path.join(root, fn), skill_dir)
                files.append(rel)
                if len(files) >= max_files:
                    return files
    except Exception:
        pass
    return files


def discover_skill_files_live(root_dir: Path) -> List[Path]:
    found_paths: Dict[str, Path] = {}
    self_hub_prefix = str(BASE_DIR.resolve())
    aihub_stage_prefix = str(HOME_DIR / ".aihub")

    def _should_skip_path(p_str: str) -> bool:
        if p_str.startswith(self_hub_prefix) or p_str.startswith(aihub_stage_prefix):
            return True
        if "/.Trash/" in p_str or "/node_modules/" in p_str or "/.git/" in p_str:
            return True
        return False

    visited_real_dirs: Set[Tuple[int, int]] = set()
    queue: List[Path] = [root_dir]

    while queue:
        curr_dir = queue.pop(0)
        curr_str = str(curr_dir)
        if _should_skip_path(curr_str):
            continue

        try:
            st = curr_dir.stat()
            # SF_DATALESS 标记表示目录尚未下载，遍历可能阻塞。
            if sys.platform == "darwin" and getattr(st, "st_flags", 0) & 0x40000000:
                continue
            inode_key = (st.st_dev, st.st_ino)
            is_dir_link = curr_dir.is_symlink()
            if inode_key in visited_real_dirs and not is_dir_link:
                continue
            visited_real_dirs.add(inode_key)
        except Exception:
            continue

        try:
            with os.scandir(curr_dir) as it:
                entries = list(it)
        except (PermissionError, OSError):
            continue

        is_library_dir = (curr_dir == HOME_DIR / "Library")

        for entry in entries:
            name = entry.name
            entry_path = curr_dir / name

            if name.upper() == "SKILL.MD":
                try:
                    if entry.is_file(follow_symlinks=True):
                        p_str = str(entry_path)
                        if not _should_skip_path(p_str):
                            found_paths[p_str] = entry_path
                except Exception:
                    pass
                continue

            try:
                is_sub_dir = entry.is_dir(follow_symlinks=True)
            except Exception:
                is_sub_dir = False

            if not is_sub_dir:
                continue

            if name in SKIP_DIR_NAMES:
                continue
            if is_library_dir and name in SKIP_LIBRARY_SUBDIRS:
                continue
            if _should_skip_path(str(entry_path)):
                continue

            if entry.is_symlink():
                candidate_md = entry_path / "SKILL.md"
                try:
                    if candidate_md.exists() and candidate_md.is_file():
                        found_paths[str(candidate_md)] = candidate_md
                        continue
                except Exception:
                    pass

            queue.append(entry_path)

    try:
        res = subprocess.run(
            ["mdfind", "-onlyin", str(root_dir), "kMDItemFSName == 'SKILL.md'c"],
            capture_output=True,
            text=True,
            timeout=4,
        )
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                s = line.strip()
                if not s or _should_skip_path(s):
                    continue
                p = Path(s)
                if p.name.upper() == "SKILL.MD" and p.exists():
                    found_paths.setdefault(str(p), p)
    except Exception:
        pass

    return [found_paths[k] for k in sorted(found_paths.keys())]


def build_instance_from_path(skill_md_path: Path) -> Optional[Dict[str, Any]]:
    try:
        content = skill_md_path.read_text(encoding="utf-8", errors="replace")
        st = skill_md_path.stat()
    except Exception:
        return None

    skill_dir = skill_md_path.parent
    dir_name = resolve_skill_group_name(skill_md_path)
    fm_name, desc = parse_skill_frontmatter(content, skill_dir.name)

    is_link = skill_md_path.is_symlink() or skill_dir.is_symlink()
    link_target = ""
    if is_link:
        try:
            link_target = str(skill_dir.resolve()) if skill_dir.is_symlink() else str(skill_md_path.resolve())
        except Exception:
            link_target = ""

    scope, scope_label, app_key, is_cache = classify_skill_location(skill_md_path)
    companion = list_companion_files(skill_dir) if not is_cache else []

    return {
        "id": sha256_text(str(skill_md_path))[:12],
        "name": dir_name,
        "frontmatter_name": fm_name,
        "description": desc,
        "skill_dir": str(skill_dir),
        "skill_md_path": str(skill_md_path),
        "scope": scope,
        "scope_label": scope_label,
        "app_key": app_key,
        "is_marketplace_cache": is_cache,
        "is_symlink": is_link,
        "symlink_target": link_target,
        "mtime": st.st_mtime,
        "mtime_str": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "size_bytes": st.st_size,
        "raw_hash": sha256_text(content),
        "norm_hash": norm_hash_text(content),
        "companion_files": companion,
        "companion_count": len(companion),
        "full_content": content,
    }


def refresh_instance_classification(inst: Dict[str, Any]) -> Dict[str, Any]:
    p = Path(inst["skill_md_path"])
    scope, scope_label, app_key, is_cache = classify_skill_location(p)
    inst["name"] = resolve_skill_group_name(p)
    inst["scope"] = scope
    inst["scope_label"] = scope_label
    inst["app_key"] = app_key
    inst["is_marketplace_cache"] = is_cache
    if "full_content" in inst:
        inst["norm_hash"] = norm_hash_text(inst["full_content"])
    return inst


ACTIVE_GLOBAL_SCOPES: Set[str] = {
    "source_repo",
    "claude_global",
    "codex_global",
    "cursor_global",
    "agents_global",
    "workbuddy_global",
    "other_agents",
}


def aggregate_skills(instances: List[Dict[str, Any]], scan_mode: str, duration_sec: float) -> Dict[str, Any]:
    by_name: Dict[str, List[Dict[str, Any]]] = {}
    for inst in instances:
        refresh_instance_classification(inst)
        by_name.setdefault(inst["name"], []).append(inst)

    def _canonical_rank(inst: Dict[str, Any]) -> Tuple[int, float]:
        if inst.get("is_marketplace_cache"):
            return (5, -inst["mtime"])
        if inst.get("is_symlink"):
            return (4, -inst["mtime"])
        p_lower = inst["skill_md_path"].lower()
        if "/work/skills/zh/" in p_lower:
            return (0, -inst["mtime"])
        if "/mtgit/aimaster-tools/skills/" in p_lower or "/mtgit/mtpipe-skill/.agents/skills/" in p_lower:
            return (1, -inst["mtime"])
        if inst["scope"] in ("claude_global", "codex_global", "cursor_global", "agents_global", "workbuddy_global"):
            return (2, -inst["mtime"])
        return (3, -inst["mtime"])

    skill_groups: List[Dict[str, Any]] = []
    user_drifted_count = 0
    user_redundant_copies = 0
    user_symlink_copies = 0
    user_unique_skills = 0
    user_total_files = 0

    for name, group_insts in sorted(by_name.items()):
        sorted_insts = sorted(group_insts, key=_canonical_rank)
        canonical = sorted_insts[0]

        non_cache_insts = [i for i in sorted_insts if not i.get("is_marketplace_cache")]
        is_user_skill = len(non_cache_insts) > 0

        eval_insts = non_cache_insts if is_user_skill else sorted_insts
        active_eval_insts = [i for i in eval_insts if i["scope"] in ACTIVE_GLOBAL_SCOPES]
        drift_check_insts = active_eval_insts if is_user_skill else eval_insts
        norm_hashes = {i["norm_hash"] for i in drift_check_insts} if drift_check_insts else {canonical["norm_hash"]}
        has_drift = len(norm_hashes) > 1

        active_real_insts = [i for i in active_eval_insts if not i["is_symlink"]]
        active_sym_insts = [i for i in active_eval_insts if i["is_symlink"]]

        if is_user_skill:
            user_unique_skills += 1
            user_total_files += len(non_cache_insts)
            if has_drift:
                user_drifted_count += 1
            if len(active_real_insts) > 1:
                user_redundant_copies += len(active_real_insts) - 1
            user_symlink_copies += sum(1 for i in non_cache_insts if i["is_symlink"])

        if is_user_skill:
            if has_drift:
                status = "drifted"
            elif len(active_real_insts) > 1:
                status = "duplicated"
            elif len(active_sym_insts) > 0:
                status = "all_symlinked"
            else:
                status = "single"
        else:
            if len(eval_insts) == 1:
                status = "single"
            elif has_drift:
                status = "drifted"
            elif all(i["is_symlink"] for i in eval_insts[1:]):
                status = "all_symlinked"
            else:
                status = "duplicated"

        app_status: Dict[str, Dict[str, Any]] = {}
        for app in ("claude", "codex", "cursor", "agents", "workbuddy"):
            matched = [i for i in sorted_insts if i["app_key"] == app]
            if not matched:
                app_status[app] = {"state": "missing", "path": ""}
            else:
                m = matched[0]
                if m["is_symlink"]:
                    st_code = "symlink"
                elif m["norm_hash"] == canonical["norm_hash"]:
                    st_code = "synced"
                else:
                    st_code = "drifted"
                app_status[app] = {
                    "state": st_code,
                    "path": m["skill_dir"],
                    "mtime_str": m["mtime_str"],
                    "hash": m["raw_hash"][:8],
                }

        diffs: List[Dict[str, Any]] = []
        if has_drift:
            c_lines = canonical["full_content"].splitlines(keepends=True)
            seen_diff_hashes: Set[str] = {canonical["norm_hash"]}
            for other in drift_check_insts:
                if other["id"] == canonical["id"]:
                    continue
                if other["norm_hash"] not in seen_diff_hashes:
                    seen_diff_hashes.add(other["norm_hash"])
                    o_lines = other["full_content"].splitlines(keepends=True)
                    diff_txt = "".join(
                        difflib.unified_diff(
                            c_lines,
                            o_lines,
                            fromfile=f"[基准版] {canonical['skill_md_path']} ({canonical['mtime_str']})",
                            tofile=f"[差异版] {other['skill_md_path']} ({other['mtime_str']})",
                            n=3,
                        )
                    )
                    diffs.append({
                        "other_id": other["id"],
                        "other_path": other["skill_md_path"],
                        "other_scope_label": other["scope_label"],
                        "other_mtime": other["mtime_str"],
                        "other_hash": other["raw_hash"][:8],
                        "other_content": other["full_content"],
                        "diff_text": diff_txt or "（仅空白字符或 Frontmatter 格式差异）",
                    })

        skill_groups.append({
            "name": name,
            "description": canonical["description"],
            "is_user_skill": is_user_skill,
            "status": status,
            "total_copies": len(eval_insts),
            "all_copies_including_cache": len(sorted_insts),
            "unique_versions": len(norm_hashes),
            "canonical_id": canonical["id"],
            "canonical_path": canonical["skill_md_path"],
            "canonical_dir": canonical["skill_dir"],
            "canonical_scope": canonical["scope"],
            "canonical_scope_label": canonical["scope_label"],
            "canonical_mtime": canonical["mtime_str"],
            "canonical_hash": canonical["raw_hash"][:8],
            "companion_files": canonical.get("companion_files", []),
            "app_status": app_status,
            "instances": sorted_insts,
            "diffs": diffs,
        })

    rank_map = {"drifted": 0, "duplicated": 1, "all_symlinked": 2, "single": 3}
    skill_groups.sort(
        key=lambda g: (0 if g["is_user_skill"] else 1, rank_map.get(g["status"], 9), -g["total_copies"], g["name"])
    )

    skill_suites = assign_skill_suites(skill_groups)

    workspaces = [
        {"label": "个人 Skill 主仓 (~/Work/skills)", "path": str(HOME_DIR / "Work/skills")},
        {"label": "AIMaster 团队工具仓 (~/MTGIT/aimaster-tools)", "path": str(HOME_DIR / "MTGIT/aimaster-tools")},
        {"label": "OptKit 工作区 (~/MTGIT/optkit-workspace)", "path": str(HOME_DIR / "MTGIT/optkit-workspace")},
        {"label": "MTPipe 技能仓 (~/MTGIT/mtpipe-skill)", "path": str(HOME_DIR / "MTGIT/mtpipe-skill")},
        {"label": "Task Agent (~/zycode/task-agent)", "path": str(HOME_DIR / "zycode/task-agent")},
        {"label": "Middle Station (~/zycode/middle_station)", "path": str(HOME_DIR / "zycode/middle_station")},
        {"label": "2026 工作区 (~/Work/2026)", "path": str(HOME_DIR / "Work/2026")},
        {"label": "用户主目录 (~)", "path": str(HOME_DIR)},
    ]

    all_scopes = (
        "source_repo",
        "claude_global",
        "codex_global",
        "cursor_global",
        "agents_global",
        "workbuddy_global",
        "other_agents",
        "project_local",
        "marketplace_cache",
    )

    summary = {
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scan_mode": scan_mode,
        "duration_sec": round(duration_sec, 2),
        "raw_total_files": len(instances),
        "raw_unique_names": len(skill_groups),
        "total_skill_files": user_total_files,
        "unique_skill_names": user_unique_skills,
        "drifted_skills": user_drifted_count,
        "redundant_copies": user_redundant_copies,
        "symlink_copies": user_symlink_copies,
        "user_suite_count": sum(1 for s in skill_suites if s["is_user_suite"]),
        "by_scope": {
            sc: sum(1 for i in instances if i["scope"] == sc)
            for sc in all_scopes
        },
    }

    return {
        "summary": summary,
        "workspaces": workspaces,
        "skill_suites": skill_suites,
        "skill_groups": skill_groups,
    }


def _match_known_suite(g: Dict[str, Any]) -> Optional[Tuple[str, str, str, int, bool]]:
    """
    返回: (suite_id, suite_title, suite_desc, suite_order, default_collapsed)
    """
    name = g["name"]
    cpath = g["canonical_path"].lower()

    if "/work/skills/zh/" in cpath:
        return (
            "core_personal",
            "⭐ 个人主控核心套件 (~/Work/skills)",
            "个人开发规范、Git 提交、写作与三大 CLI 调度核心技能",
            1,
            False,
        )
    if name.startswith(("lark-", "feishu-")):
        return (
            "lark_feishu",
            "🐦 飞书 / Lark 全家桶套件",
            "飞书文档、多维表格、IM、日历、会议纪要、审批、OKR 等成套办公技能",
            2,
            True,
        )
    if "/mtgit/aimaster-tools/" in cpath or name.startswith(("aimaster-", "am-")):
        return (
            "aimaster_suite",
            "🚀 AIMaster 算力与平台套件",
            "AIMaster 远程机器控制、SSH/SFTP、性能剖析与平台发布工具集",
            3,
            True,
        )
    if "/mtgit/mtpipe-skill/" in cpath or name.startswith("infer-"):
        return (
            "mtpipe_infer",
            "⚙️ MTPipe 算法推理与部署套件",
            "MTPipe 算法部署流水线、API 契约校验与子模块技能集",
            4,
            True,
        )
    if name.startswith(("optkit-", "dit-", "parity-", "acceleration-", "model-integration", "model-acceleration", "aqua-")):
        return (
            "optkit_accel",
            "⚡ OptKit 与模型加速评测套件",
            "模型推理加速、DiT 优化、精度对齐测试与 Aqua 性能评测套件",
            5,
            True,
        )
    if name.startswith("meitu-") or "algo-monitor" in cpath or "meitu" in name or name == "Downloads":
        return (
            "meitu_internal",
            "🏢 美图内部协同与算法监测套件",
            "美图 Confluence、内部连接器、GitLab MR 评审与新算法监测查询套件",
            6,
            True,
        )
    if name.startswith("openspec-"):
        return (
            "openspec_suite",
            "📐 OpenSpec 规范变更工作流套件",
            "OpenSpec 规范创建、变更应用、验证、归档与同步成套工作流",
            7,
            True,
        )
    if "/superpowers/" in cpath or name in ("test-driven-development",):
        return (
            "superpowers_suite",
            "🦸 Superpowers 研发工程方法论套件",
            "TDD、系统化调试、代码评审、多 Agent 并行调度与分支收尾方法论",
            8,
            True,
        )
    if "xbtlin-ai-berkshire" in cpath or "daily_stock_analysis" in cpath:
        return (
            "investment_suite",
            "📈 AI 投研与财报分析套件",
            "行业漏斗、财报复盘、公司深度研究、投资组合与个股分析套件",
            9,
            True,
        )
    if "vscode-synced-customization-agent-host-copilotcli" in cpath:
        return (
            "copilot_pr_suite",
            "🐙 Git & PR 研发协作套件 (Copilot)",
            "PR 创建/更新、CI 修复、分支同步与代码评审自动化套件",
            10,
            True,
        )
    if "local-agent-mode-sessions/skills-plugin" in cpath:
        return (
            "claude_cowork_suite",
            "📎 Claude 办公文档与日常套件",
            "Word/PDF/PPTX/XLSX 文档处理、日程管理与记忆归档套件",
            11,
            True,
        )
    if g["canonical_scope"] == "workbuddy_global" or name.endswith("__skillhub"):
        return (
            "workbuddy_suite",
            "🤖 WorkBuddy 专属技能套件",
            "安装在 ~/.workbuddy/skills 下的全局扩展技能",
            12,
            True,
        )
    return None


def assign_skill_suites(skill_groups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    为每个 Skill Group 标记所属套件 (suite_id / suite_title / suite_order)，
    并支持对未命中预设规则但具有相同前缀 (>=3 个) 的成套技能自动聚类。
    """
    unmatched_user: List[Dict[str, Any]] = []
    unmatched_cache: List[Dict[str, Any]] = []

    for g in skill_groups:
        known = _match_known_suite(g)
        if known and g["is_user_skill"]:
            sid, title, desc, order, collapsed = known
            g["suite_id"] = sid
            g["suite_title"] = title
            g["suite_desc"] = desc
            g["suite_order"] = order
            g["suite_default_collapsed"] = collapsed
        elif g["is_user_skill"]:
            unmatched_user.append(g)
        else:
            unmatched_cache.append(g)

    # 对未命中固定规则的用户 Skill：若同前缀 >= 3 个，自动归为动态套件
    prefix_buckets: Dict[str, List[Dict[str, Any]]] = {}
    for g in unmatched_user:
        parts = re.split(r"[-_]", g["name"])
        prefix = parts[0].lower() if len(parts) > 1 and len(parts[0]) >= 2 else ""
        prefix_buckets.setdefault(prefix, []).append(g)

    dyn_order = 20
    for prefix, bucket in sorted(prefix_buckets.items()):
        if prefix and len(bucket) >= 3:
            sid = f"auto_{prefix}"
            title = f"📦 {prefix}-* 系列套件"
            desc = f"自动归纳的 {prefix}-* 前缀成套技能 ({len(bucket)} 个)"
            for g in bucket:
                g["suite_id"] = sid
                g["suite_title"] = title
                g["suite_desc"] = desc
                g["suite_order"] = dyn_order
                g["suite_default_collapsed"] = True
            dyn_order += 1
        else:
            for g in bucket:
                g["suite_id"] = "standalone_misc"
                g["suite_title"] = "🧩 其他独立与专项 Skill"
                g["suite_desc"] = "未归入成套系列的独立工具或单项目技能"
                g["suite_order"] = 50
                g["suite_default_collapsed"] = True

    # 对插件商城缓存 Skill 按来源或前缀分组
    for g in unmatched_cache:
        p = g["canonical_path"]
        if "/scientific-skills/" in p:
            sid, title, order = ("cache_scientific", "🔬 [商城缓存] 科研计算技能集 (scientific-skills)", 90)
        elif "/workbuddy-connector-plugins-official/" in p:
            sid, title, order = ("cache_wb_connectors", "🔌 [商城缓存] WorkBuddy 官方连接器套件", 91)
        elif "/codebuddy-plugins-official/" in p:
            sid, title, order = ("cache_codebuddy", "🧰 [商城缓存] CodeBuddy 官方插件套件", 92)
        elif "/.codex/.tmp/plugins/" in p:
            sid, title, order = ("cache_codex_plugins", "📦 [商城缓存] Codex 内置插件缓存套件", 93)
        else:
            sid, title, order = ("cache_other", "🏪 [商城缓存] 其他内置与第三方缓存套件", 95)
        g["suite_id"] = sid
        g["suite_title"] = title
        g["suite_desc"] = "第三方插件商城或系统内置缓存（默认隐藏）"
        g["suite_order"] = order
        g["suite_default_collapsed"] = True

    # 汇总生成 skill_suites 元数据列表
    suites_map: Dict[str, Dict[str, Any]] = {}
    for g in skill_groups:
        sid = g["suite_id"]
        if sid not in suites_map:
            suites_map[sid] = {
                "suite_id": sid,
                "suite_title": g["suite_title"],
                "suite_desc": g.get("suite_desc", ""),
                "suite_order": g["suite_order"],
                "default_collapsed": g["suite_default_collapsed"],
                "is_user_suite": g["is_user_skill"],
                "skill_count": 0,
                "drifted_count": 0,
                "duplicated_count": 0,
                "all_symlinked_count": 0,
                "single_count": 0,
                "skill_names": [],
            }
        sm = suites_map[sid]
        sm["skill_count"] += 1
        sm["skill_names"].append(g["name"])
        st = g["status"]
        if st == "drifted":
            sm["drifted_count"] += 1
            sm["default_collapsed"] = False  # 存在版本分叉的套件默认自动展开提醒！
        elif st == "duplicated":
            sm["duplicated_count"] += 1
        elif st == "all_symlinked":
            sm["all_symlinked_count"] += 1
        else:
            sm["single_count"] += 1

    return sorted(suites_map.values(), key=lambda x: (x["suite_order"], x["suite_title"]))


def run_full_scan(root_dir: Path = HOME_DIR, save_index: bool = True, reaggregate_only: bool = False) -> Dict[str, Any]:
    t0 = time.time()
    instances: List[Dict[str, Any]] = []

    if reaggregate_only and INDEX_OUTPUT_PATH.exists():
        old = json.loads(INDEX_OUTPUT_PATH.read_text(encoding="utf-8"))
        for g in old.get("skill_groups", []):
            for inst in g.get("instances", []):
                p = Path(inst.get("skill_md_path", ""))
                if p.exists():
                    instances.append(inst)
        scan_mode = old.get("summary", {}).get("scan_mode", "live_full_scan")
    else:
        paths = discover_skill_files_live(root_dir)
        if len(paths) > 10:
            scan_mode = "live_full_scan"
            for p in paths:
                inst = build_instance_from_path(p)
                if inst:
                    instances.append(inst)
        elif INDEX_OUTPUT_PATH.exists():
            old = json.loads(INDEX_OUTPUT_PATH.read_text(encoding="utf-8"))
            for g in old.get("skill_groups", []):
                for inst in g.get("instances", []):
                    instances.append(inst)
            scan_mode = "cached_full_scan"

    duration = time.time() - t0
    result = aggregate_skills(instances, scan_mode=scan_mode, duration_sec=duration)

    if save_index:
        INDEX_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        INDEX_OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


def print_cli_report(data: Dict[str, Any]) -> None:
    s = data["summary"]
    bs = s["by_scope"]
    print("=" * 78)
    print(f"🔍 本机 Skill 全盘扫描报告 ({s['scanned_at']} | 模式: {s['scan_mode']})")
    print("=" * 78)
    print(f"  [全盘物理检出] SKILL.md 总计 : {s['raw_total_files']} 份 (去重后 {s['raw_unique_names']} 个，含插件商城缓存 {bs['marketplace_cache']} 份)")
    print(f"  [我的有效技能] SKILL.md 总计 : {s['total_skill_files']} 份 (去重后 {s['unique_skill_names']} 个独立 Skill)")
    print(f"  [多处重复状态] 冗余拷贝/链接 : {s['redundant_copies']} 份 (其中已建软链: {s['symlink_copies']} 份)")
    print(f"  [内容版本分叉] 存在冲突 Skill: {s['drifted_skills']} 个")
    print("-" * 78)
    print("各工具与仓库分布:")
    print(
        f"  源码仓(Work/MTGIT): {bs['source_repo']} | "
        f"Claude(~/.claude): {bs['claude_global']} | "
        f"Codex(~/.codex): {bs['codex_global']} | "
        f"Cursor(~/.cursor): {bs['cursor_global']}\n"
        f"  Agents(~/.agents): {bs['agents_global']} | "
        f"WorkBuddy(~/.workbuddy): {bs['workbuddy_global']} | "
        f"其他Agent(.trae/.qwen等): {bs['other_agents']} | "
        f"项目/iCloud局部: {bs['project_local']}"
    )
    print("-" * 78)
    drifted = [g for g in data["skill_groups"] if g["is_user_skill"] and g["status"] == "drifted"]
    if drifted:
        print(f"⚠️  发现 {len(drifted)} 个存在内容分叉的个人/项目 Skill:")
        for g in drifted:
            print(f"  - {g['name']:28s} (有效拷贝 {g['total_copies']} 份, {g['unique_versions']} 个版本 | 基准: {g['canonical_path']})")
    print(f"\n📄 完整索引文件: {INDEX_OUTPUT_PATH}")


def main() -> int:
    parser = argparse.ArgumentParser(description="全盘扫描本机所有 SKILL.md")
    parser.add_argument("--root", default=str(HOME_DIR), help="扫描根目录 (默认 ~)")
    parser.add_argument("--reaggregate", action="store_true", help="基于已有索引快速重算分类与分叉")
    parser.add_argument("--json", action="store_true", help="输出 JSON 摘要")
    args = parser.parse_args()

    res = run_full_scan(
        Path(os.path.expanduser(args.root)).resolve(),
        save_index=True,
        reaggregate_only=args.reaggregate,
    )
    if args.json:
        print(json.dumps(res["summary"], ensure_ascii=False, indent=2))
    else:
        print_cli_report(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
