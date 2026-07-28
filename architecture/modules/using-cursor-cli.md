---
name: using-cursor-cli
code_paths:
  - zh/using-cursor-cli/**
---

# using-cursor-cli

## 职责

指导 agent 通过本地 Cursor Agent CLI 执行只读分析、规划、复核、结构化自动化与隔离代码修改；统一入口、权限、工作区、低带宽输出、会话和验收边界。Cursor 承担主要推理与执行，调用方默认等待完成唤醒，只接收最终摘要与窄验收结果。

## 对外接口

- `$using-cursor-cli`:SKILL.md 协议触发。
- `cursor-agent`:外部 CLI；skill 不封装脚本，只规定调用契约。

## 依赖

- 本机已安装并认证的 Cursor Agent CLI。
- 写任务的隔离模式依赖 git worktree；结构化结果解析示例依赖 `jq`。

## 注意点

- `--trust` 不等于 `--force`；写任务必须先获明确授权并使用独立 worktree。
- `stream-json` 的 stdout 和 stderr 分别写系统临时文件，禁止 `tee` 或回传原始事件；默认不轮询，等待完成通知或最终输出唤醒。
- 宿主没有完成通知时使用最长阻塞等待；只有用户要求进度或必须诊断失联时才做窄状态检查。
- 成功条件是退出码为 0 且存在成功的最终 `type=result`；验收完成后删除临时日志。
- 参数默认值以本机 `cursor-agent --help` 为准，不在 skill 中固化模型清单。
