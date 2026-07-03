---
format: arch-module/v0.1
name: Parser Loader
described: 读取 arch.json 图结构和 Markdown 模块 front matter
module_form: atomic
module_kind: function-flow
main_subject: load_graph()
status: draft
---

# Parser Loader

## 模块定位

Parser Loader 是从 JSON 图结构和 Markdown 模块文档到 Graph Model 的转换流程。它读取入口 `*.arch.json`，解析 `objects`、`groups`、`relations`，并加载被引用模块文档的 front matter。

## 当前实现

当前实现位于 `render_modular_graph.py`：

- `read_text()` 读取文件。
- `parse_key_values()` 解析轻量 `key: value`。
- `parse_front_matter()` 读取 front matter。
- `load_document_meta()` 加载被引用文档元信息。
- `load_graph()` 解析对象、组合和关系。
- `build_containment()` 建立成员到父 group 的包含映射，校验未知成员、多父、自包含并拆除成环链接。
- `descendant_object_ids()` 展开 group 的 `contains` 子树，用于接口 provider 校验。
- `relation_endpoint_scope()` 按包含树返回端点 scope（对象/group 取父 group，interface 与所属 group 同 scope）。

## 约束

当前 parser 是原型级实现：front matter 不是完整 YAML，但图结构本身已经是标准 JSON。后续如果模块 front matter 复杂化，应引入正式 YAML parser。
