# Modular Programming Workflow

This project uses the modular-programming workflow. Architecture docs own module boundaries; `project-management.md` (PM) owns work state and evidence.

## Preferences

- `docs-language`: <zh | en | follow-project> — language for PM, architecture, knowledge, optional proposal docs, and decision summaries.
- `confirmation`: <high-touch | standard | low-touch> — confirmation granularity; semantics defined in the workflow's Preference Profiles. `low-touch` never skips L3 acceptance, module map approval, first AI-doc write, or L2-to-L3 promotion.

## Session Entry

- At the start of a new session, read `project-management.md` and `architecture/main-design.md` before non-trivial work.
- If the request relates to an active task, ask the user whether to resume it. Never silently resume, duplicate, or close active tasks.

## Module Gate And Levels

Non-trivial changes must name a primary module, impacted modules, and a level before implementation planning. Default to the lightest path that preserves future understanding:

- L0 trivial edit: implement and verify; PM optional. Bug fixes are at least L1: reproduce first, verify the failing case after the fix, record root cause at completion.
- L1 local change: implement -> verify -> concise evidence. Use Active Tasks only when the work crosses sessions, carries risk/release evidence, belongs to an existing active task, or the user asks for tracking.
- L2 module change: PM start -> decision summary + user confirmation -> feature branch first architecture patch commit -> implement -> verify -> PM complete.
- L3 architecture change: PM start -> decision summary + user acceptance -> feature branch first architecture patch commit / ADR when needed -> implement -> verify -> PM complete.

If the primary module or root cause is unclear, use diagnostic mode first: reproduce, inspect, and gather evidence without structural changes or completion claims.

L2/L3 default to branch-carried architecture patches. Do not create long-lived standalone proposal files unless complexity, offline review, or non-git collaboration requires them. Do not merge an architecture patch branch until code and module map agree.

L2/L3 confirmation requests must embed a decision summary of 3-8 bullets (key changes, ambiguities, risks) in the request itself — not in a separate earlier message — so the user can decide without opening a separate proposal.

## Skill Routing

Primary user-facing entries:

- `modular-init`: set up or repair workflow files.
- `modular-change`: any feature, bug fix, or refactor request.
- `modular-audit`: consistency check, legacy migration, PM compression.
- `modular-knowledge`: record reusable commands, facts, and lessons.

Internal or advanced entries:

- `modular-architecture`: module maps, ADRs, baseline updates, and optional graph visualization.
- `modular-autopilot`: advanced autonomous execution for accepted and reviewed L2/L3 architecture patches or optional proposals.
- `modular-advisor`: advanced advisory role for modularity assessment, legacy refactoring proposals, and new-project modular design discussion; proposals only, never implementation.
- `modular-status`: PM start/update/complete/archive when explicit tracking is needed.
- `modular-review`: check architecture patches, optional proposals, ADRs, PM rows, and maintained graphs.
