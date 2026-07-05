---
format: arch-module/v0.1
name: Diagnostics
described: 收集解析、引用和关系校验过程中的 warning
module_form: atomic
module_kind: utility-support
main_subject: warnings collector
status: draft
---

# Diagnostics

## 模块定位

Diagnostics 是轻量诊断支撑模块。它收集解析过程中的可恢复问题，并把这些问题交给 HTML Output 展示。

## 当前内容

当前实现使用 `warnings: List[str]`：

- 引用文件不存在。
- 引用文件缺少 `name` 或 `described`。
- 对象 ID 重复。
- 组合模块缺少 `contains`。
- 组合模块包含未知对象。
- 关系引用未知端点。

## 后续边界

如果项目继续扩大，Diagnostics 应从普通字符串升级为结构化诊断对象，包含级别、位置、来源文件和修复建议。
