---
title: 受控词表单一事实源（vocab 清单）
level: L3
status: implemented
review_status: reviewed
primary_module: shared-references
impacted_modules: [audit-checker]
---

# 受控词表单一事实源（vocab 清单）

## Request

消除受控词表在"规则散文"与"checker 硬编码"之间的同步耦合。评估痛点 1：`module_kind / status / review_status / relation / style` 五类词表以散文形式散落在多个 reference 文件，又以 Python set 硬编码在 checker，两侧无自动交叉校验，靠人工"同一变更内同步"。用户已选定方案 A（机器可读清单作唯一 owner）。

## Current Baseline

- checker 硬编码词表（唯一被强制的一份）：`check_modular_project.py:28-38`
  - `MODULE_FORMS` = {atomic, composite}
  - `MODULE_KINDS` = 9 类（layout-style … utility-support）
  - `RELATION_KINDS` = {uses, reads, writes, triggers, distributes}、`RELATION_STYLES` = {solid, dashed}
  - `DESIGN_STATUSES`、`REVIEW_STATUSES`
- 同批词表的散文副本分布（verified）：
  - module_kind：`module-authoring-rules.md`、`module-kind-classification.md`
  - status/review_status：`storage-schema.md`、`review-rules.md`、`module-kind-classification.md`
  - relation/style：`architecture-graph-json-format.md`（arch-graph/v0.3 契约）
- 现状：词表事实上由 audit-checker 隐式拥有，散文各自罗列枚举值；无单一事实源；基线 Shared Constraints 已把"规则文本与 checker 词表必须同一变更内同步"列为人工约束。

## Target Architecture

### 1. 新增受控词表清单（shared-references 拥有）

- 新文件 `modular-programming/_shared/references/vocab.md`，由 **shared-references** 模块拥有，作为全部受控词表的唯一事实源。
- 内容：module_form / module_kind / relation kind / relation style / design status / review status / requirement-task status 各一张表，列出枚举值（可含一句语义注释）。
- 格式对解析友好（稳定的 Markdown 表格或 fenced 列表），沿用项目 stdlib-only、无第三方依赖的风格。

### 2. checker 改为读取清单

- `check_modular_project.py` 启动时解析 `vocab.md`（复用手写 `parse_front_matter` 同风格的轻量解析，不引入 yaml/第三方），用解析结果替换硬编码 set。
- **过渡回退**：解析失败或清单缺项时，告警并回退到内置默认 set，保证 checker 永不因清单问题全表失效。
- 清单路径相对 checker 定位（`_shared/references/vocab.md`），随套件平铺分发后仍可解析。

### 3. 散文引用改造

- `module-authoring-rules.md`、`storage-schema.md`、`review-rules.md`、`architecture-graph-json-format.md`、`module-kind-classification.md` 中"罗列枚举值"的段落改为"引用 `vocab.md` 为准"，保留语义说明、去掉重复枚举。
- 各 reference 仍可解释每个词的含义与用法；唯一取消的是"并列的枚举清单副本"。

## Module Impact

| Module | Impact |
| --- | --- |
| shared-references | 新增 `vocab.md`（词表唯一 owner）；5 个散文文件的枚举段改为引用 |
| audit-checker | checker 改为运行时读取 `vocab.md`，删除硬编码 set，保留 fallback |

## Data Ownership

- 受控词表数据的 owner 从"audit-checker 隐式"迁移为"**shared-references 显式拥有**（`vocab.md`）"。
- audit-checker 与 shared-references 之间新增一条依赖边：**audit-checker `reads` shared-references/vocab**。两模块 module doc 的 Dependencies 节需同步这条边。
- 这是本设计的核心所有权决策，需在评审要点摘要中明确。

## Migration Loop（单模块闭环，独立提交）

1. 确认词表所有权归 shared-references → 2. 定义并落地 `vocab.md` 契约（格式、字段）→ 3. checker 增加清单解析 + fallback（旧 set 暂留作 fallback）→ 4. 5 个散文文件改为引用 → 5. 删除 checker 硬编码 set 的"主用"路径（仅留 fallback 常量）→ 6. 更新 audit-checker / shared-references 两个 module doc 的 Dependencies（新增 `audit-checker reads shared-references`）→ 7. 在架构图 `architecture/graphs/current-project.arch.json` 增加同一条 `reads` 关系并重渲染 `rendered/current-project-architecture.{html,svg}`（保持 doc Dependencies ⊆ graph relations）→ 8. 同步 shared-references module doc 的 Constraints 与 `main-design.md` Shared Constraints 中"规则文本与 checker 词表须手工同步"一句（该约束被本设计消解）→ 独立提交。

## Risks / Rollback

- 清单解析出错可能让 checker 校验全表失效 → 步骤 3 的 fallback 常量兜底：解析失败即告警并用内置默认词表继续，单 commit 可回滚整套改造。
- 清单格式若过于自由会增加解析脆弱性 → 固定表格结构，解析规则写入 vocab.md 顶部注释。
- 分发一致性：`vocab.md` 属 `_shared/references/**`，installer 平铺复制自动覆盖，无需改 installer。

## Validation（提案阶段的预期验证信号，落地时执行）

- `python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'` 仍 0 error / 0 warning。
- 新增 test：向 `vocab.md` 加入一个假词 → checker 接受该假词、拒绝一个已删除的旧词，证明"清单驱动"生效而非仍走硬编码。
- fallback test：破坏/删除 `vocab.md` → checker 告警并回退默认词表，不崩溃。
- `python3 -m unittest discover -s modular-programming/modular-audit/tests` 全绿。
- `./install.sh --dry-run` 覆盖含 `vocab.md`。
- 架构图渲染无误，`current-project.arch.json` 含新 `audit-checker reads shared-references` 关系，rendered html/svg 已更新；checker `check_graph` 无 error。

## Review Notes

- 状态：accepted / reviewed。由 modular-architect 依据 2026-07-04 评估痛点 1 提出，用户选定方案 A。
- 人工接受（2026-07-04）：用户接受词表所有权归 shared-references、新增 `audit-checker reads shared-references` 依赖边、fallback 策略。
- 决策：**不补 ADR**（用户决定）——A over B 的理由记录于本文档 Target Architecture 与本节，不单独立 ADR。
- modular-review：机械合规、迁移闭环已补图更新步骤（见 Migration Loop 步骤 7-8）。
