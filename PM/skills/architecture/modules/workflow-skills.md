---
name: Workflow Skills
described: 八个 modular-* 技能入口文档，定义架构优先工作流的全部执行规则
module_form: atomic
module_kind: config-rule
main_subject: SKILL.md 技能入口文档
code_paths: ["modular-programming/*/SKILL.md", "modular-programming/*/agents/*"]
status: implemented
review_status: reviewed
---

# Workflow Skills

## Responsibility

拥有八个技能入口（init / change / status / architecture / review / knowledge / audit / autopilot）的 SKILL.md 文档。它们是 agent 消费的工作流规则入口，定义各技能的触发条件、工作流步骤与交接关系。

## Public Contract

- 每个技能目录 `modular-programming/<skill>/SKILL.md`，front matter 含 `name` 与 `description`（含中英触发词）。
- 技能间交接协议：modular-change 是日常入口，按 L0-L3 路由到其他技能；modular-autopilot 接手已接受设计的自主执行。
- 每个技能的 `agents/openai.yaml` 为 OpenAI 兼容入口的附属配置。

## Internal Design

- 所有技能通过 `../_shared/references/*.md` 相对路径读取共享规则，通过 `../_shared/assets/*.md` 读取模板。
- modular-autopilot 硬依赖 superpowers 插件（writing-plans、subagent-driven-development、using-git-worktrees），缺席时报错并指引安装。

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

## Validation

- `./install.sh --dry-run` 应列出全部八个技能目录。
- `grep -c "^name:" modular-programming/*/SKILL.md` 每个文件恰好 1。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
