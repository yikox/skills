---
name: Audit Checker
described: modular-audit 的确定性检查脚本，机械校验项目记忆的一致性
module_form: atomic
module_kind: function-flow
main_subject: check_modular_project.py
code_paths: ["modular-programming/modular-audit/scripts/**"]
status: implemented
review_status: reviewed
---

# Audit Checker

## Responsibility

拥有 `check_modular_project.py`：对 pm-root 做确定性一致性检查（必备文件、模块 front matter、代码所有权、图与文档关系子集、设计/计划/ADR front matter、PM 表格结构），输出 ERROR/WARNING，退出码 1 表示存在 error。

## Public Contract

- CLI：`python3 check_modular_project.py <pm-root> [--repo-root <path>] [--exclude <glob>]...`
- 检查项词表硬编码：DESIGN_STATUSES、REVIEW_STATUSES、MODULE_KINDS、RELATION_KINDS 等，与 shared-references 的规则文本保持同步。
- `check_plans` 校验 `plans/*.md` 与 `modules/*/plans/*.md`：`source_design` 存在且不越出 pm 根、`level` 合法且与目录匹配（plans/ 存 L3，modules/*/plans/ 存 L2）、源设计已 implemented 时告警归档。

## Internal Design

- 单文件、stdlib-only；`parse_front_matter` 手写解析（不依赖 yaml 库）；error/warn 累积后统一输出。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | in | modular-audit 技能启动时运行本脚本 |

## Constraints

- 仅用 Python 3 标准库（安装目标环境不保证第三方包）。
- glob 语义：`/**` 结尾匹配目录前缀下全部文件，其余按 fnmatch 全路径匹配。

## Validation

- `python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills` 退出码 0。
- 构造缺 `source_design` 的计划 fixture 应产生 `[plans]` ERROR。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
