# Modular Workflow Rules

Use these rules for the modular programming workflow. The workflow is architecture-first: module structure and relationships are the source of truth, while project management records current work state and durable evidence.

Default to the lightest path that preserves future understanding. Use strict PM, design, review, ADR, and graph artifacts only when the change complexity justifies them.

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
architecture/graphs/*.arch.json              # optional advanced visualization source
architecture/rendered/*.html|svg             # optional advanced visualization output
```

Architecture owns what the system is and how modules relate. PM owns what is happening, why it matters now, who/what it affects, and whether it is done.
For AI continuity, `architecture/main-design.md` plus `architecture/modules/*.md` is the default source of truth. Graphs are a human-facing advanced capability, not a required baseline artifact.

## Session Entry

At the start of a new session (or after losing context), before any non-trivial work:

1. Read `project-management.md` for active tasks, blockers, and current focus.
2. Read `architecture/main-design.md` for the current module map.
3. If the request appears to continue an active task, ask the user whether to resume it. Never silently resume, duplicate, or close active tasks.
4. If PM or architecture is missing or stale, repair it with `modular-init` or `modular-audit` before large changes.

Do not re-read these files on every message within the same session unless they may have changed.

## Routing Quick Reference

| Request shape | Skill | Typical level | Expected artifact |
| --- | --- | --- | --- |
| Set up / repair workflow files | `modular-init` | - | PM, knowledge, baseline architecture |
| Define or migrate module map, optional graphs, ADR | `modular-architecture` | - | baseline/target docs; optional advanced graph/rendered diagram |
| Feature, bug fix, refactor, behavior change | `modular-change` | L0-L3 | level-specific path |
| Record start/progress/completion/archive for tracked work | `modular-status` | L2/L3, tracked L1 | PM rows and evidence; concise notes for untracked L1 |
| Hands-off execution of an accepted, reviewed L2/L3 design | `modular-autopilot` | L2-L3 | intake confirmation, decision log, final report |
| Modularity assessment, refactoring proposal, modular design discussion | `modular-architect` | - | assessment report; staged refactoring proposal; new-project design proposal |
| Understand or explain an existing project, plain-language, read-only | `modular-narrator` | - | conversational explanation only; no files produced |
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

When module docs declare `code_paths`, locate the primary module deterministically: intersect the paths you expect to change with each module's `code_paths`. One match = primary module; no match or multi-module ambiguity = architecture gap flow above.

### Diagnostic Mode

If the primary module or root cause is unclear, enter diagnostic mode before planning implementation:

- allowed: read code, run tests, reproduce symptoms, inspect logs, add temporary local diagnostics when needed;
- not allowed: structural refactors, public contract changes, PM completion, or baseline updates;
- exit by identifying the likely primary module and routing to L1/L2/L3, or by recording an architecture gap if the module map is insufficient.

Use diagnostic mode for old projects, unclear bugs, and requests whose real module ownership is unknown. Do not use it as a shortcut to implement without the module gate.

## Code Ownership

Module docs declare owned code via frontmatter `code_paths` (repo-relative globs):

- Every behavior-bearing code path belongs to exactly one module. Overlapping claims are a boundary smell: fix the mapping or split the file.
- Tests follow the module they test; generated artifacts follow the module that produces them.
- Repo meta files (README, LICENSE, CI config, AI collaboration docs) need no owner by default; other intentional exceptions are listed in `main-design.md` Shared Constraints.
- `code_paths` is required for new and migrated modules. Existing docs without it stay valid; `modular-audit` flags them for backfill, plus orphan paths (owned by no module) and ghost globs (matching nothing).

## Change Levels

### L3 Architecture Change

Use L3 when the change:

- creates, splits, merges, or removes modules;
- changes module responsibilities or ownership boundaries;
- changes cross-module contracts, core data flow, state ownership, persistence, runtime model, or external system boundaries;
- requires a durable technical decision that future work must respect.

Flow:

```text
PM start -> architecture change design / ADR -> review
-> decision summary (3-8 bullets) -> human acceptance
-> implementation plan -> implementation -> verification
-> update implemented baseline -> PM complete
```

Write target/proposed architecture before implementation. Do not overwrite current baseline as implemented until evidence exists.

### L2 Module Change

Use L2 when the change:

- has one clear primary module;
- usually touches more than a tiny local behavior or needs more than one coherent implementation step;
- changes module internals, file organization, algorithms, internal state flow, or substantial implementation structure;
- does not change external module contracts, or changes them only compatibly;
- needs a target module design to avoid implementation drift.

Flow:

```text
PM start -> module change design -> review
-> decision summary (3-8 bullets) -> user confirmation -> implementation
-> verification -> update module architecture -> PM complete
```

### L1 Lightweight Module Change

Use L1 when the change:

- has one clear primary module;
- usually touches 1-3 files;
- adds, removes, or adjusts local behavior;
- does not change module boundaries, public contracts, or core flow;
- can be understood without a design document and verified locally in the current session.

Flow:

```text
optional light PM note -> implementation -> verification
-> update module doc if the baseline would otherwise become stale
-> concise completion evidence
```

L1 does not require a full change design. Do not add an Active Tasks row for routine L1 work unless it crosses sessions, carries release/risk evidence, is explicitly requested by the user, or belongs to an existing active task. A concise Recent Updates entry is enough when durable evidence matters.

### L0 Trivial Change

Use L0 for typo, comment, formatting, local constants, small docs wording, or mechanical edits that do not change behavior or module understanding.

Flow:

```text
tag module -> implementation -> verification -> optional PM/architecture update
```

PM is optional for L0 unless the user explicitly asked for the change, the work belongs to an existing active task, or release evidence matters.

## Bug Fix Path

Bug fixes route through the same levels, with these specifics:

- A bug fix changes behavior, so it is at least L1 — never L0 (docs-only typo fixes excepted).
- Before fixing, reproduce the bug or capture concrete evidence (failing command, error output, user-confirmed symptom). Do not fix from guesses. If the root cause or module ownership is unclear, start in diagnostic mode.
- Choose the level by the shape of the fix, not the severity of the symptom:
  - **L1 bug fix**: root cause is local to one module and the fix is a small localized change.
    Flow: `optional light PM note (symptom + suspected module) -> reproduce -> locate root cause -> fix -> verify (the failing case passes and existing validation still passes) -> concise completion evidence`.
  - **L2 bug fix**: the fix needs multi-step restructuring inside one module, or the root cause is structural.
    Flow: the normal L2 path; the module change design must include a root cause analysis section.
- Record the root cause in PM completion. If it is reusable (environment trap, recurring pattern), also record it via `modular-knowledge`.
- If the root cause reveals wrong module boundaries or cross-module contract defects, confirm promotion to L3 with the user before restructuring.

## PM Start, Update, Complete

For L2 and L3 work, update `project-management.md` at the beginning and the end. For L1, update PM only when the work crosses sessions, affects release evidence, carries meaningful risk, belongs to an active task, or the user explicitly wants tracking.

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

Do not leave stale active tasks after completion. Do not turn PM into a transcript; keep the main file focused on current state, open work, blockers, design indexes, and durable evidence.

## Baseline vs Target Architecture

Baseline architecture describes implemented or explicitly accepted current structure. Target architecture describes a reviewed direction that has not landed yet.

Use these statuses unless the project already has equivalent terms:

- `draft`: incomplete or assumption-heavy;
- `proposed`: ready for review;
- `accepted`: approved target direction;
- `implemented`: landed in code and reflected in baseline;
- `obsolete`: superseded.

Never present proposed target architecture as implemented baseline.

## User Confirmation Points

Blocking — do not proceed until the user confirms:

- the initial module map for a new project or migration baseline (module boundaries and names);
- the project memory location and the first write into project AI docs (`CLAUDE.md`, `AGENTS.md`, or equivalent);
- classifying work as L3 and entering the architecture change path;
- an L2 module change design, before implementation;
- an L3 target architecture or ADR direction, after review;
- promoting L2 to L3;
- product scope tradeoffs or choosing among materially different module ownership options;
- cancelling active tasks or archiving large amounts of history.

When asking for L2/L3 confirmation, present a decision summary of 3-8 bullets covering key changes, ambiguities, and risks. The user should be able to decide without reading the full design.

Embed the summary in the confirmation request itself — inside the question prompt or its option previews — never only in a separate earlier message. Confirmation UI may appear without the preceding text, so a detached summary is a summary the user never saw. If the summary is too long to embed, send it as its own message, wait for the user's reply, and only then ask for confirmation.

Report-only — proceed and report, correct if the user objects:

- lightweight PM notes for L1 and PM start/update/complete records for L2/L3;
- L0/L1 classification;
- baseline updates and graph re-rendering after verified implementation;
- archiving a single completed row.

## Preference Profiles

`modular-init` asks the user's workflow preferences and records them in the project AI docs (`Preferences` section of the merged rules snippet). All skills honor them. When unset, use `follow-project` + `standard`.

`docs-language` — language for PM, architecture, knowledge, and design docs, and for decision summaries:

- `zh`: write these docs in Chinese.
- `en`: write these docs in English.
- `follow-project`: follow the dominant language of existing project docs.

`confirmation` — adjusts the User Confirmation Points above:

| Profile | Semantics |
| --- | --- |
| `high-touch` | All standard points, plus: give a one-line summary and confirm before L1 implementation; walk through L2/L3 designs section by section. |
| `standard` | The User Confirmation Points above, unchanged. |
| `low-touch` | L2 confirmation becomes report-only: send the decision summary, then implement without waiting; the user can stop at any time. Everything else stays blocking. |

Safety floor: no profile may skip L3 direction acceptance, module map approval, the first write into project AI docs, or L2-to-L3 promotion.

## Design, ADR, And Plan Boundaries

Use a design when describing how a change will modify the system.

Use an ADR when recording why a durable architecture direction was chosen among meaningful alternatives.

Do not write an ADR when there is no real decision to preserve. A useful ADR has at least two viable options, a decision that will constrain future work, and a plausible future reader asking "why did we choose this?"

Use an implementation plan only after the architecture or module design is accepted enough to execute. Plans are temporary execution aids, not source-of-truth architecture. Store plans under `plans/` beside the design's `changes/` directory with `source_design` and `level` front matter (see `storage-schema.md` Plan Files), and archive or delete them once PM completion is recorded.
