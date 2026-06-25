# Review Artifact Rules

Use these rules for automatic review before human confirmation.

## Review Modes

Requirement review checks a `Requirements Backlog` / `需求待办` row.

Architecture baseline review checks:

```text
architecture/main-design.md
architecture/modules/<module-slug>.md
```

Design review checks a module change design doc under:

```text
architecture/modules/<module-slug>/changes/<YYYY-MM-DD>-<change-slug>.md
```

## Requirement Checklist

Verify that the requirement has:

- stable ID and date;
- clear user or project goal;
- expected behavior or outcome;
- primary module from architecture docs, or an explicit candidate/unknown marker;
- modification summary as current-to-target behavior;
- scope and non-goals when relevant;
- impact points for modules, workflows, data/state, API/contracts, UI, tests, operations, migration, or compatibility;
- acceptance criteria or validation signal;
- status that matches completeness;
- concise next step or open question.

Safe fixes:

- fill missing module names from architecture docs when there is only one clear owner;
- move scattered notes into module, change summary, scope/impact, or next-step fields;
- change status to `needs-clarification` when required intake fields are missing;
- change status to `ready-for-design` only when the quality bar is met.

Human questions:

- competing module owners;
- missing non-goals or acceptance criteria that affect scope;
- unclear user intent, data semantics, compatibility, or product tradeoff.

## Architecture Baseline Checklist

Verify that baseline architecture docs have:

- clear system scope and module map in `architecture/main-design.md`;
- module docs for indexed modules in `project-management.md`;
- module responsibilities, boundaries, contracts, data/state, dependencies, and constraints;
- diagrams that have already passed diagram validation when diagrams are present;
- separation between current/accepted baseline and future plans;
- assumptions marked explicitly when facts are not verified from code or user input;
- PM `Design Documents` / `设计文档` index rows that point to existing files;
- no implementation plan, pending-change queue, or speculative roadmap content in baseline docs.

Safe fixes:

- add missing links between main design and module docs when paths are obvious;
- correct PM index paths or module names when the file layout is clear;
- move future work notes out of baseline text into open questions or PM backlog references;
- label unverified claims as assumptions;
- add `Review Notes` / `Open Questions` for unresolved module, data, security, privacy, migration, or compatibility questions.

Human questions:

- unverified current-code claims;
- module boundary disputes;
- target architecture that is not yet accepted;
- data ownership, persistence, privacy, security, migration, rollback, observability, accessibility, or performance implications that are not documented.

## Design Checklist

Verify that the change design has:

- requirement ID and PM row reference;
- module matching the requirement's primary module or a documented reason for different ownership;
- current state separated from target design;
- target behavior that satisfies the requirement without expanding scope silently;
- in-scope and out-of-scope boundaries;
- impacted modules and contract/data/UI/test impacts;
- implementation plan at design level, not overly low-level code churn;
- testing and validation strategy;
- security, privacy, compatibility, migration, rollback, observability, accessibility, and performance impact notes when relevant;
- risks and open questions;
- lifecycle sync table matching PM;
- review status.

Safe fixes:

- add missing PM paths, requirement IDs, or design index links from clear sources;
- correct module/status mismatches when the source of truth is obvious;
- move unanswered issues into `Open Questions` or `Review Findings`;
- add missing `Review status` or lifecycle sync rows;
- mark `Review status: reviewed` only when no human questions remain.

Human questions:

- architecture tradeoffs;
- module ownership conflicts;
- acceptance criteria changes;
- compatibility or migration decisions;
- privacy, security, data retention, rollback, observability, accessibility, or performance tradeoffs;
- risky implementation sequencing;
- claims about current code behavior that lack evidence.

## Review Findings Format

For design docs, add or update:

```markdown
## Review Findings

| Type | Finding | Resolution |
| --- | --- | --- |
| fixed |  |  |
| needs-human |  |  |
```

Use `fixed` for corrections already made. Use `needs-human` for unresolved questions.

For requirement rows, keep findings concise in `Next Step / Notes` / `下一步 / 备注`.
