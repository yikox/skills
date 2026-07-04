# Modular Review Rules

Use these checks for requirements, PM entries, architecture docs, change designs, ADRs, graphs, and implementation completion evidence.

## Universal Checks

- The artifact names a primary module for every non-trivial change.
- Impacted modules are listed separately from the primary module.
- The change level is present and justified.
- PM start exists for L2/L3 work, and for L1 only when it is explicitly tracked.
- PM completion evidence exists before tracked active tasks are closed.
- Baseline architecture and target architecture are not mixed.
- Proposed facts are marked as proposed, accepted, or implemented.
- Status fields are synchronized across PM, design docs, and architecture index rows.
- Open questions are explicit and not hidden in prose.
- New or migrated module docs declare owned `code_paths`; ownership claims do not overlap across modules. `shared_paths` and `ignored_paths` are documented exceptions, not owners.
- Module docs follow `module-authoring-rules.md`: concrete public contracts (or explicit "No external contract"), no code restating, executable validation, uncertain facts marked `(inferred)` or `(unclear)`.
- When graph artifacts exist, module doc Dependencies tables are a subset of the graph relations; relation `kind` values come from the closed vocabulary in `vocab.md` (the single source of truth, described in the graph format reference).

## L3 Checks

- The architecture change states current baseline, target design, impact, migration path, validation, and rollback or mitigation.
- ADR exists only when a durable technical direction is chosen among meaningful alternatives.
- Human acceptance is required before implementation, requested with a 3-8 bullet decision summary of key changes, ambiguities, and risks.
- The current graph is not overwritten by a proposed graph unless the change is implemented.

## L2 Checks

- The module change belongs to one primary module.
- External contracts are unchanged or compatibility is explained.
- Implementation and validation are concrete enough to execute.
- User confirmation is requested before implementation, with a 3-8 bullet decision summary of key changes, ambiguities, and risks.
- The module baseline is updated only after implementation lands.

## L1 Checks

- PM start and completion exist only for tracked L1 work; otherwise a concise completion/update note is enough when durable evidence matters.
- The change is local to one module.
- A full design document is not required unless risk or ambiguity grows.
- The module doc is updated when the behavior or constraint would otherwise be stale.

## Completion Evidence

Acceptable implementation evidence includes:

- commit hash;
- PR or issue link;
- changed file summary plus verification command;
- user confirmation when code is outside the agent's reachable workspace.

Do not mark a design implemented just because it was written or accepted.
