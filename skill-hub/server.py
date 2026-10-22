#!/usr/bin/env python3
"""
server.py - 本机 Skill 管理与 App 快捷启动服务（纯本地轻量工具）

功能：
1. 调用 scan_skills.py 全量扫描本机全部 SKILL.md 并提供可视化检索、重复/分叉对比与在线编辑。
2. 快捷启动本地 AI 工具：
   - CLI 类 (codex / claude / cursor-agent)：自动拉起终端窗口 (iTerm2 / Terminal) 并 cd 到选定项目目录执行。
   - GUI 类 (Cursor / Claude Desktop / Antigravity / Finder)：直接调用 macOS open 唤起对应应用。
3. 支持一键将选定版本同步或替换为软链（自动备份原目录到 vault/backups）。
4. 支持在页面右上角一键安全关闭后台服务（POST /api/server/stop）。

启动方式：
  python3 server.py [--port 8788]
"""

import argparse
import importlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict

import scan_skills
import sync_skills
from scan_skills import HOME_DIR, INDEX_OUTPUT_PATH


BASE_DIR = Path(__file__).resolve().parent
BACKUP_ROOT = BASE_DIR / "vault" / "backups"
PID_FILE = BASE_DIR / "vault" / "server.pid"
PORT_FILE = BASE_DIR / "vault" / "server.port"
LAUNCHER_CONFIG_FILE = BASE_DIR / "launcher_config.json"
DEFAULT_PORT = 8788

DEFAULT_LAUNCHER_CONFIG: Dict[str, Any] = {
    "launchers": [
        {"id": "codex", "label": "⚡ 启动 Codex (终端 CLI)", "type": "cli", "target": "codex", "pass_workdir": True, "custom_workdir": "", "style": "codex", "enabled": True},
        {"id": "claude", "label": "🤖 启动 Claude Code (终端 CLI)", "type": "cli", "target": "claude", "pass_workdir": True, "custom_workdir": "", "style": "claude", "enabled": True},
        {"id": "cursor_cli", "label": "🧭 启动 Cursor Agent (CLI)", "type": "cli", "target": "cursor-agent", "pass_workdir": True, "custom_workdir": "", "style": "default", "enabled": True},
        {"id": "cursor_app", "label": "🖥️ 打开 Cursor 桌面端", "type": "app", "target": "Cursor", "pass_workdir": True, "custom_workdir": "", "style": "default", "enabled": True},
        {"id": "claude_app", "label": "💬 打开 Claude 桌面端", "type": "app", "target": "Claude", "pass_workdir": False, "custom_workdir": "", "style": "default", "enabled": True},
        {"id": "antigravity", "label": "🪐 打开 Antigravity", "type": "app", "target": "Antigravity", "pass_workdir": True, "custom_workdir": "", "style": "default", "enabled": True},
        {"id": "workbuddy", "label": "🦊 打开 WorkBuddy", "type": "app", "target": "WorkBuddy", "pass_workdir": False, "custom_workdir": "", "style": "default", "enabled": True},
        {"id": "terminal", "label": "💻 在此目录打开终端", "type": "cli", "target": "", "pass_workdir": True, "custom_workdir": "", "style": "default", "enabled": True},
        {"id": "finder", "label": "📂 在 Finder 打开目录", "type": "finder", "target": "", "pass_workdir": True, "custom_workdir": "", "style": "default", "enabled": True},
    ],
    "workdir_presets": [
        {"label": "🛠️ Skill 个人源仓 (~/Work/skills)", "path": str(HOME_DIR / "Work" / "skills")},
        {"label": "🏢 美团研发主仓 (~/MTGIT)", "path": str(HOME_DIR / "MTGIT")},
        {"label": "🧪 算法优化工作区 (~/Work/algorithm-opt-workspace)", "path": str(HOME_DIR / "Work" / "algorithm-opt-workspace")},
        {"label": "🏠 个人主目录 (~)", "path": str(HOME_DIR)},
    ],
}


def get_launcher_config() -> Dict[str, Any]:
    if LAUNCHER_CONFIG_FILE.exists():
        try:
            data = json.loads(LAUNCHER_CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "launchers" in data:
                if "workdir_presets" not in data:
                    data["workdir_presets"] = DEFAULT_LAUNCHER_CONFIG["workdir_presets"]
                return data
        except Exception:
            pass
    LAUNCHER_CONFIG_FILE.write_text(
        json.dumps(DEFAULT_LAUNCHER_CONFIG, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return json.loads(json.dumps(DEFAULT_LAUNCHER_CONFIG))


def save_launcher_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
    if config_data.get("reset"):
        LAUNCHER_CONFIG_FILE.write_text(
            json.dumps(DEFAULT_LAUNCHER_CONFIG, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return get_launcher_config()

    launchers = config_data.get("launchers")
    presets = config_data.get("workdir_presets")
    if not isinstance(launchers, list):
        raise ValueError("launchers 字段必须是数组")
    normalized = {
        "launchers": launchers,
        "workdir_presets": presets if isinstance(presets, list) else DEFAULT_LAUNCHER_CONFIG["workdir_presets"],
    }
    LAUNCHER_CONFIG_FILE.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return normalized


def detect_installed_apps() -> list[str]:
    apps = set()
    for root in (Path("/Applications"), HOME_DIR / "Applications"):
        if root.exists():
            try:
                for p in root.iterdir():
                    if p.suffix == ".app":
                        apps.add(p.stem)
            except Exception:
                pass
    return sorted(apps, key=lambda s: s.lower())


def _cleanup_pid_files() -> None:
    """仅当 PID_FILE 记录的是当前进程 PID 时才清理，防止误删其他实例的状态文件。"""
    my_pid = str(os.getpid())
    try:
        if PID_FILE.exists() and PID_FILE.read_text(encoding="utf-8").strip() == my_pid:
            PID_FILE.unlink()
            if PORT_FILE.exists():
                PORT_FILE.unlink()
    except Exception:
        pass

APP_TARGETS = {
    "claude": HOME_DIR / ".claude" / "skills",
    "codex": HOME_DIR / ".codex" / "skills",
    "cursor": HOME_DIR / ".cursor" / "skills",
    "agents": HOME_DIR / ".agents" / "skills",
}


def get_cached_or_scan(force_rescan: bool = False) -> Dict[str, Any]:
    if not force_rescan and INDEX_OUTPUT_PATH.exists():
        try:
            cached = json.loads(INDEX_OUTPUT_PATH.read_text(encoding="utf-8"))
            if "skill_suites" in cached:
                return cached
            importlib.reload(scan_skills)
            return scan_skills.run_full_scan(HOME_DIR, save_index=True, reaggregate_only=True)
        except Exception:
            pass
    importlib.reload(scan_skills)
    return scan_skills.run_full_scan(HOME_DIR, save_index=True)


def _open_terminal_with_cmd(resolved_dir: Path, cli_cmd: str, tag_id: str = "custom") -> Dict[str, Any]:
    quoted_dir = shlex.quote(str(resolved_dir))
    shell_cmd = f"cd {quoted_dir} && clear && {cli_cmd}" if cli_cmd else f"cd {quoted_dir} && clear"

    has_iterm = Path("/Applications/iTerm.app").exists()
    try:
        if has_iterm:
            osa = (
                'tell application "iTerm"\n'
                '  activate\n'
                f'  create window with default profile command "zsh -lic {shlex.quote(shell_cmd)}"\n'
                'end tell'
            )
        else:
            osa = (
                'tell application "Terminal"\n'
                '  activate\n'
                f'  do script "{shell_cmd.replace(chr(34), chr(92) + chr(34))}"\n'
                'end tell'
            )
        res = subprocess.run(["osascript", "-e", osa], capture_output=True, text=True, timeout=4)
        if res.returncode == 0:
            return {
                "ok": True,
                "message": f"已在 {'iTerm2' if has_iterm else 'Terminal'} 中启动 {cli_cmd or '终端'} (目录: {resolved_dir})",
            }
    except Exception:
        pass

    safe_tag = "".join(c if c.isalnum() or c in "-_" else "_" for c in tag_id) or "custom"
    cmd_script = Path(f"/tmp/aihub-launch-{safe_tag}.command")
    script_body = (
        "#!/usr/bin/env zsh\n"
        f"cd {quoted_dir} || exit 1\n"
        "clear\n"
        f'echo "🚀 已进入工作目录: $(pwd)"\n'
    )
    if cli_cmd:
        script_body += f'echo "⚡ 正在启动 {cli_cmd} ..."\nexec {cli_cmd}\n'
    else:
        script_body += "exec zsh -l\n"
    cmd_script.write_text(script_body, encoding="utf-8")
    cmd_script.chmod(0o755)
    subprocess.run(["open", str(cmd_script)], check=False)
    return {
        "ok": True,
        "message": f"已通过系统终端拉起 {cli_cmd or 'Shell'} (目录: {resolved_dir})",
    }


def launch_local_tool(app_id: str, workdir: str = "", target_path: str = "", custom_item: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """在 macOS 本机启动可配置的 CLI (拉起终端进入工作目录)、GUI 应用、URL 或后台命令。"""
    # 1. 优先从自定义配置项查找
    cfg = get_launcher_config()
    item = custom_item
    if not item and app_id:
        for entry in cfg.get("launchers", []):
            if entry.get("id") == app_id:
                item = entry
                break

    effective_workdir = (item.get("custom_workdir") if item else "") or workdir
    resolved_dir = Path(os.path.expanduser(effective_workdir)).resolve() if effective_workdir else HOME_DIR
    if not resolved_dir.exists():
        resolved_dir = HOME_DIR

    if item:
        ltype = item.get("type", "cli")
        target = (item.get("target") or "").strip()
        pass_workdir = bool(item.get("pass_workdir", True))
        item_id = item.get("id") or "custom"

        if ltype == "cli":
            return _open_terminal_with_cmd(resolved_dir, target, tag_id=item_id)

        if ltype == "app":
            if not target:
                raise ValueError("未配置要打开的 macOS 应用名称")
            open_target = target_path if target_path else (str(resolved_dir) if pass_workdir else "")
            cmd = ["open", "-a", target]
            if open_target:
                cmd.append(open_target)
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode != 0:
                raise ValueError(f"无法打开应用 '{target}': {(res.stderr or '').strip() or '请检查应用名称是否安装在 /Applications'}")
            return {
                "ok": True,
                "message": f"已唤起应用 {target}" + (f" ({open_target})" if open_target else ""),
            }

        if ltype == "url":
            if not target:
                raise ValueError("未配置要打开的 URL")
            subprocess.run(["open", target], check=False)
            return {"ok": True, "message": f"已在浏览器打开: {target}"}

        if ltype == "finder":
            p = Path(os.path.expanduser(target_path or target or str(resolved_dir)))
            if p.is_file():
                subprocess.run(["open", "-R", str(p)], check=False)
            else:
                subprocess.run(["open", str(p)], check=False)
            return {"ok": True, "message": f"已在 Finder 中打开: {p}"}

        if ltype == "bg_cmd":
            if not target:
                raise ValueError("未配置后台命令")
            subprocess.Popen(target, shell=True, cwd=str(resolved_dir))
            return {"ok": True, "message": f"已在后台执行命令: {target} (目录: {resolved_dir})"}

    # 2. 内置兜底 ID（供详情页固定按钮调用）
    cli_commands = {
        "codex": "codex",
        "claude": "claude",
        "cursor_cli": "cursor-agent",
        "terminal": "",
    }
    if app_id in cli_commands:
        return _open_terminal_with_cmd(resolved_dir, cli_commands[app_id], tag_id=app_id)

    if app_id == "cursor_app":
        open_target = target_path if target_path else str(resolved_dir)
        subprocess.run(["open", "-a", "Cursor", open_target], check=False)
        return {"ok": True, "message": f"已使用 Cursor 打开: {open_target}"}

    if app_id == "claude_app":
        subprocess.run(["open", "-a", "Claude"], check=False)
        return {"ok": True, "message": "已唤起 Claude 桌面客户端"}

    if app_id == "antigravity":
        open_target = target_path if target_path else str(resolved_dir)
        subprocess.run(["open", "-a", "Antigravity", open_target], check=False)
        return {"ok": True, "message": f"已使用 Antigravity 打开: {open_target}"}

    if app_id == "finder":
        p = Path(os.path.expanduser(target_path or str(resolved_dir)))
        if p.is_file():
            subprocess.run(["open", "-R", str(p)], check=False)
        else:
            subprocess.run(["open", str(p)], check=False)
        return {"ok": True, "message": f"已在 Finder 中打开: {p}"}

    raise ValueError(f"不支持的启动目标: {app_id}")


def save_skill_content(skill_md_path: str, content: str) -> Dict[str, Any]:
    p = Path(os.path.expanduser(skill_md_path)).resolve()
    if p.name.upper() != "SKILL.MD":
        raise ValueError("仅允许编辑 SKILL.md 文件")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    if INDEX_OUTPUT_PATH.exists():
        try:
            data = json.loads(INDEX_OUTPUT_PATH.read_text(encoding="utf-8"))
            for grp in data.get("skill_groups", []):
                for inst in grp.get("instances", []):
                    if inst["skill_md_path"] == str(p):
                        inst["full_content"] = content
            INDEX_OUTPUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
    return {"ok": True, "path": str(p)}


def link_skill_to_apps(skill_name: str, canonical_dir: str, apps: list[str]) -> Dict[str, Any]:
    """将指定 Skill 挂载（软链）到选定的本地工具目录 (~/.claude/skills 等)，原物理目录自动备份。"""
    src_dir = Path(os.path.expanduser(canonical_dir)).resolve()
    if not (src_dir / "SKILL.md").exists():
        raise ValueError(f"源目录不存在 SKILL.md: {src_dir}")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    linked = []
    for app in apps:
        target_root = APP_TARGETS.get(app)
        if not target_root:
            continue
        target_root.mkdir(parents=True, exist_ok=True)
        dst = target_root / skill_name
        if dst.resolve() == src_dir and not dst.is_symlink():
            continue
        if dst.is_symlink():
            dst.unlink()
        elif dst.exists():
            bkp = BACKUP_ROOT / ts / app / skill_name
            bkp.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dst), str(bkp))
        os.symlink(str(src_dir), str(dst))
        linked.append(f"{app} -> {dst}")

    return {"ok": True, "linked": linked}


TRASH_ROOT = BASE_DIR / "vault" / "trash"

PROTECTED_BROAD_DIRS = {
    HOME_DIR.resolve(),
    (HOME_DIR / "Downloads").resolve(),
    (HOME_DIR / "Desktop").resolve(),
    (HOME_DIR / "Documents").resolve(),
    (HOME_DIR / "Work").resolve(),
    (HOME_DIR / "MTGIT").resolve(),
}


def _safe_remove_instance(skill_md_path_str: str, batch_trash_dir: Path, idx: int = 0) -> Dict[str, Any]:
    """
    安全移除单个 Skill 实例：
    - 若目录或文件本身是软链接：直接 unlink（不伤及指向的源目录）
    - 若是物理目录：
      - 若该目录本身是受保护大目录（如 ~/Downloads）或含 .git 仓库根，则仅将 SKILL.md 移入回收站
      - 否则将整个 Skill 目录移入 vault/trash/<timestamp>/ 备份回收站，随时可恢复
    """
    md_path = Path(os.path.expanduser(skill_md_path_str))
    skill_dir = md_path.parent

    if skill_dir.is_symlink():
        target = os.readlink(skill_dir)
        skill_dir.unlink()
        return {"action": "unlink_dir", "path": str(skill_dir), "target": target}

    if md_path.is_symlink():
        target = os.readlink(md_path)
        md_path.unlink()
        return {"action": "unlink_file", "path": str(md_path), "target": target}

    if not md_path.exists():
        return {"action": "already_missing", "path": str(md_path)}

    batch_trash_dir.mkdir(parents=True, exist_ok=True)
    resolved_dir = skill_dir.resolve()
    is_protected_or_repo_root = (resolved_dir in PROTECTED_BROAD_DIRS) or (resolved_dir / ".git").exists()

    if is_protected_or_repo_root:
        dst = batch_trash_dir / f"{idx:03d}__{skill_dir.name}__SKILL.md"
        shutil.move(str(md_path), str(dst))
        return {"action": "trash_file", "path": str(md_path), "trash_path": str(dst)}

    dst = batch_trash_dir / f"{idx:03d}__{skill_dir.parent.name}__{skill_dir.name}"
    shutil.move(str(skill_dir), str(dst))
    return {"action": "trash_dir", "path": str(skill_dir), "trash_path": str(dst)}


def delete_skills_by_names(skill_names: list[str]) -> Dict[str, Any]:
    """彻底删除一个或多个 Skill（清理本机所有软链并将物理源目录移入 vault/trash 回收站）。"""
    target_set = set(skill_names)
    if not target_set:
        raise ValueError("未指定要删除的 Skill 名称")

    cur_data = get_cached_or_scan(force_rescan=False)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_trash_dir = TRASH_ROOT / ts
    records = []
    deleted_skills = []
    idx = 0

    for grp in cur_data.get("skill_groups", []):
        if grp["name"] not in target_set:
            continue
        deleted_skills.append(grp["name"])
        insts = grp.get("instances", [])
        # 若是用户 Skill，默认清理其所有非商城缓存实例；若本身就是缓存 Skill，则清理其全部实例
        target_insts = [i for i in insts if not i.get("is_marketplace_cache")] if grp.get("is_user_skill") else insts
        # 先删软链接，再删物理目录
        symlinks = [i for i in target_insts if i.get("is_symlink")]
        real_dirs = [i for i in target_insts if not i.get("is_symlink")]
        for inst in symlinks + real_dirs:
            idx += 1
            rec = _safe_remove_instance(inst["skill_md_path"], batch_trash_dir, idx=idx)
            rec["skill_name"] = grp["name"]
            records.append(rec)

    if records:
        batch_trash_dir.mkdir(parents=True, exist_ok=True)
        (batch_trash_dir / "manifest.json").write_text(
            json.dumps({"deleted_at": ts, "skills": deleted_skills, "records": records}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    importlib.reload(scan_skills)
    new_data = scan_skills.run_full_scan(HOME_DIR, save_index=True, reaggregate_only=True)
    return {
        "ok": True,
        "deleted_skills": deleted_skills,
        "removed_instances_count": len(records),
        "trash_dir": str(batch_trash_dir) if records else "",
        "data": new_data,
    }


def delete_single_instance(skill_name: str, skill_md_path: str) -> Dict[str, Any]:
    """仅删除某个 Skill 的单处路径副本；若删的是物理源目录，同时自动清理指向它的失效悬空软链。"""
    cur_data = get_cached_or_scan(force_rescan=False)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_trash_dir = TRASH_ROOT / f"{ts}-single"
    records = []

    rec = _safe_remove_instance(skill_md_path, batch_trash_dir, idx=1)
    rec["skill_name"] = skill_name
    records.append(rec)

    # 检查同组中是否有指向该被删目录的失效软链接，一并清理避免产生死链
    for grp in cur_data.get("skill_groups", []):
        if grp["name"] == skill_name:
            for inst in grp.get("instances", []):
                p = Path(inst["skill_md_path"])
                d = p.parent
                if d.is_symlink() and not d.exists():
                    d.unlink()
                    records.append({"action": "unlink_broken_symlink", "path": str(d), "skill_name": skill_name})

    batch_trash_dir.mkdir(parents=True, exist_ok=True)
    (batch_trash_dir / "manifest.json").write_text(
        json.dumps({"deleted_at": ts, "skill": skill_name, "records": records}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    importlib.reload(scan_skills)
    new_data = scan_skills.run_full_scan(HOME_DIR, save_index=True, reaggregate_only=True)
    return {
        "ok": True,
        "removed_instances_count": len(records),
        "trash_dir": str(batch_trash_dir),
        "data": new_data,
    }


class LocalHubHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write(f"[Local-Skill-Hub] {fmt % args}\n")

    def _send_json(self, data: Dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            ui_path = BASE_DIR / "ui" / "index.html"
            raw = ui_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        if parsed.path == "/api/health":
            self._send_json({
                "ok": True,
                "service": "skill-hub",
                "pid": os.getpid(),
                "hub_dir": str(BASE_DIR),
            })
            return

        if parsed.path == "/api/skills":
            self._send_json(get_cached_or_scan(force_rescan=False))
            return

        if parsed.path == "/api/launcher-config":
            self._send_json({
                "ok": True,
                "config": get_launcher_config(),
                "installed_apps": detect_installed_apps(),
                "config_file": str(LAUNCHER_CONFIG_FILE),
            })
            return

        self._send_json({"ok": False, "error": "Not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        try:
            body = self._read_json()
            if parsed.path == "/api/scan":
                data = get_cached_or_scan(force_rescan=True)
                self._send_json({"ok": True, "data": data})
                return

            if parsed.path == "/api/launch":
                res = launch_local_tool(
                    app_id=body.get("app", ""),
                    workdir=body.get("workdir", ""),
                    target_path=body.get("target_path", ""),
                    custom_item=body.get("custom_item"),
                )
                self._send_json(res)
                return

            if parsed.path == "/api/launcher-config":
                saved = save_launcher_config(body)
                self._send_json({"ok": True, "config": saved})
                return

            if parsed.path == "/api/skill/save":
                res = save_skill_content(
                    skill_md_path=body["skill_md_path"],
                    content=body["content"],
                )
                self._send_json(res)
                return

            if parsed.path == "/api/skill/link":
                res = link_skill_to_apps(
                    skill_name=body["skill_name"],
                    canonical_dir=body["canonical_dir"],
                    apps=body.get("apps", ["claude", "codex", "cursor", "agents"]),
                )
                self._send_json(res)
                return

            if parsed.path == "/api/suite/link":
                suite_id = body["suite_id"]
                apps = body.get("apps", ["claude", "codex", "cursor", "agents"])
                cur_data = get_cached_or_scan(force_rescan=False)
                linked_skills = []
                for grp in cur_data.get("skill_groups", []):
                    if grp.get("suite_id") == suite_id:
                        safe_name = grp["name"].split("/")[-1]
                        link_skill_to_apps(
                            skill_name=safe_name,
                            canonical_dir=grp["canonical_dir"],
                            apps=apps,
                        )
                        linked_skills.append(grp["name"])
                new_data = scan_skills.run_full_scan(HOME_DIR, save_index=True, reaggregate_only=False)
                self._send_json({"ok": True, "linked_count": len(linked_skills), "data": new_data})
                return

            if parsed.path == "/api/skill/delete":
                names = body.get("skill_names") or ([body["skill_name"]] if body.get("skill_name") else [])
                res = delete_skills_by_names(names)
                self._send_json(res)
                return

            if parsed.path == "/api/skill/delete-instance":
                res = delete_single_instance(
                    skill_name=body["skill_name"],
                    skill_md_path=body["skill_md_path"],
                )
                self._send_json(res)
                return

            if parsed.path == "/api/suite/delete":
                suite_id = body["suite_id"]
                cur_data = get_cached_or_scan(force_rescan=False)
                names = [
                    grp["name"]
                    for grp in cur_data.get("skill_groups", [])
                    if grp.get("suite_id") == suite_id and grp.get("is_user_skill")
                ]
                res = delete_skills_by_names(names)
                self._send_json(res)
                return

            if parsed.path == "/api/skills/sync-all":
                importlib.reload(sync_skills)
                sync_res = sync_skills.sync_all_skills(dry_run=bool(body.get("dry_run", False)))
                data = get_cached_or_scan(force_rescan=True)
                self._send_json({"ok": True, "sync": sync_res, "data": data})
                return

            if parsed.path == "/api/server/stop":
                self._send_json({"ok": True, "message": "本地 Skill Hub 服务已关闭"})

                def _shutdown() -> None:
                    time.sleep(0.25)
                    _cleanup_pid_files()
                    os._exit(0)

                threading.Thread(target=_shutdown, daemon=True).start()
                return

            self._send_json({"ok": False, "error": f"Unknown endpoint {parsed.path}"}, status=404)
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=400)


def main() -> int:
    parser = argparse.ArgumentParser(description="本机 Skill 管理与 App 快捷启动台")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"本地端口 (默认 {DEFAULT_PORT})")
    args = parser.parse_args()

    PID_FILE.parent.mkdir(parents=True, exist_ok=True)

    srv = None
    bound_port = args.port
    for candidate_port in range(args.port, args.port + 20):
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", candidate_port), LocalHubHandler)
            bound_port = candidate_port
            break
        except OSError:
            continue

    if srv is None:
        sys.stderr.write(f"❌ 无法绑定端口 {args.port}~{args.port + 19}\n")
        return 1

    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    PORT_FILE.write_text(str(bound_port), encoding="utf-8")

    print(f"🚀 本地 Skill 管理与启动台已就绪: http://127.0.0.1:{bound_port} (PID: {os.getpid()})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        _cleanup_pid_files()
    return 0


if __name__ == "__main__":
    sys.exit(main())
