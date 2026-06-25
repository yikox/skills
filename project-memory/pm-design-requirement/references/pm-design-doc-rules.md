# PM Design Document Rules

Use these rules for architecture and requirement design documents stored in project memory.

## Default Paths

Default design root:

```text
PM/<project-slug>/architecture/
```

Default files:

```text
architecture/main-design.md
architecture/modules/<module-slug>.md
architecture/modules/<module-slug>/changes/<YYYY-MM-DD>-<change-slug>.md
```

Do not use `README.md` as the main design document. If an older `README.md` already exists, preserve it and either link it from `main-design.md` or migrate only after user approval.

## Document Roles

- `main-design.md`: current or accepted baseline system scope, module map, cross-module flows, shared constraints, and links to module docs.
- `modules/<module-slug>.md`: current or accepted baseline design for one module, including responsibilities, boundaries, contracts, data/state, flows, dependencies, and constraints.
- `modules/<module-slug>/changes/*.md`: detailed design for one proposed, accepted, or implemented module change. These files are created by `pm-design-requirement`, not by architecture baseline maintenance.

## Status Values

Use these values unless the existing project uses a different status vocabulary:

- `draft`: incomplete or assumption-heavy.
- `proposed`: ready for review.
- `accepted`: explicitly approved direction or confirmed project design.
- `implemented`: design has been implemented in code and is now landed / 已落地.
- `obsolete`: superseded by a newer design.

For requirement backlog and implementation lifecycle status, follow [pm-lifecycle-rules.md](pm-lifecycle-rules.md).

## Slug Rules

- Use lowercase ASCII slugs.
- Replace spaces and punctuation with hyphens.
- Keep module slugs stable once referenced from PM.
- Prefer domain names such as `editor`, `ai-agent`, `ui`, `sync`, `storage`, or `auth`.

## Module Ownership

Every detailed change design should belong to one primary module. For cross-module changes, choose the module that owns the main state, API, or workflow being changed, and list secondary modules in the detailed design.

If no current module fits, record the candidate module owner in the change design and PM index. Do not add it to `main-design.md` or module docs as baseline until the design is accepted as target architecture or implemented.

## Baseline vs Change Design

Architecture baseline docs do not contain plan sections, implementation plans, pending-change queues, or `Planned Changes` tables.

Use `pm-document-architecture` to index main and module design docs in PM. Use `pm-design-requirement` to create and index detailed change design docs after a requirement has been converted into design.

After a change design is implemented, mark that detailed design and its PM index row as `implemented` / `已落地`, then update main/module architecture docs only with the durable architecture that actually landed.

## Lifecycle Sync

- When a requirement row enters design work, mark it `designing`.
- When the detailed design file exists and is indexed, mark the requirement row `designed`.
- When a design is ready but not approved, keep the design doc `proposed` and the requirement row `designed`.
- When review finds blockers or unclear evidence, keep or mark the relevant PM row `needs-review` and record the open questions.
- When the design is explicitly accepted, mark the design doc and `Design Documents` row `accepted`; mark the requirement row `accepted` when that row tracks the same lifecycle.
- When implementation starts, mark the requirement row or active task `implementing`.
- When implementation is complete, mark the requirement row, change design doc, and `Design Documents` row `implemented`.

## PM Index

Maintain a `Design Documents` section in `project-management.md` when design docs exist.

Suggested English table:

```markdown
## Design Documents

| Type | Path | Status | Notes |
| --- | --- | --- | --- |
| Main Design | architecture/main-design.md | draft |  |
| Module: AI Agent | architecture/modules/ai-agent.md | draft |  |
```

Suggested Chinese table:

```markdown
## 设计文档

| 类型 | 路径 | 状态 | 备注 |
| --- | --- | --- | --- |
| 主设计文档 | architecture/main-design.md | draft |  |
| 模块: AI Agent | architecture/modules/ai-agent.md | draft |  |
```

When converting a requirement or task to a detailed design, also update the requirement backlog row, task row, or task note with the design path.

## Writing Rules

- Match the language of existing PM docs.
- Keep design docs concise but decision-ready.
- Separate current implementation facts from proposed design.
- Link related PM tasks, ADRs, issues, PRs, or commits when available.
- Do not store secrets, credentials, private keys, access tokens, personal data unrelated to the project, or temporary scratch notes.
