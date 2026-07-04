---
source_design: architecture/changes/2026-07-04-lightweight-default-workflow.md
level: L3
---

# Lightweight Default Workflow Implementation Plan

> **For agentic workers:** Execute inline in this session. Keep changes textual and scoped; do not remove graph tooling.

**Goal:** Make modular-programming default to a lightweight daily workflow while preserving strict L2/L3 governance and graph rendering as an advanced capability.

**Architecture:** Update shared references first, then skill entry docs, then templates/README/PM baseline. Keep audit checker compatible with optional graph files.

**Tech Stack:** Markdown skill docs and Python stdlib checker.

---

## Task 1: Shared Workflow Rules

**Files:**
- Modify: `modular-programming/_shared/references/modular-workflow-rules.md`
- Modify: `modular-programming/_shared/references/storage-schema.md`
- Modify: `modular-programming/_shared/references/pm-maintenance-rules.md`
- Modify: `modular-programming/_shared/references/module-authoring-rules.md`

Steps:

- [x] Add “lightweight by default, strict when complexity rises”.
- [x] Change L1 PM from mandatory Active Tasks to conditional lightweight evidence.
- [x] Add diagnostic mode before module gate completion for unknown bugs/old projects.
- [x] Add hard L1/L2/L3 decision rules.
- [x] Make graph files optional advanced artifacts in storage schema.
- [x] Add ADR gate and module-doc slimming guidance.

## Task 2: Skill Entry Docs

**Files:**
- Modify: `modular-programming/modular-init/SKILL.md`
- Modify: `modular-programming/modular-architecture/SKILL.md`
- Modify: `modular-programming/modular-change/SKILL.md`
- Modify: `modular-programming/modular-status/SKILL.md`
- Modify: `modular-programming/modular-review/SKILL.md`
- Modify: `modular-programming/modular-autopilot/SKILL.md`

Steps:

- [x] Make init/migration create `main-design.md` and module docs by default, not graphs.
- [x] Make architecture rendering an advanced optional mode.
- [x] Teach change/status L1 lightweight PM and diagnostic mode.
- [x] Present autopilot as advanced execution for accepted L2/L3 designs.

## Task 3: Templates And User Docs

**Files:**
- Modify: `modular-programming/_shared/assets/project-management-template.md`
- Modify: `modular-programming/_shared/assets/main-design-template.md`
- Modify: `modular-programming/_shared/assets/module-design-template.md`
- Modify: `modular-programming/_shared/assets/ai-rules-snippet.md`
- Modify: `README.md`

Steps:

- [x] Remove placeholder active-task/backlog rows that encourage PM noise.
- [x] Mark Architecture Graph as optional advanced visualization.
- [x] Update AI routing to four primary user-facing entries plus internal/advanced tools.
- [x] Update README with the simplified default workflow.

## Task 4: Project Memory Closeout

**Files:**
- Modify: `PM/skills/project-management.md`
- Modify: `PM/skills/architecture/main-design.md`
- Modify module docs if their public contract changes.

Steps:

- [x] Update design index/status and PM completion evidence.
- [x] Note graph-tooling remains implemented but advanced.
- [x] Run validation commands.
