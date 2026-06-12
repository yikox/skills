# Personal Skills

This repository stores reusable agent skills. Each top-level directory that
contains a `SKILL.md` file is treated as one installable skill.

## Included Skills

- `notes-project-memory`: Store, retrieve, and update durable project memory in
  Markdown notes.

## Install

Run the installer from the repository root:

```sh
./install.sh
```

By default, it copies every skill in this repository into these common agent
skills directories:

```text
~/.codex/skills
~/.claude/skills
~/codex/skills
~/claude/skills
```

You can preview changes first:

```sh
./install.sh --dry-run
```

You can also choose explicit target directories:

```sh
./install.sh ~/.codex/skills ~/.claude/skills ~/my-agent/skills
```

The installer uses `rsync --delete` for each skill directory, so the repository
copy is treated as the source of truth for that skill inside each target.

## Add A Skill

Create a new top-level folder with this shape:

```text
my-skill/
  SKILL.md
  references/
  scripts/
  assets/
```

Only `SKILL.md` is required. Optional folders can be added when the skill needs
extra instructions, helper scripts, or reusable assets.
