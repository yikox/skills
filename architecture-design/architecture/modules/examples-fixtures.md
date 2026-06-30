---
format: arch-module/v0.1
name: Examples Fixtures
described: 提供格式、组合模块和渲染行为的输入样例
module_form: atomic
module_kind: resource-file
main_subject: examples/*.arch.json
status: draft
---

# Examples Fixtures

## 模块定位

Examples Fixtures 是项目的可执行样例集合。它用于说明格式写法，也用于人工或自动验证渲染器行为。

## 当前内容

- `examples/system-overview.arch.json`：基础对象和关系示例。
- `examples/tooling-overview.arch.json`：组合模块 `groups` 示例。
- `examples/*.md`：被引用对象或组合模块文档。

## 交互

CLI Orchestrator 可直接使用这些 `.arch.json` 文件作为输入。Parser Loader 读取它们并生成 Graph Model。
