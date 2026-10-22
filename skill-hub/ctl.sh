#!/bin/bash
set -euo pipefail

# ctl.sh - Skill Hub 本地服务启停与原生窗口控制脚本 (兼容 macOS bash 3.2)
# 用法:
#   ./ctl.sh app      # 打开 macOS 独立桌面窗口 (Dock 图标 + 顶部状态栏图标，关窗口自动停服务)
#   ./ctl.sh start    # 启动后台服务并打开浏览器
#   ./ctl.sh stop     # 停止后台服务（严格校验进程身份，绝不误杀同端口其他服务如 AgentBridge）
#   ./ctl.sh restart  # 重启后台服务
#   ./ctl.sh status   # 查看服务运行状态

HUB_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_PORT="${SKILL_HUB_PORT:-8788}"
PID_FILE="${HUB_DIR}/vault/server.pid"
PORT_FILE="${HUB_DIR}/vault/server.port"
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

# 严格校验 PID 是否属于当前 Skill Hub 的 server.py 进程（防止误认/误杀 AgentBridge 等其他服务）
is_skill_hub_pid() {
  local pid="${1:-}"
  case "$pid" in
    ''|*[!0-9]*) return 1 ;;
  esac
  if ! kill -0 "$pid" 2>/dev/null; then
    return 1
  fi
  local cmdline
  cmdline="$(ps -p "$pid" -o command= 2>/dev/null || true)"
  case "$cmdline" in
    *"${HUB_DIR}/server.py"*|*"skill-hub/server.py"*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

get_running_pid() {
  # 1. 优先从 PID_FILE 读取并校验进程身份
  if [ -f "$PID_FILE" ]; then
    local saved_pid
    saved_pid="$(tr -d '[:space:]' <"$PID_FILE" 2>/dev/null || true)"
    if is_skill_hub_pid "$saved_pid"; then
      echo "$saved_pid"
      return 0
    else
      rm -f "$PID_FILE" "$PORT_FILE"
    fi
  fi

  # 2. 通过进程命令行精确查找 skill-hub/server.py
  if command -v pgrep >/dev/null 2>&1; then
    local cand
    for cand in $(pgrep -f "${HUB_DIR}/server.py" 2>/dev/null || true); do
      if is_skill_hub_pid "$cand"; then
        echo "$cand"
        return 0
      fi
    done
  fi

  # 3. 兜底检查端口监听进程，但必须通过 is_skill_hub_pid 身份核验
  if command -v lsof >/dev/null 2>&1; then
    local port_cand
    for port_cand in $(lsof -ti tcp:"${DEFAULT_PORT}" -sTCP:LISTEN 2>/dev/null || true); do
      if is_skill_hub_pid "$port_cand"; then
        echo "$port_cand"
        return 0
      fi
    done
  fi

  echo ""
}

get_active_port() {
  local pid="${1:-}"
  if [ -f "$PORT_FILE" ]; then
    local saved_port
    saved_port="$(tr -d '[:space:]' <"$PORT_FILE" 2>/dev/null || true)"
    if [ -n "$saved_port" ]; then
      echo "$saved_port"
      return 0
    fi
  fi
  if [ -n "$pid" ] && command -v lsof >/dev/null 2>&1; then
    local lsof_port
    lsof_port="$(lsof -Pan -p "$pid" -iTCP -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {sub(/.*:/, "", $9); print $9; exit}' || true)"
    if [ -n "$lsof_port" ]; then
      echo "$lsof_port"
      return 0
    fi
  fi
  echo "$DEFAULT_PORT"
}

start_server() {
  local open_browser="${1:-1}"
  local pid
  pid="$(get_running_pid)"
  if [ -n "$pid" ]; then
    local active_port
    active_port="$(get_active_port "$pid")"
    local url="http://127.0.0.1:${active_port}"
    echo "$pid" >"$PID_FILE"
    echo "$active_port" >"$PORT_FILE"
    echo "🟢 Skill Hub 已在运行中 (PID: ${pid} | ${url})"
    if [ "$open_browser" = "1" ]; then
      open "$url"
    fi
    return 0
  fi

  mkdir -p "${HUB_DIR}/vault"
  local py_bin
  py_bin="$(find_python)"
  nohup "$py_bin" "${HUB_DIR}/server.py" --port "$DEFAULT_PORT" >"$LOG_FILE" 2>&1 &
  local new_pid=$!

  local i=0
  while [ $i -lt 30 ]; do
    if [ -f "$PID_FILE" ] && [ -f "$PORT_FILE" ]; then
      local check_pid
      check_pid="$(get_running_pid)"
      if [ -n "$check_pid" ]; then
        break
      fi
    fi
    sleep 0.1
    i=$((i + 1))
  done

  local final_pid
  final_pid="$(get_running_pid)"
  if [ -z "$final_pid" ]; then
    echo "❌ Skill Hub 启动失败，请查看日志: ${LOG_FILE}" >&2
    return 1
  fi

  local active_port
  active_port="$(get_active_port "$final_pid")"
  local url="http://127.0.0.1:${active_port}"
  echo "🚀 Skill Hub 已启动 (PID: ${final_pid} | ${url})"
  if [ "$open_browser" = "1" ]; then
    open "$url"
  fi
}

stop_server() {
  local stopped_any=0
  local pid
  pid="$(get_running_pid)"
  if [ -n "$pid" ] && is_skill_hub_pid "$pid"; then
    kill "$pid" 2>/dev/null || true
    stopped_any=1
  fi

  if command -v pgrep >/dev/null 2>&1; then
    local cand
    for cand in $(pgrep -f "${HUB_DIR}/server.py" 2>/dev/null || true); do
      if is_skill_hub_pid "$cand"; then
        kill "$cand" 2>/dev/null || true
        stopped_any=1
      fi
    done
  fi

  rm -f "$PID_FILE" "$PORT_FILE"
  if [ "$stopped_any" = "1" ]; then
    echo "🛑 Skill Hub 服务已停止"
  else
    echo "⚪ Skill Hub 未在运行（未触碰任何其他进程）"
  fi
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
      active_port="$(get_active_port "$pid")"
      echo "🟢 运行中 (PID: ${pid} | http://127.0.0.1:${active_port})"
    else
      echo "⚪ 未运行"
    fi
    ;;
  *)
    echo "用法: $0 {app|start|stop|restart|status}" >&2
    exit 1
    ;;
esac
