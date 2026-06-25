# PM Archive Rules

Use these rules when cleaning active PM sections without losing traceability.

## Principles

- Archive is a location or section, not a lifecycle status.
- Keep the final lifecycle status visible, such as `implemented`, `obsolete`, or the project's equivalent wording.
- Preserve dates, requirement IDs, design paths, commits, PRs, release notes, or user-confirmed evidence.
- Prefer moving rows to an archive section over deleting them.
- Do not archive anything whose next action is still active, blocked, or unclear.

## Archive Candidates

- Active tasks marked done/completed after the outcome is summarized in Recent Updates or a release/milestone section.
- Requirement rows marked `implemented` with implementation evidence or explicit user confirmation.
- Requirement rows marked `obsolete` with a brief reason.
- Change design index rows marked `implemented` or `obsolete`.
- Stale rows identified by `pm-audit-memory` and confirmed by evidence or the user.

## Suggested Sections

Use existing section names when present. Otherwise add only the archive sections needed:

- `Requirements Archive` / `需求归档`
- `Design Archive` / `设计归档`
- `Task Archive` / `任务归档`

For small projects, a single `Archive` / `归档` section with compact tables is enough.

## What Not To Archive

Do not archive rows with these active statuses unless the user explicitly cancels them:

- `needs-clarification`
- `ready-for-design`
- `designing`
- `designed`
- `accepted`
- `implementing`
- `blocked`
- `needs-review`

Keep `architecture/main-design.md` and module baseline docs indexed in `Design Documents`. Archive only change design index rows by default.

## File Movement

Do not move design files by default. Moving files can break PM links and future agent context.

If the user explicitly asks to move old design files:

1. Move them to a stable archive path such as `architecture/modules/<module>/changes/archive/`.
2. Update every PM path, requirement row, module doc link, and design cross-reference.
3. Run `pm-audit-memory` after the move.
