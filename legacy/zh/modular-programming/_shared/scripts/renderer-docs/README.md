# 渲染器内部架构

`render_modular_graph.py`（架构图渲染器）和 `serve_modular_graph.py`
（本地架构笔记浏览器）的模块文档。
修改任一脚本前请先阅读相关文档。

| 文档 | 涵盖内容 |
| --- | --- |
| format-spec.md | `.arch.json` 输入契约 |
| parser-loader.md | JSON 加载与校验 |
| graph-model.md | 内存中的图模型 |
| rules-layer.md | 关系/层级校验规则 |
| module-kind-taxonomy.md | 模块分类语义与颜色 |
| layout-engine.md | 布局计算 |
| svg-renderer.md | SVG 输出 |
| html-output.md | HTML 包装输出 |
| render-runtime.md | 端到端的解析 + 布局 + 渲染管线 |
| cli-orchestrator.md | CLI 入口与管线编排 |
| diagnostics.md | warning 与错误报告 |
| notes-server.md | 本地多项目浏览服务（serve_modular_graph.py） |
