---
name: modular-knowledge
description: Maintain `knowledge-summary.md` for reusable modular programming project knowledge. Use when the agent should record or recall verified commands, module facts, conventions, troubleshooting results, architecture lessons, validation workflows, operational notes, reusable decisions, or Chinese requests such as 记录知识, 记住这个, 项目知识, 故障结论, 可复用经验.
---

# Modular Knowledge

Use this skill to keep durable project knowledge separate from PM status and architecture baseline.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`

Use:

- `../_shared/assets/knowledge-summary-template.md`

## What To Record

Record verified, reusable knowledge:

- commands that build, test, lint, release, deploy, or diagnose the project;
- stable module facts discovered during implementation or debugging;
- project conventions and naming rules;
- troubleshooting symptoms, causes, and fixes;
- environment constraints;
- validation workflows;
- lessons that should guide future modular changes.

Do not record temporary scratch notes, full commit logs, secrets, or status updates that belong in PM.

## Workflow

1. Read `knowledge-summary.md` and relevant architecture/PM context.
2. Decide whether the information is reusable beyond the current task.
3. Add or update the smallest section that preserves the fact.
4. Link to architecture docs, ADRs, commits, PRs, or issue references when useful.
5. Keep entries concise and evidence-based.
