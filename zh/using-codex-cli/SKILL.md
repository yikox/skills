---
name: using-codex-cli
description: Use when a task should run through the local Codex CLI, including non-interactive analysis, planning, code review, structured automation, session continuation, model or profile selection, MCP use, web-search decisions, or isolated code changes.
---

# 使用 Codex CLI

## 核心原则

让 Codex 承担主要推理与执行，调用它的 agent 只负责限定任务、等待完成和独立验收。无交互任务统一使用 `codex exec`，显式限定工作目录、审批策略和 sandbox。只读任务使用 `read-only`；写任务必须获得明确授权，并先由调用方创建独立 git worktree，再把 `-C` 指向该 worktree。

## 低带宽调度契约

Codex 的 JSONL 事件流只属于本地执行日志；`--output-last-message` 单独保存最终答复：

```text
调用方给出一次完整任务
  → Codex 独立推理、执行
  → stdout JSONL、stderr、最终消息分别写入系统临时文件
  → 调用方等待完成通知或最终输出唤醒
  → 检查退出码和 turn.completed
  → 只读取最终消息
  → 独立窄验收
  → 删除临时日志
```

- 禁止对 `--json` 使用 `tee`，禁止回传 reasoning、工具参数、原始 JSONL、原始 stderr、usage 或 thread 元数据。
- 任务提示一次说完整。已有计划只传原文或路径中的一种；要求 Codex 不复述计划、命令和长输出。
- 在提示末尾约定最终答复只含“状态、改动、验证、剩余风险”，不超过 1200 个中文字符。
- 默认不检查进度、进程状态或日志大小；使用宿主的完成通知或最长阻塞等待。超时后继续等待，不读取日志。
- 只有用户明确要求进度，或必须诊断失联时，才检查一次退出状态或经过 `jq` 严格过滤的事件类型。
- 需要续接时，只把准确 `thread_id` 保存在本地变量中，不打印；并发时不使用 `--last`。
- 独立验收使用窄输出命令。验收结束立即删除日志；承载交付改动的 worktree 不属于临时日志，不能自动删除。

## 调用前检查

```bash
command -v codex
codex --version
codex --help
codex exec --help
codex exec resume --help
```

参数、配置键和事件格式会变化；本机帮助优先于旧文档。自动化使用 `codex exec`，不要启动交互 TUI。审批参数是顶层参数，写在子命令之前：`codex -a never exec ...`，不是 `codex exec -a never ...`。

## 数据边界

- 本地 `codex` 命令通常仍会把提示和工具读取到的内容发送给已配置的模型服务。执行前确认用户已要求通过 Codex CLI 处理该任务，或已明确同意发送这部分任务上下文；技能被隐式命中本身不构成外发授权。
- 只发送完成任务所需的最小目录和文件。提示中给出工作区路径可能使 Codex 读取其中内容；先排除 `.env`、密钥、凭据、个人数据和任务范围外的专有资料。
- `--oss` 或本地 provider 也要先核实实际路由和数据边界。无法确认 provider、数据范围或授权时，先停下说明，不绕过安全审查。

## 选择调用方式

| 任务 | 审批与 sandbox | 工作目录 |
| --- | --- | --- |
| 解释、复核、查询、规划 | `-a never` + `--sandbox read-only` | `--cd <workspace>` |
| 获得授权的代码修改 | `-a never` + `--sandbox workspace-write` | `--cd <isolated-worktree>` |
| 需要调用方参与审批 | 不使用无人值守骨架；由支持审批事件的宿主直接编排 | 明确限定 |

`-a never` 表示无人值守时不发起交互审批：越界操作会失败并返回给模型。它必须与 `read-only` 或隔离 worktree 内的 `workspace-write` 配对；不能与 `danger-full-access` 或 `--dangerously-bypass-approvals-and-sandbox` 配对。

一次性任务且不需要续接时加 `--ephemeral`。需要续接时不要加，并从事件流中保存准确的 `thread_id`。

## 标准调用

短任务和长任务都使用同一静默捕获骨架，避免 JSONL 进入调用方上下文：

```bash
workspace="$PWD"
codex_log="$(mktemp "${TMPDIR:-/tmp}/codex-exec.XXXXXX")"
codex_err="$(mktemp "${TMPDIR:-/tmp}/codex-exec-error.XXXXXX")"
codex_final="$(mktemp "${TMPDIR:-/tmp}/codex-exec-final.XXXXXX")"

cleanup_codex_logs() {
  rm -f -- "$codex_log" "$codex_err" "$codex_final"
}
trap cleanup_codex_logs EXIT

codex_rc=0
codex -a never exec \
  --sandbox read-only \
  --cd "$workspace" \
  --ephemeral \
  --json \
  --output-last-message "$codex_final" \
  "只分析当前 git diff，报告有证据的正确性问题；不要修改文件。最终只报告状态、结论、验证和风险，不复述过程；不超过 1200 个中文字符。" \
  >"$codex_log" 2>"$codex_err" || codex_rc=$?

turn_state="$(
  jq -c 'select(
    .type == "turn.completed" or
    .type == "turn.failed"
  ) | {type, error}' "$codex_log" |
    tail -n 1
)"

if ((codex_rc != 0)); then
  printf 'codex failed: exit=%d turn=%s stderr_bytes=%s\n' \
    "$codex_rc" \
    "${turn_state:-missing}" \
    "$(wc -c <"$codex_err" | tr -d ' ')"
  exit "$codex_rc"
fi

if ! jq -e 'select(.type == "turn.completed")' \
  "$codex_log" >/dev/null ||
  [[ ! -s "$codex_final" ]]; then
  printf 'codex failed: exit=0 turn=%s final_bytes=%s\n' \
    "${turn_state:-missing}" \
    "$(wc -c <"$codex_final" | tr -d ' ')"
  exit 1
fi

jq -Rsr '
  if length > 4000
  then .[0:4000] + "\n[摘要已截断]"
  else .
  end
' "$codex_final"
```

提交后等待进程或会话句柄发出完成通知，不主动轮询。诊断时只读取最终事件类型、错误状态和 stderr 字节数；不要读取日志正文。把独立窄验收放在最终消息提取之后，验收结束时由 `trap` 删除三个临时文件。

若任务要求机器可验证的最终结构，在系统临时目录创建 JSON Schema，并传 `--output-schema <file>`；仍通过 `--output-last-message` 读取最终值。不要仅为一次调用在项目目录遗留 schema。

## 写任务

Codex CLI 没有与 Claude/Cursor 等价的写任务 `--worktree` 参数。只有用户明确允许修改文件和运行命令时，才先创建独立 worktree：

```bash
base_ref="$(git branch --show-current)"
test -n "$base_ref" || exit 2

worktree_parent="$(mktemp -d "${TMPDIR:-/tmp}/codex-worktree.XXXXXX")"
worktree="$worktree_parent/repo"
branch_name="codex/task-name"

git worktree add -b "$branch_name" "$worktree" "$base_ref"
```

为任务选择唯一、可读的 `branch_name`；不要覆盖已有分支。随后把标准骨架中的调用替换为：

```bash
codex -a never exec \
  --sandbox workspace-write \
  --cd "$worktree" \
  --ephemeral \
  --json \
  --output-last-message "$codex_final" \
  "实现指定任务并运行验证。最终只报告状态、改动、验证和风险，不复述计划、命令或长输出；不超过 1200 个中文字符。" \
  >"$codex_log" 2>"$codex_err" || codex_rc=$?
```

- 不给主工作区加 `--add-dir`，也不让多个写代理共享同一个 worktree。
- 不使用 `danger-full-access` 或危险 bypass；需要网络、额外目录或系统级操作时，停止无人值守调用，由外层宿主按动作审批。
- 完成后检查 worktree 的 diff 摘要和必要文件，并独立重跑窄验证。不要自动合并、应用或删除承载交付改动的 worktree。
- 任务验收失败时保留 worktree 供检查；只清理日志。没有交付改动且用户同意放弃时，才按 git worktree 的安全流程清理。

## 会话、模型与外部能力

需要续接时，不加 `--ephemeral`，从成功事件流提取准确 ID：

```bash
thread_id="$(
  jq -er 'select(.type == "thread.started") |
    .thread_id' "$codex_log" |
    tail -n 1
)"

codex -a never \
  --sandbox read-only \
  --cd "$workspace" \
  exec resume "$thread_id" \
  --json \
  --output-last-message "$codex_final" \
  "继续上一轮，只回答剩余问题。" \
  >"$codex_log" 2>"$codex_err" || codex_rc=$?
```

- 并发时禁止 `codex exec resume --last`；始终使用准确的 `thread_id`。续接写任务时继续指向同一个隔离 worktree，并保持 `workspace-write`。
- 只在任务需要时用 `--model`、`--profile` 或 `--config`；以本机帮助和用户配置为准，不硬编码完整模型清单或未验证的配置键。
- 用 `codex mcp list` 和 `codex mcp get <name>` 盘点外部能力。不要为了任务方便而隐式增删全局 MCP 配置。
- 只有用户明确要求最新网络信息时才使用顶层 `--search`，并把来源核验纳入验收。
- 认证使用 `codex login` 管理的本机状态或安全环境；不要把 token 写进命令、日志或项目文件。
- 中间输出只放系统临时目录，不在项目里遗留 JSONL、schema、最终消息副本或执行报告；任务明确要求交付报告时例外。

## 常见错误

| 错误 | 修正 |
| --- | --- |
| 直接调用交互式 `codex` | 自动化使用 `codex exec` |
| 把 `-a never` 写在 `exec` 后 | 审批参数放在顶层：`codex -a never exec` |
| 用 `-a never` 就认为只读 | 同时显式指定 `--sandbox read-only` |
| 写任务指向主工作区 | 先创建独立 git worktree，再用 `--cd` 指向它 |
| 用 `--add-dir` 暴露主工作区 | 保持单一、最小的可写根 |
| `--json \| tee` 保存日志 | JSONL、stderr、最终消息分别写系统临时文件 |
| 从 JSONL 重组最终答复 | 使用 `--output-last-message` |
| 定时轮询进程或日志大小 | 默认等待完成唤醒；诊断时做一次窄检查 |
| 并发时恢复 `--last` | 保存并使用准确的 `thread_id` |
| 为避免审批使用危险 bypass | 保持 read-only/workspace-write 边界，由外层宿主审批越界动作 |

## 完成检查

1. 确认退出码为 0、存在 `turn.completed`，且最终消息文件非空。
2. 确认调用方上下文中没有原始 JSONL、reasoning、工具参数、usage、完整命令回放或长 stderr。
3. 只读任务比较调用前后的状态和 diff 摘要；写任务检查隔离 worktree 的必要 diff。
4. 独立运行任务所需的窄测试或验证，不能只采信 Codex 总结。
5. 删除临时输出，不打印账号、密钥、thread ID 或请求 ID。
