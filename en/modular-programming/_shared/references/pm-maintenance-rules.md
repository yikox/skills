# PM Maintenance Rules

Use these rules when archiving finished PM rows (`modular-status`) or when auditing and compressing an oversized `project-management.md` (`modular-audit`). The goal is a PM file where current state is visible at a glance without losing traceability.

## Archive Principles

- Archive is a location or section, not a lifecycle status.
- Keep the final lifecycle status visible, such as `implemented`, `obsolete`, or the project's equivalent wording.
- Preserve dates, requirement IDs, architecture patch commits, optional proposal paths, implementation commits, PRs, release notes, or user-confirmed evidence.
- Prefer moving rows to an archive section over deleting them.
- Do not archive anything whose next action is still active, blocked, or unclear.

## Archive Candidates

- Active tasks marked done/completed after the outcome is summarized in Recent Updates or a release/milestone section.
- Requirement rows marked `implemented` with implementation evidence or explicit user confirmation.
- Requirement rows marked `obsolete` with a brief reason.
- Optional proposal index rows marked `implemented` or `obsolete`.
- Stale rows identified by `modular-audit` and confirmed by evidence or the user.

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

Keep `architecture/main-design.md` and module baseline docs indexed in the Modular Design Index. Archive only optional proposal index rows by default. Branch-carried architecture patch commits are PM evidence, not design index rows.

## Archive Sections

Use existing section names when present. Otherwise add only the archive sections needed:

- `Requirements Archive` / `需求归档`
- `Design Archive` / `设计归档`
- `Task Archive` / `任务归档`

For small projects, a single `Archive` / `归档` section with compact tables is enough.

## Optional Proposal File Movement

Do not move proposal files by default. Moving files can break PM links and future agent context.

If the user explicitly asks to move old proposal files:

1. Move them to a stable archive path such as `architecture/modules/<module>/changes/archive/`.
2. Update every PM path, requirement row, module doc link, and design cross-reference.
3. Run `modular-audit` after the move.

## Compression Triggers

Recommend compression when one or more are true:

- `project-management.md` is hard to scan because current state is buried under history.
- The file is larger than about 25 KB, or a single line/update is longer than about 1,000 characters.
- `Recent Updates` / `最近更新` has more than 8-12 entries or contains implementation/debug narratives.
- `Milestones` / `里程碑` repeats release notes that already live in release pages, optional proposal docs, commits, or `knowledge-summary.md`.
- Old completed work dominates the file while active tasks, blockers, requirements, and next steps are small.

## Preserve In Main File

Keep these visible in `project-management.md`:

- project overview and current status;
- current version, latest release status, and active blocker;
- active tasks, current focus, and next concrete steps;
- open risks and blockers;
- requirements backlog and modular design index;
- active roadmap/todo items;
- recent 5-8 updates as concise outcome-oriented bullets;
- links to archive/history files where details moved.

Do not remove stable IDs, dates, architecture patch commits, optional proposal paths, release URLs, commit SHAs, tags, PR links, blocker evidence, or user-confirmed implementation evidence.

## Evidence Single Home

This is a **write-time** rule: evidence goes into exactly one home at the moment it is written, instead of being written in several places and compressed later.

- Each piece of evidence has one home:
  - L2/L3 work using the default branch architecture patch — evidence is one PM completion pointer to the architecture patch commit plus implementation commit/PR;
  - work with an optional proposal — validation and implementation evidence goes only into that proposal's Validation / Implementation sections, or into an archived execution artifact if the proposal is not kept active;
  - work without an optional proposal (L0/L1) — evidence is a single `Recent Updates` line (outcome plus verification command or commit).
- All other PM sections (Active Tasks notes, Archive evidence column, design index notes, Current Status) hold one line of outcome plus a pointer (patch commit / implementation commit / optional proposal / requirement ID) — no command litanies, no implementation narratives.
- A given fact appears in at most one section of the PM main file. Lifecycle transitions (an Active Task finishing and entering Archive) **move** the row; they do not copy it.
- If branch-patch work still needs long-lived explanation beyond one PM evidence line and commit messages, treat that as a signal for an optional proposal or archived execution artifact.

## Lightweight PM Pattern

Routine L1 work should not make the PM file noisy. Prefer a single outcome-oriented note in `Recent Updates` when future context needs it:

```markdown
- 2026-07-04 - 修复 checker 对 group interface provider 越界未拦截的问题；验证 `python3 -m unittest discover -s modular-programming/modular-audit/tests` 通过。
```

Use `Active Tasks` for L1 only when the work crosses sessions, carries notable risk or release evidence, is part of an existing active task, or the user explicitly asks for tracking.

## Move Or Condense

Move or summarize these:

- older `Recent Updates` details;
- long per-release implementation narratives;
- detailed debugging root causes and test logs;
- repeated CI/build/release procedure notes;
- lessons learned that are reusable across future work;
- completed active task details already represented in milestones, release notes, optional proposal docs, or commits.

Use the destination that preserves future usefulness:

- `knowledge-summary.md`: reusable commands, root causes, testing/deploy workflows, environment constraints, conventions, and lessons.
- `architecture/...`: durable architecture facts, module boundaries, ADRs, optional proposal archives, and implemented baseline updates.
- `archives/project-management-history-YYYY.md`: historical PM update details that are not current state but should remain traceable.
- Release pages, changelogs, commits, or PRs: external evidence already exists; keep only a compact pointer in PM.

## Archive File Format

When moving detailed history out of the main file, create or append to:

```text
archives/project-management-history-YYYY.md
```

Use this shape:

```markdown
# Project Management History YYYY

Source: project-management.md
Compressed on: YYYY-MM-DD

## YYYY-MM

- YYYY-MM-DD - Original detailed update or a faithful condensed version.
```

Preserve enough detail to recover why a decision was made. Do not move secrets or temporary scratch content.

## Main File Compression Pattern

Replace long entries with compact bullets:

```markdown
## 最近更新

- 2026-06-25 - 修复列表块编辑态 4 个交互问题，提交 `e4b39be`，测试 629 绿；详细根因和实现过程已归档到 `archives/project-management-history-2026.md`。
- 2026-06-24 - 完成列表块块内子块渲染并合并到 main；patch `abc1234`，实现 `def5678`。
```

Compress current-status sections to the facts a future agent needs first:

```markdown
- Current version: 0.4.11; local macOS dmg exists.
- Latest public GitHub Release: v0.4.8.
- v0.4.9-v0.4.11 are blocked from full release by CI billing/spending limit.
- Current focus: editor and AI conversation experience.
```

For `Milestones` / `里程碑`, keep version/date/outcome only. Put implementation details in compact Recent Updates notes, optional proposal docs, commits/PRs, or archive history.

## Compression Procedure

1. Read `project-management.md`, `knowledge-summary.md`, relevant architecture docs, and any existing `archives/project-management-history-*.md`.
2. Identify current-state sections versus historical sections.
3. Build a preservation checklist:
   - current version and release status;
   - active blockers and risks;
   - active tasks and next steps;
   - open requirements and accepted architecture patches/proposals;
   - latest useful updates;
   - all links/IDs/evidence that must remain reachable.
4. Draft the compressed main file in the same language and heading style as the existing PM.
5. Move older details to archive/history files, knowledge docs, optional proposal docs, or commits/PRs as appropriate.
6. Add compact pointers from `project-management.md` to any archive/history file.
7. Run `modular-review` on the changed PM afterwards.
8. Report before/after size, sections compressed, archive files created/updated, and any facts intentionally left in main.

## Safety Rules

- Do not compress by deleting evidence. Move or summarize with a link.
- Do not compress unresolved blockers, active requirements, active tasks, active architecture patches/proposals, or current focus into archive-only history.
- Do not rewrite project meaning or status while summarizing.
- Do not mark work complete, accepted, obsolete, or implemented as part of compression unless evidence already supports it.
- Prefer small section-level edits over full rewrites.
- Ask the user before moving large amounts of history if the request was only an audit, not an explicit compression request.
