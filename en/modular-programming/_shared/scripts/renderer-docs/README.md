# Renderer Internal Architecture

Module docs for `render_modular_graph.py` (the architecture graph renderer)
and `serve_modular_graph.py` (the local architecture-notes browser).
Read the relevant docs before modifying either script.

| Doc | Covers |
| --- | --- |
| format-spec.md | `.arch.json` input contract |
| parser-loader.md | JSON loading and validation |
| graph-model.md | in-memory graph model |
| rules-layer.md | relation/level validation rules |
| module-kind-taxonomy.md | module kind semantics and colors |
| layout-engine.md | layout computation |
| svg-renderer.md | SVG output |
| html-output.md | HTML wrapper output |
| render-runtime.md | end-to-end parse + layout + render pipeline |
| cli-orchestrator.md | CLI entry and pipeline orchestration |
| diagnostics.md | warnings and error reporting |
| notes-server.md | local multi-project browse server (serve_modular_graph.py) |
