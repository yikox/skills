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

## `layout-style`

### 什么模块属于这类

主体是一组布局区域、样式规则、视觉层级或组件分布。它的关键设计不是某个函数，而是页面结构如何组织、样式如何约束、区域如何响应状态变化。

常见例子：

- 编辑器主界面布局模块。
- 工具栏、侧边栏、状态栏、画布区域的组合模块。
- 主题系统、样式 token、颜色/间距/排版规则模块。
- 一个复杂控件的布局和交互状态样式。

### 图形设计

- 语义图形：`frame`
- 推荐颜色：`#2563eb`
- 图形含义：一个带内部区域分隔的界面框。
- 默认节点摘要：显示 `name`、`described`、主要区域数量。

### 展开方式

默认展开为布局区域图：

```text
Layout Module
  -> header / toolbar
  -> sidebar
  -> editor canvas
  -> status bar
  -> floating panels
```

展开后重点显示区域之间的包含关系、对齐关系、覆盖层级和响应式断点。不要把每个 CSS 属性都画出来，细节放在表格里。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个 UI / 样式模块管理哪些界面区域，哪些区域不属于它。

## 主体结构

列出主要布局区域、组件层级、包含关系和层级顺序。

## 样式规则

记录核心 token、尺寸、间距、颜色、字体、阴影、z-index、状态样式。

## 响应式与状态变化

说明不同窗口尺寸、编辑状态、加载状态、禁用状态下的布局变化。

## 与其他模块关系

说明它依赖哪些状态、事件或渲染结果，以及它向外暴露哪些样式/布局能力。

## 约束与非目标

说明哪些样式不能在本模块之外覆盖，哪些视觉规则暂不处理。

## 验证方式

说明截图、视觉回归、组件测试或手动检查路径。
```

## `function-flow`

### 什么模块属于这类

主体是一个或几个核心函数、算法、管线、流程或时序。技术人员理解它时，最重要的是输入如何经过步骤变成输出，以及中间有哪些分支、缓存、异常和副作用。

常见例子：

- 编辑器渲染模块：`renderDocument()`。
- Markdown front matter / JSON 图结构解析模块：`parseDocument()` 或 `loadGraph()`。
- 架构图布局计算模块：`layoutGraph()`。
- 编译管线、格式化管线、任务调度器。

### 图形设计

- 语义图形：`hexagon`
- 推荐颜色：`#7c3aed`
- 图形含义：处理节点 / 转换节点。
- 默认节点摘要：显示核心函数名、输入和输出。

### 展开方式

默认展开为流程图或时序图：

```text
input
  -> validate
  -> normalize
  -> transform
  -> render
  -> output
```

如果流程跨对象协作，用时序图；如果主要是纯函数管线，用流程图；如果有复杂分支，用决策图。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个流程解决什么技术问题，在哪些调用路径中被使用。

## 主函数 / 主流程

列出核心函数签名、入口、出口、同步/异步性质。

## 输入与输出

说明输入结构、输出结构、前置条件和后置条件。

## 流程步骤

按顺序说明主要步骤、分支条件、循环、缓存点和副作用。

## 时序与调用关系

说明调用哪些模块，被哪些模块调用，以及关键时序约束。

## 错误处理

说明错误类型、恢复策略、降级行为和诊断信息。

## 性能与复杂度

说明复杂度、热点路径、批处理策略、增量策略。

## 验证方式

说明单元测试、快照测试、流程用例和边界条件。
```

## `interface-object`

### 什么模块属于这类

主体是一组接口、一个对象、一个 class、一个 service、一个 manager 或一个 client。关键设计是它向外暴露什么能力、生命周期如何管理、内部状态如何被保护。

常见例子：

- `DocumentReader` / `DocumentWriter`。
- `SyncClient`、`EditorSession`、`PluginManager`。
- SDK 的 public facade。
- 一个负责协调多个内部函数的 service 对象。

### 图形设计

- 语义图形：`rounded-rect`
- 推荐颜色：`#059669`
- 图形含义：可调用对象 / 稳定接口。
- 默认节点摘要：显示对象名、主要方法数量、生命周期状态。

### 展开方式

默认展开为接口和方法图：

```text
EditorSession
  + open()
  + update()
  + save()
  + close()
```

如果对象状态很重要，展开时附带生命周期状态；如果方法之间调用关系很复杂，链接到 `function-flow` 文档。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个对象代表什么抽象，负责保护什么边界。

## 对外接口

列出公开方法、参数、返回值、错误、同步/异步性质。

## 生命周期

说明创建、初始化、使用、暂停、销毁或释放资源的顺序。

## 内部状态

说明对象持有什么状态，哪些状态可变，哪些状态只读。

## 协作对象

说明依赖哪些对象，被哪些对象持有或调用。

## 兼容性约束

说明 API 稳定性、版本策略、废弃策略。

## 验证方式

说明契约测试、mock 测试、生命周期测试和错误路径测试。
```

## `data-state`

### 什么模块属于这类

主体是数据结构、状态树、缓存、索引、数据库表、持久化格式或状态迁移。关键设计是数据如何被拥有、读取、修改、同步和迁移。

常见例子：

- 编辑器文档状态 `DocumentState`。
- undo/redo 历史栈。
- 本地缓存、索引、快照存储。
- 文件元数据、同步游标、冲突记录。

### 图形设计

- 语义图形：`cylinder`
- 推荐颜色：`#d97706`
- 图形含义：状态容器 / 数据所有权。
- 默认节点摘要：显示数据名、读写入口、一致性级别。

### 展开方式

默认展开为数据模型和状态流转图：

```text
clean
  -> editing
  -> dirty
  -> saving
  -> clean
```

如果是结构型数据，展开为字段关系图；如果是运行时状态，展开为状态机；如果是存储，展开为读写路径图。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个模块拥有或管理哪些数据。

## 数据模型

列出核心结构、字段、约束、索引和派生数据。

## 状态流转

说明状态集合、迁移条件、非法迁移和恢复路径。

## 读写路径

说明谁可以读、谁可以写、写入如何校验、是否有事务或批处理。

## 一致性与并发

说明缓存一致性、并发写入、冲突处理、锁或版本号。

## 迁移与兼容

说明格式版本、升级、回滚、旧数据兼容策略。

## 验证方式

说明数据结构测试、状态机测试、迁移测试和并发测试。
```

## `event-message`

### 什么模块属于这类

主体是事件、消息、订阅关系、广播通道、异步通知或同步协议。关键设计是事件谁产生、谁消费、顺序是否重要、消息是否可靠。

常见例子：

- 编辑器事件总线。
- 文档变更广播。
- 多端同步消息通道。
- 插件 hook / extension event。

### 图形设计

- 语义图形：`diamond`
- 推荐颜色：`#dc2626`
- 图形含义：事件分发 / 消息路由。
- 默认节点摘要：显示事件族、生产者数量、消费者数量。

### 展开方式

默认展开为事件流图：

```text
producer
  -> event
  -> consumer A
  -> consumer B
```

如果事件有严格时序，展开为时序图；如果事件种类多，展开为事件目录表；如果涉及可靠性，展开为确认、重试和去重路径。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个模块负责哪些事件或消息流。

## 事件目录

列出事件名、payload、生产者、消费者、触发条件。

## 传递语义

说明同步/异步、顺序保证、是否可丢弃、是否可重复。

## 消费规则

说明订阅、取消订阅、过滤、幂等和错误隔离。

## 可靠性

说明重试、确认、去重、死信、超时和降级。

## 与状态关系

说明事件如何改变状态，是否可重放，是否用于审计。

## 验证方式

说明事件契约测试、顺序测试、幂等测试和异常消费者测试。
```

## `config-rule`

### 什么模块属于这类

主体是配置项、规则集、策略表、插件声明、feature flag 或校验 schema。关键设计是默认值、覆盖顺序、优先级、校验和生效时机。

常见例子：

- 编辑器配置系统。
- 渲染规则配置。
- 插件 manifest。
- lint / format 规则集。

### 图形设计

- 语义图形：`document`
- 推荐颜色：`#475569`
- 图形含义：声明式规则 / 配置文档。
- 默认节点摘要：显示配置入口、schema、优先级来源。

### 展开方式

默认展开为规则链和配置表：

```text
default config
  -> project config
  -> user config
  -> runtime override
```

如果规则互斥或有优先级，展开为决策表；如果配置结构复杂，展开为 schema 树。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个模块管理哪些配置或规则。

## 配置结构

列出 schema、字段类型、默认值、必填项和废弃项。

## 合并与优先级

说明默认配置、项目配置、用户配置、运行时覆盖的顺序。

## 校验规则

说明非法配置、错误提示、兼容转换和自动修复。

## 生效时机

说明配置在启动、加载、热更新或运行中何时生效。

## 扩展方式

说明插件或外部模块如何增加配置项或规则。

## 验证方式

说明 schema 测试、兼容测试、优先级测试和错误提示测试。
```

## `resource-file`

### 什么模块属于这类

主体是文件、目录、模板、静态资源、文档格式或资源包。关键设计是文件如何组织、被谁引用、如何加载、如何缓存、如何版本化。

常见例子：

- `*.arch.json` 架构图结构。
- 示例文档和 fixture 集合。
- 模板目录、主题资源包、图标资源。
- 工作区文件结构约定。

### 图形设计

- 语义图形：`folder`
- 推荐颜色：`#0891b2`
- 图形含义：文件集合 / 资源结构。
- 默认节点摘要：显示根路径、主要文件类型、引用方式。

### 展开方式

默认展开为文件树和引用图：

```text
docs/
  architecture-graph-json-format.md
examples/
  system-overview.arch.json
  api-gateway.md
```

如果是文件格式，展开为格式结构；如果是目录约定，展开为文件树；如果引用复杂，展开为引用关系图。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个资源或文件结构服务于哪个运行流程。

## 文件结构

列出目录、文件类型、命名规则和必须存在的文件。

## 格式规则

说明文件内容结构、front matter、字段、代码块或二进制格式。

## 加载与解析

说明加载顺序、路径解析、缓存和错误处理。

## 引用关系

说明文件之间如何引用，是否允许循环引用。

## 版本与迁移

说明格式版本、兼容策略和迁移方式。

## 验证方式

说明 fixture、格式校验、引用校验和渲染快照。
```

## `adapter-io`

### 什么模块属于这类

主体是系统边界和外部 IO。它把内部模型转换成外部协议，或者把外部数据转换成内部模型。关键设计是协议、失败模式、重试、权限和兼容性。

常见例子：

- 文件系统读写适配器。
- 浏览器渲染 / 预览适配器。
- HTTP API client。
- 数据库访问、远程同步服务、第三方 SDK 封装。

### 图形设计

- 语义图形：`port`
- 推荐颜色：`#ea580c`
- 图形含义：外部边界 / IO 端口。
- 默认节点摘要：显示协议、外部目标、失败策略。

### 展开方式

默认展开为边界协议图：

```text
internal model
  -> adapter
  -> external system
```

如果外部协议复杂，展开为请求/响应表；如果失败模式重要，展开为错误映射和重试流程；如果有权限要求，展开为认证和授权路径。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个适配器连接哪个外部边界。

## 外部契约

说明协议、请求、响应、文件格式、权限和限制。

## 内外映射

说明内部模型和外部数据之间如何转换。

## 失败模式

说明超时、重试、限流、权限错误、格式错误和降级行为。

## 兼容性

说明外部版本差异、平台差异和能力探测。

## 可观测性

说明日志、诊断、指标和错误上下文。

## 验证方式

说明 mock、契约测试、集成测试和失败注入测试。
```

## `utility-support`

### 什么模块属于这类

主体是通用支撑能力。它通常不是某个完整业务流程，也不是一个复杂对象，而是一组被其他模块复用的工具函数、日志能力、诊断能力、错误辅助、格式化辅助或环境探测能力。

常见例子：

- `utils`：字符串、路径、集合、时间、对象合并等工具函数。
- `logs`：logger、log level、输出格式、上下文绑定。
- `diagnostics`：warning 收集、错误位置、调试 trace。
- `helpers`：只服务于本项目内部的小型复用函数。

### 图形设计

- 语义图形：`small-rect`
- 推荐颜色：`#64748b`
- 图形含义：共享支撑能力。
- 默认节点摘要：显示工具能力类别、主要调用方、是否允许反向依赖。

### 展开方式

默认展开为工具能力清单：

```text
utility-support
  -> path helpers
  -> string helpers
  -> logger
  -> diagnostics collector
```

展开时重点显示能力分组、稳定性、依赖限制和调用方。不要把每个小函数都画成节点，除非它是架构关键点。

### 文档模板

```md
# <模块名称>

## 模块定位

说明这个支撑模块提供哪些通用能力，服务哪些模块。

## 能力分组

按工具类别列出主要能力，比如路径、字符串、日志、诊断、错误格式化。

## 对外接口

列出稳定可用的函数、对象或常量。

## 依赖限制

说明它可以依赖什么，不允许依赖什么，避免支撑模块反向依赖上层模块。

## 日志与诊断

如果包含 logs 或 diagnostics，说明输出格式、上下文、级别、错误定位。

## 稳定性

说明哪些能力是稳定 API，哪些只是内部 helper。

## 验证方式

说明单元测试、边界值测试、调用方测试和依赖规则检查。
```

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
