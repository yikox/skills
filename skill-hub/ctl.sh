#!/bin/bash
set -euo pipefail

# ctl.sh - Skill Hub 本地服务启停与 macOS App 交互控制脚本 (兼容 macOS bash 3.2)
# 用法:
#   ./ctl.sh start    # 启动后台服务并打开管理面板
#   ./ctl.sh stop     # 停止后台服务
#   ./ctl.sh restart  # 重启后台服务并打开管理面板
#   ./ctl.sh status   # 查看服务运行状态
#   ./ctl.sh gui      # macOS App 双击入口（未启动则一键启动并打开；已启动则弹出控制面板选择打开/重启/关闭）

HUB_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${SKILL_HUB_PORT:-8765}"
URL="http://127.0.0.1:${PORT}"
PID_FILE="${HUB_DIR}/vault/server.pid"
LOG_FILE="${HUB_DIR}/vault/server.log"

find_python() {
  for p in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3; do
    if [ -x "$p" ]; then
      echo "$p"
      return 0
    fi
  done
  command -v python3
}

get_running_pid() {
  local pid=""
  if command -v lsof >/dev/null 2>&1; then
    pid="$(lsof -ti tcp:"${PORT}" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
  fi
  if [ -z "$pid" ] && [ -f "$PID_FILE" ]; then
    local saved_pid
    saved_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [ -n "$saved_pid" ] && kill -0 "$saved_pid" 2>/dev/null; then
      pid="$saved_pid"
    fi
  fi
  echo "$pid"
}

notify_macos() {
  local title="$1"
  local msg="$2"
  osascript -e "display notification \"${msg}\" with title \"${title}\"" >/dev/null 2>&1 || true
}

start_server() {
  local open_browser="${1:-1}"
  local pid
  pid="$(get_running_pid)"
  if [ -n "$pid" ]; then
    echo "🟢 Skill Hub 已在运行中 (PID: ${pid} | ${URL})"
    if [ "$open_browser" = "1" ]; then
      open "$URL"
    fi
    return 0
  fi

  mkdir -p "${HUB_DIR}/vault"
  local py_bin
  py_bin="$(find_python)"
  nohup "$py_bin" "${HUB_DIR}/server.py" --port "$PORT" >"$LOG_FILE" 2>&1 &
  local new_pid=$!
  echo "$new_pid" >"$PID_FILE"

  # 等待端口就绪（最多 2 秒）
  local i=0
  while [ $i -lt 20 ]; do
    if [ -n "$(get_running_pid)" ]; then
      break
    fi
    sleep 0.1
    i=$((i + 1))
  done

  echo "🚀 Skill Hub 已启动 (PID: ${new_pid} | ${URL})"
  if [ "$open_browser" = "1" ]; then
    open "$URL"
  fi
}

stop_server() {
  local pid
  pid="$(get_running_pid)"
  if [ -z "$pid" ]; then
    pkill -f "${HUB_DIR}/server.py" 2>/dev/null || true
    rm -f "$PID_FILE"
    echo "⚪ Skill Hub 当前未运行"
    return 0
  fi

  kill "$pid" 2>/dev/null || true
  pkill -f "${HUB_DIR}/server.py" 2>/dev/null || true
  rm -f "$PID_FILE"
  echo "🛑 Skill Hub 已停止 (原 PID: ${pid})"
}

gui_entry() {
  local pid
  pid="$(get_running_pid)"
  if [ -z "$pid" ]; then
    start_server 1
    notify_macos "Skill Hub 已启动" "管理面板已打开: ${URL}"
    return 0
  fi

  # 若已在运行，弹出原生对话框方便一键打开、重启或关闭
  local choice
  choice="$(osascript -e "button returned of (display dialog \"🟢 Skill Hub 正在后台运行中\\n\\n地址: ${URL}\\n进程 PID: ${pid}\" with title \"Skill Hub 控制台\" buttons {\"🛑 关闭服务\", \"🔄 重启服务\", \"🌐 打开面板\"} default button \"🌐 打开面板\")" 2>/dev/null || true)"

  case "$choice" in
    "🛑 关闭服务")
      stop_server
      notify_macos "Skill Hub 已关闭" "后台服务 (PID: ${pid}) 已安全退出"
      ;;
    "🔄 重启服务")
      stop_server
      sleep 0.2
      start_server 1
      notify_macos "Skill Hub 已重启" "管理面板已重新加载: ${URL}"
      ;;
    "🌐 打开面板")
      open "$URL"
      ;;
    *)
      ;;
  esac
}

cmd="${1:-gui}"
case "$cmd" in
  start)
    start_server 1
    ;;
  start-headless)
    start_server 0
    ;;
  stop)
    stop_server
    ;;
  restart)
    stop_server
    sleep 0.2
    start_server 1
    ;;
  status)
    pid="$(get_running_pid)"
    if [ -n "$pid" ]; then
      echo "🟢 运行中 (PID: ${pid} | ${URL})"
    else
      echo "⚪ 未运行"
    fi
    ;;
  gui)
    gui_entry
    ;;
  *)
    echo "用法: $0 {start|stop|restart|status|gui}" >&2
    exit 1
    ;;
esac
