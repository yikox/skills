---
name: Graph Tooling
described: 高级架构图 JSON 的渲染器与本地预览服务
module_form: atomic
module_kind: function-flow
main_subject: render_modular_graph.py
code_paths: ["en/modular-programming/_shared/scripts/**"]
status: implemented
review_status: reviewed
---

# Graph Tooling

## Responsibility

拥有高级可视化能力：`render_modular_graph.py`（把 `*.arch.json` 渲染为 HTML/SVG）、`serve_modular_graph.py`（本地预览与笔记服务）及 renderer-docs 内部文档。默认 AI 工作流不要求项目创建或维护图。

## Public Contract

- CLI：`python3 render_modular_graph.py <input.arch.json> [-o out.html] [--svg-output out.svg]`
- 输入契约：shared-references 中 `architecture-graph-json-format.md` 定义的 `arch-graph/v0.3`（兼容 v0.1/v0.2）。
- 节点 `ref` 指向模块 Markdown，渲染器读取其 front matter 决定形状与颜色。

## Internal Design

- 见 `en/modular-programming/_shared/scripts/renderer-docs/` 内部文档。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | in | modular-architecture 高级可视化模式触发渲染 |

## Constraints

- 仅用 Python 3 标准库。

## Validation

- `python3 en/modular-programming/_shared/scripts/render_modular_graph.py en/modular-programming/_shared/examples/nested-overview.arch.json -o /tmp/t.html` 退出码 0。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
