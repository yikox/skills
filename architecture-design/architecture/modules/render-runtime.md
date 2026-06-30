---
format: arch-module/v0.1
name: 渲染运行时
described: 从入口 .arch.json 生成自包含 HTML/SVG 的运行链路
module_form: composite
main_subject: parse + layout + render
status: draft
---

# 渲染运行时

## 模块定位

渲染运行时是当前项目的执行主体。当前实现集中在 `scripts/render_arch_graph.py`，但内部已经呈现出清晰的解析、模型、布局、渲染和输出边界。

## 子模块清单

| 子模块 | module_kind | 当前实现位置 |
| --- | --- | --- |
| CLI Orchestrator | `interface-object` | `parse_args()`、`main()` |
| Parser Loader | `function-flow` | `load_graph()`、`parse_front_matter()` 等 |
| Graph Model | `data-state` | `Diagram*` dataclass |
| Diagnostics | `utility-support` | `warnings` 列表与告警写入 |
| Layout Engine | `function-flow` | `object_positions()`、`group_bounds()`、`boundary_point()` |
| SVG Renderer | `function-flow` | `render_svg()`、`render_object()`、`render_group()`、`render_relation()`、文档链接包装 |
| HTML Output | `resource-file` | `render_html()` 与输出文件写入 |

## 依赖方向

运行时应保持单向依赖：CLI 调用 Parser Loader，Parser Loader 生成 Graph Model，Layout Engine 和 SVG Renderer 消费 Graph Model，HTML Output 包装渲染结果。节点和组合框跳转由 SVG Renderer 根据 Graph Model 中的 `ref` 生成。
