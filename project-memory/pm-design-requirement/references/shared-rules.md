# Shared Rules

Resolve notes paths using project AI docs first, then environment variables and config.

Priority:

1. User-provided path in the current request.
2. Existing `Project Memory` rules in `AGENTS.md`, `.codex/AGENTS.md`, `.agents/AGENTS.md`, `CLAUDE.md`, or `.claude/CLAUDE.md`.
3. `PROJECT_MEMORY_ROOT` as the direct `PM` root.
4. `NOTES_WORKSPACE`, `NOTES_ROOT`, or `MARKDOWN_NOTES_ROOT` as the notes root; use its `PM/` child.
5. `~/.config/project-memory/config.json` or `~/.config/notes-project-memory/config.json`.
6. GitNote `~/.gitnote/config.json` `activeWorkspace`.

Use `PM/<project-slug>/project-management.md`. Reuse existing files from `notes-project-memory`; do not rename old project folders. If no path can be resolved safely, ask the user for the notes root.

Before writing:

- Read the target file first.
- Preserve user-written sections and wording unless obsolete or contradicted by verified facts.
- Prefer section-level edits over full rewrites.
- Avoid duplicate bullets; merge related facts.
- Include dates for status changes, releases, commit checkpoints, risks, milestones, ADRs, and design-document changes.
- Do not store secrets, credentials, access tokens, private keys, or temporary scratch notes.

After writing, report the project folder, changed file, whether it was created or updated, and any ambiguity that remains.
