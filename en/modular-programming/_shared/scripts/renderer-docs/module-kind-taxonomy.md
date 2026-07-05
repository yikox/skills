---
format: arch-module/v0.1
name: Module Kind Taxonomy
described: 定义底层模块分类、组合形态、图形和颜色映射
module_form: atomic
module_kind: config-rule
main_subject: ../../references/module-kind-classification.md
status: draft
---

# Module Kind Taxonomy

## 模块定位

Module Kind Taxonomy 定义模块文档如何声明自身的表达类型。它是渲染器选择默认图形和颜色的语义来源。

## 当前内容

底层分类包括 `layout-style`、`function-flow`、`interface-object`、`data-state`、`event-message`、`config-rule`、`resource-file`、`adapter-io`、`utility-support`。

组合形态通过 `module_form: composite` 表达，渲染为包住内部对象的外框。复合模块对外协作时，可在图 JSON 的 `groups[].interfaces[]` 声明公开接口，但接口不是新的 `module_kind`，它只是复合模块边界上的关系端点。

## 与其他模块关系

Parser Loader 读取被引用文档的 `module_kind` 和 `module_form`。SVG Renderer 根据 `module_kind` 使用对应图形和颜色。
