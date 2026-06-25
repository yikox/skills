# PM Workflow Map

Use this map to choose the next project-memory skill after PM has already been initialized. `pm-init` is setup and is intentionally not part of this delivery workflow.

## Main Flow

```text
pm-document-architecture
  -> pm-review-artifact
  -> pm-record-requirement
  -> pm-review-artifact
  -> pm-groom-roadmap
  -> pm-design-requirement
  -> pm-review-artifact
  -> human confirmation
  -> AI implements from accepted spec
  -> pm-design-requirement marks landing and updates PM evidence
  -> pm-document-architecture refreshes durable baseline if needed
  -> pm-audit-memory
  -> pm-track-status archives implemented/obsolete rows when appropriate
```

## Branches

- Use `pm-record-knowledge` whenever implementation, debugging, architecture discovery, or validation produces reusable project knowledge.
- Use `pm-migrate-memory` before broad edits when PM docs use older schema, old skill names, or missing design/requirement sections.
- Use `pm-groom-roadmap` whenever priority, current focus, roadmap, or milestone order is unclear.
- Use `pm-audit-memory` after implementation completion, migration, milestone cleanup, or long pauses.

## Confirmation Rules

- Automatic review may fix clear defects and mark review as complete.
- Human confirmation is required for accepted design direction, product tradeoffs, major scope decisions, and implementation landing claims without evidence.
- Implementation itself does not require a PM skill. The AI implements from the accepted spec, then updates PM/design status and evidence through the existing design/status skills.
