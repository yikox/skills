---
name: modular-status
description: Maintain `project-management.md` for the modular programming workflow. Use when starting, updating, completing, archiving, or summarizing tracked work; recording active tasks, requirements, change backlog rows, modular design indexes, ADR summaries, validation evidence, blockers, risks, roadmap, milestones, or Chinese requests such as 记录进行中, 完成记录, PM 更新, 项目状态, 设计索引, 归档.
---

# 模块化状态（Modular Status）

用这个 skill 让项目管理状态与"架构优先"的模块化工作流保持一致。PM 记录当前状态与持久证据；它不定义模块边界，也不应变成一份流水账。

## 必读参考

阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- 归档或压缩 PM 历史时阅读 `../_shared/references/pm-maintenance-rules.md`。

使用：

- `../_shared/assets/project-management-template.md`

## PM Start

对 L2/L3，在设计/实现工作开始之前或临近开始时，更新 `Active Tasks` 或其本地等价物。

对 L1，仅当工作跨会话、携带显著风险或发布证据、隶属于某个既有进行中任务，或用户明确希望被跟踪时，才使用 Active Tasks。否则跳过 PM start。

记录：

- 日期；
- 任务摘要；
- 主模块；
- 受影响模块；
- 变更级别；
- 状态；
- 下一步；
- 已知时，预期的设计/ADR/架构产物。

## PM Update

在以下情况更新同一任务或 backlog 行：

- 主模块变化；
- 受影响模块扩大；
- L1 变为 L2，或 L2 变为 L3；
- 设计、评审或人工接受状态变化；
- 任务被阻塞；
- 验证策略或风险发生实质变化。

## PM Complete

工作完成时，用以下内容更新 PM：

- 成果；
- 最终状态；
- 变更的设计或架构路径；
- 验证命令/结果；
- 实现证据；
- 架构基线是否发生变化。

然后按文档的风格，移除、标记完成或归档陈旧的 active-task 行。

对未被跟踪的 L1 工作，仅当结果是有价值的未来上下文时，才倾向于补一条简洁的 `Recent Updates` 条目。不要为例行的 L1 工作添加归档行。

## Backlog 与设计索引

用 Requirements / Change Backlog 记录已请求但尚未实现的工作。包含主模块、受影响模块、级别、范围/影响与下一步。

用 Modular Design Index 记录主架构、模块文档、架构变更、ADR 与模块变更。

不要重复普通的提交日志。记录持久的项目状态，而非每一次文件编辑。

## 归档

只有在保留了最终状态、设计路径与证据之后，才归档已实现、已过时或已被取代的工作。保持当前架构基线与在用目标设计处于被索引状态。

归档候选、受保护状态与压缩遵循 `pm-maintenance-rules.md`。
