---
name: modular-knowledge
description: Maintain `knowledge-summary.md` for reusable modular programming project knowledge. Use when the agent should record or recall verified commands, module facts, conventions, troubleshooting results, architecture lessons, validation workflows, operational notes, reusable decisions, or Chinese requests such as 记录知识, 记住这个, 项目知识, 故障结论, 可复用经验.
---

# 模块化知识（Modular Knowledge）

用这个 skill 把持久的项目知识与 PM 状态、架构基线分开保存。

## 必读参考

阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`

使用：

- `../_shared/assets/knowledge-summary-template.md`

## 记录什么

记录经核实、可复用的知识：

- 用于构建、测试、lint、发布、部署或诊断项目的命令；
- 在实现或调试中发现的稳定模块事实；
- 项目约定与命名规则；
- 故障排查的症状、原因与修复；
- 环境约束；
- 验证工作流；
- 应指导未来模块化变更的经验教训。

不要记录临时草稿、完整提交日志、密钥，或属于 PM 的状态更新。

## 工作流

1. 阅读 `knowledge-summary.md` 及相关的架构/PM 上下文。
2. 判断这条信息是否在当前任务之外仍可复用。
3. 在能保留该事实的最小章节中新增或更新。
4. 有价值时，链接到架构文档、ADR、提交、PR 或 issue 引用。
5. 保持条目简洁且基于证据。
