# Architecture Graph 当前项目架构

状态：draft  
日期：2026-06-30

## 范围

当前项目是一个用于架构设计、架构修改和架构图渲染的 Codex skill。它包含：

- `SKILL.md` skill 触发规则、工作流和质量检查。
- `agents/openai.yaml` Codex UI 元数据。
- `*.arch.json` 架构图结构规则。
- Markdown 模块文档规则。
- `module_kind` / `module_form` 模块表达类型规则。
- 一个零依赖 Python 渲染器。
- 示例文档和渲染产物。

当前执行代码主要集中在 `scripts/render_arch_graph.py`，skill 入口集中在 `SKILL.md` 和 `agents/openai.yaml`。下面的模块拆分是基于现有代码、skill 文件和文档反推出的架构边界，其中一部分已经实现为函数/数据结构，一部分是文档与配置边界。

## 架构图

架构图源文件：

- `architecture/graphs/current-project.arch.json`

渲染输出：

- `dist/current-project-architecture.html`

## 模块分析

### Skill 包装层

Skill 包装层让本项目可以作为 `$architecture-design` 被 Codex 发现和复用。

| 模块 | module_kind | 当前状态 | 说明 |
| --- | --- | --- | --- |
| Skill Instructions | `config-rule` | 已实现为 `SKILL.md` | 定义触发条件、老项目/新项目/已有文档修改流程和质量检查 |
| Agent UI Metadata | `config-rule` | 已实现为 `agents/openai.yaml` | 定义 UI 展示名、短描述和默认提示 |

### 规则层

规则层定义文档语法和模块分类，是渲染器的输入契约来源。

| 模块 | module_kind | 当前状态 | 说明 |
| --- | --- | --- | --- |
| Format Spec | `resource-file` | 已有文档 | 由 `docs/architecture-graph-json-format.md` 定义 `objects`、`groups`、`relations` |
| Module Kind Taxonomy | `config-rule` | 已有文档 | 由 `docs/module-kind-classification.md` 定义 `module_kind` 和 `module_form` |

### 运行时层

运行时层负责从入口文件生成 HTML/SVG 输出。当前实现集中在单个 Python 文件中，但模块边界已经比较清晰。

| 模块 | module_kind | 当前状态 | 说明 |
| --- | --- | --- | --- |
| CLI Orchestrator | `interface-object` | 已实现为 `parse_args()` / `main()` | 负责命令行入口和输出路径 |
| Parser Loader | `function-flow` | 已实现为解析函数 | 读取 `*.arch.json` 和引用模块 Markdown，解析 front matter |
| Graph Model | `data-state` | 已实现为 dataclass | 保存 `Diagram`、`DiagramObject`、`DiagramGroup`、`Relation` |
| Diagnostics | `utility-support` | 已实现为 warnings 列表 | 收集缺失引用、重复 ID、未知端点等告警 |
| Layout Engine | `function-flow` | 已实现为布局函数 | 计算对象位置、组合框边界、连线边界 |
| SVG Renderer | `function-flow` | 已实现为 SVG 函数 | 渲染节点、组合框、关系线、箭头、标签偏移、文档跳转链接和独立 SVG |
| HTML Output | `resource-file` | 已实现为 HTML 包装函数 | 生成自包含 HTML 页面 |

### 示例与产物层

示例与产物层用于验证格式和渲染器。

| 模块 | module_kind | 当前状态 | 说明 |
| --- | --- | --- | --- |
| Examples Fixtures | `resource-file` | 已有示例 | `examples/*.arch.json` 和被引用的 `.md` 模块文档 |
| Rendered Artifacts | `resource-file` | 已有输出 | `dist/*.html`，由渲染器生成 |

## 模块层级关系

高层关系如下：

1. Skill 包装层提供 `$architecture-design` 调用入口和执行规则。
2. 规则层定义输入契约。
3. 示例层提供具体 `*.arch.json` 输入。
4. CLI 入口把输入路径交给 Parser Loader。
5. Parser Loader 读取 JSON 图结构和 Markdown 模块元信息并生成 Graph Model。
6. Diagnostics 记录解析和引用问题。
7. Layout Engine 根据 Graph Model 计算位置和组合框。
8. SVG Renderer 使用 Graph Model 和布局结果生成 SVG，并把对象/组合的 `ref` 渲染为文档跳转链接。
9. HTML Output 包装 SVG 并写到 Rendered Artifacts。

## 交互情况

主要运行链路：

```text
examples/*.arch.json
  -> CLI Orchestrator
  -> Parser Loader
  -> Graph Model
  -> Layout Engine
  -> SVG Renderer
  -> HTML Output
  -> dist/*.html
```

skill 调用链路：

```text
agents/openai.yaml
  -> SKILL.md
  -> Format Spec + Module Kind Taxonomy
  -> architecture/modules/*.md + architecture/graphs/*.arch.json
  -> scripts/render_arch_graph.py
  -> dist/*.html
```

规则依赖链路：

```text
Format Spec + Module Kind Taxonomy
  -> Parser Loader
  -> Graph Model / Renderer
```

诊断链路：

```text
Parser Loader
  -> Diagnostics
  -> HTML Output warnings
```

## 约束

- 当前 YAML/front matter 解析是轻量 `key: value` 解析，不支持完整 YAML。
- 当前图结构以 JSON 为唯一源格式，旧 `.mdx` 图源已废弃。
- 当前项目作为 skill 使用时，`SKILL.md` 是流程入口；`docs/` 下文档是详细参考，不应把全部细节复制进 skill 主体。
- 当前布局是显式 `at` 网格坐标加简单自动布局，不是通用图布局算法；关系线使用快速候选加正交轨道搜索的混合折线路由，并通过评分避让节点、组合标题区和长距离叠线，hover 气泡可用 `label_offset` 做局部微调。
- 当前组合模块 `groups` 只支持按 `contains` 包住对象，不支持关系直接连接到 group。
- 当前渲染器是单文件实现，后续如果复杂度增加，建议按本文模块边界拆分。

## Review Notes

自动审查结果：已检查架构图节点、关系和模块文档是否能对应到当前仓库事实。

- 已验证：Skill 包装层对应 `SKILL.md` 和 `agents/openai.yaml`；规则层对应 `docs/` 文档；示例与产物层对应 `examples/` 和 `dist/`；运行时函数和数据结构对应 `scripts/render_arch_graph.py`。
- 已标注：运行时模块是从当前单文件实现中推导出的架构边界，不表示代码已经拆成多个包。
- 已标注：旧 `.mdx` 图源已废弃，当前基线以 `*.arch.json` 为唯一图结构源。
- 未配置外部 PM 记忆路径，因此没有更新 `project-management.md` 的 Design Documents 索引。

## 模块文档

- `architecture/modules/format-spec.md`
- `architecture/modules/module-kind-taxonomy.md`
- `architecture/modules/skill-instructions.md`
- `architecture/modules/agent-ui-metadata.md`
- `architecture/modules/cli-orchestrator.md`
- `architecture/modules/parser-loader.md`
- `architecture/modules/graph-model.md`
- `architecture/modules/diagnostics.md`
- `architecture/modules/layout-engine.md`
- `architecture/modules/svg-renderer.md`
- `architecture/modules/html-output.md`
- `architecture/modules/examples-fixtures.md`
- `architecture/modules/rendered-artifacts.md`
- `architecture/modules/rules-layer.md`
- `architecture/modules/skill-package.md`
- `architecture/modules/render-runtime.md`
- `architecture/modules/fixtures-output.md`
