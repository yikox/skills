# Modular Storage Schema

Use this schema when creating or repairing modular programming project memory.

## Default Project Memory Layout

```text
PM/<project-slug>/
  project-management.md
  knowledge-summary.md
  architecture/
    main-design.md
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
    graphs/
      current-project.arch.json
      proposed/
        <YYYY-MM-DD>-<change>.arch.json
    rendered/
      current-project-architecture.html
      current-project-architecture.svg
```

The default AI-readable baseline is `architecture/main-design.md` plus `architecture/modules/*.md`. `graphs/` and `rendered/` are optional advanced visualization directories; create them only when the project uses graph review, a user asks for diagrams, or an advanced skill needs them.

## PM Sections

Prefer these sections for new `project-management.md` files. Preserve equivalent existing headings when repairing an old project.

1. Overview
2. Current Status
3. Active Tasks
4. Requirements / Change Backlog
5. Modular Design Index
6. Roadmap (optional: small projects can fold this into Requirements / Change Backlog)
7. Milestones (optional: small projects can fold this into Archive)
8. Blockers and Risks
9. ADR Summary
10. Archive
11. Recent Updates

There is no Testing and Validation section: currently runnable verification commands belong in `knowledge-summary.md`, and per-change validation evidence belongs in the corresponding design doc (see Evidence Single Home in pm-maintenance-rules).

## Active Task Fields

Use a table or concise bullets for active L2/L3 work, and for L1 only when it crosses sessions, carries release/risk evidence, belongs to an active task, or the user explicitly wants tracking. Capture:

- date;
- task;
- primary module;
- impacted modules;
- level;
- status;
- next step / notes.

## Backlog Fields

Use a backlog row when the user states a non-trivial requirement or change that is not yet implemented:

- stable ID;
- date;
- request;
- primary module;
- impacted modules;
- change level;
- change summary;
- scope / impact;
- status;
- priority;
- design path / next step.

## Modular Design Index

Index durable design artifacts:

- Main Architecture: `architecture/main-design.md`;
- Module: `architecture/modules/<module>.md`;
- Architecture Change: `architecture/changes/<date>-<change>.md`;
- ADR: `architecture/adrs/ADR-<date>-<decision>.md`;
- Module Change: `architecture/modules/<module>/changes/<date>-<change>.md`.

Graph JSON and rendered diagrams are optional advanced visualization artifacts. Index them only when a project actively uses graph review or a specific change/design needs visual communication. `main-design.md` and module docs remain sufficient for the default AI workflow.

## Module Frontmatter

Module docs (`architecture/modules/<module>.md`) use this frontmatter:

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | display name |
| `described` | yes | one-sentence responsibility |
| `module_form` | yes | `atomic` or `composite` |
| `module_kind` | yes | see `module-kind-classification.md` |
| `main_subject` | yes | primary technical subject (function, file, format) |
| `code_paths` | yes for new/migrated modules | repo-relative glob list of code this module owns |
| `shared_paths` | no | repo-relative globs this module uses or documents but does not exclusively own |
| `ignored_paths` | no | repo-relative globs intentionally outside module ownership, with explanation in main-design Shared Constraints |
| `status` | yes | design status vocabulary below |
| `review_status` | yes | review status vocabulary below |

`code_paths` follows single ownership: every behavior-bearing code path belongs to exactly one module (see Code Ownership in `modular-workflow-rules.md`). Existing docs without `code_paths` stay valid; `modular-audit` flags them for backfill.
`shared_paths` and `ignored_paths` do not grant ownership; they document exceptions such as shared utilities, framework glue, integration tests, generated output, or repo-level configuration.

## Slug Rules

- Use lowercase ASCII slugs.
- Replace spaces and punctuation with hyphens.
- Keep module slugs stable after PM or design references them.
- Prefer technical ownership names over feature marketing names.

## Status Vocabulary

The enforced enumerated values for `design_status` and `review_status` have a single source of truth in `vocab.md` (parsed by audit-checker); the flows below only explain their ordering and meaning. Requirement/task statuses are descriptive and not machine-enforced.

Requirement/task statuses:

```text
needs-clarification -> ready-for-design -> designing -> designed
  -> accepted -> implementing -> implemented
```

Design statuses:

```text
draft -> proposed -> accepted -> implemented
```

Review statuses:

```text
not-reviewed -> needs-review -> reviewed
```

Use project-native status words when they already exist, but keep the meaning consistent.

## Plan Files

Implementation plans are temporary execution aids, not architecture. They live in `plans/` next to their design's `changes/` directory — L3 plans under `architecture/plans/`, L2 plans under `architecture/modules/<module-slug>/plans/`. Never store plans inside a `changes/` directory.

Plan front matter:

| Field | Required | Meaning |
| --- | --- | --- |
| `source_design` | yes | pm-root-relative path to the design the plan implements |
| `level` | yes | `L2` or `L3`, matching the source design; a plan's directory must match its level (`plans/` holds L3, `modules/<module-slug>/plans/` holds L2) |

Archive or delete a plan once its PM completion is recorded; `modular-audit` warns about plans whose source design is already `implemented`. To archive, move the plan into an `archive/` subdirectory beside it (e.g. `architecture/plans/archive/`); the checker intentionally skips archived plans.
