---
format: arch-module/v0.1
name: Format Spec
described: 定义 .arch.json 架构图文件、对象、复合模块接口和同层关系结构
module_form: atomic
module_kind: resource-file
main_subject: ../../references/architecture-graph-json-format.md
status: draft
---

# Format Spec

## 模块定位

Format Spec 定义 Architecture Graph JSON 的文件格式。它说明 `*.arch.json` 顶层字段、`objects`、`groups`、`groups[].interfaces`、`relations` 如何书写。

## 当前内容

- `*.arch.json` 图文件使用 `format: arch-graph/v0.3`，渲染器兼容读取 v0.1 / v0.2。
- 被引用 Markdown 模块文档使用 `name`、`described`、`module_form`、`module_kind`。
- `objects[]` 表示节点。
- `groups[]` 表示复合模块外框；`contains` 成员可以是对象或其他 group（多层嵌套），包含关系必须成森林（无环、单父、不含自身）。
- `groups[].interfaces[]` 表示复合模块对外接口，端点写作 `<group-id>.<interface-id>`，provider 允许来自 `contains` 子树。
- `relations[]` 表示同层端点之间的有向连线和关系说明；scope 随包含树递归（成员属于其父 group 的 scope）。

## 与其他模块关系

Parser Loader 按这个规则解析输入。Graph Model 的对象、复合模块、接口、关系端点和同层 scope 约束也来自这个规则。
