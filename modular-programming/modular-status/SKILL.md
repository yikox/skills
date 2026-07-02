---
name: modular-status
description: Maintain `project-management.md` for the modular programming workflow. Use when starting, updating, completing, archiving, or summarizing L1/L2/L3 work; recording active tasks, requirements, change backlog rows, modular design indexes, ADR summaries, validation evidence, blockers, risks, roadmap, milestones, or Chinese requests such as 记录进行中, 完成记录, PM 更新, 项目状态, 设计索引, 归档.
---

# Modular Status

Use this skill to keep project management state aligned with the architecture-first modular workflow. PM records work lifecycle and evidence; it does not define module boundaries.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/pm-maintenance-rules.md` when archiving or compressing PM history.

Use:

- `../_shared/assets/project-management-template.md`

## PM Start

For L1/L2/L3, update `Active Tasks` or the local equivalent before or near the beginning of implementation/design work.

Record:

- date;
- task summary;
- primary module;
- impacted modules;
- change level;
- status;
- next step;
- expected design/ADR/architecture artifact when known.

## PM Update

Update the same task or backlog row when:

- the primary module changes;
- impacted modules expand;
- L1 becomes L2 or L2 becomes L3;
- design, review, or human acceptance status changes;
- the task becomes blocked;
- validation strategy or risk changes materially.

## PM Complete

When work completes, update PM with:

- outcome;
- final status;
- changed design or architecture paths;
- verification command/result;
- implementation evidence;
- whether architecture baseline changed.

Then remove, mark done, or archive stale active-task rows according to the document's style.

## Backlog And Design Index

Use Requirements / Change Backlog for requested work not yet implemented. Include primary module, impacted modules, level, scope/impact, and next step.

Use Modular Design Index for main architecture, module docs, architecture changes, ADRs, and module changes.

Do not duplicate ordinary commit logs. Record durable project state, not every file edit.

## Archive

Archive implemented, obsolete, or superseded work only after preserving final status, design paths, and evidence. Keep current architecture baseline and active target designs indexed.

Follow `pm-maintenance-rules.md` for archive candidates, protected statuses, and compression.
