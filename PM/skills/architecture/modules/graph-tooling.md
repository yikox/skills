---
name: Graph Tooling
described: 架构图 JSON 的渲染器与本地预览服务
module_form: atomic
module_kind: function-flow
main_subject: render_modular_graph.py
code_paths: ["modular-programming/_shared/scripts/**"]
status: implemented
review_status: reviewed
---

# Graph Tooling

## Responsibility

拥有 `render_modular_graph.py`（把 `*.arch.json` 渲染为 HTML/SVG）、`serve_modular_graph.py`（本地预览与笔记服务）及 renderer-docs 内部文档。

## Public Contract

- CLI：`python3 render_modular_graph.py <input.arch.json> [-o out.html] [--svg-output out.svg]`
- 输入契约：shared-references 中 `architecture-graph-json-format.md` 定义的 `arch-graph/v0.3`（兼容 v0.1/v0.2）。
- 节点 `ref` 指向模块 Markdown，渲染器读取其 front matter 决定形状与颜色。

## Internal Design

- 见 `modular-programming/_shared/scripts/renderer-docs/` 内部文档。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | in | modular-architecture 技能触发渲染 |

## Constraints

- 仅用 Python 3 标准库。

## Validation

- `python3 modular-programming/_shared/scripts/render_modular_graph.py modular-programming/_shared/examples/nested-overview.arch.json -o /tmp/t.html` 退出码 0。

## Review Notes

- Review status: reviewed（2026-07-03 基线与代码核对一致）
