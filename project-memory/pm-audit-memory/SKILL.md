---
name: pm-audit-memory
description: Audit external project-memory PM notes for consistency, stale entries, missing design links, lifecycle mismatches, older-schema drift, roadmap/priority drift, archive candidates, and architecture baseline drift. Use when Codex should inspect `project-management.md`, `knowledge-summary.md`, architecture docs, requirement backlog rows, design document indexes, active tasks, roadmap, milestones, archive sections, or implementation evidence without immediately creating new requirements or designs; when PM docs need cleanup after implementation; or for Chinese requests such as 检查 PM, 审计项目记忆, 清理待办, 检查设计落地, 归档检查, 路线图检查, 优先级检查, 旧 PM 结构检查, or PM 一致性检查.
---

# PM Audit Memory

Use this skill to inspect project memory for inconsistencies and stale planning state. Default to reporting findings and recommended fixes; edit files only when the user asks to apply fixes.

## Required References

Read these before auditing:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) for requirement/design/implementation status consistency.
- [references/pm-archive-rules.md](references/pm-archive-rules.md) when reporting archive candidates or stale active rows.

Use [scripts/check_pm_project.py](scripts/check_pm_project.py) for a deterministic first pass when the user asks for a broad PM project lint or consistency check.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md`, `knowledge-summary.md` if present, and architecture docs under `architecture/` if present.
3. Inspect relevant repository state when available and useful:
   - git status, recent commits, branches, or tags;
   - changed files or implementation evidence named in PM;
   - existing architecture/module files referenced by PM.
4. Check PM consistency:
   - project lint output from `scripts/check_pm_project.py` when running the script is appropriate;
   - stale `Active Tasks` / `进行中的任务`;
   - older schema drift, such as missing `Requirements Backlog` / `需求待办`, missing `Design Documents` / `设计文档`, old skill names, or old `architecture/README.md` main design paths;
   - requirement rows missing clear next steps, statuses, primary module, modification summary, scope, impact points, or design paths when expected;
   - roadmap or milestone items that conflict with current requirement/design lifecycle status;
   - priority rows where blocked, obsolete, or unclear work is ranked above accepted/ready work without explanation;
   - `Requirements Backlog` / `需求待办` rows whose statuses conflict with design docs;
   - `Design Documents` / `设计文档` rows pointing to missing files;
   - change design docs whose status conflicts with PM index rows;
   - implemented designs that did not refresh architecture baseline docs when required;
   - completed, implemented, obsolete, or stale rows that should be archived;
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
- Do not perform automatic artifact review for newly generated requirements or designs; recommend `pm-review-artifact`.
- Do not perform broad prioritization or roadmap grooming; recommend `pm-groom-roadmap`.
- Do not migrate older PM schemas; recommend `pm-migrate-memory` unless the user explicitly asks audit to apply a small safe fix.
- Do not mark anything implemented without evidence such as user confirmation, commits, changed files, PRs, release notes, or explicit PM notes.
- Do not archive active or unclear items. Prefer `needs-review` over hiding uncertainty in an archive.
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
