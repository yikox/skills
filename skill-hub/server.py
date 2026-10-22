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
  python3 server.py [--port 8765]
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

APP_TARGETS = {
    "claude": HOME_DIR / ".claude" / "skills",
    "codex": HOME_DIR / ".codex" / "skills",
    "cursor": HOME_DIR / ".cursor" / "skills",
    "agents": HOME_DIR / ".agents" / "skills",
}


def get_cached_or_scan(force_rescan: bool = False) -> Dict[str, Any]:
    if not force_rescan and INDEX_OUTPUT_PATH.exists():
        try:
            return json.loads(INDEX_OUTPUT_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    importlib.reload(scan_skills)
    return scan_skills.run_full_scan(HOME_DIR, save_index=True)


def launch_local_tool(app_id: str, workdir: str = "", target_path: str = "") -> Dict[str, Any]:
    """在 macOS 本机启动 CLI (拉起终端进入工作目录) 或 GUI 应用。"""
    resolved_dir = Path(os.path.expanduser(workdir)).resolve() if workdir else HOME_DIR
    if not resolved_dir.exists():
        resolved_dir = HOME_DIR

    cli_commands = {
        "codex": "codex",
        "claude": "claude",
        "cursor_cli": "cursor-agent",
        "terminal": "",
    }

    if app_id in cli_commands:
        cli_bin = cli_commands[app_id]
        quoted_dir = shlex.quote(str(resolved_dir))
        shell_cmd = f"cd {quoted_dir} && clear && {cli_bin}" if cli_bin else f"cd {quoted_dir} && clear"

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
                    "message": f"已在 {'iTerm2' if has_iterm else 'Terminal'} 中启动 {cli_bin or '终端'} (目录: {resolved_dir})",
                }
        except Exception:
            pass

        cmd_script = Path(f"/tmp/aihub-launch-{app_id}.command")
        script_body = (
            "#!/usr/bin/env zsh\n"
            f"cd {quoted_dir} || exit 1\n"
            "clear\n"
            f'echo "🚀 已进入工作目录: $(pwd)"\n'
        )
        if cli_bin:
            script_body += f'echo "⚡ 正在启动 {cli_bin} ..."\nexec {cli_bin}\n'
        else:
            script_body += "exec zsh -l\n"
        cmd_script.write_text(script_body, encoding="utf-8")
        cmd_script.chmod(0o755)
        subprocess.run(["open", str(cmd_script)], check=False)
        return {
            "ok": True,
            "message": f"已通过系统终端拉起 {cli_bin or 'Shell'} (目录: {resolved_dir})",
        }

    if app_id == "cursor_app":
        open_target = target_path if target_path else str(resolved_dir)
        subprocess.run(["open", "-a", "Cursor", open_target], check=False)
        return {"ok": True, "message": f"已使用 Cursor 打开: {open_target}"}

    if app_id == "claude_app":
        subprocess.run(["open", "-a", "Claude"], check=False)
        return {"ok": True, "message": "已唤起 Claude 桌面客户端"}

    if app_id == "codex_app":
        res = subprocess.run(["open", "-a", "Codex", str(resolved_dir)], capture_output=True, text=True)
        if res.returncode == 0:
            return {"ok": True, "message": f"已唤起 Codex App ({resolved_dir})"}
        return launch_local_tool("codex", workdir=str(resolved_dir))

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

        if parsed.path == "/api/skills":
            self._send_json(get_cached_or_scan(force_rescan=False))
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
                )
                self._send_json(res)
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
                    try:
                        if PID_FILE.exists():
                            PID_FILE.unlink()
                    except Exception:
                        pass
                    os._exit(0)

                threading.Thread(target=_shutdown, daemon=True).start()
                return

            self._send_json({"ok": False, "error": f"Unknown endpoint {parsed.path}"}, status=404)
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=400)


def main() -> int:
    parser = argparse.ArgumentParser(description="本机 Skill 管理与 App 快捷启动台")
    parser.add_argument("--port", type=int, default=8765, help="本地端口 (默认 8765)")
    args = parser.parse_args()

    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), LocalHubHandler)
    print(f"🚀 本地 Skill 管理与启动台已就绪: http://127.0.0.1:{args.port} (PID: {os.getpid()})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        try:
            if PID_FILE.exists():
                PID_FILE.unlink()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
