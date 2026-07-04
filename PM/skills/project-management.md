# skills 仓库 Modular Programming

Last updated: 2026-07-04

## Overview

- modular-programming 技能套件的源仓库项目记忆：跟踪技能演进、架构变更与验证证据。
- 工作流偏好：docs-language `zh`；confirmation `standard`。

## Current Status

| Field | Value |
| --- | --- |
| Version | main @ 2026-07-04 |
| State | 9 技能（含高级角色 modular-architect）+ 共享层稳定；安装副本待同步 |
| Current focus | 运行 `./install.sh` 同步已安装 skills；modular-autopilot 演练仍待执行 |
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
| Architecture Change | architecture/changes/2026-07-04-lightweight-default-workflow.md | implemented | reviewed | 计划已归档至 plans/archive/；图作为高级功能 |
| Architecture Change | architecture/changes/2026-07-04-modular-architect-skill.md | implemented | reviewed | 模块化架构师高级角色；merge 22c98e8；计划已归档 |
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
- 2026-07-03 审计跟进修复验证：`python3 -m unittest discover -s modular-programming/modular-audit/tests`、`python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'`、三个 Python 脚本 py_compile、架构图渲染、`./install.sh --dry-run`、`git diff --check` 全部通过。
- 2026-07-04 轻量默认工作流验证：`python3 -m unittest discover -s modular-programming/modular-audit/tests`、`python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'`、三个 Python 脚本 py_compile、高级架构图渲染、`./install.sh --dry-run`、`git diff --check` 全部通过。

## Blockers and Risks

| Risk / Blocker | Impact | Mitigation / Status |
| --- | --- | --- |
| superpowers 插件升级可能改变 writing-plans/SDD 行为 | autopilot 衔接点失效 | 插件升级后重跑演练（设计 Risks 节） |
| 已安装 skill 副本尚未同步本次源码修复 | Codex/Claude/agents 目录仍加载旧版，直到安装脚本运行 | `./install.sh --dry-run` 已确认待同步内容；实际 `./install.sh` 因权限/额度审批限制未执行 |

## ADR Summary

| Date | ADR | Decision | Status | Notes |
| --- | --- | --- | --- | --- |
| 2026-07-03 | [ADR-2026-07-03-autopilot-as-main-session-skill](architecture/adrs/ADR-2026-07-03-autopilot-as-main-session-skill.md) | 监督者为主会话技能而非 agent；授权前置为入口一次确认 | accepted | Follow-Up：演练待跑 |

## Archive

### Completed Work

| Date | Task / Requirement | Final Status | Evidence |
| --- | --- | --- | --- |
| 2026-07-04 | 新增高级角色 modular-architect（模块化架构师）+ 方法论/评估共享参考（L3） | implemented in source; install pending | autopilot 托管执行；SDD 四任务全绿 + 终审 Ready to merge；merge 22c98e8；baseline（main-design/workflow-skills/shared-references）已更新；checker 0 error、unittest OK、install dry-run 见新技能；决策日志见 plans/archive/2026-07-04-modular-architect-decisions.md |
| 2026-07-04 | 轻量默认模块化工作流改造（L3） | implemented in source; install pending | 共享规则、技能入口、模板、README、checker 与 PM baseline 已更新；最终验证见 Testing and Validation |
| 2026-07-03 | 审计跟进修复：autopilot 收尾语义、8 技能曝光、复合图校验 | implemented in source; install pending | 新增 checker unittest；modular-audit 0 error/0 warning；py_compile、架构图渲染、install dry-run、diff-check 通过；实际安装因审批额度限制未执行 |
| 2026-07-03 | modular-autopilot 监督者技能（L3） | implemented | commits 7e55bf5..fa0b54b + e128077 收尾 + 77b70c2 加固；SDD 每任务双评审 + 最终全分支评审 Ready to merge；checker fixture 全绿 |

### Design Archive

| Type | Path | Final Status | Notes |
| --- | --- | --- | --- |
| Plan | architecture/plans/archive/2026-07-04-modular-architect-skill-plan.md | implemented | L3 模块化架构师技能实现计划 |
| Decisions | architecture/plans/archive/2026-07-04-modular-architect-decisions.md | implemented | autopilot 决策日志 + SDD 执行记录 |
| Plan | architecture/plans/archive/2026-07-04-lightweight-default-workflow-plan.md | implemented | L3 轻量默认工作流改造计划 |
| Plan | architecture/plans/archive/2026-07-03-modular-autopilot-plan.md | implemented | 随设计 implemented 归档 |

## Recent Updates

- 2026-07-03 - 初始化本仓库 modular 项目记忆（模块地图 6 模块、图、PM、知识文档）。
- 2026-07-03 - modular-autopilot 技能合入 main；check_plans 加固（路径越界、目录级别匹配）。
- 2026-07-03 - 修复审计发现：autopilot 未落地不标 implemented、README/AI snippet/openai.yaml 补齐 8 技能曝光、audit-checker 增加 group/interface/scope 校验与 unittest；安装同步待审批可用后运行。
- 2026-07-04 - 落地轻量默认模块化工作流：L1 PM 减重、诊断模式、硬化 L1/L2/L3、图降为高级可视化、默认事实源改为 main-design + modules。
- 2026-07-04 - 评审后修复：checker 例外 glob（shared/ignored_paths）加幽灵检查、v0.3 结构校验对 v0.1/v0.2 老图降级为 warning；audit SKILL/Routing Quick Reference/module-authoring-rules 补齐"图可选、L1 减重"漏改；验证 `python3 -m unittest discover -s modular-programming/modular-audit/tests`（7 tests OK）与自审计 0 error/0 warning。
- 2026-07-04 - 新增第 9 个技能 modular-architect（模块化架构师，高级顾问角色，只提案不实现）+ modular-methodology/modular-assessment 两个共享参考；autopilot 托管执行 SDD 四任务全绿，merge 22c98e8，baseline 与 PM 已同步。
