# Architecture Graph JSON 格式规则草案

状态：draft v0.3。

这份文档定义机器可读的架构图结构。它取代把图结构写进 `.mdx` fenced block 的做法。

核心分工：

- Markdown 模块文档：写给人读，保存模块职责、接口、流程、约束和 front matter。
- `*.arch.json` 图结构：写给工具读，保存对象、组合、关系和布局。
- HTML/SVG 输出：由渲染器根据 JSON 图结构和 Markdown 模块元信息生成。

## 文件位置

建议放在：

```text
architecture/graphs/<graph-id>.arch.json
```

模块文档放在：

```text
architecture/modules/<module-id>.md
```

## 顶层结构

```json
{
  "format": "arch-graph/v0.3",
  "id": "current-project",
  "name": "Architecture Graph 项目架构",
  "described": "当前项目的规则层、运行时层、示例与产物层关系",
  "objects": [],
  "groups": [],
  "relations": []
}
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `format` | 是 | 当前使用 `arch-graph/v0.3`；渲染器兼容读取 `arch-graph/v0.1` / `v0.2` |
| `id` | 推荐 | 图的稳定 ID |
| `name` | 是 | 图标题 |
| `described` | 是 | 图的简短描述 |
| `objects` | 是 | 节点列表 |
| `groups` | 否 | 复合模块外框与对外接口列表 |
| `relations` | 否 | 同层模块端点之间的有向关系列表 |

## Object

对象表示图中的一个模块节点。

```json
{
  "id": "parser-loader",
  "ref": "../modules/parser-loader.md",
  "at": [1, 2]
}
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | 图内唯一对象 ID |
| `ref` | 推荐 | 指向模块 Markdown 文档，路径相对 JSON 文件；渲染后也是节点点击跳转目标 |
| `at` | 否 | 网格坐标 `[列, 行]` |
| `shape` | 否 | 手动覆盖图形 |
| `stroke` | 否 | 手动覆盖边框色 |
| `fill` | 否 | 手动覆盖填充色 |
| `name` | 否 | 覆盖模块文档的 `name` |
| `described` | 否 | 覆盖模块文档的 `described` |

默认情况下，渲染器读取 `ref` 指向 Markdown 文档的 front matter，并根据 `module_kind` 决定图形和颜色。HTML/SVG 输出中，带 `ref` 的对象节点会链接到该 Markdown 文档。

## Group

复合模块表示一个容器外框。它可以只作为视觉边界，也可以声明对外接口，让外部关系连接到复合模块边界，而不是直接连接内部子模块。

`contains` 的成员可以是对象 ID，也可以是其他 group ID，因此复合模块支持多层嵌套（group 套 group）。包含关系必须构成森林：每个成员至多有一个父 group，不允许成环、不允许包含自身；违反时渲染器给出 warning 并忽略成环的父级链接。

一个复合模块始终渲染为一个完整边界框，嵌套的子 group 外框完整地画在父 group 外框内部（父先画、子后画）。渲染器不会把跨行或包含很多子模块的复合模块拆成多个视觉分片；如果边界过大或内部过密，应在设计层拆分层级、调整布局或重新定义复合模块范围。

```json
{
  "id": "render-runtime",
  "ref": "../modules/render-runtime.md",
  "contains": ["cli-orchestrator", "parser-loader", "graph-model"],
  "interfaces": [
    {
      "id": "graph-input",
      "name": "图输入",
      "described": "读取 JSON 图结构和 Markdown 模块元信息",
      "provided_by": ["parser-loader", "graph-model"]
    }
  ]
}
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | 图内唯一 group ID |
| `ref` | 推荐 | 指向组合模块 Markdown 文档，该文档建议 `module_form: composite`；渲染后也是组合框点击跳转目标 |
| `contains` | 是 | 属于该组合模块的成员 ID 列表，成员可以是对象或其他 group |
| `interfaces` | 否 | 复合模块对外接口列表，接口端点写作 `<group-id>.<interface-id>` |
| `at` | 否 | 容器位置；缺省时根据内部对象自动计算 |
| `name` | 否 | 覆盖模块文档的 `name` |
| `described` | 否 | 覆盖模块文档的 `described` |

### Group Interface

接口表示复合模块对外暴露的能力入口，不是独立子模块，也不是可见节点。接口由内部子模块实现，但外部关系应该连接到接口端点；渲染时接口端点会收敛到复合模块完整边界，并按另一端位置就近选择上、下、左、右连接点。

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | group 内唯一接口 ID，不能包含 `.`；完整端点为 `<group-id>.<interface-id>` |
| `name` | 否 | 接口显示名称 |
| `described` | 否 | 接口简短描述 |
| `provided_by` | 否 | 实现该接口的内部对象 ID 列表；应属于该 group 的 `contains` 子树（含嵌套 group 内的对象） |

## Relation

关系表示两个同层端点之间的有向连接。端点可以是对象、复合模块，或者复合模块接口。

```json
{
  "from": "rules-layer.graph-format",
  "to": "render-runtime.graph-input",
  "described": "定义架构图输入契约",
  "style": "solid",
  "label_offset": [0, -18]
}
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `from` | 是 | 起点端点：对象 ID、group ID 或 `<group-id>.<interface-id>` |
| `to` | 是 | 终点端点：对象 ID、group ID 或 `<group-id>.<interface-id>` |
| `described` | 是 | 关系说明，默认不直接显示，鼠标悬停到关系线时以气泡显示 |
| `kind` | 否 | 关系类型，见下方封闭词表，默认 `uses` |
| `style` | 否 | `solid` 或 `dashed`，默认 `solid`，语义见下 |
| `label_offset` | 否 | hover 气泡相对自动锚点的像素偏移 `[x, y]`，用于微调气泡位置 |

## 关系语义

**箭头 = 依赖方向**：`A -> B` 读作"A 使用/依赖 B"。数据流向与依赖方向不一致时，把流向写进 `described`，不要反转箭头。

`kind` 封闭词表（五个，不扩展）：

| kind | 含义 |
| --- | --- |
| `uses` | 泛化使用/调用（默认） |
| `reads` | 读取对方的数据、配置或规则 |
| `writes` | 写入对方管理的数据或产物 |
| `triggers` | 事件、消息或调度触发 |
| `distributes` | 打包、分发或同步对方内容 |

`style` 语义：`solid` = 运行时依赖；`dashed` = 非运行时依赖（构建、验证夹具、同步约定）。

**维护图时，图是模块间关系的权威可视化来源**：模块文档的 Dependencies 表必须是图中该模块关系的子集（补充原因说明）。表里出现图中没有的关系时，补图或删表行。未维护图的项目以 `main-design.md` 和模块文档为默认事实来源。

## 同层关系规则

关系的核心约束是同层连接，而不是强制所有关系都发生在复合模块之间。scope 随包含关系构成树：

- 没有父 group 的对象、group 属于顶层 scope；group 的 interface 与该 group 属于同一个 scope。
- 有父 group 的成员（对象或嵌套 group）属于父 group 的内部 scope。
- 同一个 scope 内的端点可以直接相互连接：顶层端点互连，或同一个 group 直接包含的对象和子 group 互连。
- 外部端点不应直接连接到某个 group 内部（任意深度）的成员；应连接到该 group 或 `group.interface`。
- 不同 group 的内部成员不应直接连接；应把关系提升到它们最近的共同父层级，或经由各自的 group interface。

渲染器会对跨 scope 的 child-object 关系给出 warning。warning 不会阻止渲染，但表示图的模块边界表达不清晰。

关系渲染会体现层级差异：

- 顶层 scope 的关系，包括顶层对象、group 和 `group.interface` 之间的关系，使用更粗的箭头。
- 任何 group 内部（含嵌套层级）的同层实现关系，使用更细的箭头。
- `group.interface` 不显示为文字小框；接口名称保留在 JSON 语义和文档中，图面只显示模块边界之间的连接。

## 管理方式

推荐工具链：

```text
architecture/modules/*.md
  -> 扫描 front matter
  -> 生成或同步 objects

architecture/graphs/*.arch.json
  -> 人工维护 groups / relations / layout
  -> validate
  -> render
```

职责分工：

- 模块增删：优先从 `architecture/modules/*.md` 扫描同步。
- 分组、接口、依赖、图上布局：由人维护 JSON，因为这是架构表达，不应完全由代码目录推断。
- 校验：工具检查 `ref` 是否存在、关系端点是否存在、group 是否包含未知成员、包含关系是否成森林（无环、单父、不含自身）、接口 provider 是否属于 `contains` 子树、重复 ID、缺失 `name/described`，以及 relation 是否跨越不同 scope。
- 渲染：工具读取 JSON，再读取 Markdown front matter，生成 HTML/SVG；节点和组合框使用 `ref` 生成文档跳转链接；group interface 作为语义端点收敛到复合模块边界；外层关系使用粗箭头，内部关系使用细箭头；关系线使用折线路由，说明文本通过 hover 气泡查看；大型图可以通过更宽松的布局坐标和 `label_offset` 微调阅读性。

## 与旧 `.mdx` 图源的关系

旧 `.mdx` 图源是早期实验格式，当前设计阶段已废弃。新图只使用 `*.arch.json`。

迁移规则：

- `object` block -> `objects[]`
- `group` block -> `groups[]`
- `relation` block -> `relations[]`
- 入口 front matter -> JSON 顶层 `name` / `described`

## 当前建议

长期维护采用：

```text
Markdown 管模块文档
JSON 管图结构
HTML/SVG 管展示输出
```
