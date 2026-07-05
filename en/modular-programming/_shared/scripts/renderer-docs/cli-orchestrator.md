---
format: arch-module/v0.1
name: CLI Orchestrator
described: 接收入口 .arch.json 和输出路径，编排解析与渲染
module_form: atomic
module_kind: interface-object
main_subject: parse_args() + main()
status: draft
---

# CLI Orchestrator

## 模块定位

CLI Orchestrator 是命令行入口。它负责读取参数、检查入口后缀、调用解析和渲染流程，并写出 HTML 文件。

## 当前实现

当前实现位于 `render_modular_graph.py`：

- `parse_args()` 定义输入文件和 `--output`。
- `main()` 检查 `.arch.json` 后缀。
- `main()` 调用 `load_graph()` 和 `render_html()`。
- `main()` 创建输出目录并写出 HTML。

## 交互

CLI Orchestrator 接收 Examples Fixtures 或用户提供的 `.arch.json` 文件，向 Parser Loader 传入路径，最后决定 Rendered Artifacts 的输出位置。
