---
name: using-claude-cli
code_paths:
  - zh/using-claude-cli/**
---

# using-claude-cli

## 职责

指导 agent 通过本地 Claude Code CLI 执行只读分析、规划、复核、结构化自动化、会话续接与隔离代码修改；统一工作目录、权限、低带宽输出和验收边界。

## 对外接口

- `$using-claude-cli`:SKILL.md 协议触发。
- `claude`:外部 CLI；skill 不封装脚本，只规定调用契约。

## 依赖

- 本机已安装并认证的 Claude Code CLI。
- 写任务的隔离模式依赖 Claude 原生 `--worktree`；结构化结果解析示例依赖 `jq`。

## 注意点

- 自动化使用 `--print`；只读任务用 Plan 权限和受限工具集，写任务用原生 worktree、`acceptEdits`、最小工具集与任务级自动批准白名单。
- 本地 CLI 仍可能把读取内容发给已配置 provider；隐式触发不构成数据外发授权，只发送用户授权的最小上下文。
- `stream-json` 的 stdout 和 stderr 分别写系统临时文件，禁止回传原始事件；默认等待完成唤醒。
- 成功条件是退出码为 0 且存在成功的最终 `type=result`；验收完成后删除临时日志。
- 参数、权限模式和模型以本机 `claude --help` 为准，不固化完整模型清单。
