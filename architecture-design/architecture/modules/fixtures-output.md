---
format: arch-module/v0.1
name: 示例与产物层
described: 提供可验证输入样例和渲染输出文件
module_form: composite
main_subject: examples + dist
status: draft
---

# 示例与产物层

## 模块定位

示例与产物层用于验证格式规则和渲染器行为。它既是人工检查入口，也是未来自动测试的 fixture 来源。

## 子模块清单

| 子模块 | module_kind | 说明 |
| --- | --- | --- |
| Examples Fixtures | `resource-file` | 提供 `.arch.json` 示例和被引用模块文档 |
| Rendered Artifacts | `resource-file` | 保存渲染器生成的 HTML |

## 约束

`dist/*.html` 是生成产物，不应作为源规则。源事实以 `docs/`、`architecture/`、`examples/` 和 `scripts/` 为准。
