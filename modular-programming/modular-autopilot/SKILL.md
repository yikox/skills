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
