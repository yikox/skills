---
name: pm-audit-memory
description: Audit external project-memory PM notes for consistency, stale entries, missing design links, lifecycle mismatches, and architecture baseline drift. Use when Codex should inspect `project-management.md`, `knowledge-summary.md`, architecture docs, requirement backlog rows, design document indexes, active tasks, or implementation evidence without immediately creating new requirements or designs; when PM docs need cleanup after implementation; or for Chinese requests such as 检查 PM, 审计项目记忆, 清理待办, 检查设计落地, or PM 一致性检查.
---

# PM Audit Memory

Use this skill to inspect project memory for inconsistencies and stale planning state. Default to reporting findings and recommended fixes; edit files only when the user asks to apply fixes.

## Required References

Read these before auditing:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) for requirement/design/implementation status consistency.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md`, `knowledge-summary.md` if present, and architecture docs under `architecture/` if present.
3. Inspect relevant repository state when available and useful:
   - git status, recent commits, branches, or tags;
   - changed files or implementation evidence named in PM;
   - existing architecture/module files referenced by PM.
4. Check PM consistency:
   - stale `Active Tasks` / `进行中的任务`;
   - requirement rows missing clear next steps, statuses, or design paths;
   - `Requirements Backlog` / `需求待办` rows whose statuses conflict with design docs;
   - `Design Documents` / `设计文档` rows pointing to missing files;
   - change design docs whose status conflicts with PM index rows;
   - implemented designs that did not refresh architecture baseline docs when required;
   - reusable knowledge that belongs in `knowledge-summary.md` but is only buried in PM updates.
5. Report findings ordered by severity and include exact file paths/sections.
6. If the user asks to fix, apply section-level PM edits:
   - update statuses using lifecycle rules;
   - add missing design paths or notes;
   - close stale active tasks only when evidence or user confirmation supports it;
   - add concise knowledge-summary entries only for reusable verified knowledge.
7. Re-read touched files after editing and report remaining risks or assumptions.

## Audit Rules

- Do not create new requirements; use `pm-record-requirement`.
- Do not create change design docs; use `pm-design-requirement`.
- Do not generate baseline architecture docs; use `pm-document-architecture`.
- Do not mark anything implemented without evidence such as user confirmation, commits, changed files, PRs, release notes, or explicit PM notes.
- Prefer `needs-review` or an open question over guessing when evidence is incomplete.
- Preserve project-specific status vocabulary, but map it to lifecycle meaning in the report.
- Match the language of existing PM documents. Use Chinese when the PM docs are Chinese.

## Finding Format

Use concise findings:

```text
Severity: high | medium | low
Location: project-management.md / Requirements Backlog
Issue: Requirement REQ-... is marked designed, but the referenced design file is missing.
Suggested fix: Change status to ready-for-design or create the missing design with pm-design-requirement.
```

When no issues are found, say that clearly and mention any areas not checked.
