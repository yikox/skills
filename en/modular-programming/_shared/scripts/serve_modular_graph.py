#!/usr/bin/env python3
"""Local architecture-notes browser: serve projects, render .arch.json graphs, read module docs."""

from __future__ import annotations

import argparse
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import parse_qs, quote, urlsplit

import render_modular_graph as renderer

IGNORED_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".obsidian", ".idea", ".vscode"}
SERVED_SUFFIXES = (".arch.json", ".md")
ROOT_PROJECT_LABEL = "（根目录）"


# ---------- filesystem tree ----------


def is_served_file(path: Path) -> bool:
    return path.name.endswith(SERVED_SUFFIXES[0]) or path.name.endswith(SERVED_SUFFIXES[1])


def scan_files(directory: Path) -> List[Path]:
    results: List[Path] = []
    for entry in sorted(directory.iterdir(), key=lambda item: item.name):
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            if entry.name in IGNORED_DIRS:
                continue
            results.extend(scan_files(entry))
        elif entry.is_file() and is_served_file(entry):
            results.append(entry)
    return results


def scan_projects(root: Path) -> List[Tuple[str, List[Path]]]:
    """Return (project name, files) pairs: first-level dirs plus root-level files."""
    projects: List[Tuple[str, List[Path]]] = []
    root_files = [
        entry
        for entry in sorted(root.iterdir(), key=lambda item: item.name)
        if entry.is_file() and is_served_file(entry) and not entry.name.startswith(".")
    ]
    if root_files:
        projects.append((ROOT_PROJECT_LABEL, root_files))
    for entry in sorted(root.iterdir(), key=lambda item: item.name):
        if not entry.is_dir() or entry.name.startswith(".") or entry.name in IGNORED_DIRS:
            continue
        files = scan_files(entry)
        if files:
            projects.append((entry.name, files))
    return projects


def safe_relative_path(root: Path, raw: str) -> Optional[Path]:
    if not raw:
        return None
    candidate = (root / raw).resolve()
    try:
        rel = candidate.relative_to(root)
    except ValueError:
        return None
    if any(part.startswith(".") or part in IGNORED_DIRS for part in rel.parts):
        return None
    if not candidate.is_file() or not is_served_file(candidate):
        return None
    return candidate


# ---------- URL helpers ----------


def file_url(root: Path, path: Path) -> Optional[str]:
    try:
        rel = path.resolve().relative_to(root)
    except ValueError:
        return None
    encoded = quote(rel.as_posix())
    if path.name.endswith(".arch.json"):
        return f"/graph?path={encoded}"
    if path.name.endswith(".md"):
        return f"/doc?path={encoded}"
    return None


def rewrite_relative_url(root: Path, current_file: Path, url: str) -> Optional[str]:
    if re.match(r"^[a-z][a-z0-9+.-]*:", url) or url.startswith(("#", "/")):
        return url
    target = (current_file.parent / url.split("#", 1)[0]).resolve()
    if not target.is_file():
        return None
    return file_url(root, target)


# ---------- minimal Markdown rendering ----------

INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def render_inline(text: str, root: Path, current_file: Path) -> str:
    escaped = renderer.escape(text)

    def replace_link(match: "re.Match[str]") -> str:
        label, url = match.group(1), match.group(2)
        resolved = rewrite_relative_url(root, current_file, url)
        if resolved is None:
            return f"{label}<span class=\"dead-link\">({url})</span>"
        return f'<a href="{renderer.escape(resolved)}">{label}</a>'

    escaped = LINK_RE.sub(replace_link, escaped)
    escaped = INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)
    escaped = BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = ITALIC_RE.sub(r"<em>\1</em>", escaped)
    return escaped


def render_meta_card(meta: Dict[str, str]) -> str:
    if not meta:
        return ""
    rows = "\n".join(
        f"<tr><th>{renderer.escape(key)}</th><td>{renderer.escape(value)}</td></tr>"
        for key, value in meta.items()
    )
    return f'<table class="meta-card">{rows}</table>'


def flush_paragraph(buffer: List[str], output: List[str], root: Path, current_file: Path) -> None:
    if buffer:
        output.append(f"<p>{render_inline(' '.join(buffer), root, current_file)}</p>")
        buffer.clear()


def flush_list(items: List[str], output: List[str], ordered: bool) -> None:
    if items:
        tag = "ol" if ordered else "ul"
        output.append(f"<{tag}>" + "".join(f"<li>{item}</li>" for item in items) + f"</{tag}>")
        items.clear()


def markdown_to_html(text: str, root: Path, current_file: Path) -> str:
    meta, body = renderer.parse_front_matter(text)
    output: List[str] = [render_meta_card(meta)]
    paragraph: List[str] = []
    list_items: List[str] = []
    list_ordered = False
    table_rows: List[str] = []
    code_lines: Optional[List[str]] = None

    def close_blocks() -> None:
        flush_paragraph(paragraph, output, root, current_file)
        flush_list(list_items, output, list_ordered)
        flush_table()

    def flush_table() -> None:
        if not table_rows:
            return
        html_rows: List[str] = []
        for index, row in enumerate(table_rows):
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if index == 1 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells if cell):
                continue
            tag = "th" if index == 0 else "td"
            html_rows.append(
                "<tr>" + "".join(f"<{tag}>{render_inline(cell, root, current_file)}</{tag}>" for cell in cells) + "</tr>"
            )
        output.append(f'<table class="doc-table">{"".join(html_rows)}</table>')
        table_rows.clear()

    for line in body.splitlines():
        stripped = line.strip()
        if code_lines is not None:
            if stripped.startswith("```"):
                code_text = "\n".join(code_lines)
                output.append(f"<pre><code>{renderer.escape(code_text)}</code></pre>")
                code_lines = None
            else:
                code_lines.append(line)
            continue
        if stripped.startswith("```"):
            close_blocks()
            code_lines = []
            continue
        if not stripped:
            close_blocks()
            continue
        if stripped.startswith("|"):
            flush_paragraph(paragraph, output, root, current_file)
            flush_list(list_items, output, list_ordered)
            table_rows.append(stripped)
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            close_blocks()
            level = len(heading.group(1))
            output.append(f"<h{level}>{render_inline(heading.group(2), root, current_file)}</h{level}>")
            continue
        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        numbered = re.match(r"^\d+[.)]\s+(.*)$", stripped)
        if bullet or numbered:
            flush_paragraph(paragraph, output, root, current_file)
            flush_table()
            ordered = bool(numbered)
            if list_items and list_ordered != ordered:
                flush_list(list_items, output, list_ordered)
            list_ordered = ordered
            content = (numbered or bullet).group(1)
            list_items.append(render_inline(content, root, current_file))
            continue
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            close_blocks()
            output.append("<hr>")
            continue
        if stripped.startswith(">"):
            close_blocks()
            output.append(f"<blockquote>{render_inline(stripped.lstrip('> '), root, current_file)}</blockquote>")
            continue
        flush_list(list_items, output, list_ordered)
        flush_table()
        paragraph.append(stripped)

    if code_lines is not None:
        code_text = "\n".join(code_lines)
        output.append(f"<pre><code>{renderer.escape(code_text)}</code></pre>")
    close_blocks()
    return "\n".join(part for part in output if part)


# ---------- page shell ----------

PAGE_CSS = """
  * { box-sizing: border-box; }
  body {
    margin: 0;
    display: flex;
    min-height: 100vh;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    color: #1e293b;
    background: #eef2f7;
  }
  nav.sidebar {
    width: 320px;
    flex: none;
    height: 100vh;
    position: sticky;
    top: 0;
    overflow-y: auto;
    background: #0f172a;
    color: #cbd5e1;
    padding: 18px 14px 32px;
  }
  nav.sidebar h1 { font-size: 16px; color: #f8fafc; margin: 0 0 4px; }
  nav.sidebar .root-path { font-size: 11px; color: #64748b; word-break: break-all; margin-bottom: 14px; }
  nav.sidebar details { margin-bottom: 6px; }
  nav.sidebar summary {
    cursor: pointer;
    font-weight: 700;
    font-size: 14px;
    color: #e2e8f0;
    padding: 4px 6px;
    border-radius: 6px;
  }
  nav.sidebar summary:hover { background: #1e293b; }
  nav.sidebar ul { list-style: none; margin: 2px 0 8px; padding-left: 12px; }
  nav.sidebar li { margin: 1px 0; }
  nav.sidebar a {
    display: block;
    color: #94a3b8;
    text-decoration: none;
    font-size: 12.5px;
    padding: 2px 6px;
    border-radius: 5px;
    word-break: break-all;
  }
  nav.sidebar a:hover { color: #f1f5f9; background: #1e293b; }
  nav.sidebar a.graph-file { color: #7dd3fc; font-weight: 600; }
  nav.sidebar a.active { background: #334155; color: #ffffff; }
  main.content { flex: 1; min-width: 0; padding: 28px 32px 48px; }
  main.content header h1 { margin: 0 0 6px; font-size: 26px; }
  main.content header p { margin: 0 0 18px; color: #64748b; line-height: 1.6; }
  .canvas {
    overflow: auto;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 18px 55px rgba(30, 41, 59, 0.12);
  }
  .diagram { display: block; width: 100%; height: auto; }
  .warnings {
    margin: 0 0 18px;
    padding: 12px 14px;
    border-left: 4px solid #fb923c;
    background: #fff7ed;
    border-radius: 6px;
  }
  .warnings h2 { margin: 0 0 8px; font-size: 15px; }
  .warnings ul { margin: 0; padding-left: 20px; }
  article.doc {
    max-width: 880px;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 30px 36px 40px;
    line-height: 1.7;
  }
  article.doc h1, article.doc h2, article.doc h3 { line-height: 1.3; }
  article.doc h1 { font-size: 24px; }
  article.doc h2 { font-size: 19px; margin-top: 28px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }
  article.doc code {
    background: #f1f5f9;
    border-radius: 4px;
    padding: 1px 5px;
    font-size: 0.9em;
  }
  article.doc pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 14px 16px;
    border-radius: 8px;
    overflow-x: auto;
  }
  article.doc pre code { background: none; padding: 0; color: inherit; }
  article.doc table { border-collapse: collapse; margin: 12px 0; width: 100%; }
  article.doc th, article.doc td { border: 1px solid #cbd5e1; padding: 6px 10px; text-align: left; font-size: 14px; }
  article.doc th { background: #f8fafc; }
  article.doc table.meta-card { max-width: 560px; font-size: 13px; margin-bottom: 20px; }
  article.doc table.meta-card th { width: 130px; color: #64748b; font-weight: 600; }
  article.doc blockquote { margin: 12px 0; padding: 6px 14px; border-left: 4px solid #cbd5e1; color: #475569; }
  article.doc .dead-link { color: #94a3b8; font-size: 0.9em; }
  .crumb { font-size: 13px; color: #64748b; margin-bottom: 14px; word-break: break-all; }
  .crumb a { color: #2563eb; text-decoration: none; }
  .project-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 14px;
    max-width: 720px;
  }
  .project-card h2 { margin: 0 0 8px; font-size: 18px; }
  .project-card a { color: #2563eb; text-decoration: none; font-size: 13.5px; }
  .project-card .file-count { color: #64748b; font-size: 12.5px; margin-left: 8px; }
"""


def sidebar_html(root: Path, projects: List[Tuple[str, List[Path]]], active: Optional[Path]) -> str:
    sections: List[str] = []
    for name, files in projects:
        is_active_project = active is not None and any(item == active for item in files)
        items: List[str] = []
        for item in files:
            href = file_url(root, item)
            if href is None:
                continue
            rel_in_project = item.relative_to(root)
            label = rel_in_project.as_posix().split("/", 1)[-1] if name != ROOT_PROJECT_LABEL else rel_in_project.as_posix()
            classes = []
            if item.name.endswith(".arch.json"):
                classes.append("graph-file")
            if active is not None and item == active:
                classes.append("active")
            class_attr = f' class="{" ".join(classes)}"' if classes else ""
            items.append(f'<li><a{class_attr} href="{renderer.escape(href)}">{renderer.escape(label)}</a></li>')
        open_attr = " open" if is_active_project else ""
        sections.append(
            f"<details{open_attr}><summary>{renderer.escape(name)}</summary><ul>{''.join(items)}</ul></details>"
        )
    return (
        '<nav class="sidebar">'
        '<h1><a href="/" style="color:#f8fafc;text-decoration:none;">架构笔记</a></h1>'
        f'<div class="root-path">{renderer.escape(str(root))}</div>'
        + "".join(sections)
        + "</nav>"
    )


def page_html(title: str, sidebar: str, content: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{renderer.escape(title)}</title>
    <style>{PAGE_CSS}</style>
  </head>
  <body>
    {sidebar}
    <main class="content">
{content}
    </main>
  </body>
</html>
"""


def index_content(root: Path, projects: List[Tuple[str, List[Path]]]) -> str:
    cards: List[str] = ["<header><h1>项目总览</h1><p>选择一张架构图或一份文档开始浏览。改动文件后刷新页面即可看到最新内容。</p></header>"]
    for name, files in projects:
        graphs = [item for item in files if item.name.endswith(".arch.json")]
        docs_count = len(files) - len(graphs)
        links = " · ".join(
            f'<a href="{renderer.escape(file_url(root, item) or "")}">{renderer.escape(item.name)}</a>'
            for item in graphs
        ) or '<span class="file-count">暂无架构图</span>'
        cards.append(
            f'<div class="project-card"><h2>{renderer.escape(name)}'
            f'<span class="file-count">{len(graphs)} 图 / {docs_count} 文档</span></h2>{links}</div>'
        )
    if len(cards) == 1:
        cards.append("<p>根目录下没有发现 .arch.json 或 .md 文件。</p>")
    return "\n".join(cards)


def crumb_html(root: Path, target: Path) -> str:
    rel = target.resolve().relative_to(root)
    return f'<div class="crumb"><a href="/">项目总览</a> / {renderer.escape(rel.as_posix())}</div>'


def graph_content(root: Path, graph_path: Path) -> str:
    diagram = renderer.load_graph(graph_path)

    def link_resolver(ref: Optional[Path]) -> Optional[str]:
        if ref is None:
            return None
        return file_url(root, ref)

    warnings_html = ""
    if diagram.warnings:
        items = "\n".join(f"<li>{renderer.escape(item)}</li>" for item in diagram.warnings)
        warnings_html = f'<section class="warnings"><h2>Warnings</h2><ul>{items}</ul></section>'
    svg = renderer.render_svg(diagram, link_resolver=link_resolver)
    return "\n".join(
        [
            crumb_html(root, graph_path),
            "<header>",
            f"<h1>{renderer.escape(diagram.meta.get('name', graph_path.stem))}</h1>",
            f"<p>{renderer.escape(diagram.meta.get('described', ''))}</p>",
            "</header>",
            warnings_html,
            f'<section class="canvas">{svg}</section>',
        ]
    )


def doc_content(root: Path, doc_path: Path) -> str:
    body = markdown_to_html(renderer.read_text(doc_path), root, doc_path)
    return "\n".join([crumb_html(root, doc_path), f'<article class="doc">{body}</article>'])


# ---------- HTTP server ----------


def make_handler(root: Path) -> type:
    class ArchNotesHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 (http.server API)
            parsed = urlsplit(self.path)
            query = parse_qs(parsed.query)
            raw_path = (query.get("path") or [""])[0]
            try:
                if parsed.path == "/":
                    self.send_page("项目总览", None, index_content(root, scan_projects(root)))
                elif parsed.path in {"/graph", "/doc"}:
                    target = safe_relative_path(root, raw_path)
                    if target is None:
                        self.send_error(404, "File not found or outside root")
                        return
                    if parsed.path == "/graph":
                        if not target.name.endswith(".arch.json"):
                            self.send_error(404, "Not an .arch.json file")
                            return
                        self.send_page(target.name, target, graph_content(root, target))
                    else:
                        if not target.name.endswith(".md"):
                            self.send_error(404, "Not a .md file")
                            return
                        self.send_page(target.name, target, doc_content(root, target))
                else:
                    self.send_error(404, "Unknown route")
            except Exception as error:  # pragma: no cover - defensive: keep server alive
                self.send_error(500, f"Render failed: {error}")

        def send_page(self, title: str, active: Optional[Path], content: str) -> None:
            sidebar = sidebar_html(root, scan_projects(root), active)
            body = page_html(title, sidebar, content).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return ArchNotesHandler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve architecture graphs and module docs as a local notes site.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Root directory containing project folders")
    parser.add_argument("--port", type=int, default=8123, help="Port to listen on (default 8123)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Root directory does not exist: {root}")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(root))
    print(f"Serving {root} at http://127.0.0.1:{args.port}/ (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
