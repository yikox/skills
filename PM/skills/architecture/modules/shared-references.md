---
name: Shared References
described: 跨技能共享的规则语料：工作流规则、存储 schema、评审/迁移/维护规则、图格式、模块化方法论与评估
module_form: atomic
module_kind: config-rule
main_subject: _shared/references 规则文档
code_paths: ["en/modular-programming/_shared/references/**"]
status: implemented
review_status: reviewed
---

# Shared References

## Responsibility

拥有全部技能共同遵循的规则文档：modular-workflow-rules（轻量默认、分级/路由/确认档位）、storage-schema（项目记忆布局与状态词表）、review-rules、migration-rules、module-authoring-rules、module-kind-classification、pm-maintenance-rules、architecture-graph-json-format、受控词表单一事实源 vocab.md，以及 modular-advisor 的方法论语料 modular-methodology 与评估语料 modular-assessment。

## Public Contract

- 技能以 `../_shared/references/<file>.md` 相对路径引用；文件名即契约，改名属于 L3 变更。
- storage-schema 定义的目录布局与 front matter 字段（模块字段、计划 `source_design`/`level`）被 audit-checker 以代码形式强制。
- `vocab.md` 是受控词表（module_form / module_kind / relation_kind / relation_style / design_status / review_status）的单一事实源，被 audit-checker 启动时解析；其它规则文档只解释语义，枚举值以 vocab.md 为准。
- architecture-graph-json-format 定义 `arch-graph/v0.3`，是高级 graph-tooling 的输入契约。

## Internal Design

- 规则按主题分文件，单一事实来源：布局归 storage-schema，语义归 workflow-rules，图结构归 graph-json-format。
- `module-kind-classification.md` 为总览 + 选择规则 + 索引；9 类 `module_kind` 的详解（什么模块属于这类/图形设计/展开方式/文档模板）分片到 `module-kinds/<kind>.md`，主文件名保留为稳定引用入口。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | in | 技能执行时读取本模块规则 |
| audit-checker | in | 启动时解析 `vocab.md` 受控词表清单 |

## Constraints

- 受控词表以 `vocab.md` 为单一事实源，audit-checker 启动时解析；改词表只改 vocab.md，无需再手工同步 checker 代码。audit-checker 的 drift-guard 测试保证 vocab.md 与内置 fallback 一致。

## Validation

- `python3 en/modular-programming/modular-audit/scripts/check_modular_project.py PM/skills` 无 error（schema 与检查器一致的间接证据）。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
