---
format: arch-module/v0.1
name: HTML Output
described: 将 SVG、标题、简介和 warnings 包装成自包含 HTML
module_form: atomic
module_kind: resource-file
main_subject: render_html()
status: draft
---

# HTML Output

## 模块定位

HTML Output 是最终展示产物生成模块。它把 SVG 图、文档标题、简介和 warnings 区块包装成可直接打开的 HTML。

## 当前实现

当前实现位于 `scripts/render_arch_graph.py`：

- `render_html()` 生成完整 HTML。
- 内联 CSS 提供基础视觉样式和可点击节点/组合框的 hover 状态。
- warnings 会显示在图下方。

## 交互

SVG Renderer 向 HTML Output 提供已经带文档链接的 SVG 字符串。Diagnostics 提供 warnings。CLI Orchestrator 负责把 HTML 写入目标路径。
