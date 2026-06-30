---
name: architecture-design
description: "Create, analyze, and maintain technical module architecture design documents and diagrams for software projects. Use when Codex needs to: generate a current module architecture for an existing codebase; discuss and design modules for a new project before implementation; update an existing architecture design after module changes; classify technical modules by their primary design carrier; produce Markdown module docs, JSON architecture graphs, and rendered HTML/SVG architecture diagrams."
---

# Architecture Design

Use this skill to turn a project into a maintainable technical architecture baseline. Focus on modules as design carriers for engineers, not business feature categories.

## Core Model

Use three artifact layers:

- `architecture/modules/*.md`: human-written module docs with front matter.
- `architecture/graphs/*.arch.json`: machine-readable graph structure with objects, groups, relations, and layout.
- `dist/*.html`: rendered HTML/SVG diagrams; nodes and groups link to module Markdown docs.

Do not create new `.mdx` graph sources. The earlier MDX idea is deprecated.

When authoring graph files, read `docs/architecture-graph-json-format.md`. When classifying modules or choosing module templates, read `docs/module-kind-classification.md`.

## Workflow Decision

First identify the project state:

- Existing project without architecture docs: inspect code, configuration, entrypoints, tests, package metadata, and README; infer modules from implementation boundaries and interaction paths.
- New project or idea: discuss enough product/technical intent to propose modules; define the module map before writing detailed docs.
- Project with existing architecture docs: read `architecture/main-design.md`, `architecture/graphs/*.arch.json`, and relevant `architecture/modules/*.md`; preserve accepted decisions and update the specific affected modules.

If the user asks for implementation changes as well as architecture changes, update the architecture baseline before or alongside code edits so the design remains traceable.

## Module Classification

Classify atomic modules by the primary design artifact a technical reader must understand:

- `layout-style`: UI layout, style rules, component regions, visual structure.
- `function-flow`: core functions, algorithms, pipelines, rendering, parsing, scheduling, timing.
- `interface-object`: services, managers, clients, facades, readers, writers, stable object APIs.
- `data-state`: state models, stores, caches, indexes, persistence shape, state transitions.
- `event-message`: event buses, subscriptions, message flow, sync ordering, broadcasts.
- `config-rule`: schemas, configuration, policies, plugin declarations, validation rules.
- `resource-file`: files, folders, templates, document formats, generated artifacts.
- `adapter-io`: filesystem, network, browser, database, third-party API boundaries.
- `utility-support`: utilities, logging, diagnostics, helpers, shared support code.

Use `module_form: atomic` for individual modules. Use `module_form: composite` for a module that groups child modules; render it as a containing frame with a name and short description.

## Existing Project Baseline

For an old project, work in this order:

1. Map code shape: list important directories, entrypoints, runtime paths, data/state stores, external boundaries, and generated artifacts.
2. Identify modules: prefer stable technical boundaries over folder names when they differ.
3. Separate composite modules from atomic modules.
4. Write `architecture/main-design.md` with scope, module analysis, hierarchy, interactions, constraints, and review notes.
5. Write one Markdown doc per module in `architecture/modules/`.
6. Write `architecture/graphs/current-project.arch.json` with objects, groups, relations, and `at` layout coordinates.
7. Render the diagram with the bundled renderer and inspect warnings.

Keep inferred statements explicit. If a module boundary is uncertain, label it as inferred and explain the evidence.

## New Project Design

For a new project, start from intent rather than files:

1. Clarify the product/tool goal, runtime environment, primary workflows, persistence needs, external systems, and expected extension points.
2. Propose a small module map with composite groups and atomic modules.
3. Ask for discussion only where module boundaries materially affect future implementation.
4. After agreement or a reasonable assumption, create the same artifact set: main design, module docs, graph JSON, and rendered diagram.

Avoid overfitting the module map to speculative future features. Prefer modules that protect real technical risks: rendering flow, IO contracts, state, configuration, synchronization, and public APIs.

## Architecture Modification

For projects that already have architecture docs:

1. Read the main design, graph JSON, and directly affected module docs.
2. Identify impacted modules, relations, composite groups, and rendered diagram changes.
3. Update module docs first, then the graph JSON, then the main design summary.
4. Re-render HTML/SVG and confirm warnings are zero or explicitly explained.
5. Summarize what changed at the module and relationship level.

When a requested change only affects one module, keep the edit local. When it changes dependencies, data flow, or ownership, update relations and composite grouping too.

## Rendering

Use the bundled renderer from this skill:

```bash
python3 <skill-dir>/scripts/render_arch_graph.py <project>/architecture/graphs/current-project.arch.json -o <project>/dist/current-project-architecture.html
```

Resolve `<skill-dir>` as the directory containing this `SKILL.md`. The renderer reads Markdown front matter from graph `ref` paths, applies module-kind styling, validates references, and emits clickable HTML/SVG.

Use `--svg-output <path>` when a standalone SVG artifact should be refreshed alongside HTML.

Run the renderer after graph changes. Treat warnings about missing references, duplicate IDs, unknown relation endpoints, invalid `label_offset`, or missing `name` / `described` as issues to fix unless the user explicitly accepts a draft with known gaps.

## Quality Checklist

Before finishing:

- Every graph object has a stable `id` and a `ref` to a module doc where possible.
- Every module doc has `name`, `described`, `module_form`, `module_kind` for atomic modules, `main_subject`, and `status`.
- Composite groups contain real object IDs and have their own module doc.
- Relations use engineering verbs that describe data, control, ownership, or call flow.
- The rendered diagram opens from `dist/` and clickable nodes/groups jump to module docs.
- The final answer names changed files and validation results.
