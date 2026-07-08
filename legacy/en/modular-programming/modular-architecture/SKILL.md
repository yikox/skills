---
name: modular-architecture
description: Create, migrate, maintain, review, and render the architecture-first module map for modular programming projects. Use when the agent should define modules for a new project, infer modules from an existing codebase, update `architecture/main-design.md`, module docs, branch-carried architecture patches, optional architecture proposal docs, ADRs, graph JSON, rendered HTML/SVG diagrams, or Chinese requests such as 模块地图, 模块架构, 全局设计图, 架构变更, ADR, 老项目模块迁移.
---

# Modular Architecture

Use this skill to maintain the authoritative module map. Architecture owns modules, boundaries, relationships, and durable contracts. PM records the lifecycle around that architecture. By default, `architecture/main-design.md` plus `architecture/modules/*.md` is sufficient for AI work; L2/L3 changes are carried as branch architecture patches, and graph rendering is an advanced human-facing visualization capability.

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

### Baseline / Branch Patch Update

Use this after implementation changes durable architecture, or when creating the first accepted architecture patch commit on a feature branch:

1. Read the accepted patch summary, optional proposal, or implemented evidence.
2. Update module docs first, then `main-design.md`.
3. If this is the first commit on a feature branch for L2/L3, also update the PM active row to point at the branch patch and keep the branch unmerged until implementation catches up.
4. If the project already uses graph artifacts or the change specifically affects a maintained graph, update graph JSON and render diagrams.
5. On main, keep only landed baseline facts in baseline docs. On a feature branch, accepted target facts may appear before implementation, but must be made true before merge.

### L3 Branch Architecture Patch

Use this before implementation when a change affects module boundaries, cross-module contracts, state ownership, persistence, runtime, or external systems:

1. Ensure PM start exists for the L3 work.
2. Prepare a 3-8 bullet target map summary and get human acceptance.
3. Create or switch to a feature branch and make the first commit the architecture patch: update `architecture/main-design.md`, relevant module docs, PM active row, and proposed graph JSON only when a visual target helps or graph artifacts are part of the accepted advanced workflow.
4. Add `architecture/adrs/ADR-<date>-<decision>.md` only when a durable decision among meaningful alternatives exists.
5. Run `modular-review` on the branch patch. Do not merge the branch until implementation and verification make the target map true.

Use `architecture/changes/<date>-<change>.md` only when the target needs a standalone proposal for complex, cross-day, offline, or non-git review.

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
- Proposed targets are clearly separated from current baseline. The separation may be by branch: main holds implemented baseline, the feature branch holds the accepted target patch.
- Architecture docs do not contain task lists, implementation plans, or PM history.
- PM indexes architecture artifacts, but does not define module boundaries.
