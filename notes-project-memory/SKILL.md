---
name: notes-project-memory
description: Store, retrieve, and update durable project memory in Markdown notes. Use when the user asks to remember, record, save, note down, keep for next time, recall, summarize, or organize project knowledge; update project status, version info, active tasks, milestones, todos, roadmap, blockers, or risks; preserve verified commands, build/test/release/deploy workflows, troubleshooting steps, architecture facts, code conventions, decisions, ADR notes, investigation results, or lessons learned for future agents and collaborators.
---

# Notes Project Memory

Use this skill to keep project memory in Markdown notes, independent of any specific note app.

## Decision Flow

1. Resolve the notes location. If the user did not give a path, follow [path-resolution.md](references/path-resolution.md).
2. Determine the project folder and target files using [storage-layout.md](references/storage-layout.md).
3. Classify the request:
   - Project state, version, tasks, milestones, todos, roadmap, blockers, risks: update `project-management.md`.
   - Commands, architecture, conventions, decisions, troubleshooting, investigation results: update `knowledge-summary.md`.
   - Mixed request: update both files.
   - Recall/search request: read the relevant file(s) first and answer from them.
4. Before writing, read existing notes and merge by section. Use [update-rules.md](references/update-rules.md).
5. For a new project folder, create both files from [file-templates.md](references/file-templates.md), then fill only known sections.
6. After writing, report the changed note paths and mention uncommitted note changes if the notes workspace is a git repo.

## Operating Rules

- Keep content in the user's language; preserve technical terms in their original form.
- Do not use external per-agent memory as the authoritative store for shared project knowledge.
- Do not store credentials, tokens, private keys, or temporary scratch notes.
- Do not auto-discover broad personal directories. Ask once when the notes root is ambiguous.
