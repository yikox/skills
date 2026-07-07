---
title: 证据单一居所 + 记账面减重（写入时防重复）
level: L2
status: implemented
review_status: reviewed
primary_module: shared-references
impacted_modules: [shared-assets]
---

# 证据单一居所 + 记账面减重（写入时防重复）

## Request

评估（`docs/modularization/2026-07-08-assessment.md`）发现 PM 主文件同一事实最多记 5 处。根因：规则只有"事后压缩"侧（pm-maintenance-rules 的 Compression Triggers），缺"写入时"规则；PM 模板提供过多平行记账面。用户确认先修根因，再做一次性压缩。

## Current Module State

- `_shared/references/pm-maintenance-rules.md`：仅含归档/压缩规则，无写入时的证据落点规则。
- `_shared/assets/project-management-template.md`：含 Testing and Validation、Roadmap、Milestones 平行节，Archive Evidence 列无粒度约束。
- 四个模板含 Review Notes 节（main-design / module-design / architecture-change / module-change）。
- checker 对 PM 只校验 Active Tasks 与 Modular Design Index 表，对基线/设计文档只校验 front matter（含 `review_status`），不依赖上述任何散文节（`check_modular_project.py:96,192,456,466`）。

## Target Module Design

### 1. pm-maintenance-rules.md 新增 "Evidence Single Home"（写入时规则）

- 每份证据只有一个居所：有设计文档的工作（L2/L3、被跟踪 L1），验证与实现证据只写进该设计文档的 Validation / Implementation 节；无设计文档的工作（L0/L1），证据写成 Recent Updates 的一条单行。
- PM 其余各节（Active Tasks Notes、Archive Evidence、Design Index Notes、Current Status）只写一行结论 + 指针（设计路径 / commit / REQ ID），不复述命令清单与实现叙事。
- 同一事实在 PM 主文件中最多出现在一个节；生命周期推进（Active → Archive）是移动而非复制。

### 2. project-management-template.md 减记账面

- 删除 Testing and Validation 节：当前可跑的验证命令归 `knowledge-summary.md`（Verified Commands），逐次变更的验证证据归各设计文档。
- Roadmap、Milestones 标注为可选节（小项目并入 Requirements Backlog / Archive），模板默认保留但加一行说明。
- Archive 的 Evidence 列表头下加说明：一行指针，不放段落。

### 3. 基线模板去掉 Review Notes 节

- 从 `main-design-template.md` 与 `module-design-template.md` 删除 Review Notes 节——与 front matter `review_status` 完全同义。
- **保留** `architecture-change-template.md` 与 `module-change-template.md` 的 Review Notes：变更设计中它承载真实评审结论（发现、修补、边界判定），不是仪式。

### 4. 连锁同步

- `storage-schema.md` 的 PM Sections 规范清单：移除第 8 节 Testing and Validation，并对 Roadmap/Milestones 标注可选（与模板保持一致，否则 schema 与模板矛盾）。
- grep 全套 SKILL.md 与 references 中提及被删节（Testing and Validation、基线 Review Notes）的其余散文，同步改写（评审时 grep 确认：en 侧除 storage-schema 与模板外无其他命中）。
- `zh/modular-programming` 镜像逐文件同步翻译（机器 token 不变）。

## Contract Impact

- checker 无契约变化（不校验上述节），无需改代码与测试。
- 模板形状变化仅影响新建项目；已有项目的旧 PM/基线不强制迁移，本仓库在随后的一次性压缩中对齐。
- 本仓库基线文档（modules/*.md、main-design.md）的 Review Notes 节删除属压缩步骤的一部分，不在本设计内执行。

## Implementation Outline

1. pm-maintenance-rules.md 增 "Evidence Single Home" 节（置于 Lightweight PM Pattern 之前）。
2. 改 project-management-template.md（删节 + 可选标注 + Evidence 说明）。
3. 删 main-design-template.md / module-design-template.md 的 Review Notes 节。
4. 改 storage-schema.md PM Sections 清单（删 Testing and Validation、标注 Roadmap/Milestones 可选）。
5. grep 并同步 SKILL.md / references 中的其余相关散文。
6. zh 镜像同步（散文翻译，token 不动）。

## Validation

- `python3 en/modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**' --exclude 'zh/**'` 0 error。
- `python3 -m unittest discover -s en/modular-programming/modular-audit/tests` 全绿。
- `grep -rn "Review Notes" en/modular-programming/_shared/assets/` 仅剩两个变更模板命中；zh 同。
- en/zh 目录逐文件对等；`./install.sh en --dry-run` 与 `zh --dry-run` 正常。

## Risks

- 规则减面后，若某次工作既无设计文档又需要多行证据——用 Recent Updates 单行 + commit 指针即可覆盖；确有长证据时说明它本就该有设计文档（判级信号）。
- zh/en 双份散文同改存在漂移风险——实现步骤将两语言放在同一提交内完成。

## Open Questions

（无）

## Decisions（2026-07-08 用户确认）

- Roadmap/Milestones 保留在模板中并标注为可选节（不删除）。
- 接受设计并开始实现（status: accepted）；创作顺序为先 zh 后 en（用户观察 zh 散文效果更好），两语言同一提交落地。

## Review Notes

- Review status: reviewed（modular-review，2026-07-08）。
- 发现并修复：连锁同步遗漏 `storage-schema.md` PM Sections 清单（第 8 节即 Testing and Validation），已显式补入 Target 与 Implementation Outline。
- 核对通过：L2 判定成立（跨 shared-references/shared-assets 两模块散文，无外部契约变化——checker 不校验涉及的散文节，`check_modular_project.py:96,192,456,466` 已核实）；主模块单一；基线/目标分离清晰；grep 确认 en 侧 "Review Notes" 仅 4 个模板命中、"Testing and Validation" 仅 storage-schema + PM 模板命中，连锁范围与设计一致；Open Questions 已清空（Roadmap/Milestones 可选已由用户拍板）。
- 待人工接受的方向点（非阻塞）：Evidence Single Home 作为写入时强规则（"同一事实最多出现在 PM 一个节"）、PM 模板删除 Testing and Validation 节。

## Implementation（2026-07-08）

- 按用户决定先 zh 后 en，两语言各改 5 个文件（共 10 个）：
  - `_shared/references/pm-maintenance-rules.md`：新增「证据单一居所 / Evidence Single Home」节（置于轻量 PM 模式之前），含判级信号条款。
  - `_shared/assets/project-management-template.md`：删 Testing and Validation 节；Roadmap/Milestones 加可选标注；Archive Evidence 列加一行指针说明。
  - `_shared/assets/main-design-template.md`、`module-design-template.md`：删 Review Notes / 评审记录节。
  - `_shared/references/storage-schema.md`：PM 小节清单删 Testing and Validation、Roadmap/Milestones 标注可选，并补"验证命令归 knowledge-summary、逐次证据归设计文档"说明。
- 验证全绿：checker 自审计 0 error/0 warning（6 模块）；unittest OK；grep 确认 en/zh 的 Review Notes（评审记录）仅剩两个变更模板命中、Testing and Validation 无残留（除有意的说明行）；`./install.sh en|zh --dry-run` 均通过；`git diff --check` 干净。
- 未提交：工作树混有上一会话 narrator 迁移的未提交改动，用户未要求提交，由用户自行分笔提交；install 实际同步照旧待运行。
