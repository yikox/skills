---
title: 拆分 module-kind-classification.md 为索引 + 分片（保契约）
level: L2
status: implemented
review_status: reviewed
primary_module: shared-references
impacted_modules: []
---

# 拆分 module-kind-classification.md 为索引 + 分片（保契约）

## Request

评估痛点 3：`module-kind-classification.md` 单文件 917 行，占整个 references 语料约 45%，承载 9 个同构 kind 段落，是规则层可理解性最低点。改任一 kind 模板需在超大文件里定位。目标：在**不破坏现有引用契约**的前提下拆小。

## Current Baseline

- `modular-programming/_shared/references/module-kind-classification.md`：917 行。
- 9 个 kind 段落各约 67 行、结构同构（`什么模块属于这类` / `图形设计` / `展开方式` / `文档模板`），起始行：
  - layout-style:91、function-flow:160、interface-object:233、data-state:301、event-message:369、config-rule:436、resource-file:503、adapter-io:571、utility-support:637
- 文件名是活契约，被 4 处引用（verified）：`module-authoring-rules.md`、`storage-schema.md`、`_shared/scripts/renderer-docs/module-kind-taxonomy.md`、`modular-architecture/SKILL.md`。
- 归属：`shared-references` 的 `code_paths: ["modular-programming/_shared/references/**"]` 已覆盖子目录。

## Target Design（向后兼容重组，语义零漂移）

### 1. 主文件瘦身为索引，文件名保留

- `module-kind-classification.md` **保留原路径与文件名**，内容瘦身为总览：`底层分类总览`、`通用 front matter`、`选择规则`，加一张"9 类 → 分片链接"的索引表。
- 现有 4 处引用零改动即可继续解析（主文件仍在）。

### 2. 9 个 kind 段落抽为分片

- 新增 `modular-programming/_shared/references/module-kinds/<kind>.md`，每个 kind 一文件（如 `function-flow.md`），含原"什么模块属于这类 / 图形设计 / 展开方式 / 文档模板"四节。
- 迁移为**纯搬运**：措辞不变，仅移动位置。

### 3. 消二次重复（可选，同一变更内）

- 若 `renderer-docs/module-kind-taxonomy.md` 或 `module-authoring-rules.md` 逐字复述了某 kind 的定义，改为引用对应分片，减少重复；不改语义。

## Module Impact

| Module | Impact |
| --- | --- |
| shared-references | 主文件瘦身为索引；新增 `module-kinds/` 分片目录（`references/**` 已覆盖，无孤儿/幽灵） |

外部契约无变化：`impacted_modules: []`，无跨模块契约改动。

## Migration Loop（纯文档搬运，独立提交）

1. 确认分片边界（1 kind = 1 文件）→ 2. 建 `module-kinds/` 目录、逐 kind 原文迁移 → 3. 主文件替换为索引 + 链接表 → 4. 更新 4 处引用处的锚点/链接（若指向具体 kind 小节）→ 5. 校验无残留重复段 → 独立提交。

## Risks / Rollback

- 纯文档搬运，无运行时风险；分片过碎可再合并。
- 唯一注意：引用方若锚定到主文件的具体小节标题，拆分后需改指向分片；步骤 4 覆盖。
- `git diff` 应显示迁移块为纯移动、措辞未变（语义零漂移证明）。

## Validation（提案阶段的预期验证信号，落地时执行）

- 契约兼容证明：`grep -rl module-kind-classification modular-programming/` 的 4 处引用仍能解析（主文件仍在）。
- `python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'` 0 error / 0 warning（`references/**` 自动覆盖新子目录）。
- `git diff` 确认 kind 段落为纯移动。

## Review Notes

- 状态：accepted / reviewed。由 modular-architect 依据 2026-07-04 评估痛点 3 提出；modular-review 实证 4 处引用无锚点、契约兼容，用户 2026-07-04 接受。
- 定级说明：shared-references 内部重组，主文件名（活契约）保留 → L2，`impacted_modules` 为空。若评审认为应显式改 `code_paths` 或引用方式，可升级讨论。
- 提案者不落地：接受后交 `modular-change` 执行，module doc 与 PM 完成记录由执行方更新。
