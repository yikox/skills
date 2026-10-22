#!/usr/bin/env python3
"""
sync_skills.py - 本机 Skill 版本对齐与软链接去重治理脚本

执行策略：
1. 个人主控仓 (~/Work/skills/zh/*)：
   - 在 ~/.claude/skills、~/.codex/skills、~/.cursor/skills、~/.agents/skills 中统一替换为指向源码仓的软链接（Symlink），改一处全工具实时生效。
2. 团队工具仓 (~/MTGIT/aimaster-tools/skills/*/*)：
   - 在 ~/.claude/skills、~/.codex/skills、~/.cursor/skills 中统一替换为指向源码仓的软链接（Symlink），消除多处物理拷贝冗余，同时保持 ~/.local/bin 下的 CLI shim 脚本完全兼容。
   - 自动备份并清理 ~/.agents/skills 与 ~/.workbuddy/skills 中滞后的旧版副本。
3. 已废弃 / 已改名的全局残留 Skill：
   - 自动备份后清理全局目录（~/.claude、~/.codex、~/.cursor、~/.agents、~/.workbuddy 及误建的 ~/claude、~/codex）中已退役的旧 Skill（含 am-v2* 系列、notes-project-memory 等）。
   - 严格保留所有历史项目文件夹内的归档文件不动。
4. 其余全局多处物理拷贝 Skill 去重：
   - 对仅存在于全局目录但有多份物理拷贝的独立 Skill（如 dit-model-opt-analysis、pm_skill、optkit-v1-guide、test-driven-development），保留基准物理目录，将其余全局物理副本自动转为指向基准目录的软链接。
5. 所有被覆盖或清理的目录均先完整备份至 vault/backups/<timestamp>/。
"""

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


HOME_DIR = Path(os.path.expanduser("~")).resolve()
BASE_DIR = Path(__file__).resolve().parent
BACKUP_ROOT = BASE_DIR / "vault" / "backups"

WORK_SKILLS_ZH_DIR = HOME_DIR / "Work" / "skills" / "zh"
AIMASTER_SKILLS_DIR = HOME_DIR / "MTGIT" / "aimaster-tools" / "skills"

GLOBAL_DIRS: Dict[str, Path] = {
    "claude": HOME_DIR / ".claude" / "skills",
    "codex": HOME_DIR / ".codex" / "skills",
    "cursor": HOME_DIR / ".cursor" / "skills",
    "agents": HOME_DIR / ".agents" / "skills",
    "workbuddy": HOME_DIR / ".workbuddy" / "skills",
}

STRAY_NON_DOT_DIRS: Dict[str, Path] = {
    "claude_nondot": HOME_DIR / "claude" / "skills",
    "codex_nondot": HOME_DIR / "codex" / "skills",
}

DEPRECATED_OR_RENAMED_GLOBAL_SKILLS: Set[str] = {
    # ~/Work/skills/install.sh 已废弃
    "auto-ai-coauthor",            # 已被 git-commit 取代
    "notes-project-memory",        # 已被 notes-sync 取代
    # ~/MTGIT/aimaster-tools/install.sh (remove_retired_skills) 已废弃/重命名
    "aimaster-machine-control",    # 已重命名为 am-machine-control
    "ssh-session",                 # 已重命名为 am-ssh-session
    "sftp-session",                # 已重命名为 am-sftp-session
    "test-runner",                 # 已重命名为 am-test-runner
    "remote-code-edit",            # 已重命名为 local-code-sync
    "remote-file-fetch",           # 已重命名为 am-sftp-session
    "remote-test-runner",          # 已重命名为 am-test-runner
    "remote-download-fallback",    # 已并入 am-sftp-session
    "multi-env-perf-aqua",         # 已重构为 aqua-perf-test
    "aqua-algodeployspec-work-num",# 已退役
    "aqua-testtask-insight-poll",  # 已退役
    "aqua-token",                  # 已退役
    "jira-mcp",                    # 已退役
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def backup_target(target_path: Path, backup_session_dir: Path, label: str, dry_run: bool) -> str:
    if not target_path.exists() and not target_path.is_symlink():
        return ""
    dest = backup_session_dir / f"{label}__{target_path.name}"
    if dry_run:
        return str(dest)
    backup_session_dir.mkdir(parents=True, exist_ok=True)
    if target_path.is_symlink():
        link_to = os.readlink(target_path)
        (backup_session_dir / f"{label}__{target_path.name}.symlink.txt").write_text(
            f"{target_path} -> {link_to}\n", encoding="utf-8"
        )
    elif target_path.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(target_path, dest, symlinks=True)
    else:
        shutil.copy2(target_path, dest)
    return str(dest)


def remove_path(target_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if target_path.is_symlink() or target_path.is_file():
        target_path.unlink()
    elif target_path.is_dir():
        shutil.rmtree(target_path)


def sync_all_skills(dry_run: bool = False) -> Dict[str, Any]:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_session_dir = BACKUP_ROOT / ts
    actions: List[Dict[str, Any]] = []
    managed_skills: Set[str] = set()

    # 1. 个人主控仓 ~/Work/skills/zh/* -> Symlink 到 claude, codex, cursor, agents (以及已存在的 workbuddy)
    if WORK_SKILLS_ZH_DIR.exists():
        for src_skill_dir in sorted(WORK_SKILLS_ZH_DIR.iterdir()):
            if not src_skill_dir.is_dir() or not (src_skill_dir / "SKILL.md").exists():
                continue
            skill_name = src_skill_dir.name
            managed_skills.add(skill_name)
            src_resolved = src_skill_dir.resolve()

            for app_key in ("claude", "codex", "cursor", "agents", "workbuddy"):
                g_dir = GLOBAL_DIRS[app_key]
                if not g_dir.exists() and not dry_run:
                    g_dir.mkdir(parents=True, exist_ok=True)
                target = g_dir / skill_name

                if target.is_symlink():
                    try:
                        if target.resolve() == src_resolved:
                            continue
                    except Exception:
                        pass

                b_path = backup_target(target, backup_session_dir, f"{app_key}_work_symlink", dry_run)
                remove_path(target, dry_run)
                if not dry_run:
                    target.symlink_to(src_skill_dir)
                actions.append({
                    "type": "symlink_personal_skill",
                    "skill": skill_name,
                    "app": app_key,
                    "target": str(target),
                    "source": str(src_skill_dir),
                    "backup": b_path,
                })

    # 2. 团队源仓 ~/MTGIT/aimaster-tools/skills/*/* -> Symlink 至 claude, codex, cursor；清理 agents, workbuddy 旧副本
    if AIMASTER_SKILLS_DIR.exists():
        for cat_dir in sorted(AIMASTER_SKILLS_DIR.iterdir()):
            if not cat_dir.is_dir():
                continue
            for src_skill_dir in sorted(cat_dir.iterdir()):
                src_md = src_skill_dir / "SKILL.md"
                if not src_skill_dir.is_dir() or not src_md.exists():
                    continue
                skill_name = src_skill_dir.name
                managed_skills.add(skill_name)
                src_resolved = src_skill_dir.resolve()

                for app_key in ("claude", "codex", "cursor"):
                    g_dir = GLOBAL_DIRS[app_key]
                    if not g_dir.exists() and not dry_run:
                        g_dir.mkdir(parents=True, exist_ok=True)
                    target = g_dir / skill_name

                    if target.is_symlink():
                        try:
                            if target.resolve() == src_resolved:
                                continue
                        except Exception:
                            pass

                    b_path = backup_target(target, backup_session_dir, f"{app_key}_aimaster_symlink", dry_run)
                    remove_path(target, dry_run)
                    if not dry_run:
                        target.symlink_to(src_skill_dir)
                    actions.append({
                        "type": "sync_aimaster_skill",
                        "skill": skill_name,
                        "app": app_key,
                        "target": str(target),
                        "source": str(src_skill_dir),
                        "backup": b_path,
                    })

                for stale_app in ("agents", "workbuddy"):
                    stale_target = GLOBAL_DIRS[stale_app] / skill_name
                    if stale_target.exists() or stale_target.is_symlink():
                        b_path = backup_target(stale_target, backup_session_dir, f"{stale_app}_stale_aimaster", dry_run)
                        remove_path(stale_target, dry_run)
                        actions.append({
                            "type": "remove_stale_copy",
                            "skill": skill_name,
                            "app": stale_app,
                            "target": str(stale_target),
                            "backup": b_path,
                        })

    # 3. 清理全局目录与误建非隐藏目录中已废弃或已改名的历史残留 Skill（含 am-v2* 退役系列）
    all_check_dirs: List[Tuple[str, Path]] = list(GLOBAL_DIRS.items()) + list(STRAY_NON_DOT_DIRS.items())
    for app_key, g_dir in all_check_dirs:
        if not g_dir.exists():
            continue
        for entry in sorted(g_dir.iterdir()):
            name = entry.name
            if name in DEPRECATED_OR_RENAMED_GLOBAL_SKILLS or name.startswith("am-v2"):
                b_path = backup_target(entry, backup_session_dir, f"{app_key}_deprecated", dry_run)
                remove_path(entry, dry_run)
                actions.append({
                    "type": "remove_deprecated_skill",
                    "skill": name,
                    "app": app_key,
                    "target": str(entry),
                    "backup": b_path,
                })

    for _, stray_dir in STRAY_NON_DOT_DIRS.items():
        if stray_dir.exists() and not dry_run:
            try:
                remaining = [p for p in stray_dir.iterdir() if p.name != ".DS_Store"]
                if not remaining:
                    shutil.rmtree(stray_dir)
                    parent = stray_dir.parent
                    if parent.exists() and not [p for p in parent.iterdir() if p.name != ".DS_Store"]:
                        shutil.rmtree(parent)
            except Exception:
                pass

    # 4. 其余全局多处物理拷贝 Skill 自动软链去重
    priority_order = ("agents", "claude", "codex", "cursor", "workbuddy")
    unmanaged_by_name: Dict[str, List[Tuple[str, Path]]] = {}
    for app_key in priority_order:
        g_dir = GLOBAL_DIRS[app_key]
        if not g_dir.exists():
            continue
        for entry in sorted(g_dir.iterdir()):
            if entry.name in managed_skills or entry.name in DEPRECATED_OR_RENAMED_GLOBAL_SKILLS:
                continue
            if (entry.is_dir() or entry.is_symlink()) and (entry / "SKILL.md").exists():
                unmanaged_by_name.setdefault(entry.name, []).append((app_key, entry))

    opencode_superpowers = HOME_DIR / ".config" / "opencode" / "skills" / "superpowers"
    if opencode_superpowers.exists():
        for entry in sorted(opencode_superpowers.iterdir()):
            if entry.name in unmanaged_by_name and (entry / "SKILL.md").exists():
                unmanaged_by_name[entry.name].append(("opencode", entry))

    for skill_name, app_entries in sorted(unmanaged_by_name.items()):
        real_entries = [(app, p) for app, p in app_entries if not p.is_symlink()]
        if len(real_entries) <= 1:
            continue
        canonical_app, canonical_dir = real_entries[0]
        canonical_resolved = canonical_dir.resolve()
        for dup_app, dup_dir in real_entries[1:]:
            if dup_dir.resolve() == canonical_resolved:
                continue
            b_path = backup_target(dup_dir, backup_session_dir, f"{dup_app}_dedup_symlink", dry_run)
            remove_path(dup_dir, dry_run)
            if not dry_run:
                dup_dir.symlink_to(canonical_dir)
            actions.append({
                "type": "dedup_global_skill",
                "skill": skill_name,
                "app": dup_app,
                "target": str(dup_dir),
                "source": str(canonical_dir),
                "backup": b_path,
            })

    summary = {
        "timestamp": ts,
        "dry_run": dry_run,
        "backup_dir": str(backup_session_dir) if actions else "",
        "total_actions": len(actions),
        "symlinked_count": sum(1 for a in actions if a["type"] in ("symlink_personal_skill", "dedup_global_skill")),
        "synced_aimaster_count": sum(1 for a in actions if a["type"] == "sync_aimaster_skill"),
        "removed_stale_count": sum(1 for a in actions if a["type"] == "remove_stale_copy"),
        "removed_deprecated_count": sum(1 for a in actions if a["type"] == "remove_deprecated_skill"),
        "actions": actions,
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="本机 Skill 版本对齐与软链接治理工具")
    parser.add_argument("--dry-run", action="store_true", help="仅预览将执行的变更，不实际修改磁盘")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式结果")
    args = parser.parse_args()

    res = sync_all_skills(dry_run=args.dry_run)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    mode_str = "[DRY-RUN 预览]" if args.dry_run else "[已执行完成]"
    print("=" * 80)
    print(f"Skill 版本对齐与软链接治理报告 {mode_str}")
    print("-" * 80)
    print(
        f"总变更项: {res['total_actions']} | "
        f"个人/全局软链去重: {res['symlinked_count']} | "
        f"aimaster-tools 软链对齐: {res['synced_aimaster_count']} | "
        f"清理过时副本: {res['removed_stale_count']} | "
        f"清理废弃/改名残留: {res['removed_deprecated_count']}"
    )
    if res["backup_dir"]:
        print(f"自动备份目录: {res['backup_dir']}")
    print("=" * 80)
    for idx, act in enumerate(res["actions"], 1):
        t = act["type"]
        sk = act["skill"]
        app = act["app"]
        tgt = act["target"]
        print(f"{idx:02d}. [{t}] {sk} ({app}) -> {tgt}")


if __name__ == "__main__":
    main()
