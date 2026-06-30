---
format: arch-module/v0.1
name: Rendered Artifacts
described: 保存渲染器生成的 HTML 展示文件
module_form: atomic
module_kind: resource-file
main_subject: dist/*.html
status: draft
---

# Rendered Artifacts

## 模块定位

Rendered Artifacts 是渲染结果目录。它保存由 CLI Orchestrator 和 HTML Output 生成的 HTML 文件。

## 当前内容

- `dist/system-overview.html`
- `dist/tooling-overview.html`
- `dist/current-project-architecture.html`

## 约束

这些文件是生成结果，不是格式规则源。需要以 `*.arch.json` 和模块文档作为可维护源文件。
