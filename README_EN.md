# Modular Programming Skills

> Language / 语言: **English** ｜ [中文](README.md)

> **⚠️ The v1 suite is frozen (2026-07-09).** The 10-skill modular-programming suite described below has moved to [`legacy/`](legacy/README.md) (git tag `modular-v1-frozen`): contract frozen, no longer installed. Its successor v2 (living-docs: two documents + three skills, Chinese-only source) is designed in [`PM/skills/architecture/changes/2026-07-09-living-docs-v2-redesign.md`](PM/skills/architecture/changes/2026-07-09-living-docs-v2-redesign.md). `./install.sh zh` currently installs only the standalone `personal-style` skill; `./install.sh en` is retired.

This repo provides a suite of `modular-programming` skills that let an AI agent develop projects the "locate the module first, then design/implement" way. The default path stays lightweight: small changes finish fast, complex ones escalate to design, review, and PM governance.

Core principles:

```text
Architecture is the authoritative source for the module map and system structure.
PM records what is being done, how far it got, and what the completion evidence is.
Non-trivial changes must locate a primary module first; otherwise do not jump into an implementation plan.
At the start of a new session, read project-management.md and architecture/main-design.md; when an active task is involved, ask the user before continuing it.
```

## When to use

Starting a new project:

```text
Use $modular-init to initialize this project's modular-programming workflow.
```

Migrating an existing project:

```text
Use $modular-architecture to infer the module map from the current code.
Use $modular-audit to check legacy PM/architecture docs and migrate them into the workflow.
```

Day-to-day feature work, bug fixes, refactors:

```text
Use $modular-change to handle this change.
```

Only updating project status:

```text
Use $modular-status to record this task's start/completion.
```

Only recording reusable knowledge:

```text
Use $modular-knowledge to record this debugging conclusion / command / project convention.
```

PM file too long, history drowning the current state:

```text
Use $modular-status to archive completed tasks and requirements.
Use $modular-audit to check whether PM needs compaction, per pm-maintenance-rules.
```

Day-to-day users only need to remember four main entry points: `modular-init`, `modular-change`, `modular-audit`, `modular-knowledge`. The other skills are internal routing or advanced capabilities.

The full "request shape -> skill -> artifact" quick reference is in the Routing Quick Reference of `en/modular-programming/_shared/references/modular-workflow-rules.md` (Chinese under `zh/…`).

## Skill responsibilities

| Skill | When to use | Main artifacts |
| --- | --- | --- |
| `modular-init` | Onboard a new project, repair project memory, initialize the modular workflow | `project-management.md`, `knowledge-summary.md`, base `architecture/` |
| `modular-architecture` | Internal/advanced: create/update the module map, migrate legacy architecture, write architecture changes or ADRs, optional rendered graphs | `architecture/main-design.md`, `architecture/modules/*.md`, optional graphs, ADRs |
| `modular-change` | Day-to-day entry: features, bugs, refactors, module changes, architecture changes | L0/L1/L2/L3 classification, design, implementation, verification, closeout |
| `modular-autopilot` | Advanced: an accepted and reviewed L2/L3 design needs one authorization then hands-off execution | intake review, implementation plan, execution, decision log, closeout/ready-to-merge report |
| `modular-advisor` | Advanced: assess modularity, discuss legacy refactoring or a new project's modular design (works even without the workflow adopted) | assessment report, staged refactoring proposal, modular design proposal (proposals only, no implementation) |
| `modular-narrator` | Advanced: read-only investigation and plain-language explanation to help users understand (standalone, no workflow dependency) | conversational explanation, no files produced |
| `modular-status` | Internal: record start, progress, completion, blockers, design index, archiving | PM active task, completion records, evidence |
| `modular-review` | Internal: auto-review module ownership, change level, design, ADR, PM status, maintained-graph consistency | review notes, fixes, open questions |
| `modular-audit` | Long-unmaintained repos, legacy migration, architecture-drift and PM-clutter checks | audit results, migration gaps, cleanup suggestions |
| `modular-knowledge` | Record build commands, test commands, failure causes, architecture facts, project conventions | `knowledge-summary.md` |

## Recommended flow

### 1. Initialize a new project

```text
Use $modular-init to initialize the project.
```

The agent should first clarify project goals, runtime, main workflows, state/storage, and external systems, then establish the module map:

```text
architecture/main-design.md
architecture/modules/<module>.md
project-management.md
knowledge-summary.md
```

`init` first asks workflow preferences via multiple choice: `docs-language` (doc language zh/en/follow-project) and `confirmation` (confirmation grain high-touch/standard/low-touch; even low-touch does not skip L3 acceptance, persisting the module map, and other safety floors). Preferences are written to the project's AI-doc Preferences section and honored by all later skills.

Architecture graphs are not a default artifact. `main-design.md + modules/*.md` are enough for the AI to work; graphs are an advanced human-facing visualization rendered by `modular-architecture` on demand.

The draft module map must be confirmed by the user before it is persisted as the baseline. `init` also merges the workflow rules (`_shared/assets/ai-rules-snippet.md`) into the project's `CLAUDE.md`/`AGENTS.md` (merge, not overwrite; confirm before the first write), so every later session automatically honors the session entry, module gate, and PM rules.

Success is not "a plan was written" but that the user can understand:

- which modules the system has;
- what each module is responsible for;
- how the modules collaborate;
- which module a future change should land in.

### 2. Migrate a legacy project

```text
Use $modular-architecture to migrate the current project's architecture.
Use $modular-audit to check the migration result.
```

Migration restores facts first and does not refactor by default:

```text
Scan code structure, entry points, config, tests, state, IO, generated artifacts
-> infer the current baseline
-> mark verified / inferred / unclear
-> produce module docs and the global graph
-> attribute TODOs, bugs, requirements to modules
-> record migration gaps in PM
```

If module boundaries are unclear, record it as an architecture gap rather than pretending it is settled.

### 3. Day-to-day development

Prefer:

```text
Use $modular-change to implement this requirement / fix this bug / refactor this module.
```

`modular-change` must pass the session entry and the module gate first:

```text
User request
-> new session first reads project-management.md (active task, blockers, current focus)
-> reads architecture/main-design.md (module map)
-> if related to an active task, ask the user before continuing; do not resume or close on your own
-> locate the Primary Module
-> list Impacted Modules
-> classify L0/L1/L2/L3 (L3 must be flagged and confirmed with the user first)
-> decide whether PM, design, ADR, review are needed
```

If the module map is missing or clearly stale so the primary module cannot be located, go back to `modular-architecture` to repair architecture before entering an implementation plan.

If the bug's root cause or module ownership is unclear, enter diagnostic mode first: reproduce, read code, run tests, gather evidence; no structural changes and no completion claims during diagnosis. Route to L1/L2/L3 after locating it; if diagnosis proves it is a module-map problem, repair architecture.

## Change levels

| Level | Scenario | Flow |
| --- | --- | --- |
| L3 major | Add/split/merge modules, change module boundaries, cross-module contracts, core data flow, state ownership, storage, runtime, external systems, or a durable architecture decision | PM start -> architecture change/ADR -> review -> decision summary -> human acceptance -> plan -> implement -> verify -> update baseline -> PM complete |
| L2 medium | Refactor, internal structure, file organization, algorithm, or state-flow change inside one primary module; external contracts unchanged or only compatibly changed | PM start -> module change design -> review -> decision summary -> user confirmation -> implement -> verify -> update module architecture -> PM complete |
| L1 small | One module, usually 1-3 files, local behavior add/remove, no change to boundaries, public contracts, core flow | implement -> verify -> a Recent Updates line if needed; enter Active Tasks only when crossing sessions / carrying risk / user requests |
| L0 trivial | Typo, comment, formatting, wording, local constants, mechanical edits that do not change behavior or module understanding | tag module -> implement -> verify; PM/architecture update optional |

Hard rules:

```text
L2/L3 must record PM start at the beginning and PM complete at the end.
L1 defaults to light traces; record fully only when crossing sessions, carrying risk, needing release evidence, requested by the user, or belonging to an active task.
L0 does not require PM by default, unless the user explicitly asks to track, it belongs to an existing task, or it affects release evidence.
```

A bug fix is at least L1 (changing behavior is not L0), classified by the shape of the fix rather than symptom severity:

```text
Small bug (local root cause, small change) L1:
  reproduce -> locate root cause -> fix
  -> verify (failing case passes + existing validation does not regress)
  -> a Recent Updates line if needed; PM start/complete only when crossing sessions / carrying risk / user requests / part of an active task
Big bug (structural root cause, multi-step restructuring) L2:
  follow the L2 flow; the module change design must include a root-cause analysis
Root cause in module boundaries / cross-module contracts -> confirm promotion to L3 with the user
Reusable root causes (environment traps, recurring patterns) go into knowledge-summary.md
```

## Points that need user confirmation

Must confirm (blocking; do not proceed until confirmed):

- the initial module map for a new/migrated project (module split, boundaries, naming) before it is persisted as the baseline;
- where project memory lives; the first creation or modification of AI docs such as CLAUDE.md/AGENTS.md;
- when classified as L3, flag and confirm before entering the architecture change flow;
- an L2 module change design, before implementation;
- L3 target architecture / ADR direction, accepted after review;
- promotion of L2 to L3;
- product-scope tradeoffs, choosing between multiple module-ownership options;
- cancelling an active task, archiving large amounts of history.

When requesting L2/L3 confirmation, first give a 3-8 bullet decision summary (key changes, ambiguities, risks) so the user can decide without reading the full design.

Report only (non-blocking; the user corrects if they object):

- PM start/update/complete records;
- L0/L1 classification;
- baseline updates after implementation is verified; if the project maintains graphs, also report graph rendering;
- archiving a single completed task.

## How Architecture and PM relate

Architecture owns "what the system is":

```text
architecture/main-design.md
architecture/modules/*.md
architecture/changes/*.md
architecture/adrs/*.md
architecture/graphs/*.arch.json        # optional advanced visualization
architecture/rendered/*.html|svg       # optional advanced visualization
```

PM owns "what is being done now and what the status is":

```text
project-management.md
```

PM may index modules, designs, and ADRs, but must not define module boundaries itself. Boundaries must come from Architecture.

Graphs are an advanced visualization, not the default source of architecture facts. The default sources are `architecture/main-design.md` and `architecture/modules/*.md`.

## Modules vs code, and relation semantics

```text
The module doc frontmatter code_paths declares the code the module owns (a glob list).
Every behavior-bearing code path belongs to exactly one module; tests follow the module under test.
shared_paths / ignored_paths record non-owner exceptions such as shared utilities, integration tests, generated artifacts, framework glue.
modular-change locates the primary module deterministically via "change paths ∩ code_paths".
modular-audit checks orphan paths, ghost globs, overlapping ownership.

An arrow in the graph = dependency direction: A -> B reads as A depends on / uses B (data flow written in described).
Relation kind, five words: uses / reads / writes / triggers / distributes.
solid = runtime dependency, dashed = non-runtime (build, validation fixtures, sync conventions).
When the project maintains an architecture graph, the graph is the authoritative visualization of inter-module relations, and module-doc Dependencies tables are a subset view of it. When no graph is maintained by default, main-design.md and module docs are authoritative.

Module authoring rules are in module-authoring-rules.md:
4-9 top-level modules; contracts must be concrete; do not restate code; validation must be executable;
mark uncertain facts (inferred)/(unclear); contract/dependency/constraint/code_paths changes must be synced into the docs.
```

## Baseline vs Target

A major change must not write an unimplemented design as current fact.

```text
baseline architecture = the current implemented or accepted system fact
target architecture = the proposed/reviewed/accepted but not-necessarily-landed target structure
```

An L3 major change should write the target architecture or ADR first, pass review, then enter implementation. Only after implementation is verified may the target be turned into the baseline. After the baseline updates, re-render affected architecture graphs.

## PM archiving and compaction

PM's value is "the current state visible at a glance". When completed history starts to drown active tasks:

- move completed/abandoned tasks, requirements, and design-index rows into the archive after preserving final status and evidence;
- when `project-management.md` exceeds ~25 KB, has more than 8-12 recent updates, or fills up with implementation-detail prose, move old detail into `archives/project-management-history-YYYY.md`, `knowledge-summary.md`, or architecture docs;
- neither archiving nor compaction may delete evidence (IDs, dates, design paths, commits, PRs, verification results) — only move it or keep a linked summary.

Details in `en/modular-programming/_shared/references/pm-maintenance-rules.md` (Chinese under `zh/…`).

## Handy prompts

```text
Use $modular-init to onboard this project into the modular-programming workflow.
Use $modular-architecture to generate a module map for this legacy project.
Use $modular-change to implement this requirement the modular way.
Use $modular-change to first classify this change as L0/L1/L2/L3.
Use $modular-autopilot to execute this accepted L2/L3 design.
Use $modular-advisor to assess this project's modularity and discuss a refactoring plan.
Use $modular-status to record the start of this L2 change.
Use $modular-status to record this task's completion with verification results.
Use $modular-review to review this module change design.
Use $modular-audit to check whether PM and Architecture have drifted.
Use $modular-status to archive completed tasks and compact overly long PM history.
Use $modular-knowledge to record this build command and failure conclusion.
```

## Installation

The suite is layered by language: `en/modular-programming/` (English, source/main) and `zh/modular-programming/` (Chinese translation mirror, directory-for-directory equivalent). The **first argument selects the language** (`zh` or `en`, required).

Run from the repo root:

```sh
./install.sh en      # install the English edition
./install.sh zh      # install the Chinese edition
```

Preview what will be installed:

```sh
./install.sh en --dry-run
```

Specify target directories:

```sh
./install.sh en ~/.agents/skills ~/.codex/skills ~/.claude/skills
```

A missing or invalid language argument prints usage and exits with code 2 (no implicit default language). The installed artifact contains no language layer — you get a single edition in the chosen language.

Default targets:

```text
~/.agents/skills
~/.codex/skills
~/.claude/skills
```

The installer installs:

```text
_shared
modular-init
modular-architecture
modular-change
modular-autopilot
modular-advisor
modular-narrator
modular-status
modular-review
modular-audit
modular-knowledge
```

The legacy `project-memory/` and `architecture-design/` were removed from the repo (recoverable via git history). The installer also cleans stale `pm-*` and `architecture-design` skill names from the targets.

## Repo structure

```text
en/modular-programming/    # English (source/main)
  _shared/
    references/          # modular flow, storage schema, review, migration, PM maintenance, graph format
    assets/              # PM, architecture, module, change, ADR, knowledge templates
    scripts/             # graph renderer (renderer-docs/ is the renderer's own module docs)
    examples/            # renderable examples
  modular-init/
  modular-architecture/
  modular-change/
  modular-autopilot/
  modular-advisor/
  modular-narrator/
  modular-status/
  modular-review/
  modular-audit/
  modular-knowledge/
zh/modular-programming/    # Chinese translation mirror, directory-for-directory equivalent to en
install.sh                 # dispatches from the chosen language dir (zh|en)
README.md / README_EN.md   # Chinese main / English
```

Language-mirror convention: only prose is translated; `*.py` scripts and controlled-vocabulary tokens (`atomic`, `function-flow`, `uses`, …) stay English single-source and are byte-for-byte identical across both language dirs.

## Verification

List current active skills (English shown; zh is isomorphic):

```sh
find en/modular-programming -name SKILL.md -print
```

Dry-run install:

```sh
./install.sh en --dry-run /tmp/modular-skills-install
```

Render an example architecture graph:

```sh
python3 en/modular-programming/_shared/scripts/render_modular_graph.py \
  en/modular-programming/_shared/examples/system-overview.arch.json \
  -o /tmp/modular-graph.html
```
