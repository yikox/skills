---
name: modular-status
description: Maintain `project-management.md` for the modular programming workflow. Use when starting, updating, completing, archiving, or summarizing tracked work; recording active tasks, requirements, change backlog rows, architecture artifact indexes, ADR summaries, validation evidence, blockers, risks, roadmap, milestones, or Chinese requests such as 记录进行中, 完成记录, PM 更新, 项目状态, 设计索引, 归档.
---

# Modular Status

Use this skill to keep project management state aligned with the architecture-first modular workflow. PM records current state and durable evidence; it does not define module boundaries and should not become a transcript.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/pm-maintenance-rules.md` when archiving or compressing PM history.

Use:

- `../_shared/assets/project-management-template.md`

## PM Start

For L2/L3, update `Active Tasks` or the local equivalent before or near the beginning of architecture patch / implementation work.

For L1, use Active Tasks only when the work crosses sessions, carries notable risk or release evidence, belongs to an existing active task, or the user explicitly wants tracking. Otherwise skip PM start.

Record:

- date;
- task summary;
- primary module;
- impacted modules;
- change level;
- status;
- next step;
- expected architecture patch, optional proposal, ADR, or architecture artifact when known.

## PM Update

Update the same task or backlog row when:

- the primary module changes;
- impacted modules expand;
- L1 becomes L2 or L2 becomes L3;
- architecture patch, optional proposal, review, or human acceptance status changes;
- the task becomes blocked;
- validation strategy or risk changes materially.

## PM Complete

When work completes, update PM with:

- outcome;
- final status;
- architecture patch commit, optional proposal path, or changed architecture paths;
- verification command/result;
- implementation evidence;
- whether architecture baseline changed.

Then remove, mark done, or archive stale active-task rows according to the document's style.

For untracked L1 work, prefer a single concise `Recent Updates` bullet only when the result is useful future context. Do not add archive rows for routine L1 work.

## Backlog And Architecture Artifact Index

Use Requirements / Change Backlog for requested work not yet implemented. Include primary module, impacted modules, level, scope/impact, and next step.

Use Modular Design Index for main architecture, module docs, ADRs, and active optional proposal docs. Branch-carried architecture patch commits are recorded in Active Tasks and completion evidence instead of as index rows.

Do not duplicate ordinary commit logs. Record durable project state, not every file edit.

## Archive

Archive implemented, obsolete, or superseded work only after preserving final status, patch/proposal pointer, and evidence. Keep current architecture baseline and active optional proposal docs indexed.

Follow `pm-maintenance-rules.md` for archive candidates, protected statuses, and compression.
