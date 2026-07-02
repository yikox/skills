# Modular Review Rules

Use these checks for requirements, PM entries, architecture docs, change designs, ADRs, graphs, and implementation completion evidence.

## Universal Checks

- The artifact names a primary module for every non-trivial change.
- Impacted modules are listed separately from the primary module.
- The change level is present and justified.
- PM start exists for L1/L2/L3 work.
- PM completion exists before active tasks are closed.
- Baseline architecture and target architecture are not mixed.
- Proposed facts are marked as proposed, accepted, or implemented.
- Status fields are synchronized across PM, design docs, and architecture index rows.
- Open questions are explicit and not hidden in prose.

## L3 Checks

- The architecture change states current baseline, target design, impact, migration path, validation, and rollback or mitigation.
- ADR exists when a durable technical direction is chosen among meaningful alternatives.
- Human acceptance is required before implementation, requested with a 3-8 bullet decision summary of key changes, ambiguities, and risks.
- The current graph is not overwritten by a proposed graph unless the change is implemented.

## L2 Checks

- The module change belongs to one primary module.
- External contracts are unchanged or compatibility is explained.
- Implementation and validation are concrete enough to execute.
- User confirmation is requested before implementation, with a 3-8 bullet decision summary of key changes, ambiguities, and risks.
- The module baseline is updated only after implementation lands.

## L1 Checks

- PM start and completion exist.
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
