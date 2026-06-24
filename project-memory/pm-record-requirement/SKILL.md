---
name: pm-record-requirement
description: Clarify and record product or project requirements into the external project-memory PM workspace before design work. Use when a user states a new feature request, bug-fix requirement, product change, technical requirement, or vague todo that should be captured in `project-management.md` `Requirements Backlog` / `需求待办`; when a requirement needs enough scope, acceptance criteria, priority, module hints, risks, or open questions before `pm-design-requirement`; or for Chinese requests such as 记录需求, 需求待办, 明确需求, 收集需求, or 先记到 PM.
---

# PM Record Requirement

Use this skill to turn an informal request into a clear PM requirement backlog item. This is the intake step before `pm-design-requirement`.

## Required References

Read these before writing requirements:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/requirement-backlog-rules.md](references/requirement-backlog-rules.md) for backlog fields, status values, and writing rules.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) for requirement/design/implementation status transitions.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md` and preserve its existing language and section style.
3. Extract the requirement from the user's request, existing notes, issue, or active discussion.
4. Clarify only the information needed to make the requirement designable:
   - user goal or problem;
   - expected behavior or outcome;
   - scope and explicit non-goals;
   - priority or urgency when available;
   - likely module or product area when inferable;
   - acceptance criteria or validation signal;
   - open questions or assumptions.
5. If missing information would materially change the requirement, ask targeted questions before recording. If the user wants to record it anyway, mark status `needs-clarification`.
6. Add or update a row in `Requirements Backlog` / `需求待办` in `project-management.md`.
7. Give the requirement a stable ID when the existing PM style supports IDs, such as `REQ-YYYYMMDD-short-slug`.
8. Set status from the lifecycle rules:
   - `needs-clarification` when important facts are missing;
   - `ready-for-design` when the requirement is clear enough for `pm-design-requirement`;
   - preserve an existing status vocabulary if the project already has one.
9. Do not create architecture or change design docs in this skill. Report the next step as `pm-design-requirement` when the requirement is ready.
10. Report the requirement ID/title, PM path, status, and open questions.

## Requirement Rules

- Record the user's intent without silently expanding scope.
- Keep the backlog item concise; detailed design belongs to `pm-design-requirement`.
- Prefer updating an existing matching requirement over adding a duplicate.
- Use assumptions explicitly when the user gives partial information.
- Link related issues, discussions, docs, or active tasks when available.
- Do not put implementation plans, design decisions, or architecture diagrams in the requirement backlog.
- Match the language of existing PM documents. Use Chinese when the PM docs are Chinese.

## Handoff To Design

When the recorded requirement is ready for design, suggest a handoff such as:

```text
Requirement REQ-YYYYMMDD-short-slug is ready-for-design. Next, use pm-design-requirement to classify it into an architecture module and create the detailed design doc.
```

If the user asks to immediately continue into design after recording, use `pm-design-requirement` only after the backlog row exists or has been updated.
