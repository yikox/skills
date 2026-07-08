# 模块化编程工作流

本项目采用 modular-programming 工作流。架构文档负责界定模块边界；`project-management.md`（PM）负责记录工作状态与证据。

## 偏好设置

- `docs-language`: <zh | en | follow-project> — PM、架构、知识、可选 proposal 文档以及决策摘要所使用的语言。
- `confirmation`: <high-touch | standard | low-touch> — 确认粒度；具体语义在工作流的 Preference Profiles 中定义。`low-touch` 绝不跳过 L3 接受、模块地图批准、首次写入 AI 文档，或 L2 到 L3 的提升。

## 会话入口

- 新会话开始时，在进行非平凡工作前先阅读 `project-management.md` 与 `architecture/main-design.md`。
- 如果请求与某个进行中任务相关，先询问用户是否恢复该任务。切勿静默恢复、重复创建或关闭进行中任务。

## 模块闸门与级别

非平凡变更在实现规划之前必须指明主模块、受影响模块和级别。默认选择既能保留未来可理解性、又最轻量的路径：

- L0 平凡编辑：实现并验证；PM 可选。Bug 修复至少为 L1：先复现，修复后验证失败用例，完成时记录根因。
- L1 局部变更：实现 -> 验证 -> 简洁证据。仅当工作跨会话、携带风险/发布证据、属于某个既有进行中任务，或用户要求跟踪时，才使用 Active Tasks。
- L2 模块变更：PM 启动 -> 决策摘要 + 用户确认 -> 功能分支第一颗 architecture patch commit -> 实现 -> 验证 -> PM 完成。
- L3 架构变更：PM 启动 -> 决策摘要 + 用户接受 -> 功能分支第一颗 architecture patch commit / 必要时 ADR -> 实现 -> 验证 -> PM 完成。

如果主模块或根因不明确，先进入诊断模式：复现、检查并收集证据，不做结构性变更，也不宣称完成。

L2/L3 默认使用分支携带的 architecture patch。除非复杂度、离线评审或非 git 协作确实需要，否则不要创建长期独立 proposal 文件。architecture patch 分支必须在代码与模块地图一致后才能合并。

L2/L3 确认请求必须在请求本身中内嵌一份 3-8 条的决策摘要（关键变更、模糊点、风险）——而不是放在此前另一条消息里——以便用户无需打开独立 proposal 即可决策。

## 技能路由

面向用户的主要入口：

- `modular-init`：搭建或修复工作流文件。
- `modular-change`：任何功能、bug 修复或重构请求。
- `modular-audit`：一致性检查、老项目迁移、PM 压缩。
- `modular-knowledge`：记录可复用的命令、事实与经验。

内部或高级入口：

- `modular-architecture`：模块地图、ADR、基线更新以及可选的图可视化。
- `modular-autopilot`：针对已接受并已评审的 L2/L3 architecture patch 或可选 proposal 的高级自主执行。
- `modular-advisor`：面向模块化评估、老项目重构提案与新项目模块化设计讨论的高级顾问角色；仅出提案，绝不实现。
- `modular-status`：需要显式跟踪时的 PM 启动/更新/完成/归档。
- `modular-review`：检查 architecture patch、可选 proposal、ADR、PM 行以及维护的图。
