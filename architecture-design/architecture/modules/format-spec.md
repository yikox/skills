---
format: arch-module/v0.1
name: Format Spec
described: 定义 .arch.json 架构图文件、对象、组合和关系结构
module_form: atomic
module_kind: resource-file
main_subject: docs/architecture-graph-json-format.md
status: draft
---

# Format Spec

## 模块定位

Format Spec 定义 Architecture Graph JSON 的文件格式。它说明 `*.arch.json` 顶层字段、`objects`、`groups`、`relations` 如何书写。

## 当前内容

- `*.arch.json` 图文件使用 `format: arch-graph/v0.1`。
- 被引用 Markdown 模块文档使用 `name`、`described`、`module_form`、`module_kind`。
- `objects[]` 表示节点。
- `groups[]` 表示组合模块外框。
- `relations[]` 表示有向连线和连线说明。

## 与其他模块关系

Parser Loader 按这个规则解析输入。Graph Model 的对象、组合和关系结构也来自这个规则。
