---
name: pm-document-architecture
description: Create and maintain architecture design documents inside the external project-memory PM workspace. Use when Codex should generate modular architecture docs from an existing repository, discuss and draft a current or accepted target architecture, create or update `architecture/main-design.md`, create module design docs, organize architecture docs by module, add Mermaid-safe architecture/flow diagrams, add SVG-first UI schematic or wireframe diagrams, validate diagram accuracy against architecture source facts, write main/module design-document paths back into `project-management.md`, or handle Chinese requests such as 架构设计文档, 主设计文档, 模块设计文档, Mermaid 图表, 图表校验, 界面示意图, or UI 布局图. Do not use this skill to track plans, pending changes, or implementation plans; use `pm-design-requirement` for requirement/change design docs. Coordinate with any available superpower design-document capability for the design-writing step while this skill owns PM placement, indexing, and lifecycle.
---

# PM Document Architecture

## Overview

Use this skill to maintain the architecture design layer of the `project-memory` suite. It owns where design docs live, how modules are indexed, and how `project-management.md` points to them.

## Required References

Read these before writing or reorganizing design docs:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/pm-design-doc-rules.md](references/pm-design-doc-rules.md) for design paths, module rules, status values, and PM index rules.
- [references/mermaid-diagram-rules.md](references/mermaid-diagram-rules.md) when creating or replacing architecture relationship, flow, sequence, state, data, or dependency diagrams.
- [references/svg-ui-diagram-rules.md](references/svg-ui-diagram-rules.md) when creating or replacing UI schematic, layout, screen-region, or wireframe diagrams.
- [references/diagram-validation-rules.md](references/diagram-validation-rules.md) when creating or replacing any diagram.

Use [assets/main-design-template.md](assets/main-design-template.md) and [assets/module-design-template.md](assets/module-design-template.md) when creating new docs. Use [assets/ui-schematic-template.svg](assets/ui-schematic-template.svg) as a starting point for UI schematic SVG assets.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md`, `knowledge-summary.md` if present, and any existing files under `architecture/`.
3. Determine the mode:
   - Existing project: inspect repository structure, key entry points, package boundaries, data stores, integrations, tests, and build/runtime configuration.
   - New or not-yet-built project: discuss enough scope with the user to identify the intended baseline architecture, modules, main flows, and known constraints.
4. Create or update `architecture/main-design.md`. Do not use `README.md` as the primary design document.
5. Create or update module docs under `architecture/modules/<module-slug>.md`.
6. For architecture relationships, flows, and state transitions, prefer inline Mermaid and follow the Mermaid safety rules. For UI layouts or screen-region diagrams, create SVG assets under `architecture/assets/ui/` and reference them from Markdown.
7. After drawing or updating a diagram, validate it against the source architecture facts. If the diagram is inaccurate or ambiguous, fix it and repeat the validation.
8. Update the `Design Documents` section in `project-management.md` with only the main design path and module design paths.
9. If the work discovers reusable architecture facts from current code, update `knowledge-summary.md` only with concise facts, not full design content.
10. Report changed files, created files, skipped ambiguous areas, and any open questions.

## Design Rules

- Use `architecture/main-design.md` as the default main architecture design document.
- Use module docs for durable module responsibilities, boundaries, contracts, flows, dependencies, and constraints.
- Keep the main design document focused on system scope, module map, cross-module flows, shared constraints, and links to module docs.
- Keep module docs focused on one module. For cross-module behavior, choose a primary owner module and list impacted modules.
- Use Mermaid for module relationships, sequence flows, state transitions, data movement, and dependency diagrams. Keep each Mermaid diagram small enough to explain one idea.
- Use SVG-first for UI schematic diagrams. Do not use ASCII box drawings for durable UI layout documentation unless the sketch is tiny and temporary.
- Store UI schematic SVGs as separate files, not large inline SVG blobs in Markdown.
- Treat diagram accuracy as part of the deliverable. Cross-check diagram nodes, edges, labels, ownership, flows, and file paths against code, existing docs, PM requirements, or explicit user input before finishing.
- Do not include plan sections, implementation plans, pending-change queues, or `Planned Changes` tables in architecture baseline docs.
- Put requirement/change designs under `pm-design-requirement`; when a change design has been implemented, refresh the relevant architecture docs to describe the new landed baseline.
- Preserve existing user-written docs and headings where possible; merge by section instead of rewriting whole files.
- Match the language of existing PM documents. Use Chinese when the PM docs are Chinese.
- Mark unverified facts as assumptions. Do not present intended architecture as implemented code unless verified from code.
- When a superpower design-document skill or workflow is available, use it to improve the design content after PM paths and module ownership are clear.

## Existing Project Notes

When generating docs from code:

- Prefer verified facts observed from files, commands, tests, or user-provided context.
- Separate current state from proposed improvements.
- Do not paste long file inventories. Summarize only architecture-relevant components.
- Include source references when useful, such as package names, app entry points, or important files, without turning the doc into a code tour.

## New Project Notes

When designing something not yet implemented:

- Ask targeted questions only when missing information would materially change module boundaries or major technical choices.
- Capture assumptions explicitly.
- Document the intended baseline architecture, not the project plan. Detailed requirement designs and implementation plans belong to `pm-design-requirement`.
