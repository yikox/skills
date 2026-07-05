# 模块化存储 Schema

在创建或修复模块化编程项目记忆时使用本 schema。

## 默认项目记忆布局

```text
PM/<project-slug>/
  project-management.md
  knowledge-summary.md
  architecture/
    main-design.md
    changes/
      <YYYY-MM-DD>-<architecture-change>.md
    plans/
      <YYYY-MM-DD>-<change>-plan.md
    adrs/
      ADR-<YYYY-MM-DD>-<decision>.md
    modules/
      <module-slug>.md
      <module-slug>/
        changes/
          <YYYY-MM-DD>-<module-change>.md
        plans/
          <YYYY-MM-DD>-<change>-plan.md
    graphs/
      current-project.arch.json
      proposed/
        <YYYY-MM-DD>-<change>.arch.json
    rendered/
      current-project-architecture.html
      current-project-architecture.svg
```

默认可供 AI 阅读的基线是 `architecture/main-design.md` 加上 `architecture/modules/*.md`。`graphs/` 与 `rendered/` 是可选的高级可视化目录；仅在项目使用图评审、用户要求图示，或某个高级技能需要时才创建它们。

## PM 小节

新建 `project-management.md` 文件时优先使用以下小节。修复老项目时保留等价的既有标题。

1. Overview
2. Current Status
3. Active Tasks
4. Requirements / Change Backlog
5. Modular Design Index
6. Roadmap
7. Milestones
8. Testing and Validation
9. Blockers and Risks
10. ADR Summary
11. Archive
12. Recent Updates

## 进行中任务字段

对进行中的 L2/L3 工作使用表格或简洁要点，对 L1 仅在其跨会话、携带发布/风险证据、属于某个进行中任务，或用户明确希望跟踪时使用。记录：

- 日期；
- 任务；
- 主模块；
- 受影响模块；
- 级别；
- 状态；
- 下一步 / 备注。

## 待办清单字段

当用户提出一个尚未实现的非平凡需求或变更时，使用一条待办行：

- 稳定 ID；
- 日期；
- 请求；
- 主模块；
- 受影响模块；
- 变更级别；
- 变更摘要；
- 范围 / 影响；
- 状态；
- 优先级；
- 设计路径 / 下一步。

## 模块化设计索引

索引持久的设计产物：

- 主架构：`architecture/main-design.md`；
- 模块：`architecture/modules/<module>.md`；
- 架构变更：`architecture/changes/<date>-<change>.md`；
- ADR：`architecture/adrs/ADR-<date>-<decision>.md`；
- 模块变更：`architecture/modules/<module>/changes/<date>-<change>.md`。

图 JSON 与渲染图是可选的高级可视化产物。仅在项目主动使用图评审，或某个具体变更/设计需要可视化沟通时才索引它们。对默认 AI 工作流而言，`main-design.md` 与模块文档仍然足够。

## 模块 front matter

模块文档（`architecture/modules/<module>.md`）使用以下 front matter：

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `name` | 是 | 显示名称 |
| `described` | 是 | 一句话职责 |
| `module_form` | 是 | `atomic` 或 `composite` |
| `module_kind` | 是 | 见 `module-kind-classification.md` |
| `main_subject` | 是 | 主要技术主题（函数、文件、格式） |
| `code_paths` | 新/迁移模块必填 | 该模块所拥有代码的相对仓库根 glob 列表 |
| `shared_paths` | 否 | 该模块使用或记录、但不独占拥有的相对仓库根 glob |
| `ignored_paths` | 否 | 有意置于模块归属之外的相对仓库根 glob，并在 main-design 的 Shared Constraints 中说明 |
| `status` | 是 | 下方的设计状态词表 |
| `review_status` | 是 | 下方的评审状态词表 |

`code_paths` 遵循单一归属：每条承载行为的代码路径都属于且仅属于一个模块（见 `modular-workflow-rules.md` 的 Code Ownership）。缺少 `code_paths` 的既有文档仍然有效；`modular-audit` 会将它们标记为待补全。
`shared_paths` 与 `ignored_paths` 不授予归属；它们记录诸如共享工具、框架胶水、集成测试、生成输出或仓库级配置之类的例外。

## Slug 规则

- 使用小写 ASCII slug。
- 将空格与标点替换为连字符。
- 一旦 PM 或设计引用了模块 slug，就保持其稳定。
- 优先使用技术归属名称，而非功能营销名称。

## 状态词表

`design_status` 与 `review_status` 的受强制枚举值以 `vocab.md`（由 audit-checker 解析）为单一事实源；下面的流程只解释它们的顺序与含义。需求/任务状态是描述性的，不受机器强制。

需求/任务状态：

```text
needs-clarification -> ready-for-design -> designing -> designed
  -> accepted -> implementing -> implemented
```

Design statuses:

```text
draft -> proposed -> accepted -> implemented
```

Review statuses:

```text
not-reviewed -> needs-review -> reviewed
```

当项目原生的状态词已经存在时使用它们，但保持含义一致。

## 计划文件

实现计划是临时的执行辅助，而非架构。它们存放在设计 `changes/` 目录旁的 `plans/` 里——L3 计划在 `architecture/plans/` 下，L2 计划在 `architecture/modules/<module-slug>/plans/` 下。绝不要把计划存放在 `changes/` 目录内。

计划 front matter：

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `source_design` | 是 | 该计划所实现设计的相对 pm 根路径 |
| `level` | 是 | `L2` 或 `L3`，与源设计一致；计划的目录必须与其级别匹配（`plans/` 放 L3，`modules/<module-slug>/plans/` 放 L2） |

一旦记录了 PM 完成，就归档或删除计划；`modular-audit` 会对源设计已为 `implemented` 的计划发出告警。归档时，把计划移入其旁边的 `archive/` 子目录（如 `architecture/plans/archive/`）；checker 会有意跳过已归档的计划。
