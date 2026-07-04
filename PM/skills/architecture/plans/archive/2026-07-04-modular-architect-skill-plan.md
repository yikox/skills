---
source_design: architecture/changes/2026-07-04-modular-architect-skill.md
level: L3
---

# Modular Architect Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the advanced advisory skill `modular-architect` (模块化架构师) plus two shared methodology references, and expose it consistently across README, ai-rules-snippet, and the routing table.

**Architecture:** Purely additive change: one new skill directory (`SKILL.md` + `agents/openai.yaml`), two new files in `_shared/references/`, and three small exposure edits. No code, no template, no installer changes.

**Tech Stack:** Markdown + YAML only. Validation via the repo's deterministic checker, unittest suite, and `./install.sh --dry-run`.

## Global Constraints

Copied verbatim from the accepted design (`architecture/changes/2026-07-04-modular-architect-skill.md`):

- 只输出方案，不动代码：不实现、不重构、不改 baseline、不标 implemented。
- 不要求项目已接入模块化工作流；读代码遵循诊断模式纪律（只读不改）。
- 高级入口，不进四个常规入口。
- 证据必须指向具体代码位置并标注 verified/inferred；禁止只看目录结构下结论。
- 新项目设计方案字段有意对齐 `main-design.md` + 模块文档。
- 工作流内老项目重构方案写成 `architecture/changes/<date>-<change>.md`（status: proposed）。
- 评估报告两种模式统一写 `docs/modularization/<date>-assessment.md`。
- SKILL.md 必须只做流程与引用，不复述语料。
- README 需保持"日常只记四个入口"的信息不被稀释。
- 与 `modular-architecture` 触发词区分：architect 强调"评估/方案/讨论"，architecture 强调"落盘/baseline/迁移执行"。

---

### Task 1: Create `_shared/references/modular-methodology.md`

**Files:**
- Create: `modular-programming/_shared/references/modular-methodology.md`

**Interfaces:**
- Produces: reference file cited by Task 3's SKILL.md as `../_shared/references/modular-methodology.md`.

- [ ] **Step 1: Write the file with exactly this content**

````markdown
# Modular Methodology

Use this corpus when reasoning about module boundaries: proposing a new-project modular design, planning legacy modularization, or judging whether a split is real modularization or just file shuffling. `modular-architect` treats this as its core thinking material; other skills may cite specific sections.

Modularization is not splitting code into files. It is dividing responsibility, controlling dependencies, and defining stable contracts so each module can be independently understood, tested, changed, and replaced. The end goal is containing change propagation, not increasing module count.

## Core Mindset

1. **Divide responsibility before dividing code.** First decide what capabilities the system has, who owns each, which belong together, and who owns which data. Splitting one big file into many files that still share global state and call each other's internals is not modularization.
2. **A module is a complete capability**, not a code-type bucket. Prefer capability modules (task scheduling, model loading, cache management) over type-only layers (controllers/services/utils); layer inside a module when needed.
3. **High cohesion, low coupling.** Inside a module everything serves one goal; between modules only necessary, explicit dependencies remain. Changing internals must not ripple outward; replacing a module must not rewrite the system.
4. **Expose capability, hide implementation** (information hiding, Parnas 1972: a module hides one design decision likely to change). Outsiders may know what a module does, how to call it, inputs, outputs, and errors — never its classes, storage, algorithms, or internal state.
5. **Dependencies must be explicit and controlled**: mostly one-directional, few, declared (not fetched via globals or implicit imports), replaceable, acyclic.
6. **Every piece of core data has exactly one owning module.** Others read or request changes through the owner's contract. Shared mutable data across modules is the fastest path to inconsistent state (the bounded-context rule from DDD: one authoritative owner per model).
7. **Modules collaborate through contracts** — public interfaces, input/output shapes, error definitions, state constraints, call ordering, event formats — never through each other's internals. Prefer data coupling; treat shared-global (common) coupling and reach-into-internals (content) coupling as defects (structured-design coupling scale).
8. **Composition over mutual penetration.** Cross-module flows are orchestrated by the application layer that composes modules; a module must not remote-control the internals of its peers.
9. **Not finer is better.** Over-splitting produces long call chains, interface explosion, and debugging pain. A module should be independently understandable yet express a complete responsibility.
10. **The goal is controlling change**: one requirement touches few modules; swapping a technical implementation leaves business logic alone; one module's failure does not cascade; new features come from composing or extending.

## New Project Design Rules

1. **List system capabilities first** (e.g. request intake, task management, scheduling, model management, inference, cache, storage, monitoring). Capabilities seed the module map — never start from file-type directories.
2. **Define each module's boundary**: what it owns, what it explicitly does NOT own, the data it owns, its public contract, its declared dependencies, its error surface. "Not responsible for" prevents boundary creep.
3. **Set dependency direction early** (dependency inversion: high-level policy never depends on low-level detail; both depend on abstractions). Interface layer -> application layer -> business modules -> abstract capabilities <- infrastructure implementations. Core business must not depend on concrete frameworks.
4. **Separate business rules from technical implementation.** Business modules state the capability they need; infrastructure modules implement it. Swapping the database or cache must not rewrite business rules.
5. **One assembly entry point** creates infrastructure objects, chooses implementations, injects dependencies, and boots the app. Modules never construct their own external dependencies.
6. **Keep public contracts small and stable.** Do not export internals for convenience; contract surface is coupling surface.
7. **No global mutable state**: no global connections, caches, config objects, or user context. Globals make dependencies invisible and break testing and initialization order.
8. **Meet real needs first, extract abstractions later.** No factories/plugin systems/registries while there is exactly one implementation. Extract the abstraction when the second real implementation arrives (YAGNI).
9. **Every module must be testable in isolation** — external dependencies replaceable, no full-system boot required. Untestable usually means over-dependent or badly bounded.
10. **Standardize cross-module communication** (direct call, events, queue, RPC, state query) — pick the allowed set once; don't let each module improvise.
11. **Guard the commons.** `common`/`shared`/`utils`/`core` directories become boundary-less landfills; admit only genuinely generic, stable, business-free code. Business rules live in their business module.
12. **Establish architecture constraints early**: forbid business-to-infrastructure direct access, cross-module internal imports, cycles, low-level-depends-on-high-level; back them with tooling where possible.

## Legacy Refactoring Rules

1. **Do not move directories first.** First map call graphs, data flow, state mutation sites, globals, shared objects, cycles, infrastructure calls, and high-risk core flows. Moving files without a dependency map relocates the mess.
2. **Establish a behavior baseline before refactoring**: core-flow tests, key input/output samples, performance baseline, error behavior, logs, production metrics. Without it you cannot tell whether behavior changed.
3. **Identify boundaries opportunistically, not perfectly.** Peel off the easy capabilities first (config, logging, cache, storage, process management, external service access); refine boundaries iteratively.
4. **Wrap before replacing.** Put a seam (interface) around direct database/cache/filesystem/third-party calls; route new code through it; replace the implementation only after call sites stabilize.
5. **Migrate one module at a time, full loop each**: confirm responsibility -> define contract -> move implementation -> update callers -> add tests -> delete old logic -> re-check dependencies -> commit independently.
6. **Replace progressively** (strangler-fig migration, Fowler): keep the old path, build the new module, shift a slice of traffic, verify equivalence, widen coverage, then delete the old path. No big-bang rewrites.
7. **Eliminate hidden dependencies first**: globals, singletons, statics, implicit init, cross-module shared caches, direct env reads, import-time side effects. Convert them to explicit parameters.
8. **Settle data ownership early.** If several modules mutate the same data, decide the owner, who may write, who may only read, which interface mediates writes, and how changes are announced. Boundaries stay unstable until ownership is settled.
9. **Treat cycles as responsibility confusion**, not import puzzles. Fix by extracting the shared capability, lifting the flow to the application layer, decoupling via events, redrawing boundaries, or merging over-split modules — never just lazy imports.
10. **Keep external behavior stable; separate refactoring commits from feature commits.** Changing logic, contract semantics, and data shapes at once makes failures undiagnosable.
11. **Watch performance.** Modularization adds call layers, conversions, serialization. Benchmark critical paths before and after; balance maintainability against hot-path cost.
12. **Delete old code at each milestone** — old entry points, duplicated helpers, temporary adapters, dead compatibility layers. Two coexisting structures are worse than one bad one.
13. **Prevent regression after refactoring**: import-path restrictions, no cross-module internal access, cycle checks, commons limits, data-ownership rules, "new code goes into a named module". Without constraints the mess grows back.

## Attribution

Supplemented concepts and their sources: information hiding (D. L. Parnas, *On the Criteria to Be Used in Decomposing Systems into Modules*, 1972); coupling/cohesion scale (structured design, Constantine & Myers); dependency inversion (R. C. Martin); strangler-fig progressive replacement (M. Fowler); bounded contexts and data ownership (E. Evans, *Domain-Driven Design*).
````

- [ ] **Step 2: Verify the file parses as clean markdown and has no stray tabs**

Run: `git diff --check && grep -c "^## " modular-programming/_shared/references/modular-methodology.md`
Expected: no whitespace errors; heading count `4`.

- [ ] **Step 3: Commit**

```bash
git add modular-programming/_shared/references/modular-methodology.md
git commit -m "Add modular methodology shared reference"
```

### Task 2: Create `_shared/references/modular-assessment.md`

**Files:**
- Create: `modular-programming/_shared/references/modular-assessment.md`

**Interfaces:**
- Produces: reference file cited by Task 3's SKILL.md as `../_shared/references/modular-assessment.md`.

- [ ] **Step 1: Write the file with exactly this content**

````markdown
# Modular Assessment

Use this rubric to judge how modular a project actually is. Directory structure alone proves nothing: a repo full of module folders can still be one tangled monolith. Every dimension below is judged from real code evidence.

## Evidence Requirements

- Every conclusion must point to concrete code locations (files, functions, call sites), not folder names.
- Mark each finding `verified` (you read the code / ran the command) or `inferred` (pattern suggests it); never present a guess as fact.
- Prefer a small number of load-bearing examples over exhaustive listings.
- An assessment that only describes the directory tree is a defect, not a deliverable.

## Assessment Dimensions

1. **Responsibility clarity** — can each module's job be stated in one sentence, plus what it does NOT do? Does its code serve one goal? Any god-modules?
2. **Contract clarity** — is there an explicit public entry? Is the public surface small and stable? Are internals leaked? Are inputs/outputs/errors defined?
3. **Dependency complexity** — how many dependencies per module; are they one-directional, explicit, acyclic; any hidden deps via globals or direct infrastructure calls?
4. **Change blast radius** — how many modules does an ordinary requirement touch? Does swapping a cache/database/format ripple into unrelated modules?
5. **Independent testability** — can a module be tested without booting the whole system, with external dependencies replaced, against its own behavior?
6. **Replaceability** — can the database, cache, an algorithm, or an external service implementation be swapped without editing callers?
7. **Independent comprehensibility** — can a newcomer understand one module by reading it alone? Clear entry point, concentrated core flow, few cross-module jumps?
8. **Data ownership clarity** — one owning module per core datum; no cross-module direct writes; state changes flow through one mechanism.
9. **Deployment/runtime independence** (large systems only) — independent deploy/scale/upgrade, fault isolation. A monolith can still score high overall; independent deployment is not a universal goal.
10. **Architecture constraint strength** — explicit dependency rules, tooling that catches illegal imports/cycles, module design docs, and adherence in new code.

## Maturity Levels

**Low** — many globals; files call each other freely; several modules mutate shared state; business code hits database/cache directly; widespread cycles; any change ripples globally; nothing testable in isolation. Directory splits exist but the system is one organism.

**Medium** — basic responsibility split and some public interfaces; parts testable in isolation; but shared state and cross-module reach-ins persist; infrastructure and business only partly separated; some changes still blast wide. Foundations exist; boundaries not yet stable.

**High** — clear responsibilities and dependency directions; stable contracts; replaceable internals; explicit data ownership; most modules independently testable; local blast radius; enforced constraints; new features land by composing or extending modules.

## Checklist

1. Can every module's responsibility be stated in one sentence?
2. Does every module state what it is NOT responsible for?
3. Does every module have a stable public contract?
4. Does anything outside access a module's internals directly?
5. Are there dependency cycles between modules?
6. Are dependencies explicitly declared?
7. Is there significant global mutable state?
8. Does every piece of core data have exactly one owning module?
9. Can modules be tested independently?
10. Can internal implementations be replaced?
11. Does changing one module force changes in many unrelated ones?
12. Does business code depend directly on database/cache/framework?
13. Are cross-module flows orchestrated by the application layer?
14. Is there a bloating common/shared/utils module?
15. Do tools or rules block illegal dependencies?
16. Can a new developer understand one module in isolation?
17. Can a new feature land by extending one module?
18. Can a module be replaced without touching its callers?

Score pragmatically: the more "healthy" answers with verified evidence, the higher the maturity. Report the 3-5 worst pain points ranked by blast radius, each with its evidence.
````

- [ ] **Step 2: Verify structure**

Run: `grep -c "^## " modular-programming/_shared/references/modular-assessment.md && grep -c "^[0-9]*\." modular-programming/_shared/references/modular-assessment.md`
Expected: heading count `4`; numbered lines ≥ 28 (10 dimensions + 18 checklist items).

- [ ] **Step 3: Commit**

```bash
git add modular-programming/_shared/references/modular-assessment.md
git commit -m "Add modular assessment rubric shared reference"
```

### Task 3: Create the `modular-architect` skill

**Files:**
- Create: `modular-programming/modular-architect/SKILL.md`
- Create: `modular-programming/modular-architect/agents/openai.yaml`

**Interfaces:**
- Consumes: `../_shared/references/modular-methodology.md` and `../_shared/references/modular-assessment.md` (Tasks 1-2).
- Produces: skill directory referenced by Task 4's exposure edits as `modular-architect`.

- [ ] **Step 1: Write `modular-programming/modular-architect/SKILL.md` with exactly this content**

````markdown
---
name: modular-architect
description: Advanced advisory role with built-in modular design thinking. Use when the user wants a modularity assessment of an existing codebase, a staged legacy modularization/refactoring proposal, or a collaborative modular design proposal for a new project — including projects that have NOT adopted the modular workflow; outputs proposals and reports only, never implements or edits baselines; Chinese triggers include 模块化架构师, 模块化评估, 模块化程度, 重构方案, 模块化重构, 模块化设计方案, 模块划分讨论, 架构咨询.
---

# Modular Architect

Act as the advanced advisory role between "an idea or a legacy codebase" and "an accepted modular proposal" — the thinking counterpart of `modular-autopilot` (which executes accepted designs). Work as a conversational design partner: ask key questions one at a time (system capabilities, data ownership, sources of change), converge step by step, and get explicit user confirmation before finalizing any proposal.

Hard boundaries:

- Proposals only. Never implement, refactor, update architecture baselines, or mark anything `implemented`.
- Reading code follows diagnostic-mode discipline (see `modular-workflow-rules.md`): read, run tests, gather evidence — no structural edits.
- The target project does NOT need to have adopted the modular workflow.
- This is an advanced entry, not one of the four primary entries.

## Required References

Read:

- `../_shared/references/modular-methodology.md` (core thinking corpus)
- `../_shared/references/modular-assessment.md` (assessment rubric and evidence rules)
- `../_shared/references/modular-workflow-rules.md` (diagnostic mode, levels, routing)

Do not restate the corpus in conversation; apply it.

## Deliverables

### 1. Modularity Assessment Report

Follow `modular-assessment.md`: judge each dimension from real code evidence (files, functions, call sites), mark findings `verified`/`inferred`, give a low/medium/high maturity rating, and rank the 3-5 worst pain points by blast radius. Never conclude from directory structure alone.

Save to `docs/modularization/<YYYY-MM-DD>-assessment.md` in both modes (an assessment is an evidence snapshot, not a baseline fact — it never goes into `architecture/`). In workflow mode, also add one PM note pointing to it.

### 2. Legacy Modularization Proposal

Built on top of an assessment (run one first if none exists). Structure:

- behavior-baseline requirements (tests, samples, metrics that must exist before refactoring starts);
- staged roadmap where every stage is one module closed loop: confirm responsibility -> define contract -> wrap/migrate -> update callers -> test -> delete old code;
- data-ownership migration order;
- risks, rollback, and per-stage verification signals.

Landing: in workflow mode write it as `architecture/changes/<YYYY-MM-DD>-<change>.md` with `status: proposed` and hand it to the existing L3 path (`modular-review` -> decision summary -> human acceptance -> `modular-change` / `modular-autopilot`). In standalone mode present it in conversation first, then save to the user's chosen location (default `docs/modularization/<YYYY-MM-DD>-<topic>.md`).

### 3. New Project Modular Design Proposal

Structure: system capability list -> module draft (responsibility / non-goals / owned data / public contract / dependency direction) -> dependency rules and assembly entry conventions -> an explicit YAGNI check (what was deliberately NOT designed). Field names intentionally align with `main-design.md` plus module docs so an accepted proposal converts directly into a baseline via `modular-init` / `modular-architecture`.

## Modes

**Standalone advisory** (project not in the workflow): understand goals -> read code / assess -> discuss -> finalize. Deliverables go to `docs/modularization/` (or wherever the user chooses) after explicit confirmation. Recommend `modular-init` as the next step when the user wants the proposal to become a live baseline — but a proposal is complete and usable without adoption.

**In-workflow** (PM/architecture structure exists): assessments get a PM note; legacy proposals become proposed architecture changes on the L3 path; new-project designs feed `modular-architecture` baseline creation. The architect never edits the baseline and never marks its own proposals accepted or implemented — proposer and executor stay separate roles.

## Process

1. Clarify the goal: assessment, legacy refactoring proposal, or new-project design.
2. Ask the load-bearing questions one at a time; prefer concrete options over open prompts.
3. For existing code: read it under diagnostic-mode discipline before forming opinions; collect evidence per `modular-assessment.md`.
4. Present findings/drafts in sections and confirm direction before writing the final document.
5. Save the deliverable to its landing place (see Deliverables) only after user confirmation.
6. Hand off: recommend the next skill (`modular-init`, `modular-review`, `modular-change`, or `modular-autopilot`) without invoking it uninvited.

## Boundary With `modular-architecture`

`modular-architect` discusses and proposes (assessment, roadmap, design draft); `modular-architecture` executes on architecture facts (writes baselines, migrates maps, maintains ADRs and optional graphs). When a proposal is accepted, the architect hands off rather than landing it itself.
````

- [ ] **Step 2: Write `modular-programming/modular-architect/agents/openai.yaml` with exactly this content**

```yaml
interface:
  display_name: "Modular Architect"
  short_description: "Assess modularity and co-design modular refactoring or new-project proposals"
  default_prompt: "Use $modular-architect to assess this project's modularity and discuss a staged modularization proposal with me."
```

- [ ] **Step 3: Verify front matter and reference paths resolve**

Run: `python3 -c "
from pathlib import Path
t = Path('modular-programming/modular-architect/SKILL.md').read_text()
assert t.startswith('---'), 'front matter missing'
for ref in ['modular-methodology.md','modular-assessment.md','modular-workflow-rules.md']:
    p = Path('modular-programming/_shared/references')/ref
    assert p.exists(), f'missing {p}'
    assert ref in t, f'SKILL does not cite {ref}'
print('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add modular-programming/modular-architect
git commit -m "Add modular-architect advanced advisory skill"
```

### Task 4: Exposure edits and full validation

**Files:**
- Modify: `README.md` (skills table, prompts, skills list, directory tree)
- Modify: `modular-programming/_shared/assets/ai-rules-snippet.md` (advanced entries)
- Modify: `modular-programming/_shared/references/modular-workflow-rules.md` (Routing Quick Reference)

**Interfaces:**
- Consumes: `modular-architect` skill directory (Task 3).

- [ ] **Step 1: README skills table — insert after the `modular-autopilot` row**

New row:

```markdown
| `modular-architect` | 高级：评估项目模块化程度、讨论老项目重构方案或新项目模块化设计（未接入工作流的项目也可用） | 评估报告、分阶段重构方案、模块化设计方案（只提案，不实现） |
```

- [ ] **Step 2: README prompts — after the line `Use $modular-autopilot 执行这份已接受的 L2/L3 设计。` add**

```text
Use $modular-architect 评估这个项目的模块化程度，讨论重构方案。
```

- [ ] **Step 3: README skills list and directory tree — add `modular-architect` after `modular-autopilot` in both the flat list and the `modular-programming/` tree**

- [ ] **Step 4: ai-rules-snippet — in "Internal or advanced entries" add after the `modular-autopilot` line**

```markdown
- `modular-architect`: advanced advisory role for modularity assessment, legacy refactoring proposals, and new-project modular design discussion; proposals only, never implementation.
```

- [ ] **Step 5: Routing Quick Reference — add after the `modular-autopilot` row**

```markdown
| Modularity assessment, refactoring proposal, modular design discussion | `modular-architect` | - | assessment report; staged refactoring proposal; new-project design proposal |
```

- [ ] **Step 6: Consistency check across the three exposure points**

Run: `grep -l "modular-architect" README.md modular-programming/_shared/assets/ai-rules-snippet.md modular-programming/_shared/references/modular-workflow-rules.md | wc -l`
Expected: `3`

- [ ] **Step 7: Full validation suite**

Run:
```bash
python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'
python3 -m unittest discover -s modular-programming/modular-audit/tests
./install.sh --dry-run | grep -c modular-architect
git diff --check
```
Expected: checker `0 error`; unittest `OK`; dry-run count ≥ 1; no whitespace errors.

- [ ] **Step 8: Commit**

```bash
git add README.md modular-programming/_shared/assets/ai-rules-snippet.md modular-programming/_shared/references/modular-workflow-rules.md
git commit -m "Expose modular-architect across README, AI snippet, and routing table"
```
