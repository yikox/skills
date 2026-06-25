---
name: pm-groom-roadmap
description: Groom and prioritize project-memory PM backlog, roadmap, and milestones. Use when Codex should review `project-management.md` requirements, active tasks, design status, risks, priorities, roadmap, or milestones; when the user asks to rank work, pick next work, clean up roadmap, plan a milestone, triage backlog, resolve priority conflicts, or rebalance PM planning; or for Chinese requests such as 排优先级, 梳理路线图, 整理需求池, backlog grooming, 路线图规划, 里程碑规划, or 下一步做什么.
---

# PM Groom Roadmap

## Overview

Use this skill to turn PM backlog and roadmap state into a clear planning order. It updates planning sections in `project-management.md` without creating requirements, writing design docs, or marking implementation complete.

## Required References

Read these before grooming:

- [references/shared-rules.md](references/shared-rules.md) for resolving the external PM folder.
- [references/pm-lifecycle-rules.md](references/pm-lifecycle-rules.md) for requirement/design/implementation status meaning.
- [references/roadmap-grooming-rules.md](references/roadmap-grooming-rules.md) for priority, roadmap, and milestone update rules.

## Workflow

1. Resolve the project root and external PM folder.
2. Read `project-management.md`, and read architecture/design docs only when roadmap decisions depend on design status or module ownership.
3. Inventory planning inputs:
   - active tasks and blockers;
   - requirement backlog rows and statuses;
   - design document statuses and accepted/implemented state;
   - milestones, roadmap, current focus, risks, and recent updates.
4. Identify stale, blocked, duplicate, or unclear planning rows. Use `needs-review` for ambiguous state instead of guessing.
5. Rank candidate work using the roadmap grooming rules and existing project priority vocabulary.
6. Update the relevant PM sections:
   - priority or next-step fields in `Requirements Backlog` / `需求待办`;
   - `Current Status` / `当前状态` current focus;
   - `Milestones` / `里程碑`;
   - roadmap or next-plan sections when present;
   - blocker/risk notes when prioritization is constrained.
7. Do not create new requirements; use `pm-record-requirement` when new requirement intake is needed.
8. Do not create change design docs; use `pm-design-requirement` when a requirement should move into design.
9. Report the top priorities, deferred work, changed PM sections, and unresolved planning questions.

## Grooming Rules

- Preserve user intent and existing priority language when present.
- Prefer ranking by evidence: accepted designs, blockers removed, user urgency, milestone dependency, risk reduction, and implementation readiness.
- Do not promote `needs-clarification` items above designable work unless clarification is the explicit next milestone.
- Treat `accepted` designs as stronger implementation candidates than merely `designed` or `proposed` designs.
- Keep `blocked` items visible with the blocker and next unblock action; do not silently drop them.
- Separate "next focus" from "backlog priority": only a small number of items should be current focus.
- Match the language of existing PM documents. Use Chinese when the PM docs are Chinese.

## Output Shape

When reporting, keep it concise:

- Top 3 next priorities and why.
- Items deferred and why.
- PM sections changed.
- Questions or blockers that still affect roadmap confidence.
