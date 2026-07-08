---
name: Shared Assets
described: 技能创建文件时使用的文档模板与示例夹具
module_form: atomic
module_kind: resource-file
main_subject: _shared/assets 模板文件
code_paths: ["en/modular-programming/_shared/assets/**", "en/modular-programming/_shared/examples/**"]
status: implemented
review_status: reviewed
---

# Shared Assets

## Responsibility

拥有文档模板（PM、知识、主设计、模块设计、可选 proposal / ADR、AI 规则片段）与高级图渲染示例夹具（examples 下的模块文档和 `nested-overview.arch.json`）。L2/L3 默认不再依赖长期维护的模块/架构变更模板；这类模板降级为复杂变更的离线审阅载体。

## Public Contract

- 技能以 `../_shared/assets/<template>.md` 引用模板；模板的节标题结构被 audit-checker 部分依赖（如 PM 的 Active Tasks、Modular Design Index 节名）。
- 默认工作流使用 PM、主设计、模块设计与知识模板；可选 proposal 模板只在复杂、跨天或非 git 协作场景下使用。
- examples 是 graph-tooling 的渲染示例输入，不参与运行时。

## Internal Design

- 模板与 storage-schema 的字段定义一一对应；模板改节名属于契约变更。

## Dependencies

| Dependency | Direction | Reason |
| --- | --- | --- |
| workflow-skills | in | 技能创建文件时读取模板 |

## Constraints

- 模板节名与 audit-checker 的 `section()` 查找字符串必须同步。

## Validation

- 用模板新建 PM 文档后跑 checker，不应出现 `[pm] 缺少 Active Tasks 章节`。
