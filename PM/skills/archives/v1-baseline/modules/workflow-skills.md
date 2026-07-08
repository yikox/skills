---
name: Workflow Skills
described: 十个 modular-* 技能入口文档，定义架构优先工作流的全部执行规则
module_form: atomic
module_kind: config-rule
main_subject: SKILL.md 技能入口文档
code_paths: ["en/modular-programming/*/SKILL.md", "en/modular-programming/*/agents/*"]
status: implemented
review_status: reviewed
---

# Workflow Skills

## Responsibility

拥有十个技能入口（init / change / status / architecture / review / knowledge / audit / autopilot / advisor / narrator）的 SKILL.md 文档。它们是 agent 消费的工作流规则入口，定义各技能的触发条件、工作流步骤与交接关系。

## Public Contract

- 每个技能目录 `en/modular-programming/<skill>/SKILL.md`，front matter 含 `name` 与 `description`（含中英触发词）。
- 技能间交接协议：modular-change 是日常入口，按 L0-L3 路由。L2/L3 默认先在分支上提交 architecture patch，再进入实现；modular-autopilot 接手已接受的分支目标地图与实现计划；modular-advisor 是高级顾问角色，只产出评估/重构/设计方案，不落盘不实现；modular-narrator 是只读讲述者角色，独立可用（不依赖工作流资产），只讲解不评估不落盘，与 advisor 以"理解 vs 提案"划界（双向 SKILL description 均声明该边界）。
- 每个技能的 `agents/openai.yaml` 为 OpenAI 兼容入口的附属配置。

## Internal Design

- 所有技能通过 `../_shared/references/*.md` 相对路径读取共享规则，通过 `../_shared/assets/*.md` 读取模板。
- modular-autopilot 硬依赖 superpowers 插件（writing-plans、subagent-driven-development、using-git-worktrees），缺席时报错并指引安装。
- L2/L3 的默认 spec 是功能分支内已接受的目标模块地图，而不是长期维护的独立过程 proposal。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| shared-references | out | 技能执行时读取共享工作流规则 |
| shared-assets | out | 技能创建文件时读取模板 |
| audit-checker | out | modular-audit 技能触发确定性检查脚本 |
| graph-tooling | out | modular-architecture 的高级可视化模式触发图渲染 |

## Constraints

- 技能正文用英文，description 中保留中文触发词（安装目标含多语言 agent 环境）。
- 修改任一技能的交接协议时必须同步检查被交接技能的对应表述。
- 不得把仅在实现期间有用的 proposal / plan / decision log 变成 main 分支的日常事实源；完成后默认归档。

## Validation

- `./install.sh <en|zh> --dry-run` 应列出全部十个技能目录。
- `grep -c "^name:" en/modular-programming/*/SKILL.md` 每个文件恰好 1。
