---
name: project-memory-init
description: Initialize or repair a project's durable memory setup in an external notes workspace. Use when Codex should connect a project to project memory; write or update memory rules in AGENTS.md, CLAUDE.md, .codex/AGENTS.md, or similar AI collaboration docs; discover, migrate, or reuse existing notes-project-memory documents; create missing project-management.md or knowledge-summary.md files; or configure when future agents should update project memory after commits, PR merges, releases, deployments, debugging, architecture changes, or verified workflows.
---

# Project Memory Init

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
8. Write or update a short `Project Memory` section in the AI collaboration file.
9. Report the AI doc path, notes folder, reused files, created files, and any unresolved ambiguity.

## AI Document Rule Block

Keep the rule block concise. Adapt paths to the resolved project.

```markdown
## Project Memory

This project uses external project memory in:

- Project notes: `<absolute-or-home-relative-notes-path>/PM/<project-slug>/`
- Project management: `<...>/project-management.md`
- Knowledge summary: `<...>/knowledge-summary.md`

Update project memory when durable project context changes:

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
- Do not duplicate content into a new `project-memory` folder.

## Templates

Use [references/project-management-template.md](references/project-management-template.md) only if no compatible project management document exists.

Use [references/knowledge-summary-template.md](references/knowledge-summary-template.md) only if no compatible knowledge document exists.

Fill only known facts. Use `待补充` or placeholders sparingly, only when collecting the missing information would be useful later.
