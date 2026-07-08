---
name: modular-review
description: Review modular programming artifacts before acceptance or completion. Use when the agent should check module routing, L0/L1/L2/L3 classification, PM start/completion records, architecture baseline vs target separation, module docs, branch architecture patches, optional proposals, ADRs, graph relations, artifact indexes, or Chinese requests such as 模块化评审, 架构评审, 设计审核, 自动审核.
---

# 模块化评审（Modular Review）

把这个 skill 作为模块化编程产物的自动评审者。它发现不一致并修复清晰的低风险缺陷，但不替代人工对重大方向的接受。

## 必读参考

阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`
- 评审图 JSON 时阅读 `../_shared/references/architecture-graph-json-format.md`。

## 工作流

1. 识别产物类型：PM 行、架构基线、分支 architecture patch、可选 proposal、ADR、模块文档、图，或完成证据。
2. 阅读为可追溯性所需的关联 PM 行、架构文档、模块文档与产物索引条目。
3. 检查模块关卡、变更级别、受影响模块、状态同步、基线/目标分离、评审状态、轻量 PM 的适配度，以及开放问题。
4. 修复清晰的机械性缺陷，如缺失路径、陈旧的索引状态、失效的本地链接或缺失的评审标签。
5. 对含糊的模块归属、范围、架构方向、产品权衡或接受决策，记录待人工回答的问题。
6. 仅当不再有阻塞性问题时，才把评审标记为 `reviewed`。
7. 先报告发现，再报告修复，最后报告开放问题。

## 人工接受的边界

自动评审可以说一个产物内部自洽。它不得：

- 接受 L3 架构方向；
- 批准产品范围的权衡；
- 在没有证据的情况下把一个分支 patch 或可选 proposal 标记为已实现；
- 在未经用户确认的情况下，从实质不同的模块归属选项中做出选择。
