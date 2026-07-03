# skills 仓库 Modular Programming

Last updated: 2026-07-03

## Overview

- modular-programming 技能套件的源仓库项目记忆：跟踪技能演进、架构变更与验证证据。
- 工作流偏好：docs-language `zh`；confirmation `standard`。

## Current Status

| Field | Value |
| --- | --- |
| Version | main @ 2026-07-03 |
| State | 基线已建立，8 技能 + 共享层 + 工具层稳定 |
| Current focus | modular-autopilot 落地后的演练验证 |
| Architecture baseline | architecture/main-design.md |

## Active Tasks

| Date | Task | Primary Module | Impacted Modules | Level | Status | Next Step / Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Requirements / Change Backlog

| ID | Date | Request | Primary Module | Impacted Modules | Level | Change Summary | Scope / Impact | Status | Priority | Design Path / Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-20260703-autopilot-rehearsal | 2026-07-03 | modular-autopilot 端到端与负路径演练 | workflow-skills | audit-checker | L1 | 按设计 Validation 节执行两类演练并记录证据 | 验证 autopilot 可用性 | accepted | P1 | 见 ADR-2026-07-03 Follow-Up |

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
| Architecture Change | architecture/changes/2026-07-03-modular-autopilot.md | implemented | reviewed | 计划已归档至 plans/archive/ |
| ADR | architecture/adrs/ADR-2026-07-03-autopilot-as-main-session-skill.md | accepted | reviewed |  |

## Roadmap

| Priority | Item | Primary Module | Status | Notes |
| --- | --- | --- | --- | --- |
| P1 | autopilot 演练（端到端 + 负路径） | workflow-skills | accepted | REQ-20260703-autopilot-rehearsal |

## Milestones

| Milestone | Status | Notes |
| --- | --- | --- |
| modular-autopilot 上线 | done | 2026-07-03 合入 main |

## Testing and Validation

- 确定性检查：`python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills` 退出码 0。
- check_plans fixture 验证：坏计划（缺 source_design / level 非法 / 越界路径 / 目录级别不匹配）全部拦截，正例与归档件静默。

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

| Date | Task / Requirement | Final Status | Evidence |
| --- | --- | --- | --- |
| 2026-07-03 | modular-autopilot 监督者技能（L3） | implemented | commits 7e55bf5..fa0b54b + e128077 收尾 + 77b70c2 加固；SDD 每任务双评审 + 最终全分支评审 Ready to merge；checker fixture 全绿 |

### Design Archive

| Type | Path | Final Status | Notes |
| --- | --- | --- | --- |
| Plan | architecture/plans/archive/2026-07-03-modular-autopilot-plan.md | implemented | 随设计 implemented 归档 |

## Recent Updates

- 2026-07-03 - 初始化本仓库 modular 项目记忆（模块地图 6 模块、图、PM、知识文档）。
- 2026-07-03 - modular-autopilot 技能合入 main；check_plans 加固（路径越界、目录级别匹配）。
