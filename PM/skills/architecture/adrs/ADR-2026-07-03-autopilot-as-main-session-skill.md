---
title: ADR-2026-07-03-autopilot-as-main-session-skill
status: accepted
review_status: reviewed
---

# ADR-2026-07-03-Autopilot As Main-Session Skill

## Context

The modular workflow needed a supervisor role that takes an accepted L2/L3 design through planning, execution, and closeout without per-step human confirmation. Two durable questions: (1) what form the supervisor takes, given it must dispatch subagent-driven-development's implementer/reviewer subagents; (2) how removing per-step confirmations squares with the interaction-profile safety floor in `modular-workflow-rules.md`.

## Decision

1. The supervisor is a **skill loaded by the main session** (`modular-autopilot`), not an agent: subagents cannot dispatch further subagents, so an agent-shaped supervisor would be unable to run subagent-driven-development.
2. Authorization is **front-loaded into one intake confirmation**: the user accepts the design (modular-change) and then confirms the intake review once; the autonomous zone replaces later confirmations with a decision log, two hard-stop conditions (unresolvable BLOCKED; facts overturning intake conclusions), a ban on push/PR/external actions, and a final accountability report. The safety floor is unaffected because L3 direction acceptance and module map approval still happen before autopilot starts.

## Alternatives Considered

| Alternative | Reason Not Chosen |
| --- | --- |
| Supervisor as `.claude/agents` agent | Cannot dispatch SDD's subagents (no nested subagent dispatch); execution phase would stall. |
| Rebuild planning as a modular-plan skill | Reinvents and must maintain writing-plans' quality rules; poor cost/benefit. |
| Hardcode the superpowers call sequence into modular-change docs | Keeps every per-step human confirmation; cannot deliver one-authorization autonomous execution. |

## Consequences

- Hard dependency on the superpowers plugin (writing-plans, subagent-driven-development, using-git-worktrees); plugin upgrades can shift the seams and the end-to-end rehearsal must be re-run after upgrades.
- The intake review is the single defense before the autonomous zone; its checklist lives in the skill and the "facts overturn intake" hard stop is the backstop.

## Follow-Up

- Run the end-to-end and negative-path rehearsals listed in the design's Validation section on a real L2 change.
