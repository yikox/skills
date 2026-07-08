---
name: modular-change
description: Route and execute project changes through the architecture-first modular programming workflow. Use when a user asks for a feature, bug fix, refactor, behavior change, module modification, architecture change, or implementation work; classifies L0/L1/L2/L3, enforces primary-module routing, records PM when tracking is needed, creates branch-carried architecture patches or optional proposals, coordinates review and implementation; Chinese triggers include 修改流程, 模块修改, 功能开发, bug 修复, 重构, 需求转实现.
---

# Modular Change

Use this as the daily development entry point. Default to the lightest path that preserves future understanding: L0/L1 should stay fast, while L2/L3 use branch-carried architecture patches by default, with standalone proposal docs only for complex/offline review.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`

Use only when the optional proposal path is needed:

- `../_shared/assets/module-change-template.md`
- `../_shared/assets/architecture-change-template.md`
- `../_shared/assets/adr-template.md`

## Workflow

1. Read the user request and current project context.
2. Read `architecture/main-design.md` and relevant `architecture/modules/*.md` if they exist.
3. Decide whether the change is L0, L1, L2, or L3 using the hard level rules in `modular-workflow-rules.md`. For L3, tell the user and confirm before entering the branch architecture patch path.
4. Identify primary module and impacted modules. When module docs declare `code_paths`, locate the primary module deterministically by intersecting the paths you expect to change with each module's `code_paths`.
5. If a non-trivial change lacks a clear primary module or root cause, enter diagnostic mode first: reproduce, inspect, and gather evidence without structural changes or completion claims. If ownership remains unclear, use `modular-architecture` to repair the module map or record an architecture gap.
6. For L2/L3, use `modular-status` to record PM start before the architecture patch or implementation work. For L1, record PM only when the work crosses sessions, carries release/risk evidence, belongs to an existing active task, or the user explicitly wants tracking.
7. Follow the level-specific path below.
8. Verify the implementation.
9. For L2/L3, the feature branch architecture patch updates the target baseline first; before merge, verify code and baseline agree. For L0/L1, update architecture baseline only when durable module behavior, contract, relationship, or constraints changed; re-render affected graphs when the project maintains them.
10. Use `modular-status` to record PM completion and evidence for L2/L3 and tracked L1 work; otherwise add a concise completion note only when durable context matters.

## Level Paths

### L3 Architecture Change

Use when the change affects module boundaries, cross-module contracts, core data/state ownership, runtime model, persistence, external systems, or durable architecture direction.

```text
PM start -> decision summary (3-8 bullets) -> human acceptance
-> create/switch feature branch -> first architecture patch commit updates PM + target module map
-> implementation plan -> implement -> verify
-> close PM and archive/delete process files
-> merge only when code and map agree
```

When asking for acceptance, present a decision summary of 3-8 bullets covering key changes, ambiguities, and risks, so the user can decide without opening a separate proposal. Embed the summary in the confirmation request itself, not only in a separate earlier message.

On acceptance, create or switch to a feature branch and make the first commit the architecture patch. The commit updates `architecture/main-design.md`, affected module docs, and the PM active row to the accepted target state. Do not merge that commit without implementation. Use a standalone proposal document only for complex, cross-day, offline, or non-git review.

### L2 Module Change

Use when one module remains the owner but its internal structure or non-trivial behavior changes.

1. Record PM start with primary module, impacted modules, level, and expected architecture patch.
2. Prepare a 3-8 bullet architecture patch summary covering current state, target map changes, contract impact, validation, risks, and open questions.
3. Ask for user confirmation with the summary embedded in the confirmation request itself.
4. On confirmation, create or switch to a feature branch and make the first commit the architecture patch: update PM plus the affected module docs to the accepted target state.
5. Implement only after the architecture patch commit exists. Alternatively, hand the accepted branch patch to `modular-autopilot` for autonomous execution and closeout.
6. Before merge, verify implementation and target module map agree.

### L1 Lightweight Module Change

Use when one module has a local behavior change that does not alter boundaries or public contracts.

1. Decide whether this L1 needs PM tracking. Skip Active Tasks for routine same-session work.
2. Implement and verify.
3. Update module documentation only if the baseline would otherwise mislead future work.
4. Record concise evidence: PM completion for tracked L1, otherwise a short Recent Updates note only when future context needs it.

### L0 Trivial Change

Use for typo, formatting, comments, tiny docs wording, local constants, and mechanical edits that do not change behavior or module understanding.

1. Tag the module when obvious.
2. Implement and verify.
3. Update PM only when the user explicitly requested tracking, the edit belongs to an active task, or release evidence matters.

## Bug Fix Routing

Bug fixes follow the Bug Fix Path in `modular-workflow-rules.md`:

- At least L1 (a bug fix changes behavior); reproduce or capture evidence before fixing.
- If the root cause or owner is unclear, start in diagnostic mode: reproduce, inspect, and gather evidence without structural changes.
- Small localized fix in one module -> L1: optional light PM note with symptom -> reproduce -> root cause -> fix -> verify the failing case plus existing validation -> concise evidence.
- Structural root cause or multi-step fix inside one module -> L2: the architecture patch summary or optional proposal must include root cause analysis.
- Root cause in module boundaries or cross-module contracts -> confirm L3 with the user.

## Escalation Rules

- If L1 grows into a multi-step refactor, promote it to L2 and record the PM update.
- If L2 changes module contracts or cross-module ownership, confirm the promotion to L3 with the user.
- If implementation discovers the module map is wrong, pause implementation and repair architecture before continuing.

## Completion Rules

Do not mark work complete until:

- verification evidence exists;
- PM completion is recorded for L2/L3 and tracked L1 work;
- PM completion points to the architecture patch commit and implementation evidence;
- the branch's architecture baseline reflects landed durable changes and agrees with code.
