---
title: 新增高级角色技能 modular-architect（模块化架构师）
level: L3
status: implemented
review_status: reviewed
primary_module: workflow-skills
impacted_modules: [shared-references, shared-assets]
---

# 新增高级角色技能 modular-architect（模块化架构师）

## Request

用户要求在"四个常规入口 + 高级角色"的结构上增加第二个高级角色：模块化架构师。该角色内置模块化设计思维，能输出老项目模块化重构方案、讨论并生成新项目模块化设计方案。用户提供了完整的模块化编程方法论文本（思维原则、新项目设计、老项目重构、模块化程度评估与分级、检查表），并授权检索补充。

## Current Baseline

- 套件当前 8 个技能：4 个常规入口（init/change/audit/knowledge）+ 内部/高级（architecture/status/review/autopilot）。
- `modular-architecture` 是落盘执行者：写 baseline、迁移、ADR、可选图；要求 PM 结构存在，不承担开放式设计讨论。
- 唯一的"高级角色"是 `modular-autopilot`（设计已接受 → 托管执行）。
- 套件没有"模块化程度评估"能力，也没有面向未接入工作流项目的咨询入口。
- 共享参考层没有模块化方法论语料；分级/路由规则里的模块化判断依赖各技能自带描述。

## Target Architecture

### 1. 角色定位

`modular-architect` 是与 `modular-autopilot` 对称的高级角色：

```text
modular-architect: 想法/存量代码 -> 讨论出可接受的模块化方案（想清楚）
modular-autopilot: 已接受设计   -> 托管执行到落地（做完）
```

角色硬边界：

- 对话式思维伙伴：关键问题一次一个（系统能力、数据归属、变化来源），逐步收敛，方案定稿前有明确用户确认点。
- 只输出方案，不动代码：不实现、不重构、不改 baseline、不标 implemented。
- 不要求项目已接入模块化工作流；读代码遵循诊断模式纪律（只读不改）。
- 高级入口，不进四个常规入口。

### 2. 三类产出

1. **模块化程度评估报告**：按评估维度（职责清晰度、接口清晰度、依赖复杂度、修改影响范围、独立测试能力、替换能力、数据所有权、架构约束强度）逐项给证据与结论；证据必须指向具体代码位置并标注 verified/inferred；结论含低/中/高分级与最痛 3-5 个问题排序。禁止只看目录结构下结论。
2. **老项目重构方案**：以评估为证据基础；分阶段 roadmap，每阶段一个模块闭环（确认职责 → 建立接口/封装 → 迁移实现 → 改调用方 → 测试 → 删旧码）；含行为基线要求、数据所有权迁移顺序、风险与回滚、每阶段验证信号。
3. **新项目设计方案**：系统能力清单 → 模块草案（职责/非职责/拥有数据/公共契约/依赖方向）→ 依赖规则与组装入口约定 → 反过度设计检查。字段有意对齐 `main-design.md` + 模块文档，接受后可被 `modular-init`/`modular-architecture` 直接转为 baseline。

### 3. 两种模式与交接

**独立咨询模式**（未接入工作流）：对话呈现 → 用户确认后写入用户指定位置（默认 `docs/modularization/<date>-<topic>.md`）→ 推荐下一步 `modular-init`；不接入也不阻塞，方案自身完整。

**工作流内模式**（已有 PM/architecture）：

- 评估报告：两种模式统一写 `docs/modularization/<date>-assessment.md`（评估是证据快照，不是 baseline 事实，不进 architecture/）；工作流内额外在 PM 加一条记录指向该路径。
- 老项目重构方案：写成 `architecture/changes/<date>-<change>.md`（status: proposed），走既有 L3 路径（review → 要点摘要 → 人工接受 → `modular-change`/`modular-autopilot` 执行）。
- 新项目设计方案：作为 `modular-architecture` 建 baseline 的输入。

### 4. 共享参考文件

- `_shared/references/modular-methodology.md`：方法论第一/二/三/七部分整理为规则化语料（先划分职责再划分代码、模块=完整能力、高内聚低耦合、契约协作、数据所有权唯一、组合优于渗透、先封装再替换、一次一个模块、渐进替换、删除旧码、防退化约束等），补充并标注出处：Parnas 信息隐藏、耦合/内聚谱系、依赖倒置、strangler-fig 渐进替换、限界上下文与数据所有权。
- `_shared/references/modular-assessment.md`：评估维度、低/中/高分级特征、18 项检查表，加"证据要求"一节（每个结论必须指向具体代码位置）。
- 本次只建立语料与 architect 的引用；`modular-review`/`modular-change` 的引用点留待后续变更。

### 5. 套件集成

- 新目录 `modular-programming/modular-architect/`（SKILL.md + agents/openai.yaml）。
- README：高级角色区、技能表、目录树各加一行。
- `ai-rules-snippet.md`：Internal or advanced entries 加一行。
- `modular-workflow-rules.md` Routing Quick Reference 加一行（评估/重构方案/设计方案讨论 → modular-architect）。
- installer 无需改动（平铺复制自动覆盖新目录）。

## Module Impact

| Module | Impact |
| --- | --- |
| workflow-skills | 新增 modular-architect 技能目录；README/snippet/routing 曝光同步 |
| shared-references | 新增 modular-methodology.md 与 modular-assessment.md 两个语料文件 |
| shared-assets | 无新模板；ai-rules-snippet 加一行入口 |

## Acceptance Summary

- 用户已确认：角色可独立工作（不要求已接入工作流）；三类产出（评估/重构方案/设计方案）；分情况落盘（工作流内进 PM 结构，独立模式默认 `docs/modularization/`）；方案 A（新增独立技能 + 两个共享参考文件）。
- 设计五节（定位/产出/模式交接/参考文件/集成验证）已逐节确认。

## Risks

- 与 `modular-architecture` 的触发词可能混淆：architect 描述强调"评估/方案/讨论"，architecture 强调"落盘/baseline/迁移执行"；review 时核对两个 description 无重叠触发。
- 方法论语料较长，SKILL.md 必须只做流程与引用，不复述语料（与既有 Required References 模式一致）。
- 技能数 8→9，README 需保持"日常只记四个入口"的信息不被稀释。

## Validation

- `python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'` 0 error。
- `python3 -m unittest discover -s modular-programming/modular-audit/tests` 通过。
- `./install.sh --dry-run` 覆盖 modular-architect 目录。
- SKILL.md front matter 含中英触发词；8+1 技能在 README/snippet/routing 三处曝光一致。
- 可选演练：对一个真实小项目跑一次评估报告。

## Review Notes

- Review status: reviewed（设计要点与用户逐节确认；要点摘要确认接受于 2026-07-04；机械检查通过：模块地图/验证命令/纯增量回滚）
- 决策：不写 ADR——方案 A/B/C 的选择与理由已记录在 Acceptance Summary，角色边界写入两个 SKILL description；见决策日志。
