---
name: docs-sync
description: living-docs 同步维护。同步门被拦时的对齐、历史抽查审计、项目文档归档压缩、旧文档体系（含 modular-programming v1）一次性迁移。push 被 pre-push 门拦下、怀疑有绕过门的漂移、项目文档过长、或用户要求迁移时使用。
---

# docs-sync

设计文档的准确性靠两道保证：**提交纪律**（改到哪个模块，文档改动和代码同一颗 commit）+ **同步门**（pre-push hook 在变更进入受管分支前跑 `check_sync.py`，"代码动了、文档没动"就拒绝）。受管分支（默认 main）上的同步因此靠归纳保持，日常零流程。本 skill 处理门以外的三件事：被拦时对齐、抽查审计、归档压缩与迁移。

## 同步门被拦时（最常见）

pre-push 报 DRIFT 或 ORPHAN：

1. `git diff <range> -- <该模块 code_paths>` 看实际变更，判断职责/对外接口/依赖/注意点是否受影响。
2. 受影响 → 更新模块文档，追进本次提交（amend 或补一颗 commit）再 push。
3. 确实无需更新 → 在 commit message 加一行 `Arch-Sync: skip <module> <一句话理由>`（理由入历史，可审计）。**不用 `--no-verify` 绕过。**
4. ORPHAN 路径三选一：补进某模块 code_paths / 新建模块（建文档 + main-design 加行）/ 加进 main-design 的 ignored_paths。

## 抽查审计（低频后盾）

门可能被绕过（`--no-verify`、没装 hook 的机器、网页直接编辑）。怀疑时对任意历史段跑：

```sh
python3 scripts/check_sync.py --arch-dir <architecture 目录> --range <起点>..HEAD
```

对被点名的模块按上面 1-3 处理（补文档提交即可，无需其他动作）。

## 归档压缩检查（project.md）

变更日志超约 50 条或文件超约 15KB → 旧条目移入 `archives/project-log-YYYY.md`，原位留一行区间摘要；知识区流水账化 → 按主题重写合并。**证据（日期、commit、结论）不删只移。**

## 一次性迁移（旧文档体系 → living-docs）

适用：modular-programming v1 项目，或有零散旧文档的项目。映射：

| 旧 | 新 |
| --- | --- |
| project-management.md 的 Overview / Current Status | project.md 概况 + 当前焦点 |
| knowledge-summary.md | project.md 知识（按主题合并） |
| Recent Updates / Completed Work | project.md 变更日志（一条一行，保留 commit 证据） |
| architecture/modules/*.md | 新模块文档（保留职责、接口、code_paths；砍 kind 分类、baseline/target、关系词表、verified/inferred 标注） |
| 旧 `.last-sync` 锚点文件 | 删除（同步门取代锚点机制） |
| changes/ adrs/ plans/ 等设计历史 | 原地保留，作为历史引用 |

规则：旧文件移入 `archives/`（加 v1- 前缀），不删除（用户明示丢弃除外）；迁移完成后按 docs-init 第 5 步安装同步门，然后走 $docs-acceptance。

## 硬规则

- 单次对齐/抽查控制在 10 分钟内；超时如实记录原因。
- 不重建、不美化：对齐只让文档回到与代码一致，重构模块划分是另一件事，需用户发起。
- 模板见 `../docs-init/templates/`（迁移建新文档、装 hook 时使用）。
- 完成对齐、抽查或迁移后必须调用 $docs-acceptance。
