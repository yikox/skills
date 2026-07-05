---
format: arch-module/v0.1
name: Graph Model
described: 保存 Diagram、对象、复合模块、接口和关系端点的中间结构
module_form: atomic
module_kind: data-state
main_subject: Diagram dataclasses
status: draft
---

# Graph Model

## 模块定位

Graph Model 是解析后的中间表示。它把 JSON 图结构和模块 Markdown 元信息合并成渲染器可以消费的数据结构。

## 当前数据结构

当前实现位于 `render_modular_graph.py`：

- `DiagramObject`：对象节点，保留引用文档路径 `ref`，供渲染器读取元信息并生成节点跳转。
- `DiagramGroup`：复合模块外框，保留组合文档路径 `ref`，供渲染器生成组合框跳转。
- `GroupInterface`：复合模块对外接口，记录接口名称、描述和内部 provider 对象。
- `Relation`：两个同层端点之间的关系，端点可以是对象、group 或 `group.interface`，包含关系说明、样式和可选气泡偏移。
- `RouteEndpoint`：渲染阶段的通用端点结构，把对象、group、group interface 统一成可路由的边界框、中心点和 scope。
- `Diagram`：入口文档、元信息、对象、组合、关系、warnings，以及成员到父 group 的包含映射 `parent_by_id`（支持 group 套 group 的树形 scope）。

## 交互

Parser Loader 生成 Graph Model 并校验同层关系。Layout Engine 使用对象、组合和接口关系计算位置。SVG Renderer 使用 Graph Model 渲染节点、组合框、连线和基于 `ref` 的文档链接；接口只作为语义端点参与路由。
