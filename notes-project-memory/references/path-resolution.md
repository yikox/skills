# Path Resolution

Resolve either a notes root or a `PM` root. Expand `~` and relative paths before use.

## Priority

1. User-provided path in the current request.
2. Environment variables:
   - `PROJECT_MEMORY_ROOT` - points directly to the `PM` root.
   - `NOTES_WORKSPACE`, `NOTES_ROOT`, or `MARKDOWN_NOTES_ROOT` - points to the notes root; use its `PM/` child.
3. Local config file:
   - `~/.config/notes-project-memory/config.json`
   - Supported JSON keys: `projectMemoryRoot`, `notesRoot`.
4. App-specific fallback:
   - GitNote: read `~/.gitnote/config.json` and use `activeWorkspace` as the notes root.
   - Do not read `~/.gitnote/secrets.json`.
5. If no single safe path is found, ask the user for the notes root and suggest setting `PROJECT_MEMORY_ROOT` or `NOTES_WORKSPACE`.

## Write Behavior

- If a resolved notes root exists but `PM/` does not, create `PM/`.
- If the configured path does not exist, ask before creating it unless the user explicitly requested that exact path.
- Do not scan broad locations such as the full home directory, iCloud, Documents, or all Obsidian vaults.
- Do not edit shell profiles or config files to persist a path unless the user explicitly asks.
