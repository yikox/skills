---
name: using-cursor-cli
description: Use when a task should run through the local Cursor Agent CLI, including headless analysis, planning, code review, structured automation, session continuation, model selection, MCP use, or isolated code changes.
---

# 使用 Cursor CLI

## 核心原则

让 Cursor 承担主要推理与执行，调用它的 agent 只负责限定任务、等待完成和独立验收。先限定权限和工作区，再调用 `cursor-agent`：只读任务用 Ask/Plan；写任务必须获得明确授权，并放进独立 worktree。自动化始终显式指定输出格式并检查退出码。

## 低带宽调度契约

长任务的完整事件流只属于 Cursor 的本地执行日志，不能再次进入调用方上下文：

```text
调用方给出一次完整任务
  → Cursor 独立推理、执行
  → stdout NDJSON 与 stderr 分别写入系统临时文件
  → 调用方等待完成通知或最终输出唤醒
  → 只提取最终 result 摘要
  → 独立窄验收
  → 删除临时日志
```

- 禁止对 `stream-json` 使用 `tee`，禁止把 NDJSON、thinking、工具参数、原始 stdout/stderr 或会话元数据回显到调用方。
- 任务提示一次说完整。已有计划只传原文或路径中的一种；要求 Cursor 不复述计划、命令和长输出。
- 在提示末尾约定最终答复只含“状态、改动、验证、剩余风险”，不超过 1200 个中文字符。
- 默认不检查进度、进程状态或日志大小；使用宿主的完成通知或阻塞等待，让 Cursor 的最终输出唤醒调用方。
- 如果宿主只有带超时的等待接口，使用它允许的最长等待；超时后继续等待，不读取日志。只有用户明确要求进度，或必须判断进程是否失联时，才检查一次必要状态；下载进度也只在被要求时返回速度和预计剩余时间。
- 完成后只解析最终 `type=result` 成功事件；需要续接时把准确的 `session_id` 留在本地变量中，不打印。
- 独立验收使用窄输出命令，只返回退出状态、服务状态、HTTP 状态码或必要字段。验收结束立即删除完整日志。

短只读任务可直接使用单对象 `json`，但仍须在 shell 内先过滤，再把 `.result` 交给调用方。

## 调用前检查

```bash
command -v cursor-agent
cursor-agent --version
cursor-agent --help
```

参数、默认值和模型会变化；本机 `--help` 优先于旧文档。自动化使用 `cursor-agent`，不用可能冲突的 `agent` 别名。

## 选择调用方式

| 任务 | 必要参数 | 输出 |
| --- | --- | --- |
| 解释、复核、查询 | `--mode ask --sandbox enabled` | `json` |
| 只读实施规划 | `--plan --sandbox enabled` | `json` |
| 获得授权的代码修改 | `--force --sandbox enabled --worktree <name>` | `stream-json` |

无交互任务都加：

```text
--print --trust --workspace <path> --output-format <format>
```

`--trust` 只确认工作区可信；它不等于 `--force`。不要用 `--yolo` 代替权限判断。

## 标准只读调用

```bash
response="$(
  cursor-agent \
    --print \
    --mode ask \
    --sandbox enabled \
    --trust \
    --workspace "$PWD" \
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

JSON 模式成功时产生一个最终对象。不要依赖默认输出格式。

## 标准长任务调用

长只读任务和写任务都使用同一个静默捕获模式。以下骨架中的 Cursor 参数和任务描述按任务类型替换：

```bash
cursor_log="$(mktemp "${TMPDIR:-/tmp}/cursor-agent.XXXXXX")"
cursor_err="$(mktemp "${TMPDIR:-/tmp}/cursor-agent-error.XXXXXX")"

cleanup_cursor_logs() {
  rm -f -- "$cursor_log" "$cursor_err"
}
trap cleanup_cursor_logs EXIT

cursor_rc=0
cursor-agent \
  --print \
  --mode ask \
  --sandbox enabled \
  --trust \
  --workspace "$PWD" \
  --output-format stream-json \
  "完成给定任务。最终只报告状态、结论、验证和风险，不复述过程；不超过 1200 个中文字符。" \
  >"$cursor_log" 2>"$cursor_err" || cursor_rc=$?

result_state="$(
  jq -c 'select(.type == "result") |
    {subtype, is_error}' "$cursor_log" |
    tail -n 1
)"

if ((cursor_rc != 0)); then
  printf 'cursor-agent failed: exit=%d result=%s stderr_bytes=%s\n' \
    "$cursor_rc" \
    "${result_state:-missing}" \
    "$(wc -c <"$cursor_err" | tr -d ' ')"
  exit "$cursor_rc"
fi

jq -er 'select(
  .type == "result" and
  .subtype == "success" and
  .is_error == false
) | .result | tostring |
if length > 4000 then .[0:4000] + "\n[摘要已截断]" else . end' "$cursor_log"
```

向执行工具提交这条命令后，等待进程或会话句柄发出完成通知；不要主动轮询。宿主没有完成通知时，使用最长的阻塞等待并在超时后继续等待。除非用户要求进度或必须诊断失联，不要查询状态，更不要读取日志正文；诊断应使用 `jq` 选择必要字段并设置严格长度上限，而不是输出原始文件。把独立窄验收追加在同一 shell 工作流的最终 `jq` 之后，验收结束时由 `trap` 删除日志。

## 写任务

只有用户明确允许修改文件和运行命令时，才把标准长任务骨架中的 `cursor-agent` 调用替换为：

```bash
base_ref="$(git branch --show-current)"
test -n "$base_ref" || exit 2

cursor-agent \
  --print \
  --force \
  --sandbox enabled \
  --trust \
  --workspace "$PWD" \
  --worktree cursor-task-name \
  --worktree-base "$base_ref" \
  --output-format stream-json \
  "实现指定任务并运行验证。最终只报告状态、改动、验证和风险，不复述计划、命令或长输出；不超过 1200 个中文字符。" \
  >"$cursor_log" 2>"$cursor_err" || cursor_rc=$?
```

保留骨架中的退出码检查、最终 result 提取和清理逻辑。需要其他基线时显式替换 `base_ref`。完成后定位 Cursor 创建的 worktree，检查 diff 摘要和必要文件，并独立重跑窄验证；不要把完整 diff 默认送入调用方上下文。不要让多个写代理共享同一工作目录，也不要自动把结果合回主工作区。

## 会话、模型与外部能力

从成功 JSON 的 `.session_id` 续接指定会话：

```bash
cursor-agent --print --resume "$session_id" --mode ask \
  --sandbox enabled --trust --workspace "$PWD" \
  --output-format json "继续上一轮，只回答剩余问题。"
```

并发时不要用“最近会话”的 `resume` 或 `--continue`。

```bash
cursor-agent status --format json
cursor-agent models
cursor-agent mcp list
cursor-agent mcp list-tools server-name
```

- 模型 ID 从 `models` 动态获取，不硬编码展示名或完整列表。
- 自动化认证通过安全环境注入 `CURSOR_API_KEY`；不要把密钥放进 `--api-key`、命令日志或项目文件。
- 先盘点 MCP 及工具，再按需启用；不要默认传 `--approve-mcps`。
- 中间输出只放系统临时目录，不在项目里遗留 `r1.json`、`EXECUTION.md`、日志等过程文件。任务确实要求交付报告时才在项目内创建报告。

## 常见错误

| 错误 | 修正 |
| --- | --- |
| 只写 `-p` 就认为只读 | 明确使用 `--mode ask` 或 `--plan` |
| 省略工作区和沙箱 | 显式写 `--workspace` 与 `--sandbox enabled` |
| 无交互调用卡在信任提示 | 对已核实目录加 `--trust` |
| 写任务直接操作当前目录 | 使用 Cursor 内建 `--worktree` |
| `stream-json \| tee` 保存日志 | 用 `>` 和 `2>` 分别写系统临时文件，不回显 |
| 定时轮询进程或日志大小 | 默认等待完成唤醒；仅在用户要求进度或诊断失联时做窄检查 |
| Cursor 读取后复述整份计划 | 只给一种输入，并在提示中禁止复述 |
| 看到 stdout 就判定成功 | 先查退出码，再验证最终 result 事件 |
| 并发时续接最近会话 | 保存并使用准确的 `session_id` |

## 完成检查

1. 确认进程退出码为 0，结构化输出存在成功的最终 result。
2. 确认调用方上下文中没有原始 NDJSON、thinking、完整命令回放或长 stdout/stderr。
3. 只读任务比较调用前后的状态和 diff 摘要；写任务检查隔离 worktree 的必要 diff。
4. 独立运行任务所需的窄测试或验证，不能只采信代理总结。
5. 删除本轮产生的临时输出，不打印账号、密钥、会话 ID 或请求 ID。
