# Personal Skills

This repository stores reusable agent skills. Skills may be grouped into suite
folders; any directory that contains a `SKILL.md` file is treated as one
installable skill.

## Included Skills

### project-memory

- `pm-init`: Set up durable project memory rules in project AI
  collaboration docs and reuse or create external memory notes.
- `pm-track-status`: Maintain external `project-management.md` notes
  for project status, commit checkpoints, releases, milestones, testing,
  deployment, risks, and ADR summaries.
- `pm-record-requirement`: Clarify new requirements and record them in the PM
  requirement backlog before design.
- `pm-review-artifact`: Automatically review PM requirements, architecture
  docs, and design docs before human confirmation, fixing clear defects and
  listing open questions.
- `pm-groom-roadmap`: Groom PM requirements, priorities, current focus,
  roadmap, and milestones.
- `pm-record-knowledge`: Maintain external `knowledge-summary.md` notes
  for verified commands, architecture facts, conventions, troubleshooting,
  investigation results, and lessons learned.
- `pm-audit-memory`: Audit PM notes for stale tasks, missing design links,
  lifecycle mismatches, and architecture baseline drift.
- `pm-migrate-memory`: Migrate older PM notes, AI rules, design indexes, and
  lifecycle fields to the current `pm-*` schema.
- `pm-document-architecture`: Create and maintain baseline
  `architecture/main-design.md` and module architecture design docs, with PM
  design-document indexing, Mermaid-safe architecture diagrams, and SVG-first
  UI schematic diagrams.
- `pm-design-requirement`: Convert PM requirements or active tasks into
  module-scoped change design docs, write the design paths back to PM, and mark
  designs landed after implementation.

Existing documents created by the previous `notes-project-memory` skill are
still reused by `pm-init`; the legacy skill itself is no longer
installed as a separate capability.

## Install

Run the installer from the repository root:

```sh
./install.sh
```

By default, it copies every skill in this repository into these common agent
skills directories:

```text
~/.agents/skills   # Codex user skills, per current Codex docs
~/.codex/skills    # Codex app/local skills observed on this machine
~/.claude/skills   # Claude Code personal skills
```

`~/codex/skills` and `~/claude/skills` are not included because I did not find
documentation or local evidence that those no-dot paths are default skills
locations.

You can preview changes first:

```sh
./install.sh --dry-run
```

You can also choose explicit target directories:

```sh
./install.sh ~/.agents/skills ~/.claude/skills ~/my-agent/skills
```

The installer uses `rsync --delete` for each skill directory, so the repository
copy is treated as the source of truth for that skill inside each target.

## Agent Paths Checked

- Codex: current Codex documentation says user skills live at
  `~/.agents/skills`; repository skills live under `.agents/skills`.
  This machine also has active Codex skills under `~/.codex/skills`, so the
  installer includes both Codex targets.
- Claude Code: personal skills live at
  `~/.claude/skills/<skill-name>/SKILL.md`; project skills live at
  `.claude/skills/<skill-name>/SKILL.md`.
- Cursor: Cursor does not use `SKILL.md` skill folders as its rules format.
  Cursor uses Project Rules in `.cursor/rules` with `.mdc` files, User Rules in
  Cursor Settings, and also supports `AGENTS.md`. Keep Cursor conversion
  separate instead of copying this repository directly into a Cursor directory.

Useful references:

- Codex Agent Skills: <https://developers.openai.com/codex/skills>
- Claude Code Skills: <https://code.claude.com/docs/en/skills>
- Cursor Rules: <https://cursor.com/docs/rules>

## Add A Skill

Create a new folder with this shape, either at the repository root or inside a
suite folder:

```text
my-suite/
  my-skill/
    SKILL.md
    references/
    scripts/
    assets/
```

A standalone skill can also live at the repository root:

```text
my-skill/
  SKILL.md
  references/
  scripts/
  assets/
```

Only `SKILL.md` is required. Optional folders can be added when the skill needs
extra instructions, helper scripts, or reusable assets.

## Maintain PM Skill References

When editing duplicated PM reference files, run:

```sh
python3 scripts/check_pm_reference_sync.py
```

## Lint A PM Project

For a deterministic first pass over one external PM project folder, run:

```sh
python3 scripts/check_pm_project.py /path/to/PM/project-slug
```

This checks requirement/design traceability, broken local design links,
architecture baseline placement, review status, and implementation evidence
consistency.
