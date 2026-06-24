# PM Lifecycle Rules

Use these rules to keep requirement, design, implementation, and PM index statuses consistent.

## Lifecycle

Default flow:

```text
needs-clarification -> ready-for-design -> designing -> designed -> accepted -> implementing -> implemented
```

Terminal or side statuses:

- `blocked`: progress is waiting on a concrete dependency.
- `needs-review`: status or evidence is unclear and should be reviewed before changing lifecycle state.
- `obsolete`: superseded, cancelled, or no longer relevant.

## Status Meaning

- `needs-clarification`: the requirement is captured but key scope, acceptance, or ownership facts are missing.
- `ready-for-design`: the requirement is clear enough for `pm-design-requirement`.
- `designing`: a design handoff has started, but the detailed design is not indexed yet.
- `designed`: a detailed change design exists and is indexed in PM.
- `accepted`: the design has been approved or confirmed as the intended direction.
- `implementing`: implementation work has started.
- `implemented`: implementation has landed and the PM row, design doc, and architecture baseline have been updated where needed.
- `blocked`: a blocker is preventing the next transition.
- `needs-review`: status or evidence is unclear and should be reviewed before changing lifecycle state.
- `obsolete`: the item should not continue through the lifecycle.

## Sync Rules

- Requirement backlog rows use requirement lifecycle statuses.
- Change design docs use design statuses: `draft`, `proposed`, `accepted`, `implemented`, or `obsolete`.
- `Design Documents` rows mirror the design doc status, not the requirement backlog status.
- When a design doc is created and indexed, update the requirement row to `designed`.
- When a design is accepted, update the design doc and `Design Documents` row to `accepted`; update the requirement row to `accepted` if it tracks the same lifecycle.
- When implementation starts, update the requirement row or active task to `implementing`; do not mark the design implemented yet.
- When implementation is complete, update the change design doc and `Design Documents` row to `implemented`, update the requirement row to `implemented`, and refresh architecture baseline docs if durable architecture changed.

Preserve existing project-specific status vocabulary when present, but keep equivalent transitions explicit in notes.
