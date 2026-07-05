---
name: modular-review
description: Review modular programming artifacts before acceptance or completion. Use when the agent should check module routing, L0/L1/L2/L3 classification, PM start/completion records, architecture baseline vs target separation, module docs, architecture changes, ADRs, module change designs, graph relations, design indexes, or Chinese requests such as 模块化评审, 架构评审, 设计审核, 自动审核.
---

# Modular Review

Use this skill as the automatic reviewer for modular programming artifacts. It finds inconsistencies and fixes clear low-risk defects, but does not replace human acceptance for major direction.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`
- `../_shared/references/architecture-graph-json-format.md` when reviewing graph JSON.

## Workflow

1. Identify the artifact type: PM row, architecture baseline, architecture change, ADR, module doc, module change, graph, or completion evidence.
2. Read the linked PM row, architecture docs, module docs, and design index entries needed for traceability.
3. Check module gate, change level, impacted modules, status sync, baseline/target separation, review status, lightweight-PM fit, and open questions.
4. Fix clear mechanical defects such as missing paths, stale index status, broken local links, or missing review labels.
5. Record human questions for ambiguous module ownership, scope, architecture direction, product tradeoffs, or acceptance decisions.
6. Mark review `reviewed` only when no blocking issue remains.
7. Report findings first, then fixes, then open questions.

## Human Acceptance Boundary

Automatic review may say an artifact is internally consistent. It must not:

- accept L3 architecture direction;
- approve product scope tradeoffs;
- mark a target implemented without evidence;
- choose among materially different module ownership options without user confirmation.
