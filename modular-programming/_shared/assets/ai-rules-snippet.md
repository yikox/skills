# Modular Programming Workflow

This project uses the modular-programming workflow. Architecture docs own module boundaries; `project-management.md` (PM) owns work state and evidence.

## Session Entry

- At the start of a new session, read `project-management.md` and `architecture/main-design.md` before non-trivial work.
- If the request relates to an active task, ask the user whether to resume it. Never silently resume, duplicate, or close active tasks.

## Module Gate And Levels

Non-trivial changes must name a primary module, impacted modules, and a level before implementation planning:

- L0 trivial edit: implement and verify; PM optional.
- L1 local change: PM start -> implement -> verify -> PM complete.
- L2 module change: PM start -> module change design -> review -> decision summary + user confirmation -> implement -> verify -> PM complete.
- L3 architecture change: PM start -> target design/ADR -> review -> decision summary + user acceptance -> implement -> verify -> baseline update -> PM complete.

Before asking L2/L3 confirmation, give the user a decision summary of 3-8 bullets covering key changes, ambiguities, and risks; do not require reading the full design.

## Skill Routing

- `modular-init`: set up or repair workflow files.
- `modular-architecture`: module map, graphs, ADRs, baseline updates.
- `modular-change`: any feature, bug fix, or refactor request.
- `modular-status`: PM start/update/complete/archive.
- `modular-review`: check designs, ADRs, PM rows, graphs.
- `modular-audit`: consistency check, legacy migration, PM compression.
- `modular-knowledge`: record reusable commands, facts, and lessons.
