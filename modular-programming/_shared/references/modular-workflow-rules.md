# Modular Workflow Rules

Use these rules for the modular programming workflow. The workflow is architecture-first: module structure and relationships are the source of truth, while project management records work state, lifecycle, and evidence.

## Artifact Hierarchy

```text
architecture/main-design.md                  # current baseline module map
architecture/modules/<module>.md             # current baseline module contract
architecture/changes/<date>-<change>.md      # L3 target architecture change
architecture/adrs/ADR-<date>-<decision>.md   # durable architecture decision
architecture/modules/<module>/changes/*.md   # L2 module change design
project-management.md                        # active work, requirements, status, indexes
knowledge-summary.md                         # reusable project knowledge
implementation plan / todo                   # temporary execution detail
```

Architecture owns what the system is and how modules relate. PM owns what is happening, why it matters now, who/what it affects, and whether it is done.

## Session Entry

Before starting any non-trivial work in a project that uses this workflow:

1. Read `project-management.md` for active tasks, blockers, and current focus.
2. Read `architecture/main-design.md` for the current module map.
3. If the request continues an active task, resume that task instead of opening a duplicate.
4. If PM or architecture is missing or stale, repair it with `modular-init` or `modular-audit` before large changes.

## Routing Quick Reference

| Request shape | Skill | Typical level | Expected artifact |
| --- | --- | --- | --- |
| Set up / repair workflow files | `modular-init` | - | PM, knowledge, baseline architecture |
| Define or migrate module map, graphs, ADR | `modular-architecture` | - | baseline/target docs, graph, rendered diagram |
| Feature, bug fix, refactor, behavior change | `modular-change` | L0-L3 | level-specific path |
| Record start/progress/completion/archive | `modular-status` | L1-L3 | PM rows and evidence |
| Check a design, ADR, PM row, or graph | `modular-review` | - | review notes, fixes, open questions |
| Consistency check or legacy migration | `modular-audit` | - | audit report, migration gaps |
| Save reusable commands/facts/lessons | `modular-knowledge` | - | knowledge-summary entries |

## Module Gate

Every non-trivial request must identify:

- primary module;
- impacted modules;
- change level: `L0`, `L1`, `L2`, or `L3`;
- expected artifact: none, PM record, module change design, architecture change, or ADR.

If a non-trivial request cannot be mapped to a primary module, stop before implementation planning. First create or repair the architecture baseline, or record the task as blocked by an architecture gap.

## Change Levels

### L3 Architecture Change

Use L3 when the change:

- creates, splits, merges, or removes modules;
- changes module responsibilities or ownership boundaries;
- changes cross-module contracts, core data flow, state ownership, persistence, runtime model, or external system boundaries;
- requires a durable technical decision that future work must respect.

Flow:

```text
PM start -> architecture change design / ADR -> review -> human acceptance
-> implementation plan -> implementation -> verification
-> update implemented baseline -> PM complete
```

Write target/proposed architecture before implementation. Do not overwrite current baseline as implemented until evidence exists.

### L2 Module Change

Use L2 when the change:

- has one clear primary module;
- changes module internals, file organization, algorithms, internal state flow, or substantial implementation structure;
- does not change external module contracts, or changes them only compatibly;
- needs a multi-step implementation and explicit validation.

Flow:

```text
PM start -> module change design -> review -> implementation
-> verification -> update module architecture -> PM complete
```

### L1 Lightweight Module Change

Use L1 when the change:

- has one clear primary module;
- adds, removes, or adjusts local behavior;
- does not change module boundaries, public contracts, or core flow;
- can be verified locally.

Flow:

```text
PM start -> implementation -> verification
-> update module doc if the baseline would otherwise become stale -> PM complete
```

L1 does not require a full change design.

### L0 Trivial Change

Use L0 for typo, comment, formatting, local constants, small docs wording, or mechanical edits that do not change behavior or module understanding.

Flow:

```text
tag module -> implementation -> verification -> optional PM/architecture update
```

PM is optional for L0 unless the user explicitly asked for the change, the work belongs to an existing active task, or release evidence matters.

## PM Start, Update, Complete

For all L1, L2, and L3 work, update `project-management.md` at the beginning and the end.

At start, record:

- date;
- task summary;
- primary module;
- impacted modules;
- change level;
- current status;
- expected artifacts and next step.

During work, update PM when:

- primary module changes;
- impact expands;
- work becomes blocked;
- design/review/acceptance state changes;
- risk or validation strategy materially changes.

At completion, record:

- outcome;
- changed design/architecture paths;
- verification result;
- implementation evidence such as commit, PR, changed files, or user confirmation;
- whether architecture baseline was updated.

Do not leave stale active tasks after completion.

## Baseline vs Target Architecture

Baseline architecture describes implemented or explicitly accepted current structure. Target architecture describes a reviewed direction that has not landed yet.

Use these statuses unless the project already has equivalent terms:

- `draft`: incomplete or assumption-heavy;
- `proposed`: ready for review;
- `accepted`: approved target direction;
- `implemented`: landed in code and reflected in baseline;
- `obsolete`: superseded.

Never present proposed target architecture as implemented baseline.

## Design, ADR, And Plan Boundaries

Use a design when describing how a change will modify the system.

Use an ADR when recording why a durable architecture direction was chosen among meaningful alternatives.

Use an implementation plan only after the architecture or module design is accepted enough to execute. Plans are temporary execution aids, not source-of-truth architecture.
