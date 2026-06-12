# Storage Layout

Use one folder per project under `PM/`.

```text
<notes-root>/
└── PM/
    └── <project-slug>/
        ├── project-management.md
        └── knowledge-summary.md
```

If `PROJECT_MEMORY_ROOT` points directly to `PM/`, start at that folder.

## Project Slug

Choose the project folder name in this order:

1. User-provided project name.
2. Existing matching project folder under `PM/`.
3. Current git repository root folder name.
4. Git remote repository name; use `owner-repo` if the plain repo name would collide.
5. Current working directory name.

Prefer lowercase hyphen-case for new project folders, for example `gitnote` or `owner-repo`. Preserve existing folder names exactly once created.

## File Responsibilities

`project-management.md`:

- Project overview and status
- Version or release state
- Active tasks and current focus
- Milestones and roadmap
- Todo list
- Blockers, risks, and decisions that affect planning
- Recent updates

`knowledge-summary.md`:

- Verified build, test, release, deploy, and troubleshooting commands
- Architecture facts and project structure
- Code conventions and recurring patterns
- Investigation results and root causes
- Technical decisions and ADR summaries
- Environment constraints and operational notes
