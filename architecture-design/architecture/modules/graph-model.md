---
format: arch-module/v0.1
name: Graph Model
described: 保存 Diagram、对象、组合模块和关系的中间结构
module_form: atomic
module_kind: data-state
main_subject: Diagram dataclasses
status: draft
---

# Graph Model

## 模块定位

Graph Model 是解析后的中间表示。它把 JSON 图结构和模块 Markdown 元信息合并成渲染器可以消费的数据结构。

## 当前数据结构

当前实现位于 `scripts/render_arch_graph.py`：

- `DiagramObject`：对象节点，保留引用文档路径 `ref`，供渲染器读取元信息并生成节点跳转。
- `DiagramGroup`：组合模块外框，保留组合文档路径 `ref`，供渲染器生成组合框跳转。
- `Relation`：两个对象之间的关系，包含连线说明、样式和可选标签偏移。
- `Diagram`：入口文档、元信息、对象、组合、关系和 warnings。

## 交互

Parser Loader 生成 Graph Model。Layout Engine 使用对象和组合关系计算位置。SVG Renderer 使用 Graph Model 渲染节点、组合框、连线和基于 `ref` 的文档链接。
