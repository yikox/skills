---
name: pm-init
description: Initialize or repair a project's durable memory setup in an external notes workspace. Use when Codex should connect a project to project memory; write or update memory rules in AGENTS.md, CLAUDE.md, .codex/AGENTS.md, or similar AI collaboration docs; discover, reuse, or offer migration for existing notes-project-memory documents; create missing project-management.md or knowledge-summary.md files; check whether architecture design docs already exist and offer optional creation through `pm-document-architecture`; or configure when future agents should update project memory after commits, PR merges, releases, deployments, debugging, architecture changes, or verified workflows.
---

# PM Init

Use this skill to connect a project to the external project-memory notes workspace. This is the setup capability in the `project-memory` suite.

## Workflow

1. Read [references/shared-rules.md](references/shared-rules.md).
2. Find the project root. Prefer the git repository root when available.
3. Inspect likely project AI collaboration files in this order:
   - `AGENTS.md`
   - `.codex/AGENTS.md`
   - `.agents/AGENTS.md`
   - `CLAUDE.md`
   - `.claude/CLAUDE.md`
   - other existing files clearly used as agent instructions.
4. If one or more files already contain project-memory or notes-project-memory rules, update the most specific existing file instead of creating another rule location.
5. If no AI collaboration file exists, choose the best target for the active agent:
   - Codex-first project: `AGENTS.md` at the project root.
   - Claude-first project with existing Claude config: `CLAUDE.md`.
   - Repo already using `.codex/` or `.agents/`: use that directory's `AGENTS.md`.
6. Resolve the external notes workspace and project folder using shared rules.
7. Reuse existing `project-management.md` and `knowledge-summary.md` if present. Create only missing files from the templates in this skill.
8. Check whether existing PM docs look like the current schema:
   - Current schema includes `Requirements Backlog` / `需求待办`, `Design Documents` / `设计文档`, lifecycle-aware status wording, and `architecture/main-design.md` when architecture docs exist.
   - If docs are older but usable, keep them as canonical and ask whether to run `pm-migrate-memory` before making large PM edits.
   - Do not perform broad migration during init without user approval. Safe fixes such as adding missing AI rule pointers are allowed.
9. Check whether architecture design docs already exist:
   - Existing architecture docs include `architecture/main-design.md`, module docs under `architecture/modules/`, or a `Design Documents` / `设计文档` PM section that points to those docs.
   - If architecture docs exist, mention them in the report and do not regenerate them unless the user asked for that.
   - If architecture docs do not exist and `pm-document-architecture` is available, ask whether to create them now. Say this is a larger token-consuming step because it may inspect the repository and produce main/module design docs. Also say the user can skip it now and later call `pm-document-architecture` directly.
   - If the user declines or does not clearly approve, leave architecture docs uncreated and report how to continue later.
10. Write or update a short `Project Memory` section in the AI collaboration file.
11. Report the AI doc path, notes folder, reused files, created files, schema/migration status, architecture-doc status, and any unresolved ambiguity.

## Optional Architecture Docs

Do not automatically generate architecture docs during initialization. Creating them can require reading much more repository context than basic PM setup.

When no architecture docs exist, use a concise prompt such as:

```text
I did not find architecture docs such as architecture/main-design.md. Creating them now with pm-document-architecture may use significantly more tokens because it needs to inspect the repo and draft main/module design docs. Do you want me to create them now? You can skip this and run pm-document-architecture later.
```

Continue with `pm-document-architecture` only after explicit approval.

## AI Document Rule Block

Keep the rule block concise. Adapt paths to the resolved project.

```markdown
## Project Memory

This project uses external project memory in:

- Project notes: `<absolute-or-home-relative-notes-path>/PM/<project-slug>/`
- Project management: `<...>/project-management.md`
- Knowledge summary: `<...>/knowledge-summary.md`
- Main design doc: `<...>/architecture/main-design.md` when architecture docs exist

Update project memory when durable project context changes:

- When starting non-trivial project work, record the current task in `project-management.md` under `Active Tasks` / `进行中的任务`; update or close that task as work progresses.
- When a user states a new requirement that is not yet ready for design or implementation, record it in `Requirements Backlog` / `需求待办`. Use `pm-record-requirement` to clarify and capture requirements before `pm-design-requirement`.
- When backlog priority, current focus, roadmap, or milestones need grooming, use `pm-groom-roadmap`.
- After a requirement row or change design doc is generated, use `pm-review-artifact` as the automatic reviewer before human confirmation. Fix clear defects, but list product, scope, module, or tradeoff questions for the human.
- When creating or changing architecture/design docs, keep `project-management.md` `Design Documents` / `设计文档` paths current. Use `architecture/main-design.md` as the main design doc and `architecture/modules/` for module docs. Index requirement/change design docs only after they are generated, and mark them implemented / 已落地 only after implementation is complete.
- When a generated design is ready, use `pm-design-requirement` for design review/acceptance before implementation; acceptance is separate from implementation.
- If architecture docs do not exist, they can be created later with `pm-document-architecture`.
- When existing PM docs use an older schema or old skill names, use `pm-migrate-memory` before broad PM rewrites.
- When PM active tables become noisy, use `pm-track-status` archive rules to move implemented/obsolete items into archive sections while preserving final statuses and design paths.
- Run `pm-audit-memory` after design handoff, implementation completion, milestone/release cleanup, or migration when PM consistency matters.
- After git commits, PR merges, releases, tags, or version bumps, check whether project status, shipped capability, milestone progress, testing, deployment, risk, blocker, or ADR information should be recorded in `project-management.md`.
- After important debugging, verified commands, architecture discoveries, workflow changes, conventions, or lessons learned, update `knowledge-summary.md`.
- Do not record tiny formatting-only edits, temporary scratch work, secrets, credentials, or ordinary commit logs.

Before editing either note, read the existing file and merge by section rather than appending duplicates.
```

## Migration From Existing Notes

When a project was previously initialized by `notes-project-memory`:

- Treat its existing `PM/<project-slug>/project-management.md` and `PM/<project-slug>/knowledge-summary.md` as canonical.
- Keep the old file names.
- Preserve existing headings unless normalizing a missing section is useful.
- Add the new git commit checkpoint rule to the project AI doc.
- Add the current skill names and handoff rules when missing: `pm-record-requirement`, `pm-review-artifact`, `pm-groom-roadmap`, `pm-design-requirement`, `pm-document-architecture`, `pm-track-status`, `pm-record-knowledge`, `pm-audit-memory`, and `pm-migrate-memory`.
- If `Requirements Backlog`, `Design Documents`, architecture design paths, lifecycle statuses, or archive sections are missing, suggest `pm-migrate-memory` and ask before applying migration.
- Do not duplicate content into a new `project-memory` folder.

## Templates

Use [references/project-management-template.md](references/project-management-template.md) only if no compatible project management document exists.

Use [references/knowledge-summary-template.md](references/knowledge-summary-template.md) only if no compatible knowledge document exists.

Fill only known facts. Use `待补充` or placeholders sparingly, only when collecting the missing information would be useful later.
