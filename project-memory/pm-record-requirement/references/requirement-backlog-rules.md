# Requirement Backlog Rules

Use these rules for `project-management.md` requirement intake.

## Section Names

Use the existing project language and heading style:

- English: `Requirements Backlog`
- Chinese: `需求待办`

If no equivalent section exists, add it near `Active Tasks` / `进行中的任务`, before `Design Documents` / `设计文档`.

## Suggested Table

English:

```markdown
## Requirements Backlog

| ID | Date | Requirement | Status | Priority | Module/Area | Next Step / Notes |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-YYYYMMDD-short-slug | <YYYY-MM-DD> |  | ready-for-design |  |  |  |
```

Chinese:

```markdown
## 需求待办

| ID | 日期 | 需求 | 状态 | 优先级 | 模块/范围 | 下一步 / 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-YYYYMMDD-short-slug | <YYYY-MM-DD> |  | ready-for-design |  |  |  |
```

Adapt to the existing table columns when the PM document already has a requirement backlog.

## Status Values

Use the lifecycle statuses from [pm-lifecycle-rules.md](pm-lifecycle-rules.md). These are the usual requirement backlog values unless the project already has a different vocabulary:

- `needs-clarification`: requirement is captured but key scope or acceptance facts are missing.
- `ready-for-design`: requirement is clear enough for `pm-design-requirement`.
- `designing`: a design handoff has started.
- `designed`: a change design doc exists.
- `accepted`: the design has been approved or confirmed as the intended direction.
- `implementing`: implementation work has started.
- `implemented`: requirement has been implemented.
- `blocked`: progress is waiting on a concrete dependency.
- `needs-review`: status or evidence is unclear and should be reviewed before changing lifecycle state.
- `obsolete`: requirement has been superseded or dropped.

## Quality Bar

A requirement is `ready-for-design` only when it has:

- clear user or project goal;
- expected behavior or outcome;
- rough scope and non-goals when relevant;
- likely module, product area, or unknown marker;
- acceptance criteria, validation signal, or observable completion condition;
- open questions called out explicitly.

Do not invent missing business rules. Record assumptions as assumptions.
