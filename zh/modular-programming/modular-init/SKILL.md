---
name: modular-init
description: Initialize or repair an architecture-first modular programming workflow for a project. Use when the agent should set up modular project memory, connect or create `project-management.md`, `knowledge-summary.md`, `architecture/main-design.md`, module docs, architecture graphs, project AI rules, or migrate a new/old project into the modular workflow; Chinese triggers include 模块化编程初始化, 项目初始化, 接入模块化工作流, 老项目接入, 修复项目记忆.
---

# 模块化初始化（Modular Init）

用这个 skill 把模块化编程工作流安装进一个项目。目标是在正常开发工作开始之前，先创建一份可用的轻量模块地图与项目记忆结构。

## 必读参考

先解析出本 skill 目录，然后阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- 编写模块文档时阅读 `../_shared/references/module-authoring-rules.md`。
- 当项目已有代码、旧 PM 文档或旧架构文档时，阅读 `../_shared/references/migration-rules.md`。

创建新文件时使用这些 asset：

- `../_shared/assets/project-management-template.md`
- `../_shared/assets/knowledge-summary-template.md`
- `../_shared/assets/main-design-template.md`
- `../_shared/assets/module-design-template.md`
- 项目 AI 协作文档使用 `../_shared/assets/ai-rules-snippet.md`。

## 工作流

1. 确定项目根，以及项目已在用的外部或仓库内记忆位置。若不存在记忆位置，提议 `PM/<project-slug>/` 并与用户确认位置。
2. 阅读既有的 AI 协作文档，如 `AGENTS.md`、`CLAUDE.md`、`.codex/AGENTS.md`，以及既有的项目记忆文档。
3. 判定模式：
   - 新项目：把产品/运行时意图澄清到足以创建一份初始模块地图；
   - 既有项目：在提议改动之前先检查代码并迁移当前事实；
   - 修复：修复缺失的章节、陈旧的路径或旧的工作流名称。
4. 在创建文件之前，以多选题形式询问用户的工作流偏好（见 `modular-workflow-rules.md` 中的 Preference Profiles）：
   - `docs-language`：PM、架构、知识与设计文档的语言（`zh` / `en` / `follow-project`）；
   - `confirmation`：确认粒度（`high-touch` / `standard` / `low-touch`）。
   用户无偏好时，默认 `follow-project` + `standard`。
5. 以所选文档语言创建或修复 `project-management.md`、`knowledge-summary.md`、`architecture/main-design.md` 与 `architecture/modules/*.md`。当这会引入一份新的或被替换的模块地图时，先把它呈现给用户并取得批准，再写基线文档。
6. 确保架构是模块的事实来源。PM 可以索引模块与任务，但不得独立定义模块边界。
7. 对既有项目，只创建经核实或明确推断的基线。把不确定的部分作为迁移缺口记入 PM。
8. 默认不创建架构图。仅当用户想要图示，或项目明确采用图评审时，才把图渲染作为一个高级可视化选项提供。
9. 把 `../_shared/assets/ai-rules-snippet.md` 合并进项目的 AI 协作文档（`CLAUDE.md`、`AGENTS.md` 或等价物）：用所选值填入 Preferences 一节，把路径与语言适配到该项目，与既有内容合并而非覆盖，并在创建或首次修改这些文件之前与用户确认。
10. 报告已创建/更新的文件、所选偏好、模块基线状态、迁移缺口，以及下一个推荐的 skill。

## 交接

- 当模块边界、图或基线文档仍需完善时，下一步用 `modular-architecture`。
- 当用户在初始化之后有了具体的变更请求时，下一步用 `modular-change`。
- 当存在旧项目记忆且一致性不确定时，用 `modular-audit`。
