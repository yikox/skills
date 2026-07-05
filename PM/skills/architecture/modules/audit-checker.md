---
name: Audit Checker
described: modular-audit 的确定性检查脚本，机械校验项目记忆的一致性
module_form: atomic
module_kind: function-flow
main_subject: check_modular_project.py
code_paths: ["en/modular-programming/modular-audit/scripts/**", "en/modular-programming/modular-audit/tests/**"]
status: implemented
review_status: reviewed
---

# Audit Checker

## Responsibility

拥有 `check_modular_project.py`：对 pm-root 做确定性一致性检查（必备文件、模块 front matter、代码所有权、可选图与文档关系子集、设计/计划/ADR front matter、PM 表格结构），输出 ERROR/WARNING，退出码 1 表示存在 error。

## Public Contract

- CLI：`python3 check_modular_project.py <pm-root> [--repo-root <path>] [--exclude <glob>]...`
- 检查项词表（DESIGN_STATUSES、REVIEW_STATUSES、MODULE_KINDS、MODULE_FORMS、RELATION_KINDS、RELATION_STYLES）在启动时由 `load_vocab()` 从 shared-references 的 `vocab.md` 解析得到，单一事实源即该清单；解析失败或缺项回退内置默认词表并告警。
- `check_plans` 校验 `plans/*.md` 与 `modules/*/plans/*.md`：`source_design` 存在且不越出 pm 根、`level` 合法且与目录匹配（plans/ 存 L3，modules/*/plans/ 存 L2）、源设计已 implemented 时告警归档。
- `check_graph` 在图文件存在时校验图端点、关系词表、group 森林、interface provider 所属子树、relation 同层 scope；缺少图文件不再告警。v0.3 引入的结构约束对 v0.1/v0.2 老图降级为 warning，不阻断老项目迁移审计。
- `check_ownership` 将 `shared_paths` / `ignored_paths` 作为已说明的非 owner 例外，不参与唯一 owner 检查，也不报孤儿路径；例外 glob 匹配不到任何文件时报幽灵例外 warning。

## Internal Design

- 单文件、stdlib-only；`parse_front_matter` 手写解析（不依赖 yaml 库）；error/warn 累积后统一输出。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | in | modular-audit 技能启动时运行本脚本 |
| shared-references | out | reads：启动时解析 `vocab.md` 受控词表清单驱动校验 |

## Constraints

- 仅用 Python 3 标准库（安装目标环境不保证第三方包）；`vocab.md` 解析亦手写，不引第三方。
- `vocab.md` 路径按 `parents[2]/_shared/references/vocab.md` 定位，仓库内与安装平铺后均成立。
- glob 语义：`/**` 结尾匹配目录前缀下全部文件，其余按 fnmatch 全路径匹配。

## Validation

- `python3 en/modular-programming/modular-audit/scripts/check_modular_project.py PM/skills` 退出码 0。
- `python3 -m unittest discover -s en/modular-programming/modular-audit/tests` 退出码 0。
- 构造缺 `source_design` 的计划 fixture 应产生 `[plans]` ERROR。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
