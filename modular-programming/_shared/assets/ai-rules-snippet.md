# Modular Programming Workflow

This project uses the modular-programming workflow. Architecture docs own module boundaries; `project-management.md` (PM) owns work state and evidence.

## Preferences

- `docs-language`: <zh | en | follow-project> — language for PM, architecture, knowledge, and design docs, and for decision summaries.
- `confirmation`: <high-touch | standard | low-touch> — confirmation granularity; semantics defined in the workflow's Preference Profiles. `low-touch` never skips L3 acceptance, module map approval, first AI-doc write, or L2-to-L3 promotion.

## Session Entry

- At the start of a new session, read `project-management.md` and `architecture/main-design.md` before non-trivial work.
- If the request relates to an active task, ask the user whether to resume it. Never silently resume, duplicate, or close active tasks.

## Module Gate And Levels

Non-trivial changes must name a primary module, impacted modules, and a level before implementation planning. Default to the lightest path that preserves future understanding:

- L0 trivial edit: implement and verify; PM optional. Bug fixes are at least L1: reproduce first, verify the failing case after the fix, record root cause at completion.
- L1 local change: implement -> verify -> concise evidence. Use Active Tasks only when the work crosses sessions, carries risk/release evidence, belongs to an existing active task, or the user asks for tracking.
- L2 module change: PM start -> module change design -> review -> decision summary + user confirmation -> implement -> verify -> PM complete.
- L3 architecture change: PM start -> target design/ADR -> review -> decision summary + user acceptance -> implement -> verify -> baseline update -> PM complete.

If the primary module or root cause is unclear, use diagnostic mode first: reproduce, inspect, and gather evidence without structural changes or completion claims.

L2/L3 confirmation requests must embed a decision summary of 3-8 bullets (key changes, ambiguities, risks) in the request itself — not in a separate earlier message — so the user can decide without reading the full design.

## Skill Routing

Primary user-facing entries:

- `modular-init`: set up or repair workflow files.
- `modular-change`: any feature, bug fix, or refactor request.
- `modular-audit`: consistency check, legacy migration, PM compression.
- `modular-knowledge`: record reusable commands, facts, and lessons.

Internal or advanced entries:

- `modular-architecture`: module maps, ADRs, baseline updates, and optional graph visualization.
- `modular-autopilot`: advanced autonomous execution for accepted and reviewed L2/L3 designs.
- `modular-architect`: advanced advisory role for modularity assessment, legacy refactoring proposals, and new-project modular design discussion; proposals only, never implementation.
- `modular-status`: PM start/update/complete/archive when explicit tracking is needed.
- `modular-review`: check designs, ADRs, PM rows, and maintained graphs.
