---
name: modular-architecture
description: Create, migrate, maintain, review, and render the architecture-first module map for modular programming projects. Use when the agent should define modules for a new project, infer modules from an existing codebase, update `architecture/main-design.md`, module docs, baseline vs proposed target architecture, architecture change docs, ADRs, graph JSON, rendered HTML/SVG diagrams, or Chinese requests such as 模块地图, 模块架构, 全局设计图, 架构变更, ADR, 老项目模块迁移.
---

# Modular Architecture

Use this skill to maintain the authoritative module map. Architecture owns modules, boundaries, relationships, and durable contracts. PM records the lifecycle around that architecture. By default, `architecture/main-design.md` plus `architecture/modules/*.md` is sufficient for AI work; graph rendering is an advanced human-facing visualization capability.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/architecture-graph-json-format.md` when authoring graph JSON.
- `../_shared/references/module-authoring-rules.md` when writing or updating module docs.
- `../_shared/references/module-kind-classification.md` when classifying modules.
- `../_shared/references/migration-rules.md` when deriving architecture from an old project.

Use:

- `../_shared/assets/main-design-template.md`
- `../_shared/assets/module-design-template.md`
- `../_shared/assets/architecture-change-template.md`
- `../_shared/assets/adr-template.md`
- `../_shared/scripts/render_modular_graph.py`

## Modes

### New Project Baseline

1. Clarify product/tool goal, runtime, primary workflows, state/persistence, integrations, and extension points only enough to choose module boundaries.
2. Propose a small module map with top-level modules, composite groups, atomic modules, public interfaces, and relationships.
3. Present the proposed module map to the user and adjust until approved. Do not write baseline docs before approval.
4. Create `architecture/main-design.md` and `architecture/modules/*.md`.
5. Create graph JSON and rendered HTML/SVG only when the user asks for visualization or the project is using graph review as an advanced capability.
6. Index the architecture docs in PM through `modular-status`.

### Existing Project Migration

1. Inspect code shape: directories, entry points, runtime paths, package metadata, tests, data/state stores, IO boundaries, generated artifacts, and docs.
2. Identify modules from stable technical responsibilities, not just folder names.
3. Mark facts as verified, inferred, or unclear.
4. Present the inferred module map to the user and adjust until approved before replacing existing baseline docs.
5. Create or replace the baseline architecture docs. Create graph JSON/rendered output only when explicitly useful for human review or an advanced workflow.
6. Record unclear boundaries and migration gaps in PM.

### Baseline Update

Use this after implementation changes durable architecture:

1. Read the accepted design or implemented evidence.
2. Update module docs first, then `main-design.md`.
3. If the project already uses graph artifacts or the change specifically affects a maintained graph, update graph JSON and render diagrams.
4. Keep only landed or accepted baseline facts in baseline docs.

### L3 Target Architecture

Use this before implementation when a change affects module boundaries, cross-module contracts, state ownership, persistence, runtime, or external systems:

1. Ensure PM start exists for the L3 work.
2. Write `architecture/changes/<date>-<change>.md`.
3. Write or update `architecture/graphs/proposed/<date>-<change>.arch.json` only when a visual target helps or graph artifacts are part of the accepted advanced workflow.
4. Add `architecture/adrs/ADR-<date>-<decision>.md` only when a durable decision among meaningful alternatives exists.
5. Run `modular-review`, then ask for acceptance with a decision summary of 3-8 bullets (key changes, ambiguities, risks) embedded in the request; do not proceed to implementation until the target is reviewed and human-accepted.

## Advanced Rendering

Graph rendering is optional and human-facing. Use it when the user asks for a diagram, when visual review would clarify a complex L3 change, or when a project explicitly maintains architecture graphs as an advanced capability.

Run:

```bash
python3 <suite-dir>/_shared/scripts/render_modular_graph.py <project>/architecture/graphs/current-project.arch.json -o <project>/architecture/rendered/current-project-architecture.html --svg-output <project>/architecture/rendered/current-project-architecture.svg
```

Resolve `<suite-dir>` as the parent directory of this skill directory.

Treat renderer warnings as issues for maintained graphs unless the user explicitly accepts a draft with known gaps.

For interactive browsing across projects (graph pages linked to module docs), the user can run the local notes server; static rendering above remains the authoritative baseline artifact:

```bash
python3 <suite-dir>/_shared/scripts/serve_modular_graph.py --root <projects-root> --port 8123
```

## Quality Rules

- Every non-trivial module has a stable slug and module doc.
- New and migrated module docs declare `code_paths` with single ownership: every behavior-bearing path has exactly one owning module.
- When a graph is maintained, relations follow arrow-equals-dependency, the closed `kind` vocabulary, and solid/dashed runtime semantics in the graph format reference; that maintained graph is the authoritative visual source of inter-module relations.
- Composite modules expose interfaces when external collaboration needs named endpoints.
- Relations connect modules at the same architecture level.
- Proposed targets are clearly separated from current baseline.
- Architecture docs do not contain task lists, implementation plans, or PM history.
- PM indexes architecture artifacts, but does not define module boundaries.
