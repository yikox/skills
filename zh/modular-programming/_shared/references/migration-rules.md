# Modular Migration Rules

Use these rules when replacing older project-memory or architecture-design documents with the modular programming workflow.

## Migration Goal

Create a trustworthy architecture-first baseline before planning refactors. Migration is not a license to rewrite code.

## Existing Project Flow

1. Inspect repository structure, entry points, runtime configuration, tests, data/state stores, IO boundaries, generated artifacts, and docs.
2. Infer current modules from technical ownership boundaries, not just folder names.
3. Mark each module fact as `verified`, `inferred`, or `unclear`.
4. Write `architecture/main-design.md` and `architecture/modules/*.md`, including `code_paths` for each module (single ownership; see Code Ownership in `modular-workflow-rules.md`).
5. Create or update the architecture graph only when the user wants visualization or the project uses graph review.
6. Move old TODOs, requirements, active work, and known bugs into PM rows with primary module, impacted modules, and change level.
7. Record migration gaps in PM instead of silently guessing.

## Old Skill Names

Treat these as legacy concepts:

- `architecture-design`;
- `pm-init`;
- `pm-document-architecture`;
- `pm-record-requirement`;
- `pm-design-requirement`;
- `pm-track-status`;
- `pm-review-artifact`;
- `pm-audit-memory`;
- `pm-groom-roadmap`;
- `pm-record-knowledge`;
- `pm-migrate-memory`.

Map them to the new modular suite by responsibility:

- initialization and repair -> `modular-init`;
- architecture/module baseline -> `modular-architecture`;
- request intake and change design -> `modular-change`;
- active/completed PM state -> `modular-status`;
- automatic review -> `modular-review`;
- consistency audit and migration -> `modular-audit`;
- reusable knowledge -> `modular-knowledge`.

## No Historical Burden

Preserve only information that is still useful:

- current module facts;
- accepted decisions;
- active or future work;
- implementation evidence;
- reusable operational knowledge.

Archive or omit stale history, duplicate status logs, old workflow descriptions, and obsolete design drafts.
