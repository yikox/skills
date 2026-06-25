---
name: pm-review-artifact
description: Review PM requirements, architecture baseline docs, and design artifacts before human confirmation. Use after `pm-record-requirement` creates or updates a requirement backlog row; after `pm-document-architecture` creates or updates `architecture/main-design.md` or module docs; after `pm-design-requirement` creates or updates a module-scoped change design doc; before asking a human to accept, approve, or implement a requirement/design; when Codex should act as an automatic reviewer, fix clear PM/design defects, list unresolved questions for humans, check requirement/design traceability, module ownership, scope, impact points, lifecycle status, architecture baseline consistency, safety/privacy/compatibility concerns, or PM index consistency; or for Chinese requests such as 自动审核, 审核官, 需求审核, 架构审核, 设计审核, 人工确认前检查, 漏洞修复, or 列出疑惑点.
---

# PM Review Artifact

## Overview

Use this skill as the automatic reviewer for newly produced PM artifacts. It can fix clear, low-risk defects and must surface ambiguous questions for human confirmation.

## Required References

Read these before reviewing:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) for lifecycle and review-gate status rules.
- [references/review-artifact-rules.md](references/review-artifact-rules.md) for requirement and design review criteria.

## Workflow

1. Resolve the project root and external PM folder.
2. Identify the artifact to review:
   - a requirement row in `Requirements Backlog` / `需求待办`;
   - architecture baseline docs such as `architecture/main-design.md` or `architecture/modules/<module>.md`;
   - a change design doc under `architecture/modules/<module>/changes/`;
   - related `Design Documents` / `设计文档` rows and module docs when relevant.
3. Read only the supporting context needed for review:
   - `project-management.md`;
   - `architecture/main-design.md` and relevant module docs;
   - the change design doc, if reviewing design;
   - linked requirement rows, design index rows, ADRs, issues, or code facts named by the artifact.
4. Review against the checklist in `review-artifact-rules.md`.
5. Apply safe fixes when the correction is clear and local.
6. Do not decide product tradeoffs, final approval, acceptance, or implementation landing.
7. If unresolved questions remain, record them in the artifact:
   - requirement rows: put concise questions in `Next Step / Notes` / `下一步 / 备注` and use `needs-clarification` or `needs-review` when appropriate;
   - architecture docs: add or update a concise `Review Notes` / `Open Questions` section when human clarification is needed;
   - change design docs: update `Review status`, add `Review Findings`, and keep `Status` / `Design status` as `draft` or `proposed`;
   - PM design index rows: keep status aligned with the design doc.
8. If no blocking issues remain, mark review as complete:
   - requirement rows can remain or become `ready-for-design`;
   - architecture docs can remain `draft` or become `proposed`; automatic review must not mark intended architecture `accepted`;
   - change design docs can use `Review status: reviewed` and remain `proposed` until human acceptance.
9. Report fixed items, remaining human questions, files changed, and whether the artifact is ready for human confirmation.

## Safe Fixes

Safe fixes include:

- filling missing module/path/status fields from existing PM or design docs;
- correcting obvious status mismatches between a design doc and PM index;
- adding missing requirement IDs, design paths, review status, or lifecycle sync evidence;
- adding missing review notes/open questions sections to architecture docs or design docs;
- moving open questions from prose into the standard open-question/review field;
- fixing contradictions caused by stale wording when the source of truth is clear;
- tightening vague wording without changing user intent.

## Human Confirmation Required

Escalate to the human instead of deciding when:

- module ownership is ambiguous and affects the design;
- scope, non-goals, acceptance criteria, or impact points are disputed or incomplete;
- the design has multiple plausible options or tradeoffs;
- implementation risk, compatibility, migration, or data semantics are unclear;
- accepting the design would create a durable product or architecture decision;
- evidence is missing for claims about implemented behavior.
- security, privacy, data retention, migration, rollback, observability, accessibility, or performance impact is unclear.

## Output

Use a concise review report:

- `Fixed`: clear defects corrected.
- `Needs human`: questions or tradeoffs requiring confirmation.
- `Ready state`: `ready-for-design`, `ready-for-human-acceptance`, `needs-clarification`, or `needs-review`.
- `Changed files`: PM/design files touched.
