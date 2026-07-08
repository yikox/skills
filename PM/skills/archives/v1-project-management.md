# skills 仓库 Modular Programming

Last updated: 2026-07-09

## Overview

- modular-programming 技能套件的源仓库项目记忆：跟踪技能演进、架构变更与验证证据。
- 工作流偏好：docs-language `zh`；confirmation `standard`。
- 历史细节见 [archives/project-management-history-2026.md](archives/project-management-history-2026.md)；证据遵循 pm-maintenance-rules「证据单一居所」。

## Current Status

| Field | Value |
| --- | --- |
| Version | main @ 2026-07-09 |
| State | v1 套件（en+zh 10 技能）已冻结入 legacy/（tag `modular-v1-frozen`）；installer 仅装 zh 独立 skill；v2 living-docs 待实现 |
| Current focus | living-docs v2（REQ-20260709）：迁移路径第 1 步冻结已完成；下一步先写验收清单与 docs-acceptance |
| Architecture baseline | architecture/main-design.md |

## Active Tasks

| Date | Task | Primary Module | Impacted Modules | Level | Status | Next Step / Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-09 | living-docs v2 落地（REQ-20260709） | workflow-skills | installer, shared-references, shared-assets | L3 | in-progress | 第 1 步冻结完成（tag + legacy/ + installer + README 公告）；下一步：验收清单 + docs-acceptance → 模板与规则 → docs-init/docs-sync。已知漂移：PM 基线模块文档的 code_paths 仍指向移动前路径，第 5 步迁移时统一处理 |

## Requirements / Change Backlog

| ID | Date | Request | Primary Module | Impacted Modules | Level | Change Summary | Scope / Impact | Status | Priority | Design Path / Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-20260709-living-docs-v2 | 2026-07-09 | 回归初心重设计：产品定义为两份文档（项目文档 + 设计文档），机制减为三 skill（init/sync/acceptance），顺带更新 + git 对账，v1 套件冻结入 legacy，中文单源 | workflow-skills | shared-references, shared-assets, installer, audit-checker, graph-tooling | L3 | 见设计 | 替代整个 v1 套件 | proposed | P0 | [architecture/changes/2026-07-09-living-docs-v2-redesign.md](architecture/changes/2026-07-09-living-docs-v2-redesign.md)；设计已评审通过，执行中（见 Active Tasks） |
| REQ-20260703-autopilot-rehearsal | 2026-07-03 | modular-autopilot 端到端与负路径演练 | workflow-skills | audit-checker | L1 | 按设计 Validation 节执行两类演练并记录证据 | 验证 autopilot 可用性 | dropped (v1 frozen) | — | v1 冻结（REQ-20260709），演练失去意义 |
| REQ-20260706-en-pure-english | 2026-07-06 | en/ 纯英文化（现为历史遗留的中英混合） | shared-references | workflow-skills, shared-assets | L2 | en/ 散文全量英文化，token 不变 | 英文用户体验 | dropped (v1 frozen) | — | v2 中文单源（REQ-20260709），en 随 v1 冻结 |

## Modular Design Index

| Type | Path | Status | Review | Notes |
| --- | --- | --- | --- | --- |
| Main Architecture | architecture/main-design.md | implemented | reviewed | 2026-07-03 基线 |
| Module | architecture/modules/workflow-skills.md | implemented | reviewed |  |
| Module | architecture/modules/shared-references.md | implemented | reviewed |  |
| Module | architecture/modules/shared-assets.md | implemented | reviewed |  |
| Module | architecture/modules/audit-checker.md | implemented | reviewed |  |
| Module | architecture/modules/graph-tooling.md | implemented | reviewed |  |
| Module | architecture/modules/installer.md | implemented | reviewed |  |

已实现的可选 proposal / 历史过程文件索引见 Archive 的 Design Archive。

## Blockers and Risks

| Risk / Blocker | Impact | Mitigation / Status |
| --- | --- | --- |
| superpowers 插件升级可能改变 writing-plans/SDD 行为 | autopilot 衔接点失效 | 插件升级后重跑演练（设计 Risks 节） |

## ADR Summary

| Date | ADR | Decision | Status | Notes |
| --- | --- | --- | --- | --- |
| 2026-07-03 | [ADR-2026-07-03-autopilot-as-main-session-skill](architecture/adrs/ADR-2026-07-03-autopilot-as-main-session-skill.md) | 监督者为主会话技能而非 agent；授权前置为入口一次确认 | accepted | Follow-Up：演练待跑 |

## Archive

### Completed Work

证据列为一行指针；默认 L2/L3 指向 architecture patch commit + implementation commit/PR，可选 proposal 的长证据留在 proposal 或归档执行产物；规则生效前的存量长证据在 archives/project-management-history-2026.md。

| Date | Task / Requirement | Final Status | Evidence |
| --- | --- | --- | --- |
| 2026-07-08 | 默认 L2/L3 改为 branch-carried architecture patch，减少长期过程文档（L3） | implemented | architecture patch bd19dfa；implementation ca17459；验证 `unittest en/zh`、`check_modular_project`、`install.sh en/zh --dry-run`、`git diff --check` |
| 2026-07-08 | 证据单一居所 + 记账面减重（L2） | implemented | 设计 architecture/modules/shared-references/changes/2026-07-08-evidence-single-home.md；commit 1bfa33a |
| 2026-07-05 | 中英双语版本：语言分层 + install 语言参数（L2） | implemented | 设计 architecture/modules/installer/changes/2026-07-05-bilingual-zh-en.md；commits 7cf18d3/03d55f3 |
| 2026-07-05 | 新增技能 modular-narrator（L2）+ architect 改名 advisor（L1） | implemented | 设计 architecture/modules/workflow-skills/changes/2026-07-05-modular-narrator.md；commits a537db2..e6d3ac8、265aa52 |
| 2026-07-04 | 词表单一事实源 vocab.md（L3） | implemented | 设计 architecture/changes/2026-07-04-vocab-single-source.md；细节见 history |
| 2026-07-04 | 拆分 module-kind-classification（L2） | implemented | 设计 architecture/modules/shared-references/changes/2026-07-04-split-module-kind-classification.md |
| 2026-07-04 | 新增角色 modular-architect + 方法论/评估参考（L3） | implemented | 设计 architecture/changes/2026-07-04-modular-architect-skill.md；merge 22c98e8 |
| 2026-07-04 | 轻量默认模块化工作流改造（L3） | implemented | 设计 architecture/changes/2026-07-04-lightweight-default-workflow.md |
| 2026-07-03 | 审计跟进修复（autopilot 收尾语义、8 技能曝光、图校验） | implemented | 细节见 history |
| 2026-07-03 | modular-autopilot 监督者技能（L3） | implemented | 设计 architecture/changes/2026-07-03-modular-autopilot.md；commits 7e55bf5..77b70c2 |
| 2026-07-03 | modular-autopilot 上线（里程碑） | done | 2026-07-03 合入 main |

### Design Archive

| Type | Path | Final Status | Notes |
| --- | --- | --- | --- |
| Architecture Change | architecture/changes/2026-07-03-modular-autopilot.md | implemented | reviewed |
| Architecture Change | architecture/changes/2026-07-04-lightweight-default-workflow.md | implemented | reviewed |
| Architecture Change | architecture/changes/2026-07-04-modular-architect-skill.md | implemented | reviewed |
| Architecture Change | architecture/changes/2026-07-04-vocab-single-source.md | implemented | reviewed |
| Module Change | architecture/modules/shared-references/changes/2026-07-04-split-module-kind-classification.md | implemented | reviewed |
| Module Change | architecture/modules/installer/changes/2026-07-05-bilingual-zh-en.md | implemented | reviewed |
| Module Change | architecture/modules/workflow-skills/changes/2026-07-05-modular-narrator.md | implemented | reviewed |
| Module Change | architecture/modules/shared-references/changes/2026-07-08-evidence-single-home.md | implemented | reviewed |
| Plan | architecture/modules/workflow-skills/plans/archive/2026-07-05-modular-narrator-plan.md | implemented | narrator 实现计划 |
| Plan | architecture/plans/archive/2026-07-04-modular-architect-skill-plan.md | implemented | L3 架构师技能实现计划 |
| Decisions | architecture/plans/archive/2026-07-04-modular-architect-decisions.md | implemented | autopilot 决策日志 + SDD 记录 |
| Plan | architecture/plans/archive/2026-07-04-lightweight-default-workflow-plan.md | implemented | L3 轻量工作流改造计划 |
| Plan | architecture/plans/archive/2026-07-03-modular-autopilot-plan.md | implemented | 随设计 implemented 归档 |

## Recent Updates

- 2026-07-09 - v1 套件冻结：tag `modular-v1-frozen`；en/zh modular-programming 移入 legacy/；install.sh 仅支持 zh、清理已装 modular-* 与 _shared；README 双语冻结公告。REQ-20260703/REQ-20260706 随冻结 dropped。
- 2026-07-08 - `./install.sh zh` 实际同步完成（3 目标目录 × 10 技能，含新规则/模板），install pending 状态全部清除。
- 2026-07-08 - PM 一次性压缩（125→103 行）：重排为单一居所结构，长证据原文移入 archives/project-management-history-2026.md；7 份基线文档去 Review Notes 节；knowledge-summary 命令路径修正为 en/ 前缀。
- 2026-07-08 - 文档减重 L2「证据单一居所 + 记账面减重」实现（设计见 Design Archive；commit 1bfa33a）。
- 2026-07-06 - zh 散文翻译落地（commit 03d55f3）；发现 en/ 为中英混合，纯英文化入 backlog（REQ-20260706）。
- 2026-07-05 - 中英双语结构层（commit 7cf18d3）；新增技能 modular-narrator；architect 改名 advisor。
- 2026-07-04 - 轻量默认工作流、vocab 单一事实源、module-kind 拆分、新增 modular-architect 角色（详见 Design Archive 各设计）。
- 2026-07-03 - 初始化项目记忆；modular-autopilot 合入 main；审计跟进修复。
