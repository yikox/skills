---
name: modular-change
description: Route and execute project changes through the architecture-first modular programming workflow. Use when a user asks for a feature, bug fix, refactor, behavior change, module modification, architecture change, or implementation work; classifies L0/L1/L2/L3, enforces primary-module routing, records PM when tracking is needed, creates branch-carried architecture patches or optional proposals, coordinates review and implementation; Chinese triggers include 修改流程, 模块修改, 功能开发, bug 修复, 重构, 需求转实现.
---

# 模块化变更（Modular Change）

把它作为日常开发的入口。默认走能保留未来理解的最轻路径：L0/L1 应保持快速；L2/L3 默认使用分支携带的 architecture patch，只有复杂/离线评审才写独立 proposal 文档。

## 必读参考

阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`

仅在需要可选 proposal 路径时使用：

- `../_shared/assets/module-change-template.md`
- `../_shared/assets/architecture-change-template.md`
- `../_shared/assets/adr-template.md`

## 工作流

1. 阅读用户请求与当前项目上下文。
2. 若存在，阅读 `architecture/main-design.md` 及相关的 `architecture/modules/*.md`。
3. 用 `modular-workflow-rules.md` 中的硬性级别规则判断变更是 L0、L1、L2 还是 L3。对 L3，先告知用户并确认，再进入分支 architecture patch 路径。
4. 识别主模块与受影响模块。当模块文档声明了 `code_paths` 时，通过把你预期会改动的路径与各模块的 `code_paths` 求交集，确定性地定位主模块。
5. 若一个非平凡变更缺少清晰的主模块或根因，先进入诊断模式：复现、检查、收集证据，不做结构性改动，也不下完成结论。若归属仍不清晰，用 `modular-architecture` 修复模块地图或记录一处架构缺口。
6. 对 L2/L3，在 architecture patch 或实现工作之前用 `modular-status` 记录 PM start。对 L1，仅在工作跨会话、携带发布/风险证据、隶属于某个既有进行中任务，或用户明确希望被跟踪时，才记录 PM。
7. 遵循下面对应级别的路径。
8. 验证实现。
9. 对 L2/L3，功能分支的 architecture patch 先更新目标基线；合并前必须验证代码与基线一致。对 L0/L1，仅当持久的模块行为、契约、关系或约束发生变化时才更新架构基线；项目维护图时才重新渲染受影响的图。
10. 对 L2/L3 及被跟踪的 L1 工作，用 `modular-status` 记录 PM 完成与证据；否则仅在持久上下文有价值时补一条简洁的完成备注。

## 级别路径

### L3 架构变更

当变更影响模块边界、跨模块契约、核心数据/状态归属、运行时模型、持久化、外部系统，或持久的架构方向时使用。

```text
PM start -> decision summary (3-8 bullets) -> human acceptance
-> create/switch feature branch -> first architecture patch commit updates PM + target module map
-> implementation plan -> implement -> verify
-> close PM and archive/delete process files
-> merge only when code and map agree
```

请求接受时，给出一份 3-8 条的决策摘要，涵盖关键改动、含糊之处与风险，让用户无需打开独立 proposal 即可决策。把摘要内嵌到确认请求本身之中，而不仅仅放在之前的单独消息里。

一旦接受，创建或切换到功能分支，并把第一颗 commit 作为 architecture patch。该 commit 更新 `architecture/main-design.md`、受影响模块文档与 PM active 行到已接受的目标状态。不要把这颗 commit 脱离实现单独合入 main。只有复杂、跨天、离线或非 git 评审才写独立 proposal 文档。

### L2 模块变更

当某个模块仍是所有者，但其内部结构或非平凡行为发生变化时使用。

1. 记录 PM start，包含主模块、受影响模块、级别与预期 architecture patch。
2. 准备 3-8 条 architecture patch 摘要，涵盖当前状态、目标地图改动、契约影响、验证、风险与开放问题。
3. 请求用户确认，并把摘要内嵌于确认请求本身之中。
4. 确认后，创建或切换到功能分支，并用第一颗 commit 提交 architecture patch：更新 PM 与受影响模块文档到已接受的目标状态。
5. 只有 architecture patch commit 存在之后才实现。或者，把已接受的分支 patch 交给 `modular-autopilot` 做自主执行与收尾。
6. 合并前，验证实现与目标模块地图一致。

### L1 轻量模块变更

当某个模块有一处不改变边界或公开契约的局部行为变化时使用。

1. 判断这个 L1 是否需要 PM 跟踪。对例行的同会话工作，跳过 Active Tasks。
2. 实现并验证。
3. 仅当基线否则会误导未来工作时，才更新模块文档。
4. 记录简洁证据：被跟踪的 L1 记 PM 完成，否则仅在未来上下文需要时补一条简短的 Recent Updates 备注。

### L0 琐碎变更

用于错别字、格式、注释、微小的文档措辞、局部常量，以及不改变行为或模块理解的机械性编辑。

1. 在明显时标注所属模块。
2. 实现并验证。
3. 仅当用户明确要求跟踪、编辑隶属于某个进行中任务，或发布证据有价值时，才更新 PM。

## Bug 修复路由

Bug 修复遵循 `modular-workflow-rules.md` 中的 Bug Fix Path：

- 至少 L1（bug 修复改变行为）；修复前先复现或采集证据。
- 若根因或所有者不清晰，从诊断模式起步：复现、检查、收集证据，不做结构性改动。
- 单个模块内的小型局部修复 -> L1：可选的带症状轻量 PM 备注 -> 复现 -> 根因 -> 修复 -> 验证失败用例及既有验证 -> 简洁证据。
- 单个模块内的结构性根因或多步修复 -> L2：architecture patch 摘要或可选 proposal 必须包含根因分析。
- 根因位于模块边界或跨模块契约 -> 与用户确认 L3。

## 升级规则

- 若 L1 长成一次多步重构，把它升为 L2 并记录 PM 更新。
- 若 L2 改变了模块契约或跨模块归属，与用户确认升级到 L3。
- 若实现中发现模块地图是错的，暂停实现，先修复架构再继续。

## 完成规则

在满足以下条件之前，不要把工作标记为完成：

- 存在验证证据；
- L2/L3 及被跟踪的 L1 工作已记录 PM 完成；
- PM 完成记录指向 architecture patch commit 与实现证据；
- 分支架构基线已反映落地的持久变更，并与代码一致。
