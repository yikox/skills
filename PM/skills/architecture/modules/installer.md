---
name: Installer
described: 把技能套件同步到各 agent skills 目录的安装脚本
module_form: atomic
module_kind: function-flow
main_subject: install.sh
code_paths: ["install.sh"]
status: implemented
review_status: reviewed
---

# Installer

## Responsibility

拥有 `install.sh`：把 `modular-programming/` 下的技能目录与 `_shared` 复制到目标 skills 目录，并清理旧版技能名（project-memory、architecture-design 系列）。

## Public Contract

- CLI：`./install.sh [--dry-run] [target_dir ...]`；默认目标 `~/.agents/skills`、`~/.codex/skills`、`~/.claude/skills`。
- 复制约定：每个技能目录 + `_shared` 平铺到目标，保证 `../_shared/` 相对引用可用。

## Internal Design

- bash + `set -euo pipefail`；无第三方依赖。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | out | 分发技能套件（连同 _shared 规则、模板与脚本一并同步） |

## Constraints

- 新增技能目录后无需改脚本（按目录通配复制），但删除/改名技能需在脚本的清理列表中同步。

## Validation

- `./install.sh --dry-run` 列出全部技能目录且退出码 0。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
