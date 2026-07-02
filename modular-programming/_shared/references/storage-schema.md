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
    adrs/
      ADR-<YYYY-MM-DD>-<decision>.md
    modules/
      <module-slug>.md
      <module-slug>/
        changes/
          <YYYY-MM-DD>-<module-change>.md
    graphs/
      current-project.arch.json
      proposed/
        <YYYY-MM-DD>-<change>.arch.json
    rendered/
      current-project-architecture.html
      current-project-architecture.svg
```

## PM Sections

Prefer these sections for new `project-management.md` files. Preserve equivalent existing headings when repairing an old project.

1. Overview
2. Current Status
3. Active Tasks
4. Requirements / Change Backlog
5. Modular Design Index
6. Roadmap
7. Milestones
8. Testing and Validation
9. Blockers and Risks
10. ADR Summary
11. Archive
12. Recent Updates

## Active Task Fields

Use a table or concise bullets that capture:

- date;
- task;
- primary module;
- impacted modules;
- level;
- status;
- next step / notes.

## Backlog Fields

Use a backlog row when the user states a requirement or change that is not yet implemented:

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

## Slug Rules

- Use lowercase ASCII slugs.
- Replace spaces and punctuation with hyphens.
- Keep module slugs stable after PM or design references them.
- Prefer technical ownership names over feature marketing names.

## Status Vocabulary

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
