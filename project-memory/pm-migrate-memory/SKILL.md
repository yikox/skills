---
name: pm-migrate-memory
description: Migrate or normalize existing external project-memory PM documents to the current `pm-*` schema. Use when project notes were created by older skills such as notes-project-memory, project-memory-init, project-management-memory, pm-architecture-docs, or pm-requirement-to-design; when `project-management.md`, `knowledge-summary.md`, architecture docs, AI collaboration rules, design paths, requirement backlog, design-document indexes, lifecycle statuses, or archive sections need schema repair; or for Chinese requests such as 迁移 PM, 修复 PM 结构, 升级项目记忆, 旧 PM 文档迁移, or 统一 PM schema.
---

# PM Migrate Memory

Use this skill to upgrade existing project-memory notes without changing their meaning. It owns schema normalization, old skill-name replacement, section repair, and safe design-path migration.

## Required References

Read these before migrating:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/pm-migration-rules.md](references/pm-migration-rules.md) for safe migration actions, approval gates, and validation.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) when normalizing requirement, design, or implementation statuses.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md`, `knowledge-summary.md`, existing `architecture/` docs, and project AI collaboration files when present.
3. Inventory the current schema:
   - section names and missing sections;
   - requirement backlog shape and status vocabulary;
   - roadmap, milestone, and priority sections;
   - design document index shape and referenced paths;
   - architecture main design path, especially old `README.md` usage;
   - old skill names in AI docs or notes;
   - archive sections and stale completed rows.
4. Separate safe edits from approval-required edits.
5. Apply safe section-level edits only:
   - add missing empty sections when they are needed for current PM workflows;
   - update AI rule blocks to current `pm-*` skill names;
   - add design index rows for existing design docs;
   - add archive sections without moving active rows.
6. Ask before high-risk edits such as moving files, renaming folders, rewriting statuses in bulk, converting an old architecture `README.md` into `main-design.md`, or archiving many rows.
7. Preserve existing project language, headings, historical notes, and user-written wording whenever possible.
8. Run or recommend `pm-audit-memory` after migration to check links, lifecycle sync, and archive candidates.
9. Report changed files, skipped high-risk items, required user decisions, and remaining inconsistencies.

## Rules

- Migration should make future PM skills work; it should not invent new requirements or designs.
- Prefer additive repair over destructive rewrite.
- If status meaning is unclear, mark the row `needs-review` or leave it unchanged with a migration note.
- Do not delete old content unless the user explicitly asks and it has been preserved elsewhere.
- Do not mark a design `accepted` or `implemented` during migration without evidence.
- Match the language of existing PM documents. Use Chinese when the PM docs are Chinese.
