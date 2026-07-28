---
name: using-claude-cli
description: Use when a task should run through the local Claude Code CLI, including headless analysis, planning, code review, structured automation, session continuation, model selection, MCP use, background-agent decisions, or isolated code changes.
---

# 使用 Claude CLI

## 核心原则

让 Claude Code 承担主要推理与执行，调用它的 agent 只负责限定任务、等待完成和独立验收。先限定权限、可用工具和工作目录，再调用 `claude`：只读任务使用 Plan 权限；写任务必须获得明确授权，并使用 Claude 原生 worktree、最小可用工具集和最小自动批准白名单。自动化始终使用 `--print`、显式输出格式并检查退出码。

## 低带宽调度契约

长任务的完整事件流只属于 Claude 的本地执行日志，不能再次进入调用方上下文：

```text
调用方给出一次完整任务
  → Claude 独立推理、执行
  → stdout JSONL 与 stderr 分别写入系统临时文件
  → 调用方等待完成通知或最终输出唤醒
  → 只提取最终 result 摘要
  → 独立窄验收
  → 删除临时日志
```

- 禁止对 `stream-json` 使用 `tee`，禁止回传 thinking、工具参数、原始 stdout/stderr、会话元数据或子代理全文。
- 任务提示一次说完整。已有计划只传原文或路径中的一种；要求 Claude 不复述计划、命令和长输出。
- 在提示末尾约定最终答复只含“状态、改动、验证、剩余风险”，不超过 1200 个中文字符。
- 默认不检查进度、进程状态或日志大小；使用宿主的完成通知或最长阻塞等待。超时后继续等待，不读取日志。
- 只有用户明确要求进度，或必须诊断失联时，才检查一次退出状态或经过 `jq` 严格过滤的必要字段。
- 完成后只解析成功的最终 `type=result` 事件。续接所需的准确 `session_id` 只保存在本地变量中，不打印。
- 独立验收使用窄输出命令，只返回退出状态、服务状态、HTTP 状态码或必要字段。验收结束立即删除日志。

短只读任务可使用单对象 `json`，但仍须在 shell 内先过滤，再把 `.result` 交给调用方。

## 调用前检查

```bash
command -v claude
claude --version
claude --help
```

参数、权限模式和模型别名会变化；本机 `--help` 优先于旧文档。无交互任务使用 `claude --print`，不要启动交互 TUI。Claude 没有独立的 `--workspace` 参数；在受信任的目标目录内启动子 shell，并仅在确有需要时使用 `--add-dir`。

## 数据边界

- 本地 `claude` 命令通常仍会把提示和工具读取到的内容发送给已配置的模型服务。执行前确认用户已要求通过 Claude CLI 处理该任务，或已明确同意发送这部分任务上下文；技能被隐式命中本身不构成外发授权。
- 只发送完成任务所需的最小目录和文件。提示中给出工作区路径可能使 Claude 读取其中内容；先排除 `.env`、密钥、凭据、个人数据和任务范围外的专有资料。
- 无法确认配置的 provider、数据范围或用户授权时，先停下说明；不要通过换命令、换网络路径或危险权限参数绕过。

## 选择调用方式

| 任务 | 必要参数 | 输出 |
| --- | --- | --- |
| 简短解释、复核、查询 | `--print --permission-mode plan --tools ...` | `json` |
| 长只读分析或规划 | `--print --permission-mode plan --tools ... --verbose` | `stream-json` |
| 获得授权的代码修改 | `--print --permission-mode acceptEdits --worktree <name> --tools ... --allowedTools ... --verbose` | `stream-json` |

一次性任务且不需要续接时加 `--no-session-persistence`。需要续接时不要加，并从成功结果中保存准确的 `session_id`。

## 标准短只读调用

```bash
workspace="$PWD"
response="$(
  cd -- "$workspace" &&
  claude \
    --print \
    --permission-mode plan \
    --tools "Read,Grep,Glob,Bash" \
    --no-session-persistence \
    --output-format json \
    "只分析当前 git diff，报告有证据的正确性问题；不要修改文件。"
)" || exit $?

printf '%s\n' "$response" |
  jq -er 'select(
    .type == "result" and
    .subtype == "success" and
    .is_error == false
  ) | .result | tostring |
  if length > 4000 then .[0:4000] + "\n[摘要已截断]" else . end'
```

JSON 模式成功时产生一个最终对象。不要依赖默认文本输出，也不要把完整 JSON 直接送回调用方。

## 标准长任务调用

以下骨架默认是长只读任务；写任务只替换其中的 Claude 参数：

```bash
workspace="$PWD"
claude_log="$(mktemp "${TMPDIR:-/tmp}/claude-code.XXXXXX")"
claude_err="$(mktemp "${TMPDIR:-/tmp}/claude-code-error.XXXXXX")"

cleanup_claude_logs() {
  rm -f -- "$claude_log" "$claude_err"
}
trap cleanup_claude_logs EXIT

claude_rc=0
(
  cd -- "$workspace" &&
  claude \
    --print \
    --permission-mode plan \
    --tools "Read,Grep,Glob,Bash" \
    --no-session-persistence \
    --verbose \
    --output-format stream-json \
    "完成给定任务。最终只报告状态、结论、验证和风险，不复述过程；不超过 1200 个中文字符。"
) >"$claude_log" 2>"$claude_err" || claude_rc=$?

result_state="$(
  jq -c 'select(.type == "result") |
    {subtype, is_error}' "$claude_log" |
    tail -n 1
)"

if ((claude_rc != 0)); then
  printf 'claude failed: exit=%d result=%s stderr_bytes=%s\n' \
    "$claude_rc" \
    "${result_state:-missing}" \
    "$(wc -c <"$claude_err" | tr -d ' ')"
  exit "$claude_rc"
fi

jq -er 'select(
  .type == "result" and
  .subtype == "success" and
  .is_error == false
) | .result | tostring |
if length > 4000 then .[0:4000] + "\n[摘要已截断]" else . end' "$claude_log"
```

提交后等待进程或会话句柄发出完成通知，不主动轮询。诊断时只读取最终事件类型、错误状态和 stderr 字节数；不要读取日志正文。把独立窄验收放在最终 `jq` 之后，验收结束时由 `trap` 删除日志。

## 写任务

只有用户明确允许修改文件和运行命令时，才把标准长任务骨架中的 Claude 调用替换为：

```bash
(
  cd -- "$workspace" &&
  claude \
    --print \
    --permission-mode acceptEdits \
    --worktree claude-task-name \
    --tools "Read,Grep,Glob,Edit,Write,Bash" \
    --allowedTools \
      "Edit" \
      "Write" \
      "Bash(git status *)" \
      "Bash(git diff *)" \
      "Bash(<validation command>)" \
    --verbose \
    --output-format stream-json \
    "实现指定任务并运行验证。最终只报告状态、改动、验证和风险，不复述计划、命令或长输出；不超过 1200 个中文字符。"
) >"$claude_log" 2>"$claude_err" || claude_rc=$?
```

- 从预期基线分支启动 Claude；`--worktree` 没有独立的 base 参数。
- 把 `<validation command>` 替换为任务实际需要的窄命令，并将 Bash 白名单收紧到必要前缀；不要照抄占位符。
- `--tools` 限制 Claude 可选择的内建工具；`--allowedTools` 只预先批准其中的必要操作。两者不能互相替代。
- `acceptEdits` 只处理编辑授权，不能替代工具范围、Bash 白名单或外部系统授权。
- 不使用 `--dangerously-skip-permissions`。只有外层已经提供无网络、无凭据且限制写入范围的独立沙箱，并且用户明确授权时，才重新评估这一例外。
- 完成后用 `git worktree list --porcelain` 定位 worktree，检查 diff 摘要和必要文件，并独立重跑窄验证。不要自动合并或删除仍承载交付改动的 worktree。

## 会话、模型与外部能力

需要续接时，先从成功结果中提取准确 ID，再显式恢复：

```bash
session_id="$(
  jq -er 'select(
    .type == "result" and
    .subtype == "success" and
    .is_error == false
  ) | .session_id' "$claude_log" |
  tail -n 1
)"

claude --print --resume "$session_id" \
  --permission-mode plan \
  --tools "Read,Grep,Glob,Bash" \
  --output-format json \
  "继续上一轮，只回答剩余问题。"
```

- 并发时不要用 `--continue` 或无参数的 `--resume`；需要保留原会话时加 `--fork-session`。
- 只在任务需要时用 `--model`、`--effort` 或 `--fallback-model`；以本机帮助和用户指定值为准，不硬编码完整模型清单。
- 用 `claude mcp list` 和 `claude mcp get <name>` 盘点外部能力。临时配置优先用 `--mcp-config`；需要排除隐式配置时加 `--strict-mcp-config`。
- 不默认启用 Chrome、远程控制、插件、`--forward-subagent-text`、`--include-partial-messages` 或 hook 事件。
- 只有用户明确要求脱离当前调用生命周期执行时才使用 `--background`，并先确认宿主能追踪和唤醒该 agent。
- 认证通过安全环境或本机凭据存储完成；不要把 API key 写进命令、日志或项目文件。

## 常见错误

| 错误 | 修正 |
| --- | --- |
| 用 `--print` 就认为只读 | 明确使用 `--permission-mode plan` |
| 在错误目录启动 | 先进入受信任的目标目录；额外目录用最小 `--add-dir` |
| 写任务直接操作当前工作区 | 使用 Claude 原生 `--worktree` |
| 写任务默认放开全部 Bash | 用任务级 `--allowedTools` 白名单 |
| `stream-json \| tee` 保存日志 | stdout/stderr 分别重定向到系统临时文件 |
| 开启 partial、hook 或子代理转发 | 默认关闭，只提取最终 result |
| 定时轮询进程或日志大小 | 默认等待完成唤醒；诊断时做一次窄检查 |
| 续接最近会话 | 保存并使用准确的 `session_id` |
| 自动化使用危险跳过权限 | 保持 Plan/acceptEdits 与工具白名单边界 |

## 完成检查

1. 确认退出码为 0，且存在 `subtype=success`、`is_error=false` 的最终 result。
2. 确认调用方上下文中没有原始 JSONL、thinking、工具参数、完整命令回放或长 stdout/stderr。
3. 只读任务比较调用前后的状态和 diff 摘要；写任务检查隔离 worktree 的必要 diff。
4. 独立运行任务所需的窄测试或验证，不能只采信 Claude 总结。
5. 删除临时输出，不打印账号、密钥、会话 ID 或请求 ID。
