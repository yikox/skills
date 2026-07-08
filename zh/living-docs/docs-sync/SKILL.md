---
name: docs-sync
description: living-docs 对账。检测代码与设计文档的漂移（git diff ∩ code_paths）并逐模块对齐；检查项目文档归档压缩；旧文档体系（含 modular-programming v1）一次性迁移。会话开始检测到漂移、或用户要求对账/压缩/迁移时使用。
---

# docs-sync

设计文档的准确性靠两件事：日常"顺带更新"，以及本 skill 的事后对账。对账由 git 证据驱动，不靠日历。

## 对账流程

1. **漂移检测**：

   ```sh
   python3 scripts/check_drift.py --arch-dir <architecture 目录> [--repo <仓库根>]
   ```

   脚本计算 `git diff <.last-sync>..工作区 ∩ 各模块 code_paths`，输出"代码动了、文档没动"的模块清单和不属于任何模块的孤儿路径。

2. **清单为空** → 报告已对齐，跳到第 5 步。
3. **逐模块对账**：对每个被点名的模块，`git diff <last-sync> -- <该模块 code_paths>` 看实际变更，判断职责/对外接口/依赖/注意点是否受影响——需要就更新模块文档；确认无需更新也算对齐（说出理由）。孤儿路径判断：该归入某模块（补 code_paths）、新模块（建文档 + main-design 加行）、或该忽略（加进 main-design 的 ignored_paths）。
4. **收锚**：全部模块有结论后，把 `architecture/.last-sync` 更新为当前 HEAD。
5. **归档压缩检查**（project.md）：变更日志超约 50 条或文件超约 15KB → 旧条目移入 `archives/project-log-YYYY.md`，原位留一行区间摘要；知识区流水账化 → 按主题重写合并。**证据（日期、commit、结论）不删只移。**
6. **验收**：完成后必须调用 $docs-acceptance 验收本次 sync。

## 一次性迁移（旧文档体系 → living-docs）

适用：modular-programming v1 项目，或有零散旧文档的项目。映射：

| 旧 | 新 |
| --- | --- |
| project-management.md 的 Overview / Current Status | project.md 概况 + 当前焦点 |
| knowledge-summary.md | project.md 知识（按主题合并） |
| Recent Updates / Completed Work | project.md 变更日志（一条一行，保留 commit 证据） |
| architecture/modules/*.md | 新模块文档（保留职责、接口、code_paths；砍 kind 分类、baseline/target、关系词表、verified/inferred 标注） |
| changes/ adrs/ plans/ 等设计历史 | 原地保留，作为历史引用 |

规则：旧文件移入 `archives/`（加 v1- 前缀），不删除；迁移完成即按对账流程收锚（.last-sync = 当前 HEAD），然后走 $docs-acceptance。

## 硬规则

- 一次对账控制在 10 分钟内；漂移大到超时，说明对账间隔太长，如实记录。
- 不重建、不美化：对账只让文档回到与代码一致，重构模块划分是另一件事，需用户发起。
- 模板见 `../docs-init/templates/`（迁移建新文档时使用）。
