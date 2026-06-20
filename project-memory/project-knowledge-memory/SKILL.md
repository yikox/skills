---
name: project-knowledge-memory
description: Maintain the knowledge-summary.md file in the external project-memory notes workspace. Use when Codex should record or recall verified commands, build/test/release/deploy workflows, troubleshooting results, root causes, investigation findings, architecture facts, code conventions, environment constraints, operational notes, technical lessons learned, or reusable project knowledge discovered during debugging, implementation, commits, PR work, deployment, or user instruction such as remember this, record this, note this down, or keep this for next time.
---

# Project Knowledge Memory

Use this skill to maintain `knowledge-summary.md`. This is the reusable-knowledge capability in the `project-memory` suite.

## What Belongs Here

Record durable knowledge that helps a future agent work faster:

- Verified build, test, release, deploy, and troubleshooting commands.
- Architecture facts, module boundaries, data flow, storage, integrations, and runtime assumptions.
- Code conventions, naming conventions, workflow conventions, and recurring patterns.
- Investigation results, root causes, and final fixes.
- Environment constraints and operational notes.
- Lessons learned, gotchas, and maintenance tips.
- Technical decisions when the reasoning is more useful as knowledge than as planning state.

Do not store secrets, credentials, private keys, access tokens, personal data unrelated to the project, or temporary scratch notes.

## Update Procedure

1. Read [references/shared-rules.md](references/shared-rules.md).
2. Resolve and read `knowledge-summary.md`.
3. Classify the new information by section.
4. Merge with existing bullets instead of adding near-duplicates.
5. Mark commands as verified only when they were run or the user explicitly says they are verified.
6. Include dates for verified commands, investigation results, major architecture discoveries, and important decisions.
7. If information is inferred from code, say it was observed from the current codebase.

## Suggested Sections

Keep existing headings when present. For new files, use [assets/knowledge-summary-template.md](assets/knowledge-summary-template.md).

Suggested sections:

1. Verified Commands
2. Architecture and Structure
3. Conventions
4. Workflows
5. Troubleshooting
6. Investigation Results
7. Decisions
8. Lessons Learned

## Commit-Related Knowledge

A git change may also require `knowledge-summary.md` when it establishes reusable knowledge:

- A new verified test, build, release, or deploy command.
- A confirmed root cause and solution.
- A new architecture or configuration constraint.
- A new convention or workflow future agents should follow.
- A recurring pitfall that was fixed or avoided.

If the commit only changes project status, use `project-management-memory` instead. If it changes both status and reusable knowledge, update both files.
