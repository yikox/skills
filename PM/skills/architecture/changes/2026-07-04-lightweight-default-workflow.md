---
title: 轻量默认模块化工作流
level: L3
status: implemented
review_status: reviewed
primary_module: shared-references
impacted_modules: [workflow-skills, shared-assets, audit-checker, graph-tooling]
---

# 轻量默认模块化工作流

## Request

用户接受上一轮审计建议，要求把 modular-programming 从“强治理默认路径”改成“日常轻量、复杂升级”的工作流；同时明确反对“满足任一条件才画图”的默认图策略，要求 `main-design.md + architecture/modules/*.md` 作为 AI 工作的默认核心，架构图降级为高级能力的一部分。

## Current Baseline

- L1 当前默认要求 PM start 与 PM complete，容易把轻量修改变成 PM 流水账。
- L1/L2/L3 分级依赖描述性判断，agent 容易过度保守，把普通修改升级为 L2/L3。
- 模块不清楚时默认停止并补架构；对 bug/老项目诊断阶段不够顺滑。
- 新项目 baseline 默认创建 graph JSON 与 rendered HTML/SVG，图被放在常规路径而不是高级可视化能力。
- ADR、module docs、PM 模板偏完整，容易鼓励“为治理而治理”。
- 用户需要理解 8 个 skill 的边界；日常入口可以更少。

## Target Architecture

### 1. 轻量默认

默认路径变为：

```text
L0: 直接改 + 验证，不写 PM
L1: 极简留痕；只有跨会话、风险、发布证据、用户要求时才进 Active Tasks
L2: 模块设计 + review + 确认 + 实现
L3: 架构变更/必要 ADR + review + 接受 + 实现
```

PM 主文件只服务“未来会话快速接续”，不记录每一次执行细节。

### 2. 硬化分级

把 L1/L2/L3 改成更可执行的判定表：

- L1：单模块、通常 1-3 个文件、不改 public contract、不需要先解释设计即可实现、可本轮验证。
- L2：单模块但需要多步内部结构/流程/状态/算法调整，或不先写目标结构就容易走偏。
- L3：模块边界、跨模块契约、状态归属、持久化、运行时模型、外部边界、长期技术方向变化。

### 3. 诊断模式

当 bug 根因或 primary module 不清楚时，允许先进入只读/低风险诊断模式：

```text
复现/读代码/运行测试/收集证据
-> 定位疑似模块
-> 再决定 L1/L2/L3
```

诊断模式不能做结构性修改，不能标完成。

### 4. 图作为高级能力

默认 baseline 只要求：

```text
architecture/main-design.md
architecture/modules/*.md
```

图相关文件、渲染器、HTML/SVG 作为高级能力保留，适用于用户请求可视化、复杂沟通、后续高级 skill 或演示；不再是 init/migration 的默认产物。

### 5. ADR 与模块文档瘦身

ADR 仅在存在真实备选方案、且决策会长期约束未来实现时创建。

模块文档默认聚焦五件事：

1. 负责什么；
2. 不负责什么；
3. 外部如何使用；
4. 依赖谁 / 谁依赖它；
5. 改它时最不能破坏什么。

### 6. 用户入口简化

对用户主推四个入口：

```text
modular-init
modular-change
modular-audit
modular-knowledge
```

`modular-status`、`modular-review`、`modular-architecture`、`modular-autopilot` 仍保留为内部/高级入口。

## Module Impact

| Module | Impact |
| --- | --- |
| shared-references | 修改 workflow、storage、maintenance、authoring 规则的默认语义 |
| workflow-skills | 修改 init/change/status/architecture/review/autopilot 的触发与执行说明 |
| shared-assets | PM/main/module/AI rules 模板改为轻量默认，图提示改为可选 |
| audit-checker | 保持兼容；必要时放松对 graph 的默认期望，只在图存在时校验 |
| graph-tooling | 能力保留，但从默认 baseline 路径降级为高级可视化能力 |

## Acceptance Summary

- 用户已明确接受 PM 减重、分级硬化、诊断模式、ADR 门槛、用户入口简化、autopilot 高级模式化、模块文档瘦身。
- 用户明确修正图策略：默认不画图，`main-design.md + modules/*.md` 足够；画图作为高级能力。
- 本变更不删除 graph tooling，只改变默认流程和文档定位。

## Validation

- `python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'`
- `python3 -m unittest discover -s modular-programming/modular-audit/tests`
- `./install.sh --dry-run`
- `git diff --check`

## Review Notes

- Review status: reviewed（用户已接受方向；本设计仅把决策写成可执行目标）
