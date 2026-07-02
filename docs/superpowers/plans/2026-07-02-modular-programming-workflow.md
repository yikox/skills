# Modular Programming Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the old architecture-graph and project-memory split with one architecture-first modular programming workflow skill suite.

**Architecture:** Create a new `modular-programming/` suite whose skills share one protocol: architecture is the module source of truth, PM records lifecycle state, and every non-trivial change must pass a module gate. Reuse the existing graph renderer as a shared implementation detail rather than as the product identity.

**Tech Stack:** Codex skill folders, Markdown instructions, YAML skill metadata, shell installer, Python graph renderer.

---

### Task 1: Create The New Suite

**Files:**
- Create: `modular-programming/_shared/references/modular-workflow-rules.md`
- Create: `modular-programming/_shared/references/storage-schema.md`
- Create: `modular-programming/_shared/references/review-rules.md`
- Create: `modular-programming/_shared/references/migration-rules.md`
- Create: `modular-programming/_shared/assets/*.md`
- Create: `modular-programming/modular-*/SKILL.md`

- [ ] Add shared workflow rules for architecture authority, module gate, L0-L3 changes, PM start/update/complete, baseline/target architecture, and design/ADR/plan boundaries.
- [ ] Add templates for PM, main architecture, module architecture, architecture change, module change, ADR, and knowledge summary.
- [ ] Add skill entry points for init, architecture, change, status, review, audit, and knowledge.

### Task 2: Reuse Graph Rendering

**Files:**
- Create: `modular-programming/_shared/scripts/render_modular_graph.py`
- Create: `modular-programming/_shared/references/architecture-graph-json-format.md`
- Create: `modular-programming/_shared/references/module-kind-classification.md`

- [ ] Copy the existing graph renderer and reference docs into the shared suite.
- [ ] Update skill instructions so rendering is used as a modular architecture output, not as a standalone architecture-design product.

### Task 3: Rename The Public Surface

**Files:**
- Modify: `README.md`
- Modify: `install.sh`

- [ ] Rewrite the repository README around `modular-programming`.
- [ ] Update installer discovery so legacy `architecture-design` and `project-memory` skills are not installed.
- [ ] Add legacy skill names to install-time cleanup.

### Task 4: Verify

**Commands:**
- `find modular-programming -name SKILL.md -print`
- `./install.sh --dry-run /tmp/modular-skills-install`
- `python3 modular-programming/_shared/scripts/render_modular_graph.py modular-programming/_shared/examples/system-overview.arch.json -o /tmp/modular-graph.html`

- [ ] Confirm the new skill set is discoverable.
- [ ] Confirm dry-run install only installs new modular skill names.
- [ ] Confirm the migrated renderer still runs.
