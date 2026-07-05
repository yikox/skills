---
name: modular-audit
description: Audit or migrate a modular programming project for consistency. Use when the agent should check stale PM tasks, missing primary modules, missing PM start/completion records, outdated architecture baselines, graph/doc drift, implemented designs not reflected in architecture, old project-memory or architecture-design schema, roadmap drift, archive candidates, or Chinese requests such as 模块化审计, 项目迁移, 架构漂移检查, 清理 PM, 旧项目迁移.
---

# 模块化审计（Modular Audit）

用这个 skill 让一个模块化编程项目随时间推移始终可信。

## 必读参考

阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`
- `../_shared/references/migration-rules.md`
- `../_shared/references/pm-maintenance-rules.md`（检查归档候选或历史压缩时）。

## 脚本

审计从运行确定性检查器开始；把它的输出并入报告（脚本负责机械检查，agent 负责语义检查）：

```bash
python3 <skill-dir>/scripts/check_modular_project.py <pm-root> [--repo-root <repo>] [--exclude <glob>]...
```

传入 `--repo-root` 以启用代码归属检查（orphan/ghost/overlap）。为 `main-design.md` 的 Shared Constraints 中列出的项目有意无归属路径添加 `--exclude`。退出码 1 表示存在错误。

## 审计检查项

检查：

- 每个进行中的 L2/L3 任务及被跟踪的 L1 任务都有 PM start 信息；
- 已完成的 L2/L3 工作及被跟踪的 L1 工作都有 PM completion 证据；
- 非平凡的 backlog 行都有 primary module、impacted modules 与 change level；
- L2/L3 设计文档已被索引且状态同步；
- 计划文件位于 `plans/` 下，且有合法的 `source_design` 与 `level`；其来源设计已实现的计划为归档候选；
- 已实现的设计有证据；
- 已落地的持久变更已反映到架构基线中；
- proposed 目标架构没有被当作已实现基线呈现；
- 当存在图产物时，图 JSON 关系与模块文档及同层关系规则一致；
- 模块文档声明所拥有的 `code_paths`；无 orphan 路径（承载行为却无模块拥有的代码）、无 ghost glob（匹配不到任何东西）、无重叠的归属声明；`shared_paths` / `ignored_paths` 是有文档记录的非归属例外；
- 当存在图产物时，模块文档的 Dependencies 表是图关系的子集，且关系 `kind` 值取自封闭词表；
- ADR 摘要行链接到 ADR 文件；
- 旧的 `project-memory` 或 `architecture-design` 术语已迁移或归档；
- 旧的详尽历史可在不丢失当前状态的前提下压缩。

## 迁移流程

1. 阅读当前的 PM 与架构文档。
2. 检测旧 schema 与旧 skill 名。
3. 保留有用的当前事实、进行中的工作、已接受的决策与证据。
4. 转换为模块化存储 schema。
5. 记录迁移缺口，而不是猜测。
6. 对改动过的 PM 与架构产物运行 `modular-review`。

## 报告

先按严重程度排序列出问题。然后列出已应用的安全修复、待解答的问题，以及推荐的下一个 skill。
