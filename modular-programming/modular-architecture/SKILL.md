---
name: modular-architecture
description: Create, migrate, maintain, review, and render the architecture-first module map for modular programming projects. Use when the agent should define modules for a new project, infer modules from an existing codebase, update `architecture/main-design.md`, module docs, baseline vs proposed target architecture, architecture change docs, ADRs, graph JSON, rendered HTML/SVG diagrams, or Chinese requests such as 模块地图, 模块架构, 全局设计图, 架构变更, ADR, 老项目模块迁移.
---

# Modular Architecture

Use this skill to maintain the authoritative module map. Architecture owns modules, boundaries, relationships, and durable contracts. PM records the lifecycle around that architecture.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/architecture-graph-json-format.md` when authoring graph JSON.
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
3. Create `architecture/main-design.md`, `architecture/modules/*.md`, and `architecture/graphs/current-project.arch.json`.
4. Render `architecture/rendered/current-project-architecture.html` and optional SVG.
5. Index the architecture docs in PM through `modular-status`.

### Existing Project Migration

1. Inspect code shape: directories, entry points, runtime paths, package metadata, tests, data/state stores, IO boundaries, generated artifacts, and docs.
2. Identify modules from stable technical responsibilities, not just folder names.
3. Mark facts as verified, inferred, or unclear.
4. Create or replace the baseline architecture docs and graph.
5. Record unclear boundaries and migration gaps in PM.

### Baseline Update

Use this after implementation changes durable architecture:

1. Read the accepted design or implemented evidence.
2. Update module docs first, then graph JSON, then `main-design.md`.
3. Render diagrams.
4. Keep only landed or accepted baseline facts in baseline docs.

### L3 Target Architecture

Use this before implementation when a change affects module boundaries, cross-module contracts, state ownership, persistence, runtime, or external systems:

1. Ensure PM start exists for the L3 work.
2. Write `architecture/changes/<date>-<change>.md`.
3. Write or update `architecture/graphs/proposed/<date>-<change>.arch.json` when a visual target helps.
4. Add `architecture/adrs/ADR-<date>-<decision>.md` only when a durable decision among meaningful alternatives exists.
5. Run `modular-review`; do not proceed to implementation until the target is reviewed and human-accepted.

## Rendering

Run:

```bash
python3 <suite-dir>/_shared/scripts/render_modular_graph.py <project>/architecture/graphs/current-project.arch.json -o <project>/architecture/rendered/current-project-architecture.html --svg-output <project>/architecture/rendered/current-project-architecture.svg
```

Resolve `<suite-dir>` as the parent directory of this skill directory.

Treat renderer warnings as issues unless the user explicitly accepts a draft with known gaps.

## Quality Rules

- Every non-trivial module has a stable slug and module doc.
- Composite modules expose interfaces when external collaboration needs named endpoints.
- Relations connect modules at the same architecture level.
- Proposed targets are clearly separated from current baseline.
- Architecture docs do not contain task lists, implementation plans, or PM history.
- PM indexes architecture artifacts, but does not define module boundaries.
