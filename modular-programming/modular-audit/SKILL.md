---
name: modular-audit
description: Audit or migrate a modular programming project for consistency. Use when the agent should check stale PM tasks, missing primary modules, missing PM start/completion records, outdated architecture baselines, graph/doc drift, implemented designs not reflected in architecture, old project-memory or architecture-design schema, roadmap drift, archive candidates, or Chinese requests such as 模块化审计, 项目迁移, 架构漂移检查, 清理 PM, 旧项目迁移.
---

# Modular Audit

Use this skill to keep a modular programming project trustworthy over time.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`
- `../_shared/references/migration-rules.md`
- `../_shared/references/pm-maintenance-rules.md` when checking archive candidates or history compression.

## Audit Checks

Check:

- every active L1/L2/L3 task has PM start information;
- completed L1/L2/L3 work has PM completion evidence;
- non-trivial backlog rows have primary module, impacted modules, and change level;
- L2/L3 design docs are indexed and status-synchronized;
- implemented designs have evidence;
- landed durable changes are reflected in architecture baseline;
- proposed target architecture is not presented as implemented baseline;
- graph JSON relations match module docs and same-scope relationship rules;
- module docs declare `code_paths`; no orphan paths (behavior-bearing code owned by no module), no ghost globs (matching nothing), no overlapping claims;
- module doc Dependencies tables are subsets of graph relations; relation `kind` values are from the closed vocabulary;
- ADR summary rows link to ADR files;
- old `project-memory` or `architecture-design` terminology has been migrated or archived;
- old detailed history can be compressed without losing current state.

## Migration Flow

1. Read current PM and architecture docs.
2. Detect old schema and legacy skill names.
3. Preserve useful current facts, active work, accepted decisions, and evidence.
4. Convert to the modular storage schema.
5. Record migration gaps instead of guessing.
6. Run `modular-review` on changed PM and architecture artifacts.

## Report

Lead with issues ordered by severity. Then list safe fixes applied, open questions, and recommended next skill.
