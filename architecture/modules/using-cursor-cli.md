---
name: using-cursor-cli
code_paths:
  - zh/using-cursor-cli/**
---

# using-cursor-cli

## 职责

指导 agent 通过本地 Cursor Agent CLI 执行只读分析、规划、复核、结构化自动化与隔离代码修改；统一入口、权限、工作区、输出、会话和验收边界。

## 对外接口

- `$using-cursor-cli`:SKILL.md 协议触发。
- `cursor-agent`:外部 CLI；skill 不封装脚本，只规定调用契约。

## 依赖

- 本机已安装并认证的 Cursor Agent CLI。
- 写任务的隔离模式依赖 git worktree；结构化结果解析示例依赖 `jq`。

## 注意点

- `--trust` 不等于 `--force`；写任务必须先获明确授权并使用独立 worktree。
- 参数默认值以本机 `cursor-agent --help` 为准，不在 skill 中固化模型清单。
