---
name: project-management-memory
description: Maintain the project-management.md file in the external project-memory notes workspace. Use after git commits, staged changes, PR merges, releases, tags, version bumps, changelog/package updates, feature completion, important bug fixes, milestone progress, blockers, risks, testing or CI changes, deployment changes, architecture decisions, or when Codex should record or recall durable project status, roadmap, version state, validation, deployment, risk, or ADR summaries. Check whether a commit changes durable project state; do not write ordinary commit logs.
---

# Project Management Memory

Use this skill to maintain `project-management.md`. This is the project-state capability in the `project-memory` suite.

## What Belongs Here

Record durable project state:

- Project overview and current status.
- Version, release, tag, or shipped capability summaries.
- Git commit checkpoints when the change affects project state.
- Active tasks, current focus, roadmap, and milestones.
- Test, CI, build, deployment, or rollback process changes.
- Blockers, risks, mitigations, and status.
- ADR summaries and important technical direction.
- User-visible bug fixes or important stability fixes.

Do not turn this file into a commit log. Record only the outcome or planning impact that a future agent should know.

## Git Checkpoint Rule

When preparing a commit, after a commit, after a PR merge, or after reviewing git changes, inspect the change scope and decide whether project management memory needs an update.

Update `project-management.md` when the git change includes:

- Feature completion or meaningful capability change.
- User-facing bug fix or important stability improvement.
- Version bump, release prep, release, tag, changelog, or package metadata change.
- Milestone progress, task completion, roadmap change, blocker removal, or new risk.
- Test strategy, CI, build, deploy, configuration, environment, or rollback change.
- Architecture or dependency decision that affects planning or maintenance.

Skip the update when the change is only:

- Formatting, typo fixes, comments, or lint-only cleanup.
- Small internal refactors with no durable project-state impact.
- File moves or renames that do not affect behavior or planning.
- Temporary debugging or local-only scratch work.
- A change already recorded accurately with no new project-state conclusion.

## Update Procedure

1. Read [references/shared-rules.md](references/shared-rules.md).
2. Resolve and read `project-management.md`.
3. If git context matters, inspect the relevant diff, staged changes, commit, tag, or PR summary.
4. Decide whether to update. If no update is warranted, say so briefly.
5. Update the most relevant existing section instead of appending a duplicate section.
6. Include the date for status, release, milestone, risk, ADR, and git checkpoint updates.
7. Keep entries concise and outcome-oriented.

## Suggested Sections

Keep existing headings when present. For new files, use [assets/project-management-template.md](assets/project-management-template.md).

Suggested sections:

1. Overview
2. Current Status
3. Version and Release Notes
4. Active Tasks
5. Milestones
6. Testing and Validation
7. Deployment
8. Blockers and Risks
9. ADR Summary
10. Recent Updates

## Writing Style

- Use Chinese when the project documents are Chinese; otherwise match the existing document language.
- Prefer tables for versions, releases, milestones, risks, and ADR summaries.
- Write conclusions first, then evidence or detail.
- Link to commits, PRs, issues, or docs when available and useful.
- Keep history summarized; do not paste long diffs or full changelogs.
