# 模块架构表达类型分类草案

状态：draft v0.1。

这份文档定义的是“模块架构文档应该用什么方式表达”，不是业务模块分类，也不是代码目录分类。

核心判断标准：

> 一个模块的主设计载体是什么？技术人员理解它时，最应该先看布局、函数流程、接口对象、数据状态，还是外部 IO 边界？

模块描述分两层：

- `module_kind`：底层表达类型，说明这个模块的主设计载体是什么。
- `module_form`：模块形态，说明这个模块是单个模块还是组合模块。

同一个模块可以有多个侧面，但文档应该选择一个 `module_kind` 作为主类型，再用 `secondary_kinds` 补充次要类型。组合模块使用 `module_form: composite`，内部成员仍然分别使用底层 `module_kind`。

```yaml
---
name: 编辑器渲染模块
described: 将文档状态渲染成可交互编辑界面
module_form: atomic
module_kind: function-flow
secondary_kinds:
  - interface-object
main_subject: renderDocument()
---
```

## 底层分类总览

`module_kind` 与 `module_form` 的合法枚举值以 `vocab.md`（audit-checker 强制）为单一事实源；下表在此基础上补充每类的主设计载体、图形与展开方式。

| module_kind | 适合什么模块 | 主设计载体 | 图形 | 颜色 | 默认展开方式 |
| --- | --- | --- | --- | --- | --- |
| `layout-style` | UI 分布、样式、视觉结构模块 | 布局区域、样式规则、组件层级 | frame | `#2563eb` | 展开为布局区域图 |
| `function-flow` | 渲染、编译、解析、调度等流程模块 | 核心函数、步骤、时序、分支 | hexagon | `#7c3aed` | 展开为流程图 / 时序图 |
| `interface-object` | reader、writer、service、manager、client 这类对象模块 | 接口、方法、生命周期、协作对象 | rounded-rect | `#059669` | 展开为接口和方法图 |
| `data-state` | 文档状态、缓存、索引、存储模型模块 | 数据结构、状态机、读写路径 | cylinder | `#d97706` | 展开为数据模型和状态流转图 |
| `event-message` | 事件总线、订阅、消息同步、广播模块 | 事件类型、生产者、消费者、顺序 | diamond | `#dc2626` | 展开为事件流图 |
| `config-rule` | 配置、规则、策略、插件声明模块 | schema、默认值、覆盖优先级、校验规则 | document | `#475569` | 展开为规则链和配置表 |
| `resource-file` | 文件、目录、资源包、模板、文档格式模块 | 文件结构、格式、引用关系、加载规则 | folder | `#0891b2` | 展开为文件树和引用图 |
| `adapter-io` | 文件系统、网络、浏览器、数据库、第三方 API 适配模块 | 外部边界、协议、错误映射、重试 | port | `#ea580c` | 展开为边界协议图 |
| `utility-support` | utils、logs、diagnostics、helper 这类支撑模块 | 工具函数、日志能力、诊断能力、共享 helper | small-rect | `#64748b` | 展开为工具能力清单 |

说明：`图形` 是语义图形名。当前最小渲染器暂时只支持一部分基础形状，后续可以把这些语义图形映射到具体 SVG。

## 通用 front matter

每个模块文档建议包含：

```yaml
---
format: arch-module/v0.1
name: 模块名称
described: 一句话说明这个模块给技术人员看的核心价值
module_form: atomic
module_kind: function-flow
secondary_kinds: []
main_subject: 主设计载体，比如 renderDocument()、EditorLayout、DocumentStore
status: draft
---
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `format` | 推荐 | 建议使用 `arch-module/v0.1` |
| `name` | 是 | 模块名称，渲染到图形标题 |
| `described` | 是 | 简短描述，渲染到图形正文 |
| `module_form` | 推荐 | `atomic` 或 `composite`，默认 `atomic` |
| `module_kind` | 是 | 本文档定义的主表达类型 |
| `secondary_kinds` | 否 | 次要表达类型，用于提示文档还有哪些侧面 |
| `main_subject` | 推荐 | 模块的主设计载体 |
| `status` | 推荐 | `draft`、`proposed`、`accepted`、`implemented` |

## 选择规则

选择 `module_kind` 时，不问“它属于哪个业务域”，而问下面几个问题：

1. 如果只能画一张图，最有解释力的是哪种图？
2. 技术人员改这个模块时，最怕破坏的是布局、流程、接口、状态，还是 IO 契约？
3. 这个模块最稳定、最应该被保护的设计资产是什么？
4. 文档正文里占最大篇幅的应该是什么？

如果一个模块看起来能归到多个类型，按主设计载体选择主类型：

- 编辑器渲染模块有对象 API，但核心是 `render()` 调用流程，选 `function-flow`。
- 文档同步模块有事件，也有对象接口；如果对外主要暴露 `SyncClient`，选 `interface-object`；如果核心风险是事件顺序和冲突合并，选 `event-message` 或 `data-state`。
- UI 模块有组件对象，但文档主体是布局、样式和区域关系，选 `layout-style`。

## 九类 module_kind 详解

每一类的“什么模块属于这类 / 图形设计 / 展开方式 / 文档模板”抽为独立分片，便于单独查阅与维护。选类型时先看上面的“底层分类总览”与“选择规则”，确定后到对应分片查图形、展开方式与文档模板：

| module_kind | 主设计载体 | 分片 |
| --- | --- | --- |
| `layout-style` | 布局区域、样式规则、组件层级 | [module-kinds/layout-style.md](module-kinds/layout-style.md) |
| `function-flow` | 核心函数、步骤、时序、分支 | [module-kinds/function-flow.md](module-kinds/function-flow.md) |
| `interface-object` | 接口、方法、生命周期、协作对象 | [module-kinds/interface-object.md](module-kinds/interface-object.md) |
| `data-state` | 数据结构、状态机、读写路径 | [module-kinds/data-state.md](module-kinds/data-state.md) |
| `event-message` | 事件类型、生产者、消费者、顺序 | [module-kinds/event-message.md](module-kinds/event-message.md) |
| `config-rule` | schema、默认值、覆盖优先级、校验规则 | [module-kinds/config-rule.md](module-kinds/config-rule.md) |
| `resource-file` | 文件结构、格式、引用关系、加载规则 | [module-kinds/resource-file.md](module-kinds/resource-file.md) |
| `adapter-io` | 外部边界、协议、错误映射、重试 | [module-kinds/adapter-io.md](module-kinds/adapter-io.md) |
| `utility-support` | 工具函数、日志能力、诊断能力、共享 helper | [module-kinds/utility-support.md](module-kinds/utility-support.md) |

## 组合模块形态

组合模块不是一种底层 `module_kind`，而是一种 `module_form`。它表示“这个模块由多个子模块组成”，图形上用一个外框把内部模块框起来。

组合模块的 front matter 建议写成：

```yaml
---
format: arch-module/v0.1
name: 工具模块
described: 提供路径处理、日志和诊断支撑能力
module_form: composite
main_subject: utils + logs + diagnostics
---
```

### 什么模块适合做组合模块

当一个模块不是单一函数、对象、状态或文件格式，而是一个有内部结构的模块包时，就适合建模为组合模块。

常见例子：

- 工具模块：由 `path-utils`、`string-utils`、`logs`、`diagnostics` 组成。
- 编辑器模块：由 `editor-layout`、`editor-renderer`、`editor-state`、`editor-events` 组成。
- 文档模块：由 `document-reader`、`document-writer`、`document-cache`、`document-sync` 组成。
- 渲染工作区：由 `parser`、`resolver`、`layout`、`renderer-html` 组成。

### 图形设计

- 语义图形：`container`
- 推荐边框颜色：`#4f46e5`
- 推荐填充颜色：`#eef2ff`
- 图形含义：模块容器 / 子模块组合。
- 标签位置：外框左上角或右上角。
- 标签内容：第一行显示 `name`，第二行显示 `described`。
- 内部内容：子模块节点按各自 `module_kind` 使用自己的图形和颜色。

示意：

```text
+--------------------------------------------------+
| 工具模块                                         |
| 提供路径处理、日志和诊断支撑能力                 |
|                                                  |
|   [path-utils]     [logger]      [diagnostics]   |
|                                                  |
+--------------------------------------------------+
```

### 展开方式

组合模块默认展开为子模块关系图：

```text
tooling
  contains path-utils
  contains logger
  contains diagnostics

path-utils -> logger: 输出路径错误上下文
diagnostics -> logger: 输出诊断信息
```

展开时重点显示：

- 子模块清单。
- 子模块各自的 `module_kind`。
- 子模块之间的依赖方向。
- 组合模块对外暴露的入口。
- 哪些内部模块不允许被外部直接依赖。

### 文档模板

```md
# <组合模块名称>

## 模块定位

说明这个组合模块为什么需要作为整体存在，对外提供什么能力。

## 子模块清单

列出子模块、`module_kind`、职责摘要、文档链接。

## 组合边界

说明哪些能力属于组合模块内部，哪些能力是对外公开入口。

## 内部关系

说明子模块之间的依赖、调用、事件、数据或资源关系。

## 对外入口

说明外部模块应该通过哪些 API、对象、文件或事件使用这个组合模块。

## 禁止依赖

说明外部模块不能直接依赖哪些内部子模块，以及原因。

## 演进规则

说明什么时候新增子模块，什么时候把子模块拆出去，什么时候合并。

## 验证方式

说明组合级集成测试、依赖方向检查、架构图快照和公开入口测试。
```

## 图形与颜色映射建议

渲染器可以先实现一个稳定映射表：

| module_kind | shape | stroke | fill | expand |
| --- | --- | --- | --- | --- |
| `layout-style` | `frame` | `#2563eb` | `#eff6ff` | `layout-regions` |
| `function-flow` | `hexagon` | `#7c3aed` | `#f5f3ff` | `flow-steps` |
| `interface-object` | `rounded-rect` | `#059669` | `#ecfdf5` | `api-methods` |
| `data-state` | `cylinder` | `#d97706` | `#fffbeb` | `state-model` |
| `event-message` | `diamond` | `#dc2626` | `#fef2f2` | `event-flow` |
| `config-rule` | `document` | `#475569` | `#f8fafc` | `rule-chain` |
| `resource-file` | `folder` | `#0891b2` | `#ecfeff` | `file-tree` |
| `adapter-io` | `port` | `#ea580c` | `#fff7ed` | `boundary-protocol` |
| `utility-support` | `small-rect` | `#64748b` | `#f8fafc` | `utility-list` |

组合模块使用单独的形态映射：

| module_form | shape | stroke | fill | expand |
| --- | --- | --- | --- | --- |
| `composite` | `container` | `#4f46e5` | `#eef2ff` | `submodule-graph` |

## 在 JSON 图结构中的引用示例

```json
{
  "objects": [
    {
      "id": "editor-renderer",
      "ref": "./modules/editor-renderer.md",
      "at": [1, 0]
    },
    {
      "id": "editor-layout",
      "ref": "./modules/editor-layout.md",
      "at": [0, 0]
    }
  ],
  "relations": [
    {
      "from": "editor-layout",
      "to": "editor-renderer",
      "described": "提供容器尺寸和可视区域",
      "style": "solid"
    }
  ]
}
```

被引用文档：

```yaml
---
format: arch-module/v0.1
name: 编辑器渲染模块
described: 将文档状态渲染成可交互编辑界面
module_kind: function-flow
main_subject: renderDocument()
---
```

渲染器读取 `module_kind` 后，可以自动决定节点图形、颜色和默认展开方式；JSON `objects[]` 条目仍然允许手动覆盖 `shape`、`stroke`、`fill` 或 `expand`。

组合模块引用示例：

```json
{
  "groups": [
    {
      "id": "tool-module",
      "ref": "./modules/tool-module.md",
      "contains": ["path-utils", "logger", "diagnostics"]
    }
  ],
  "objects": [
    {
      "id": "path-utils",
      "ref": "./modules/path-utils.md",
      "at": [0, 0]
    },
    {
      "id": "logger",
      "ref": "./modules/logger.md",
      "at": [1, 0]
    },
    {
      "id": "diagnostics",
      "ref": "./modules/diagnostics.md",
      "at": [2, 0]
    }
  ]
}
```

`groups[]` 渲染为一个外框，`contains` 中的对象渲染在外框内部。外框角标显示组合模块文档的 `name` 和 `described`。

## 需要继续讨论的问题

1. `module_kind` 是否作为必填字段，还是仅在模块文档中必填、普通说明文档可选？
2. `secondary_kinds` 是否需要渲染出来，还是只作为文档提示？
3. `module_form: composite` 是否必须配套 `group`，还是允许只在文档中声明组合模块？
4. 展开方式是通过 `expand: true` 自动选择，还是显式写 `expand: flow-steps` / `expand: submodule-graph`？
5. 颜色是否写死为规范，还是允许主题覆盖？
6. `layout-style` 是否应该拆成 `layout` 和 `style` 两类，还是先合并更好？
