#!/bin/bash
set -euo pipefail

# ctl.sh - Skill Hub 本地服务启停与原生窗口控制脚本 (兼容 macOS bash 3.2)
# 用法:
#   ./ctl.sh app      # 打开 macOS 独立桌面窗口 (Dock 图标 + 顶部状态栏图标，关窗口自动停服务)
#   ./ctl.sh start    # 启动后台服务并打开浏览器
#   ./ctl.sh stop     # 停止后台服务与桌面窗口
#   ./ctl.sh restart  # 重启后台服务
#   ./ctl.sh status   # 查看服务运行状态

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

start_server() {
  local open_browser="${1:-1}"
  local pid
  pid="$(get_running_pid)"
  if [ -n "$pid" ]; then
    echo "$pid" >"$PID_FILE"
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

  local i=0
  while [ $i -lt 25 ]; do
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
  if [ -n "$pid" ]; then
    kill "$pid" 2>/dev/null || true
  fi
  pkill -f "${HUB_DIR}/server.py" 2>/dev/null || true
  rm -f "$PID_FILE"
  echo "🛑 Skill Hub 服务已停止"
}

cmd="${1:-app}"
case "$cmd" in
  app|gui)
    open "${HUB_DIR}/Skill Hub.app"
    ;;
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
  *)
    echo "用法: $0 {app|start|stop|restart|status}" >&2
    exit 1
    ;;
esac
