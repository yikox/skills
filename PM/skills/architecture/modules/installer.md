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

拥有 `install.sh`：按语言从 `<lang>/modular-programming/`（`lang` ∈ {zh, en}）把技能目录与 `_shared` 复制到目标 skills 目录，并清理旧版技能名（project-memory、architecture-design 系列）。

## Public Contract

- CLI：`./install.sh <lang> [--dry-run] [target_dir ...]`；首个位置参数为语言（`zh|en`，必填），其余为目标目录；默认目标 `~/.agents/skills`、`~/.codex/skills`、`~/.claude/skills`。
- 缺少或非法 `<lang>` → 打印 usage 并以退出码 2 结束（不设隐式默认语言）。
- 复制约定：选定语言下每个技能目录 + `_shared` 平铺到目标，保证 `../_shared/` 相对引用可用；安装产物不含语言层。

## Internal Design

- bash + `set -euo pipefail`；无第三方依赖。
- 源根为 `$repo_dir/<lang>/modular-programming`；`find` 在该根下扫描 `SKILL.md`。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | out | 分发技能套件（连同 _shared 规则、模板与脚本一并同步） |

## Constraints

- 新增技能目录后无需改脚本（按目录通配复制），但删除/改名技能需在脚本的清理列表中同步。
- 语言编辑对等：`zh/` 与 `en/` 目录结构须逐目录对应，二者同一技能装出的目录名一致（仅内容语言不同）。

## Validation

- `./install.sh en --dry-run` 与 `./install.sh zh --dry-run` 各列出全部技能目录且退出码 0；`./install.sh`（缺 lang）退出码 2。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
