---
name: pm-record-requirement
description: Clarify and record product or project requirements into the external project-memory PM workspace before design work. Use when a user states a new feature request, bug-fix requirement, product change, technical requirement, or vague todo that should be captured in `project-management.md` `Requirements Backlog` / `需求待办`; when a requirement needs enough scope, acceptance criteria, priority, module ownership from `pm-document-architecture`, modification summary, affected modules, impact points, risks, automatic review, or open questions before `pm-design-requirement`; or for Chinese requests such as 记录需求, 需求待办, 明确需求, 收集需求, 确定模块, 修改范围, 影响点, 需求审核, or 先记到 PM.
---

# PM Record Requirement

Use this skill to turn an informal request into a clear PM requirement backlog item. This is the intake step before `pm-design-requirement`.

## Required References

Read these before writing requirements:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/architecture-module-rules.md](references/architecture-module-rules.md) for mapping the requirement to modules created by `pm-document-architecture`.
- [references/requirement-backlog-rules.md](references/requirement-backlog-rules.md) for backlog fields, status values, and writing rules.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) for requirement/design/implementation status transitions.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md` and preserve its existing language and section style.
3. If architecture docs exist, read `architecture/main-design.md` and the relevant module docs or `Design Documents` / `设计文档` rows needed to identify module ownership.
4. Extract the requirement from the user's request, existing notes, issue, or active discussion.
5. Clarify only the information needed to make the requirement designable:
   - user goal or problem;
   - expected behavior or outcome;
   - primary module created by `pm-document-architecture`, or an explicit candidate/unknown module note;
   - modification summary: what should change from current behavior to target behavior;
   - scope and explicit non-goals;
   - impact points: affected modules, user workflows, data/state, API/contracts, UI, tests, operations, or compatibility;
   - priority or urgency when available;
   - acceptance criteria or validation signal;
   - open questions or assumptions.
6. If missing information would materially change the requirement, especially primary module, change summary, scope, impact, or acceptance criteria, ask targeted questions before recording. If the user wants to record it anyway, mark status `needs-clarification`.
7. Add or update a row in `Requirements Backlog` / `需求待办` in `project-management.md`.
8. Give the requirement a stable ID when the existing PM style supports IDs, such as `REQ-YYYYMMDD-short-slug`.
9. Set status from the lifecycle rules:
   - `needs-clarification` when important facts are missing;
   - `ready-for-design` when the requirement is clear enough for `pm-design-requirement`;
   - preserve an existing status vocabulary if the project already has one.
10. Run `pm-review-artifact` on the created or updated requirement row before handing it to design. Apply clear review fixes and record human questions in the row.
11. Do not create architecture or change design docs in this skill. Report the next step as `pm-design-requirement` when the requirement is reviewed and ready.
12. Report the requirement ID/title, primary module, modification summary, PM path, status, review result, impact points, and open questions.

## Requirement Rules

- Record the user's intent without silently expanding scope.
- Keep the backlog item concise; detailed design belongs to `pm-design-requirement`.
- Choose the primary module from `pm-document-architecture` module docs when possible. If architecture docs do not exist, record a candidate module or `unknown` and recommend `pm-document-architecture` when module ownership matters.
- Record the modification as a current-to-target change, not a low-level implementation plan.
- Record impacted modules or areas separately from the primary owner module when they differ.
- Record scope and non-goals clearly enough that `pm-design-requirement` can proceed without redoing intake.
- Prefer updating an existing matching requirement over adding a duplicate.
- Use assumptions explicitly when the user gives partial information.
- Link related issues, discussions, docs, or active tasks when available.
- Do not put implementation plans, design decisions, or architecture diagrams in the requirement backlog.
- Use `pm-review-artifact` as the automatic reviewer before design handoff; do not treat automatic review as human approval.
- Match the language of existing PM documents. Use Chinese when the PM docs are Chinese.

## Handoff To Design

When the recorded requirement is ready for design, suggest a handoff such as:

```text
Requirement REQ-YYYYMMDD-short-slug is ready-for-design for module <module-slug>. Next, use pm-design-requirement to create the module-scoped detailed design doc.
```

If the user asks to immediately continue into design after recording, use `pm-design-requirement` only after the backlog row exists or has been updated.
