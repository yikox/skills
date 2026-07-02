---
name: modular-init
description: Initialize or repair an architecture-first modular programming workflow for a project. Use when the agent should set up modular project memory, connect or create `project-management.md`, `knowledge-summary.md`, `architecture/main-design.md`, module docs, architecture graphs, project AI rules, or migrate a new/old project into the modular workflow; Chinese triggers include 模块化编程初始化, 项目初始化, 接入模块化工作流, 老项目接入, 修复项目记忆.
---

# Modular Init

Use this skill to install the modular programming workflow into a project. The goal is to create a usable module map and project memory structure before normal development work begins.

## Required References

Resolve this skill directory, then read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/migration-rules.md` when the project already has code, old PM docs, or old architecture docs.

Use these assets for new files:

- `../_shared/assets/project-management-template.md`
- `../_shared/assets/knowledge-summary-template.md`
- `../_shared/assets/main-design-template.md`
- `../_shared/assets/module-design-template.md`
- `../_shared/assets/ai-rules-snippet.md` for project AI collaboration docs.

## Workflow

1. Identify the project root and the external or in-repo memory location the project already uses. If no memory location exists, propose `PM/<project-slug>/` and confirm the location with the user.
2. Read existing AI collaboration docs such as `AGENTS.md`, `CLAUDE.md`, `.codex/AGENTS.md`, and existing project memory docs.
3. Determine mode:
   - new project: clarify product/runtime intent enough to create an initial module map;
   - existing project: inspect code and migrate current facts before proposing changes;
   - repair: fix missing sections, stale paths, or old workflow names.
4. Ask the user's workflow preferences as multiple-choice questions before creating files (see Preference Profiles in `modular-workflow-rules.md`):
   - `docs-language`: language for PM, architecture, knowledge, and design docs (`zh` / `en` / `follow-project`);
   - `confirmation`: confirmation granularity (`high-touch` / `standard` / `low-touch`).
   Default to `follow-project` + `standard` when the user has no preference.
5. Create or repair `project-management.md`, `knowledge-summary.md`, and `architecture/main-design.md` in the chosen docs language. When this introduces a new or replaced module map, present it to the user and get approval before writing baseline docs.
6. Ensure architecture is the module source of truth. PM may index modules and tasks, but must not define module boundaries independently.
7. For existing projects, create only a verified or explicitly inferred baseline. Record uncertain areas as migration gaps in PM.
8. Merge `../_shared/assets/ai-rules-snippet.md` into the project's AI collaboration docs (`CLAUDE.md`, `AGENTS.md`, or equivalent): fill the Preferences section with the chosen values, adapt paths and language to the project, merge with existing content instead of overwriting, and confirm with the user before creating or first modifying these files.
9. Report created/updated files, chosen preferences, module baseline status, migration gaps, and the next recommended skill.

## Handoff

- Use `modular-architecture` next when module boundaries, graphs, or baseline docs still need work.
- Use `modular-change` next when the user has a concrete change request after initialization.
- Use `modular-audit` when old project memory exists and consistency is uncertain.
