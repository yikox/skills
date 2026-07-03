---
name: Shared References
described: 跨技能共享的规则语料：工作流规则、存储 schema、评审/迁移/维护规则、图格式
module_form: atomic
module_kind: config-rule
main_subject: _shared/references 规则文档
code_paths: ["modular-programming/_shared/references/**"]
status: implemented
review_status: reviewed
---

# Shared References

## Responsibility

拥有全部技能共同遵循的规则文档：modular-workflow-rules（分级/路由/确认档位）、storage-schema（项目记忆布局与状态词表）、review-rules、migration-rules、module-authoring-rules、module-kind-classification、pm-maintenance-rules、architecture-graph-json-format。

## Public Contract

- 技能以 `../_shared/references/<file>.md` 相对路径引用；文件名即契约，改名属于 L3 变更。
- storage-schema 定义的目录布局与 front matter 字段（模块字段、计划 `source_design`/`level`、状态词表）被 audit-checker 以代码形式强制。
- architecture-graph-json-format 定义 `arch-graph/v0.3`，是 graph-tooling 的输入契约。

## Internal Design

- 规则按主题分文件，单一事实来源：布局归 storage-schema，语义归 workflow-rules，图结构归 graph-json-format。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | in | 技能执行时读取本模块规则 |

## Constraints

- 规则文本与 audit-checker 的硬编码词表（状态、kind、关系词）必须同步修改，否则 checker 误报。

## Validation

- `python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills` 无 error（schema 与检查器一致的间接证据）。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
