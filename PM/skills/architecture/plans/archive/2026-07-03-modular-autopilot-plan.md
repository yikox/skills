---
source_design: architecture/changes/2026-07-03-modular-autopilot.md
level: L3
---

# modular-autopilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `modular-autopilot` supervisor skill that takes an accepted L2/L3 change design through intake review → writing-plans → subagent execution → modular closeout autonomously, with a decision log and a final report.

**Architecture:** One new skill directory alongside the existing seven modular-programming skills, plus surgical edits to `modular-change` (acceptance sets `status: accepted`, handoff pointer), the two shared references (plan storage + lifecycle rules), and the modular-audit deterministic checker (new `check_plans` function). An ADR records the two durable decisions.

**Tech Stack:** Markdown skill docs (house style: English body, Chinese triggers in description), Python 3 stdlib for the checker.

## Global Constraints

Copied verbatim from the accepted design (`PM/skills/architecture/changes/2026-07-03-modular-autopilot.md`):

- 技能形态而非 agent 形态：由主会话加载执行（subagent 不能再派发 subagent）。
- push / PR / 任何仓库外可见动作一律不做，报告中给出建议命令由用户执行。
- 计划存放：`architecture/modules/<module>/plans/`（L2）或 `architecture/plans/`（L3），**不放** `changes/` 目录。
- 计划 front matter 含 `source_design:`（设计文档路径）与 `level:`，供 audit 追溯。
- 中途硬停机条件仅两条：SDD BLOCKED 三板斧失效；执行中事实推翻入口审阅结论。
- superpowers 缺席时技能应明确报错并指引安装，不提供内联降级路径。
- 决策日志与 SDD progress ledger 同目录（`.superpowers/sdd/`）。
- Repo commit style: short imperative subject; end message with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

## File Structure

| File | Responsibility |
| --- | --- |
| `modular-programming/modular-autopilot/SKILL.md` | Create — the supervisor skill (all four phases, hard stops, log, report) |
| `modular-programming/modular-change/SKILL.md` | Modify — acceptance sets `status: accepted`; handoff pointer to autopilot (L2 + L3 paths) |
| `modular-programming/_shared/references/storage-schema.md` | Modify — `plans/` directories in layout; plan front matter fields |
| `modular-programming/_shared/references/modular-workflow-rules.md` | Modify — plan storage & lifecycle rules in "Design, ADR, And Plan Boundaries" |
| `modular-programming/modular-audit/scripts/check_modular_project.py` | Modify — new `check_plans` function |
| `modular-programming/modular-audit/SKILL.md` | Modify — one bullet in Audit Checks |
| `PM/skills/architecture/adrs/ADR-2026-07-03-autopilot-as-main-session-skill.md` | Create — ADR for the two durable decisions |

No test framework exists in this repo and introducing one is out of scope; the checker change is verified with disposable CLI fixtures in the scratchpad, following the TDD rhythm (observe the miss first, then implement, then observe the catch).

---

### Task 1: Create the modular-autopilot skill

**Files:**
- Create: `modular-programming/modular-autopilot/SKILL.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: plan storage convention `architecture/plans/<date>-<change>-plan.md` (L3) / `architecture/modules/<module>/plans/<date>-<change>-plan.md` (L2) and plan front matter fields `source_design`, `level` — Tasks 3 and 4 must use these exact paths and field names. Skill name `modular-autopilot` — Task 2's handoff text references it.

- [ ] **Step 1: Write the skill file**

Create `modular-programming/modular-autopilot/SKILL.md` with exactly this content:

````markdown
---
name: modular-autopilot
description: Supervise autonomous execution of an accepted L2/L3 change design through intake review, implementation planning, subagent-driven execution, and modular closeout, with a decision log and final report. Use when the user hands an accepted design over for hands-off execution and wants one confirmation at intake plus a report at the end; Chinese triggers include 自主执行, 托管执行, 监督执行, 交给监督者, 自动落地, 全程代办.
---

# Modular Autopilot

Act as the supervising role between "design accepted" and "change landed". Ask the user for exactly one confirmation at intake; afterwards run planning, execution, and closeout autonomously, log every decision made on the user's behalf, and deliver a final report. Never push, open PRs, or take any externally visible action — put the recommended commands in the report instead.

## Hard Dependencies

This skill requires the superpowers plugin skills `writing-plans`, `subagent-driven-development`, and `using-git-worktrees`. If any of them is unavailable, stop and tell the user to install the superpowers plugin. There is no inline fallback.

## Required References

Read:

- `../_shared/references/modular-workflow-rules.md`
- `../_shared/references/storage-schema.md`
- `../_shared/references/review-rules.md`

## Preconditions

Accept only a change design document whose front matter says `status: accepted` with `review_status: reviewed`. For anything else, refuse and route the user back to `modular-change` / `modular-review`. The design phase is not this skill's job.

## Phase 1: Intake Review (the only human confirmation)

Check three categories before anything else:

1. **Module map correctness.** The design's primary and impacted modules match `architecture/main-design.md` and the modules' `code_paths`; the module map shows no obvious drift from the actual code. Problems stop here — never carry a broken map into the autonomous zone.
2. **Design consistency and plannability.** Target design, contract impact, and validation sections do not contradict each other; no wording is too vague to plan from; an L2 design hides no L3 content (boundary or cross-module contract changes).
3. **Execution prerequisites.** The validation commands the design names actually exist and run; a git worktree can be created; the impacted modules' contract docs exist.

Send the user an intake report: findings, suggestions, and a short outline of how you will execute. Wait for explicit confirmation. After confirmation, do not come back to the user except under Hard Stops.

## Phase 2: Implementation Plan

1. Invoke `superpowers:writing-plans` with the design document, `architecture/main-design.md`, and the impacted modules' docs as the spec.
2. Copy the design's module boundary and contract constraints **verbatim** into the plan's Global Constraints section — subagent-driven-development hands that section to every task reviewer, which makes each reviewer a module-boundary gatekeeper for free.
3. Save the plan to `architecture/modules/<module>/plans/<YYYY-MM-DD>-<change>-plan.md` (L2) or `architecture/plans/<YYYY-MM-DD>-<change>-plan.md` (L3). Never save under a `changes/` directory. The plan front matter must include `source_design:` (pm-root-relative path to the design) and `level:`.
4. Run the plan-vs-design self-review: no task crosses the module boundaries beyond the design's declared impact; every item in the design's Validation section has a matching verification step in the plan; Global Constraints carries all contract constraints.
5. On pass, self-approve and append a decision-log line. Skip writing-plans' execution-handoff question entirely; proceed straight to Phase 3.

## Phase 3: Subagent Execution

1. Create an isolated workspace via `superpowers:using-git-worktrees`.
2. Execute the plan with `superpowers:subagent-driven-development` unmodified: pre-flight plan review, per-task implementer plus task-reviewer, fix loops for Critical/Important findings, final whole-branch review, progress ledger.
3. Where SDD would ask the human to adjudicate a plan-mandated conflict, rule it yourself by "the design document governs", and log the ruling.
4. Do not enter `finishing-a-development-branch`. When the final whole-branch review passes, move to Phase 4.

## Phase 4: Closeout

1. Collect verification evidence against the design's Validation section: SDD ledger, commit range, test output, review verdicts.
2. Update module/architecture baselines and re-render affected graphs (see `modular-architecture` Baseline Update).
3. Mark the design `status: implemented`.
4. Record PM completion with evidence via `modular-status`.
5. Run modular-audit's deterministic checker as a drift self-check; fold findings into the report.
6. Deliver the final report.

When the PM directory lives inside the code repository, perform all modular doc updates (baseline, PM, design status) in the main workspace — never inside the worktree, where they would strand on an unmerged branch. The report then recommends the merge command; note in the PM record that the code merge is pending user action.

## Hard Stops

Only two conditions pause the autonomous zone and return to the user:

1. SDD reports BLOCKED and all three remedies failed: more context, a stronger model, splitting the task.
2. Facts discovered during execution overturn an intake-review conclusion (for example, the code seriously contradicts the module docs). The intake review missed something — stop rather than push through.

Regardless of anything else: never push, never create PRs, never destroy data outside the worktree.

## Decision Log

Append one line per autonomous ruling to `.superpowers/sdd/decision-log.md` (same directory as the SDD progress ledger):

```text
<ISO-8601 time> | <decision> | <reason>
```

Log at minimum: plan self-approval, every plan-mandated conflict ruling, every Minor-finding deferral.

## Final Report

Deliver these sections, in order:

1. **Outcome and evidence** — what landed, commit range, test output, final review verdict.
2. **Decisions made on your behalf** — the decision-log digest, each with its reason, for after-the-fact accountability.
3. **Deviations from the design** — every divergence and how it was handled.
4. **Leftovers** — Minor findings, risks, suggested follow-ups.
5. **Recommended actions** — the exact merge/push/PR commands for the user to run.
````

- [ ] **Step 2: Verify the file parses as a valid skill doc**

Run: `head -5 modular-programming/modular-autopilot/SKILL.md`
Expected: front matter opens with `---`, `name: modular-autopilot`, and a `description:` line.

Run: `grep -c "^## " modular-programming/modular-autopilot/SKILL.md`
Expected: `10` (Hard Dependencies, Required References, Preconditions, Phase 1, Phase 2, Phase 3, Phase 4, Hard Stops, Decision Log, Final Report)

- [ ] **Step 3: Commit**

```bash
git add modular-programming/modular-autopilot/SKILL.md
git commit -m "Add modular-autopilot supervisor skill (L3)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Wire acceptance status and handoff into modular-change

**Files:**
- Modify: `modular-programming/modular-change/SKILL.md:43-51` (L3 flow) and `:55-63` (L2 steps)

**Interfaces:**
- Consumes: skill name `modular-autopilot` from Task 1.
- Produces: the rule "acceptance sets `status: accepted`" that modular-autopilot's precondition depends on.

- [ ] **Step 1: Update the L3 flow block and its trailing paragraph**

In `modular-programming/modular-change/SKILL.md`, replace:

```text
PM start -> modular-architecture creates target change / ADR
-> modular-review -> decision summary (3-8 bullets) -> human acceptance
-> implementation plan -> implement -> verify
-> modular-architecture updates baseline
-> PM complete
```

with:

```text
PM start -> modular-architecture creates target change / ADR
-> modular-review -> decision summary (3-8 bullets) -> human acceptance
-> set design status: accepted
-> implementation plan -> implement -> verify
-> modular-architecture updates baseline
-> PM complete
```

Then, immediately after the existing paragraph "When asking for acceptance, present a decision summary ... not only in a separate earlier message.", append this new paragraph:

```text
On acceptance, set the design front matter to `status: accepted`. From that point the user may hand the design to `modular-autopilot`, which runs implementation planning, subagent execution, and closeout autonomously and reports back; otherwise continue with the steps above.
```

- [ ] **Step 2: Update the L2 steps**

In the same file, replace step 5 and 6 of "L2 Module Change":

```text
5. Ask for user confirmation with a decision summary of 3-8 bullets covering key changes, ambiguities, and risks embedded in the confirmation request itself.
6. Implement only after review passes and the user confirms.
```

with:

```text
5. Ask for user confirmation with a decision summary of 3-8 bullets covering key changes, ambiguities, and risks embedded in the confirmation request itself. On confirmation, set the design front matter to `status: accepted`.
6. Implement only after review passes and the user confirms. Alternatively, hand the accepted design to `modular-autopilot` for autonomous execution and closeout.
```

- [ ] **Step 3: Verify**

Run: `grep -c "modular-autopilot" modular-programming/modular-change/SKILL.md`
Expected: `2`

Run: `grep -c "status: accepted" modular-programming/modular-change/SKILL.md`
Expected: `3` (one in the L3 flow block, one in the L3 paragraph, one in L2 step 5)

- [ ] **Step 4: Commit**

```bash
git add modular-programming/modular-change/SKILL.md
git commit -m "Wire design acceptance status and modular-autopilot handoff into modular-change

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Add plan storage and lifecycle to the shared references

**Files:**
- Modify: `modular-programming/_shared/references/storage-schema.md:7-29` (layout) and end of file
- Modify: `modular-programming/_shared/references/modular-workflow-rules.md:238-244` ("Design, ADR, And Plan Boundaries")

**Interfaces:**
- Consumes: plan path convention and front matter fields (`source_design`, `level`) from Task 1.
- Produces: the documented schema that Task 4's checker enforces.

- [ ] **Step 1: Add `plans/` to the storage layout**

In `storage-schema.md`, replace:

```text
    changes/
      <YYYY-MM-DD>-<architecture-change>.md
    adrs/
      ADR-<YYYY-MM-DD>-<decision>.md
    modules/
      <module-slug>.md
      <module-slug>/
        changes/
          <YYYY-MM-DD>-<module-change>.md
```

with:

```text
    changes/
      <YYYY-MM-DD>-<architecture-change>.md
    plans/
      <YYYY-MM-DD>-<change>-plan.md
    adrs/
      ADR-<YYYY-MM-DD>-<decision>.md
    modules/
      <module-slug>.md
      <module-slug>/
        changes/
          <YYYY-MM-DD>-<module-change>.md
        plans/
          <YYYY-MM-DD>-<change>-plan.md
```

- [ ] **Step 2: Add a Plan Files section to storage-schema.md**

Append at the end of `storage-schema.md`:

```markdown
## Plan Files

Implementation plans are temporary execution aids, not architecture. They live in `plans/` next to their design's `changes/` directory — L3 plans under `architecture/plans/`, L2 plans under `architecture/modules/<module-slug>/plans/`. Never store plans inside a `changes/` directory.

Plan front matter:

| Field | Required | Meaning |
| --- | --- | --- |
| `source_design` | yes | pm-root-relative path to the design the plan implements |
| `level` | yes | `L2` or `L3`, matching the source design |

Archive or delete a plan once its PM completion is recorded; `modular-audit` warns about plans whose source design is already `implemented`.
```

- [ ] **Step 3: Extend the plan boundary rule in modular-workflow-rules.md**

In `modular-workflow-rules.md`, replace:

```text
Use an implementation plan only after the architecture or module design is accepted enough to execute. Plans are temporary execution aids, not source-of-truth architecture.
```

with:

```text
Use an implementation plan only after the architecture or module design is accepted enough to execute. Plans are temporary execution aids, not source-of-truth architecture. Store plans under `plans/` beside the design's `changes/` directory with `source_design` and `level` front matter (see `storage-schema.md` Plan Files), and archive or delete them once PM completion is recorded.
```

- [ ] **Step 4: Verify**

Run: `grep -c "plans/" modular-programming/_shared/references/storage-schema.md`
Expected: at least `4`

Run: `grep -c "source_design" modular-programming/_shared/references/modular-workflow-rules.md`
Expected: `1`

- [ ] **Step 5: Commit**

```bash
git add modular-programming/_shared/references/storage-schema.md modular-programming/_shared/references/modular-workflow-rules.md
git commit -m "Document plan file storage and lifecycle in shared references

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Teach the modular-audit checker about plan files

**Files:**
- Modify: `modular-programming/modular-audit/scripts/check_modular_project.py` (new `check_plans` function; call it in `main()` after `check_designs(pm)`)
- Modify: `modular-programming/modular-audit/SKILL.md:30-46` (Audit Checks list)

**Interfaces:**
- Consumes: plan path convention and front matter fields from Tasks 1/3.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: Build a failing fixture and observe the miss**

```bash
FIX=$(mktemp -d)/pm
mkdir -p "$FIX/architecture/plans"
printf -- '---\ntitle: t\n---\nbody\n' > "$FIX/architecture/plans/2026-07-03-bad-plan.md"
python3 modular-programming/modular-audit/scripts/check_modular_project.py "$FIX" | grep '\[plans\]'
echo "grep-exit=$?"
```

Expected: no `[plans]` lines, `grep-exit=1` — the checker does not yet see plan files.

- [ ] **Step 2: Implement `check_plans`**

In `check_modular_project.py`, insert after the `check_designs` function (after its final line `error(f"[designs] {rel} review_status 非法: {meta.get('review_status')}")` block ends, before `def check_pm_doc`):

```python
def check_plans(pm: Path) -> None:
    arch = pm / "architecture"
    for pattern in ["plans/*.md", "modules/*/plans/*.md"]:
        for doc in sorted(arch.glob(pattern)):
            meta = parse_front_matter(doc.read_text(encoding="utf-8"))
            rel = doc.relative_to(pm).as_posix()
            if not meta:
                error(f"[plans] {rel} 缺少 front matter")
                continue
            src = meta.get("source_design")
            if not isinstance(src, str) or not src:
                error(f"[plans] {rel} 缺少 source_design")
            elif not (pm / src).exists():
                error(f"[plans] {rel} source_design 路径不存在: {src}")
            else:
                smeta = parse_front_matter((pm / src).read_text(encoding="utf-8"))
                if smeta.get("status") == "implemented":
                    warn(f"[plans] {rel} 的源设计已 implemented，计划应归档或删除")
            if meta.get("level") not in {"L2", "L3"}:
                error(f"[plans] {rel} level 非法: {meta.get('level')}")
```

In `main()`, change:

```python
    check_designs(pm)
    check_pm_doc(pm)
```

to:

```python
    check_designs(pm)
    check_plans(pm)
    check_pm_doc(pm)
```

- [ ] **Step 3: Re-run the failing fixture and observe the catch**

```bash
python3 modular-programming/modular-audit/scripts/check_modular_project.py "$FIX" | grep '\[plans\]'
```

Expected output (two lines):

```text
ERROR   [plans] architecture/plans/2026-07-03-bad-plan.md 缺少 source_design
ERROR   [plans] architecture/plans/2026-07-03-bad-plan.md level 非法: None
```

- [ ] **Step 4: Positive and orphan fixtures**

```bash
printf -- '---\ntitle: d\nstatus: accepted\nreview_status: reviewed\n---\n' > "$FIX/architecture/design.md"
printf -- '---\nsource_design: architecture/design.md\nlevel: L3\n---\n' > "$FIX/architecture/plans/2026-07-03-good-plan.md"
python3 modular-programming/modular-audit/scripts/check_modular_project.py "$FIX" | grep 'good-plan'
echo "grep-exit=$?"
```

Expected: no output, `grep-exit=1` (the valid plan produces neither error nor warning).

```bash
printf -- '---\ntitle: d\nstatus: implemented\nreview_status: reviewed\n---\n' > "$FIX/architecture/design.md"
python3 modular-programming/modular-audit/scripts/check_modular_project.py "$FIX" | grep 'good-plan'
```

Expected output:

```text
WARNING [plans] architecture/plans/2026-07-03-good-plan.md 的源设计已 implemented，计划应归档或删除
```

- [ ] **Step 5: Real-tree regression**

```bash
python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills | grep '\[plans\]'
echo "grep-exit=$?"
```

Expected: no output, `grep-exit=1` — the repo's own plan file (`PM/skills/architecture/plans/2026-07-03-modular-autopilot-plan.md`, front matter `source_design: architecture/changes/2026-07-03-modular-autopilot.md`, `level: L3`) passes cleanly.

- [ ] **Step 6: Add the audit-checks bullet**

In `modular-programming/modular-audit/SKILL.md`, in the "Audit Checks" bullet list, insert after the line `- L2/L3 design docs are indexed and status-synchronized;`:

```text
- plan files live under `plans/` with valid `source_design` and `level`; plans whose source design is implemented are archive candidates;
```

- [ ] **Step 7: Commit**

```bash
git add modular-programming/modular-audit/scripts/check_modular_project.py modular-programming/modular-audit/SKILL.md
git commit -m "Add plan-file checks to modular-audit (source_design, level, orphan plans)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Record the ADR

**Files:**
- Create: `PM/skills/architecture/adrs/ADR-2026-07-03-autopilot-as-main-session-skill.md`

**Interfaces:**
- Consumes: decisions documented in Tasks 1-2.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: Write the ADR**

Create the file with exactly this content:

```markdown
---
title: ADR-2026-07-03-autopilot-as-main-session-skill
status: accepted
review_status: reviewed
---

# ADR-2026-07-03-Autopilot As Main-Session Skill

## Context

The modular workflow needed a supervisor role that takes an accepted L2/L3 design through planning, execution, and closeout without per-step human confirmation. Two durable questions: (1) what form the supervisor takes, given it must dispatch subagent-driven-development's implementer/reviewer subagents; (2) how removing per-step confirmations squares with the interaction-profile safety floor in `modular-workflow-rules.md`.

## Decision

1. The supervisor is a **skill loaded by the main session** (`modular-autopilot`), not an agent: subagents cannot dispatch further subagents, so an agent-shaped supervisor would be unable to run subagent-driven-development.
2. Authorization is **front-loaded into one intake confirmation**: the user accepts the design (modular-change) and then confirms the intake review once; the autonomous zone replaces later confirmations with a decision log, two hard-stop conditions (unresolvable BLOCKED; facts overturning intake conclusions), a ban on push/PR/external actions, and a final accountability report. The safety floor is unaffected because L3 direction acceptance and module map approval still happen before autopilot starts.

## Alternatives Considered

| Alternative | Reason Not Chosen |
| --- | --- |
| Supervisor as `.claude/agents` agent | Cannot dispatch SDD's subagents (no nested subagent dispatch); execution phase would stall. |
| Rebuild planning as a modular-plan skill | Reinvents and must maintain writing-plans' quality rules; poor cost/benefit. |
| Hardcode the superpowers call sequence into modular-change docs | Keeps every per-step human confirmation; cannot deliver one-authorization autonomous execution. |

## Consequences

- Hard dependency on the superpowers plugin (writing-plans, subagent-driven-development, using-git-worktrees); plugin upgrades can shift the seams and the end-to-end rehearsal must be re-run after upgrades.
- The intake review is the single defense before the autonomous zone; its checklist lives in the skill and the "facts overturn intake" hard stop is the backstop.

## Follow-Up

- Run the end-to-end and negative-path rehearsals listed in the design's Validation section on a real L2 change.
```

- [ ] **Step 2: Verify the ADR passes the checker**

```bash
python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills | grep 'ADR-2026-07-03'
echo "grep-exit=$?"
```

Expected: no output, `grep-exit=1` (valid front matter, no `[designs]` errors for the ADR).

- [ ] **Step 3: Commit**

```bash
git add PM/skills/architecture/adrs/ADR-2026-07-03-autopilot-as-main-session-skill.md
git commit -m "Add ADR: autopilot as main-session skill with front-loaded authorization

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Post-Plan Validation (manual, after all tasks)

From the design's Validation section — these are interactive rehearsals, not plan tasks:

1. End-to-end rehearsal: run a real L2 change through intake review → confirmation → plan → SDD → closeout → report; check decision-log and report completeness.
2. Negative path: feed a design with a module-map error, confirm intake blocks it; simulate BLOCKED with all three remedies failing, confirm hard stop instead of pushing through.
