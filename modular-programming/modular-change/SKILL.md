---
name: modular-change
description: Route and execute project changes through the architecture-first modular programming workflow. Use when a user asks for a feature, bug fix, refactor, behavior change, module modification, architecture change, or implementation work; classifies L0/L1/L2/L3, enforces primary-module routing, records PM start and completion, creates module or architecture change designs, coordinates review and implementation; Chinese triggers include 修改流程, 模块修改, 功能开发, bug 修复, 重构, 需求转实现.
---

# Modular Change

Use this as the daily development entry point. Every non-trivial change starts by identifying the primary module and change level.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`

Use:

- `../_shared/assets/module-change-template.md`
- `../_shared/assets/architecture-change-template.md`
- `../_shared/assets/adr-template.md`

## Workflow

1. Read the user request and current project context.
2. Read `architecture/main-design.md` and relevant `architecture/modules/*.md` if they exist.
3. Decide whether the change is L0, L1, L2, or L3.
4. Identify primary module and impacted modules.
5. If a non-trivial change lacks a clear primary module, stop before implementation planning and use `modular-architecture` to repair the module map or record an architecture gap.
6. For L1/L2/L3, use `modular-status` to record PM start before implementation work.
7. Follow the level-specific path below.
8. Verify the implementation.
9. Update architecture baseline only when durable module behavior, contract, relationship, or constraints changed; re-render affected graphs (see `modular-architecture` Baseline Update).
10. Use `modular-status` to record PM completion and evidence.

## Level Paths

### L3 Architecture Change

Use when the change affects module boundaries, cross-module contracts, core data/state ownership, runtime model, persistence, external systems, or durable architecture direction.

```text
PM start -> modular-architecture creates target change / ADR
-> modular-review -> human acceptance
-> implementation plan -> implement -> verify
-> modular-architecture updates baseline
-> PM complete
```

### L2 Module Change

Use when one module remains the owner but its internal structure or non-trivial behavior changes.

1. Record PM start with primary module, impacted modules, level, and expected design path.
2. Create `architecture/modules/<module>/changes/<date>-<change>.md`.
3. Include current module state, target module design, contract impact, implementation outline, validation, risks, and open questions.
4. Run `modular-review`.
5. Implement only after the module design is review-ready and accepted when acceptance is needed.
6. After implementation, update the module baseline doc if it would otherwise be stale.

### L1 Lightweight Module Change

Use when one module has a local behavior change that does not alter boundaries or public contracts.

1. Record PM start with primary module, impacted modules, level, and expected validation.
2. Implement and verify.
3. Update module documentation only if the baseline would otherwise mislead future work.
4. Record PM completion.

### L0 Trivial Change

Use for typo, formatting, comments, tiny docs wording, local constants, and mechanical edits that do not change behavior or module understanding.

1. Tag the module when obvious.
2. Implement and verify.
3. Update PM only when the user explicitly requested tracking, the edit belongs to an active task, or release evidence matters.

## Escalation Rules

- If L1 grows into a multi-step refactor, promote it to L2 and record the PM update.
- If L2 changes module contracts or cross-module ownership, promote it to L3.
- If implementation discovers the module map is wrong, pause implementation and repair architecture before continuing.

## Completion Rules

Do not mark work complete until:

- verification evidence exists;
- PM completion is recorded for L1/L2/L3;
- implemented change designs are marked implemented when applicable;
- architecture baseline reflects landed durable changes.
