---
name: using-codex-cli
code_paths:
  - zh/using-codex-cli/**
---

# using-codex-cli

## 职责

指导 agent 通过本地 Codex CLI 执行无交互分析、规划、复核、结构化自动化、会话续接与隔离代码修改；统一工作目录、审批、sandbox、低带宽输出和验收边界。仅在用户显式调用 `$using-codex-cli` 或明确要求使用本地 Codex CLI 时触发。

## 对外接口

- `$using-codex-cli`:SKILL.md 协议触发。
- `codex exec`:外部 CLI；skill 不封装脚本，只规定调用契约。

## 依赖

- 本机已安装并认证的 Codex CLI。
- 写任务由调用方创建 git worktree；JSONL 状态解析与最终消息截断示例依赖 `jq`。

## 注意点

- 自动化使用 `codex exec`；`-a never` 放在子命令前，并与 `read-only` 或隔离 worktree 内的 `workspace-write` 配对。
- 本地 CLI 仍可能把读取内容发给已配置 provider；隐式触发不构成数据外发授权，只发送用户授权的最小上下文。
- Codex CLI 没有写任务 worktree 参数；调用方必须先建 worktree，再用 `--cd` 指向它。
- JSONL、stderr 与 `--output-last-message` 分别写系统临时文件；成功条件是退出码为 0、存在 `turn.completed` 且最终消息非空。
- 禁止把无人值守骨架与 `danger-full-access` 或危险 bypass 组合；参数以本机帮助为准。
