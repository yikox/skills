# Shared Rules

## Path Resolution

Resolve either a notes root or a `PM` root. Expand `~` and relative paths before use.

Priority:

1. User-provided path in the current request.
2. Existing `Project Memory` rules in `AGENTS.md`, `.codex/AGENTS.md`, `.agents/AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, or similar project AI docs.
3. Environment variables:
   - `PROJECT_MEMORY_ROOT` points directly to the `PM` root.
   - `NOTES_WORKSPACE`, `NOTES_ROOT`, or `MARKDOWN_NOTES_ROOT` points to the notes root; use its `PM/` child.
4. Local config file:
   - `~/.config/project-memory/config.json`
   - `~/.config/notes-project-memory/config.json`
   - Supported JSON keys: `projectMemoryRoot`, `notesRoot`.
5. App-specific fallback:
   - GitNote: read `~/.gitnote/config.json` and use `activeWorkspace` as the notes root.
   - Do not read `~/.gitnote/secrets.json`.
6. If no single safe path is found, ask the user for the notes root and suggest setting `PROJECT_MEMORY_ROOT` or `NOTES_WORKSPACE`.

If a resolved notes root exists but `PM/` does not, create `PM/`. If the configured path does not exist, ask before creating it unless the user explicitly requested that exact path. Do not scan broad personal locations such as the full home directory, iCloud, Documents, or all Obsidian vaults.

## Storage Layout

Use one folder per project under `PM/`.

```text
<notes-root>/
└── PM/
    └── <project-slug>/
        ├── project-management.md
        └── knowledge-summary.md
```

Choose the project folder name in this order:

1. User-provided project name.
2. Existing matching project folder under `PM/`.
3. Existing path found in project AI docs.
4. Current git repository root folder name.
5. Git remote repository name; use `owner-repo` if the plain repo name would collide.
6. Current working directory name.

Prefer lowercase hyphen-case for new project folders. Preserve existing folder names exactly once created.

## Existing Document Compatibility

Reuse existing documents before creating new ones.

Compatible existing files:

- `project-management.md`
- `knowledge-summary.md`
- Files created by the earlier `notes-project-memory` skill with the same names.
- Existing files referenced from `AGENTS.md`, `CLAUDE.md`, `.codex/AGENTS.md`, `.agents/AGENTS.md`, or similar project AI docs.

Do not rename existing documents just to match a preferred slug. If old folder or file names are already referenced by project rules, keep them stable and update the rules only when they are missing or wrong.

## Update Rules

- Read the target file before writing.
- Preserve user-written sections and wording unless they are obsolete or contradicted by verified facts.
- Prefer section-level edits over full rewrites.
- Avoid duplicate bullets; merge related facts.
- Keep content in the user's language; preserve technical terms in their original form.
- Do not store secrets, credentials, private keys, access tokens, or temporary scratch notes.
