---
format: arch-module/v0.1
name: Notes Server
described: 多项目架构笔记浏览服务：项目树、图渲染页与模块文档页
module_form: atomic
module_kind: interface-object
main_subject: serve_modular_graph.py
status: draft
---

# Notes Server

## 模块定位

Notes Server 是仿笔记软件的本地只读浏览服务，实现于独立文件 `serve_modular_graph.py`，`import render_modular_graph` 复用解析、布局与 SVG 管线。渲染器本体保持纯 CLI/库，不包含服务逻辑。

## 启动方式

```bash
python3 serve_modular_graph.py --root <项目根目录> --port 8123
```

`--root` 默认当前目录，推荐指向包含多个项目文件夹的项目记忆根目录（每个项目一个文件夹）。服务只绑定 `127.0.0.1`，按需启动、无持久化状态。

## 路由

| 路由 | 行为 |
| --- | --- |
| `GET /` | 项目总览：root 一级子目录即项目，列出各项目的架构图与文档数量 |
| `GET /graph?path=<rel>` | 现场执行 parse → layout → render 返回图页面；warning 显示在页面顶部；节点/组合框链接改写为 `/doc` |
| `GET /doc?path=<rel>` | Markdown 渲染为 HTML 阅读页；文内相对链接 `.md` → `/doc`、`.arch.json` → `/graph` |

每个页面带左侧项目树侧边栏（`.arch.json` 高亮、当前文件标记）。每次请求现场读盘重渲染，改文件后刷新即见。

## 内部组成

- 文件树扫描：`scan_projects()` / `scan_files()`，跳过隐藏目录与 `IGNORED_DIRS`。
- 路径安全：`safe_relative_path()` 把 `path` 参数限制在 root 内，只放行 `.arch.json` 与 `.md`，隐藏路径段一律拒绝。
- Markdown 最小子集转换：`markdown_to_html()`，支持 front matter 元信息卡、标题、列表、表格、代码块、引用、链接、粗斜体；不追求完整 CommonMark，渲染不了的按原文行展示。
- 链接改写：图页通过 `render_svg(..., link_resolver=...)` 注入 URL 改写；文档页通过 `rewrite_relative_url()` 改写文内相对链接。

## 约束

- 仅 Python 3 标准库；`http.server` 属开发级服务器，只定位本地浏览，不承诺并发与生产用途。
- 只读服务：不提供任何写操作。
- 静态 CLI 导出（`render_modular_graph.py <graph> -o <html>`）仍是 baseline 产物的权威形态，本服务不接管该角色。
