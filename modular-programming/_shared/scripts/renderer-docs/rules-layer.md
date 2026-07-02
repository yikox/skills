---
format: arch-module/v0.1
name: 规则层
described: 定义 Architecture Graph JSON 的输入契约和模块分类规则
module_form: composite
main_subject: format spec + module taxonomy
status: draft
---

# 规则层

## 模块定位

规则层是渲染器的输入契约来源。它不直接执行渲染，而是定义 `*.arch.json` 如何描述对象、复合模块、复合模块接口、同层关系和模块分类。

## 子模块清单

| 子模块 | module_kind | 说明 |
| --- | --- | --- |
| Format Spec | `resource-file` | 定义文件后缀、`objects`、`groups`、`interfaces`、`relations` 和同层关系规则 |
| Module Kind Taxonomy | `config-rule` | 定义 `module_kind`、`module_form`、图形、颜色和展开方式 |

## 内部关系

Format Spec 负责语法结构和关系 scope 约束，Module Kind Taxonomy 负责模块语义。Parser Loader 同时读取这两类信息。
