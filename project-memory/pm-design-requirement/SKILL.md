---
name: pm-design-requirement
description: Convert project-management requirements or active tasks into module-scoped design documents inside the external project-memory PM workspace. Use when a PM `Requirements Backlog` / `需求待办` row is ready for design; when a PM todo is only a requirement and needs a concrete design; when Codex should classify a requirement into an architecture module; when a detailed change design doc should be created under that module; when the design path must be written back into `project-management.md` `Design Documents` / `设计文档`; when a generated design has been implemented and should be marked implemented/落地; or for Chinese requests such as 需求转设计文档, 待办转设计, 模块变更设计, or 设计落地. Use `pm-record-requirement` first when the requirement is not yet clear enough to design. Coordinate with any available superpower design-document capability for the detailed design content while this skill owns PM placement, module classification, status lifecycle, and indexing.
---

# PM Design Requirement

## Overview

Use this skill to turn a clarified PM requirement into a concrete design artifact that belongs to a specific architecture module. It keeps the original requirement connected to the design doc and keeps PM aware of the design status.

## Required References

Read these before writing requirement design docs:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/pm-design-doc-rules.md](references/pm-design-doc-rules.md) for design paths, module rules, status values, and PM index rules.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) for requirement/design/implementation status transitions.

Use [assets/change-design-template.md](assets/change-design-template.md) when creating a detailed change design.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md`, `architecture/main-design.md`, and the relevant module design docs.
3. Locate the requirement from `Requirements Backlog` / `需求待办`, the user's request, or `Active Tasks` / `进行中的任务`, in that order.
4. Classify the requirement into a primary module. If multiple modules are affected, choose the owner module and list the impacted modules in the design.
5. If architecture docs do not exist, first establish them with `$pm-document-architecture` or create the minimal main/module docs needed before continuing.
6. Create a detailed change design at `architecture/modules/<module-slug>/changes/<YYYY-MM-DD>-<change-slug>.md`.
7. Update `project-management.md` `Design Documents` / `设计文档` so the change design is indexed after the file exists.
8. Update the original PM requirement or task according to the lifecycle rules so it points to the design document and has an accurate status.
9. Add an ADR summary only if the design records a durable accepted decision, not for every proposed option.
10. Do not update module architecture docs with plan or `Planned Changes` entries.
11. Report the requirement, selected module, design path, PM update, and unresolved questions.

## Classification Rules

- Prefer the module already named by the requirement.
- If the requirement names behavior rather than a module, map it to the module that owns the state, API, or user workflow being changed.
- For cross-module work, choose one primary owner module and list secondary modules in `Impacted Modules`.
- If no existing module fits, choose a candidate module slug in the change design and PM index, but do not add it to `architecture/main-design.md` as baseline until the design is accepted as target architecture or implemented.
- Ask the user only when two or more plausible module owners would lead to meaningfully different designs.

## Design Rules

- Preserve the original requirement text or summarize it without changing its intent.
- If the requirement is vague, use `pm-record-requirement` first instead of designing from ambiguity.
- Separate current state, target design, implementation plan, tests, risks, and open questions.
- Translate template headings and metadata labels to match the existing PM document language.
- Mark the design as `draft` while assumptions remain unresolved, `proposed` when ready for review, and `accepted` only when the user or project record confirms it.
- Do not mark the design or PM task as implemented just because the design doc exists.
- Mark a design as `implemented` / `已落地` only after the generated design has been implemented.
- Keep requirement, design doc, and `Design Documents` statuses synchronized with [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md).
- After implementation, refresh `architecture/main-design.md` or the relevant module docs only if the implementation changes the durable architecture baseline.
- Match the language of existing PM documents. Use Chinese when the PM docs are Chinese.
- When a superpower design-document skill or workflow is available, use it for the detailed design content after the PM path and module ownership are clear.

## PM Update Rules

- Update the requirement row in `Requirements Backlog` / `需求待办` when the requirement exists there.
- Update the task row in `project-management.md` when the task exists in `Active Tasks` / `进行中的任务`.
- If no requirement or task row exists and the user is clearly asking to design a new requirement, first record it with `pm-record-requirement` unless the user explicitly asks to proceed directly and provides enough detail.
- Use a concise note such as `Design: architecture/modules/ai-agent/changes/2026-06-23-context-redesign.md`.
- Mark the requirement row `designing` while the design is being created and `designed` after the design path is indexed, unless the project has a different status vocabulary.
- Update the `Design Documents` / `设计文档` section after creating the detailed design file; use `Change Design` / `变更设计` as the row type when useful.
- Keep change design rows in `draft`, `proposed`, or `accepted` until implementation is complete; then update them to `implemented` / `已落地`.
- Keep PM entries concise; the detailed reasoning belongs in the design document.

## Implementation Completion

When the user says a generated design has been implemented:

1. Read the change design and relevant PM task.
2. Verify or summarize the implementation evidence when available, such as commits, changed files, PRs, or user confirmation.
3. Update the change design status to `implemented` / `已落地` and add the completion date or evidence.
4. Update the PM requirement row or task row and `Design Documents` row to show the design has landed.
5. Update main/module architecture docs only with the new durable architecture baseline, never with the old plan.
