# PM Migration Rules

Use these rules to normalize older project-memory documents to the current `pm-*` schema.

## Current Schema Checklist

`project-management.md` should support these workflows when relevant:

- `Active Tasks` / `进行中的任务`
- `Requirements Backlog` / `需求待办`
- `Design Documents` / `设计文档`
- `Roadmap` / `路线图` when the project tracks future planning beyond milestones
- milestone, validation, risk, ADR, and recent update sections
- archive sections when completed or obsolete rows need cleanup

Architecture docs should use:

- `architecture/main-design.md` for the main architecture design doc
- `architecture/modules/<module-slug>.md` for module baseline docs
- `architecture/modules/<module-slug>/changes/<YYYY-MM-DD>-<change-slug>.md` for requirement change designs

AI collaboration docs should mention current skills:

- `pm-init`
- `pm-track-status`
- `pm-record-requirement`
- `pm-review-artifact`
- `pm-groom-roadmap`
- `pm-design-requirement`
- `pm-document-architecture`
- `pm-record-knowledge`
- `pm-audit-memory`
- `pm-migrate-memory`

## Safe Edits

These can usually be applied without separate approval after reading existing files:

- Add missing empty PM sections needed by current workflows.
- Add a `Design Documents` / `设计文档` table that indexes existing architecture docs.
- Add a `Requirements Backlog` / `需求待办` table when requirements are present but unstructured.
- Add preferred requirement columns for primary module, change summary, and scope/impact when creating or lightly normalizing a backlog table.
- Add archive sections without moving active rows.
- Replace old skill names in AI rule blocks with current `pm-*` names.
- Add a note that `architecture/main-design.md` is the current main design path.

## Approval Required

Ask before these edits:

- Renaming project PM folders.
- Moving or renaming existing PM documents.
- Moving design files into archive folders.
- Replacing `architecture/README.md` with `architecture/main-design.md`.
- Rewriting many historical statuses at once.
- Deleting old sections or collapsing long history.
- Marking designs accepted or implemented based only on inference.

## Status Mapping

Map old statuses only when the meaning is clear:

- unclear, TBD, or pending-question -> `needs-clarification`
- ready, scoped, or clarified -> `ready-for-design`
- design in progress -> `designing`
- design doc exists -> `designed`
- approved, accepted, confirmed -> `accepted`
- in progress or coding -> `implementing`
- done, shipped, landed, released -> `implemented` only when evidence is present
- cancelled, superseded, dropped -> `obsolete`

When uncertain, preserve the old wording and add `needs-review` or a migration note.

## Design Path Migration

Do not use `README.md` as the main architecture design document in new schema.

If an old `architecture/README.md` exists:

1. Preserve it.
2. Ask before converting or moving content.
3. Prefer creating `architecture/main-design.md` that summarizes or links the old file.
4. Update `Design Documents` / `设计文档` only after the new path exists.

## Validation

After migration, check:

- referenced PM paths exist;
- requirement rows with design paths point to existing files;
- `Design Documents` rows match design doc statuses;
- active tasks do not contain completed work that should be archived;
- AI docs point to the PM folder and current skill names;
- no secrets or temporary scratch notes were added.
