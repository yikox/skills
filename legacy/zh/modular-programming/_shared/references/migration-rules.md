# 模块化迁移规则

在用模块化编程工作流替换较旧的项目记忆或架构设计文档时使用这些规则。

## 迁移目标

在规划重构之前，建立一个可信的、以架构为先的基线。迁移不是重写代码的许可证。

## 现有项目流程

1. 检查仓库结构、入口点、运行时配置、测试、数据/状态存储、IO 边界、生成物与文档。
2. 从技术归属边界推断当前模块，而不只是从文件夹名称。
3. 将每条模块事实标注为 `verified`、`inferred` 或 `unclear`。
4. 撰写 `architecture/main-design.md` 与 `architecture/modules/*.md`，为每个模块包含 `code_paths`（单一归属；见 `modular-workflow-rules.md` 的 Code Ownership）。
5. 仅在用户想要可视化或项目使用图评审时，才创建或更新架构图。
6. 把旧的 TODO、需求、进行中工作与已知缺陷，连同主模块、受影响模块与变更级别，迁入 PM 行。
7. 在 PM 中记录迁移缺口，而不是静默猜测。

## 旧技能名称

把以下这些当作遗留概念：

- `architecture-design`;
- `pm-init`;
- `pm-document-architecture`;
- `pm-record-requirement`;
- `pm-design-requirement`;
- `pm-track-status`;
- `pm-review-artifact`;
- `pm-audit-memory`;
- `pm-groom-roadmap`;
- `pm-record-knowledge`;
- `pm-migrate-memory`.

按职责把它们映射到新的模块化套件：

- 初始化与修复 -> `modular-init`；
- 架构/模块基线 -> `modular-architecture`；
- 请求接入与分支 architecture patch / 可选 proposal 流程 -> `modular-change`；
- 进行中/已完成的 PM 状态 -> `modular-status`；
- 自动评审 -> `modular-review`；
- 一致性审计与迁移 -> `modular-audit`；
- 可复用知识 -> `modular-knowledge`。

## 无历史包袱

只保留仍然有用的信息：

- 当前模块事实；
- 已接受的决策；
- 进行中或未来的工作；
- 实现证据；
- 可复用的运维知识。

归档或省略陈旧历史、重复的状态日志、旧的工作流描述，以及过时的设计草稿。
