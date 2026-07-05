---
name: modular-architecture
description: Create, migrate, maintain, review, and render the architecture-first module map for modular programming projects. Use when the agent should define modules for a new project, infer modules from an existing codebase, update `architecture/main-design.md`, module docs, baseline vs proposed target architecture, architecture change docs, ADRs, graph JSON, rendered HTML/SVG diagrams, or Chinese requests such as 模块地图, 模块架构, 全局设计图, 架构变更, ADR, 老项目模块迁移.
---

# 模块化架构（Modular Architecture）

用这个 skill 维护权威的模块地图。架构拥有模块、边界、关系与持久契约。PM 记录围绕该架构的生命周期。默认情况下，`architecture/main-design.md` 加 `architecture/modules/*.md` 足以支撑 AI 工作；图渲染是一项面向人类的高级可视化能力。

## 必读参考

阅读：

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/architecture-graph-json-format.md`（编写图 JSON 时）。
- `../_shared/references/module-authoring-rules.md`（编写或更新模块文档时）。
- `../_shared/references/module-kind-classification.md`（对模块分类时）。
- `../_shared/references/migration-rules.md`（从老项目推导架构时）。

使用：

- `../_shared/assets/main-design-template.md`
- `../_shared/assets/module-design-template.md`
- `../_shared/assets/architecture-change-template.md`
- `../_shared/assets/adr-template.md`
- `../_shared/scripts/render_modular_graph.py`

## 模式

### 新项目基线

1. 澄清产品/工具目标、运行时、主要工作流、状态/持久化、集成与扩展点——只需足以选定模块边界即可。
2. 提出一份精简的模块地图，包含顶层模块、复合组、原子模块、公开接口与关系。
3. 把提议的模块地图呈现给用户，反复调整直至获批。获批前不要写基线文档。
4. 创建 `architecture/main-design.md` 与 `architecture/modules/*.md`。
5. 仅当用户要求可视化，或项目将图评审作为高级能力使用时，才创建图 JSON 与渲染出的 HTML/SVG。
6. 通过 `modular-status` 把架构文档索引进 PM。

### 老项目迁移

1. 考察代码形态：目录、入口点、运行时路径、包元数据、测试、数据/状态存储、IO 边界、生成产物与文档。
2. 从稳定的技术职责识别模块，而不只是文件夹名字。
3. 把事实标记为 verified、inferred 或 unclear。
4. 在替换既有基线文档前，把推断出的模块地图呈现给用户，反复调整直至获批。
5. 创建或替换基线架构文档。仅当对人工评审或高级工作流明确有用时，才创建图 JSON/渲染输出。
6. 把不清楚的边界与迁移缺口记录进 PM。

### 基线更新

在实现改动了持久架构之后使用：

1. 阅读已接受的设计或已实现的证据。
2. 先更新模块文档，再更新 `main-design.md`。
3. 若项目已使用图产物，或该变更特别影响到某个维护中的图，则更新图 JSON 并渲染图表。
4. 基线文档中只保留已落地或已接受的基线事实。

### L3 目标架构

当变更影响模块边界、跨模块契约、状态归属、持久化、运行时或外部系统时，在实现前使用：

1. 确保该 L3 工作已有 PM start。
2. 写 `architecture/changes/<date>-<change>.md`。
3. 仅当可视化目标有帮助，或图产物属于已接受的高级工作流时，才写入或更新 `architecture/graphs/proposed/<date>-<change>.arch.json`。
4. 仅当存在需在多个有意义备选方案间做出的持久决策时，才添加 `architecture/adrs/ADR-<date>-<decision>.md`。
5. 运行 `modular-review`，然后请求接受，并把一段 3-8 条要点的决策摘要（关键变更、含糊点、风险）内嵌在请求中；在目标经过评审并获人工接受前，不要进入实现。

## 高级渲染

图渲染是可选的、面向人类的。当用户要图、当可视化评审有助于厘清复杂的 L3 变更，或当项目明确把架构图作为高级能力维护时使用。

运行：

```bash
python3 <suite-dir>/_shared/scripts/render_modular_graph.py <project>/architecture/graphs/current-project.arch.json -o <project>/architecture/rendered/current-project-architecture.html --svg-output <project>/architecture/rendered/current-project-architecture.svg
```

把 `<suite-dir>` 解析为本 skill 目录的父目录。

对维护中的图，把渲染器警告当作问题对待，除非用户明确接受一份有已知缺口的草稿。

若要跨项目交互浏览（图页面链接到模块文档），用户可运行本地笔记服务器；上面的静态渲染仍是权威的基线产物：

```bash
python3 <suite-dir>/_shared/scripts/serve_modular_graph.py --root <projects-root> --port 8123
```

## 质量规则

- 每个非平凡模块都有稳定的 slug 与模块文档。
- 新建及迁移的模块文档声明 `code_paths` 并采用单一归属：每条承载行为的路径恰好有一个拥有它的模块。
- 当维护图时，关系遵循"箭头即依赖"、封闭的 `kind` 词表，以及图格式参考中的实线/虚线运行时语义；该维护中的图是模块间关系的权威可视化来源。
- 当外部协作需要具名端点时，复合模块暴露接口。
- 关系连接的是处于同一架构层级的模块。
- 提议的目标与当前基线清晰分离。
- 架构文档不包含任务清单、实现计划或 PM 历史。
- PM 索引架构产物，但不定义模块边界。
