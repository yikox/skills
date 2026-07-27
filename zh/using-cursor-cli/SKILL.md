---
name: using-cursor-cli
description: Use when a task should run through the local Cursor Agent CLI, including headless analysis, planning, code review, structured automation, session continuation, model selection, MCP use, or isolated code changes.
---

# 使用 Cursor CLI

## 核心原则

先限定权限和工作区，再调用 `cursor-agent`。只读任务用 Ask/Plan；写任务必须获得明确授权，并放进独立 worktree。自动化始终显式指定输出格式并检查退出码。

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
  ) | .result'
```

JSON 模式成功时产生一个最终对象。长任务改用 `stream-json`；逐行消费 NDJSON，并把最终 `type=result` 事件作为完成条件。需要暂存流时用系统临时文件，并设置 `trap` 在退出时删除。不要依赖默认输出格式。

## 写任务

只有用户明确允许修改文件和运行命令时，才使用：

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
  "实现指定任务，运行验证，并总结改动。"
```

需要其他基线时显式替换 `base_ref`。完成后定位 Cursor 创建的 worktree，检查完整 diff，并独立重跑验证。不要让多个写代理共享同一工作目录，也不要自动把结果合回主工作区。

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
cursor-agent mcp list-tools <server>
```

- 模型 ID 从 `models` 动态获取，不硬编码展示名或完整列表。
- 自动化认证通过安全环境注入 `CURSOR_API_KEY`；不要把密钥放进 `--api-key`、命令日志或项目文件。
- 先盘点 MCP 及工具，再按需启用；不要默认传 `--approve-mcps`。
- 中间输出放系统临时目录或通过管道处理，不在项目里遗留 `r1.json`、日志等过程文件。

## 常见错误

| 错误 | 修正 |
| --- | --- |
| 只写 `-p` 就认为只读 | 明确使用 `--mode ask` 或 `--plan` |
| 省略工作区和沙箱 | 显式写 `--workspace` 与 `--sandbox enabled` |
| 无交互调用卡在信任提示 | 对已核实目录加 `--trust` |
| 写任务直接操作当前目录 | 使用 Cursor 内建 `--worktree` |
| 看到 stdout 就判定成功 | 先查退出码，再验证最终 result 事件 |
| 并发时续接最近会话 | 保存并使用准确的 `session_id` |

## 完成检查

1. 确认进程退出码为 0，结构化输出存在成功的最终 result。
2. 只读任务比较调用前后的状态和 diff 摘要；写任务检查隔离 worktree 的 diff。
3. 独立运行任务所需的测试或验证，不能只采信代理总结。
4. 删除本轮产生的临时输出，不打印账号、密钥、会话 ID 或请求 ID。
