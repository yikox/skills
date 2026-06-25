# Roadmap Grooming Rules

Use these rules when prioritizing PM requirements, active tasks, roadmap items, and milestones.

## Priority Inputs

Consider these signals, in this order unless the project already defines a different priority model:

1. User-stated urgency, deadline, or milestone commitment.
2. Blocking dependency for other accepted work.
3. Accepted design that is ready for implementation.
4. Risk reduction, validation need, or unknown that blocks planning confidence.
5. User-visible value or product learning.
6. Implementation size and sequencing cost.

## Suggested Priority Vocabulary

Preserve the project's existing vocabulary. If none exists, use:

- `P0`: urgent blocker or critical fix.
- `P1`: next committed work.
- `P2`: important but not immediate.
- `P3`: backlog or nice-to-have.

Do not assign everything `P1`. A useful roadmap needs visible tradeoffs.

## Status-Aware Ranking

- `needs-clarification`: prioritize only if clarification is itself the next needed work.
- `ready-for-design`: good candidate for `pm-design-requirement` before implementation.
- `designed`: design exists, but review/acceptance may still be needed.
- `accepted`: strong candidate for implementation planning.
- `implementing`: should appear in active focus, not just backlog.
- `blocked`: keep visible with unblock action.
- `needs-review`: do not promote until reviewed.
- `obsolete`: move toward archive, not roadmap.

## PM Update Rules

- Update priority, next-step, milestone, and current-focus fields; do not rewrite requirement intent.
- Preserve primary module, change summary, scope, and impact fields captured by `pm-record-requirement`.
- Keep current focus small, usually one to three items.
- Record why top items outrank deferred items when the choice is not obvious.
- Keep blocked items visible with their blocker and owner/next action when known.
- If grooming reveals a missing requirement, stop and use `pm-record-requirement`.
- If grooming reveals a design gap, point to `pm-design-requirement` instead of writing design details into the roadmap.

## Suggested Sections

Use existing sections when present:

- `Current Status` / `当前状态`
- `Active Tasks` / `进行中的任务`
- `Requirements Backlog` / `需求待办`
- `Milestones` / `里程碑`
- `Roadmap` / `路线图`
- `Blockers and Risks` / `阻塞与风险`

If no roadmap section exists, use `Milestones` and `Current Status` first. Add a new `Roadmap` / `路线图` section only when the project has enough future work to justify it.
