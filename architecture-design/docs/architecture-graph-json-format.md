# Architecture Graph JSON 格式规则草案

状态：draft v0.1。

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
  "format": "arch-graph/v0.1",
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
| `format` | 是 | 当前使用 `arch-graph/v0.1` |
| `id` | 推荐 | 图的稳定 ID |
| `name` | 是 | 图标题 |
| `described` | 是 | 图的简短描述 |
| `objects` | 是 | 节点列表 |
| `groups` | 否 | 组合模块外框列表 |
| `relations` | 否 | 节点之间的有向关系列表 |

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

组合模块表示一个容器外框。

```json
{
  "id": "render-runtime",
  "ref": "../modules/render-runtime.md",
  "contains": ["cli-orchestrator", "parser-loader", "graph-model"]
}
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | 图内唯一 group ID |
| `ref` | 推荐 | 指向组合模块 Markdown 文档，该文档建议 `module_form: composite`；渲染后也是组合框点击跳转目标 |
| `contains` | 是 | 属于该组合模块的对象 ID 列表 |
| `at` | 否 | 容器位置；缺省时根据内部对象自动计算 |
| `name` | 否 | 覆盖模块文档的 `name` |
| `described` | 否 | 覆盖模块文档的 `described` |

## Relation

关系表示两个对象之间的有向连接。

```json
{
  "from": "parser-loader",
  "to": "graph-model",
  "described": "生成 Diagram IR",
  "style": "solid",
  "label_offset": [0, -18]
}
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `from` | 是 | 起点对象 ID |
| `to` | 是 | 终点对象 ID |
| `described` | 是 | 关系说明，默认不直接显示，鼠标悬停到关系线时以气泡显示 |
| `style` | 否 | `solid` 或 `dashed`，默认 `solid` |
| `label_offset` | 否 | hover 气泡相对自动锚点的像素偏移 `[x, y]`，用于微调气泡位置 |

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
- 分组、依赖、图上布局：由人维护 JSON，因为这是架构表达，不应完全由代码目录推断。
- 校验：工具检查 `ref` 是否存在、关系端点是否存在、group 是否包含未知对象、重复 ID、缺失 `name/described`。
- 渲染：工具读取 JSON，再读取 Markdown front matter，生成 HTML/SVG；节点和组合框使用 `ref` 生成文档跳转链接；关系线使用折线路由，说明文本通过 hover 气泡查看；大型图可以通过更宽松的布局坐标和 `label_offset` 微调阅读性。

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
