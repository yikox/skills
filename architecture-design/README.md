# Architecture Graph

这是一个用于架构设计、架构修改和架构图渲染的 Codex skill，同时包含 JSON 图结构草案和最小渲染器。

当前约定：

- `SKILL.md` 定义 `$architecture-design` 的触发条件、工作流和质量检查。
- `agents/openai.yaml` 定义 Codex UI 中的展示信息和默认提示。
- 模块文档使用 Markdown，front matter 描述 `name`、`described`、`module_kind`、`module_form`。
- 图结构使用 `*.arch.json`，描述 `objects`、`groups`、`relations` 和布局坐标。
- 渲染器读取 JSON 图结构，再读取被引用 Markdown 模块文档的元信息。
- 渲染器是零依赖 Python 脚本，会输出一个自包含 HTML 文件；带 `ref` 的节点和组合框可点击跳转到对应 Markdown 文档。

## 使用

```bash
python3 scripts/render_arch_graph.py examples/system-overview.arch.json -o dist/system-overview.html
python3 scripts/render_arch_graph.py examples/tooling-overview.arch.json -o dist/tooling-overview.html
python3 scripts/render_arch_graph.py architecture/graphs/current-project.arch.json -o dist/current-project-architecture.html
python3 scripts/render_arch_graph.py architecture/graphs/current-project.arch.json -o dist/current-project-architecture.html --svg-output dist/current-project-architecture.svg
```

然后在浏览器中打开 `dist/current-project-architecture.html`，点击节点或组合框可查看对应模块文档。

## 文件

- `SKILL.md`: architecture-design skill 的主入口。
- `agents/openai.yaml`: Codex UI 元数据。
- `docs/architecture-graph-json-format.md`: JSON 图结构规则草案。
- `docs/module-kind-classification.md`: 模块架构表达类型分类草案。
- `architecture/main-design.md`: 当前项目架构说明。
- `architecture/graphs/current-project.arch.json`: 当前项目架构图源文件。
- `architecture/modules/*.md`: 当前项目模块文档。
- `examples/*.arch.json`: 可渲染示例图。
- `scripts/render_arch_graph.py`: JSON-only 最小渲染器。
