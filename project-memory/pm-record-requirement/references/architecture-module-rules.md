# Architecture Module Rules

Use these rules to connect requirement intake to modules created by `pm-document-architecture`.

## Sources

When architecture docs exist, use them to identify module ownership:

- `architecture/main-design.md` for module map, boundaries, and cross-module flows.
- `architecture/modules/<module-slug>.md` for module responsibilities, contracts, state, and dependencies.
- `project-management.md` `Design Documents` / `设计文档` for indexed module design paths.

If architecture docs do not exist, do not invent a false baseline. Record `unknown` or a candidate module and suggest `pm-document-architecture` when module ownership would affect design.

## Primary Module

Record one primary module whenever possible. Choose the module that owns the main state, API, workflow, or user-visible behavior being changed.

Examples:

- Editor behavior -> `editor`
- Agent memory, prompt context, tool orchestration -> `ai-agent`
- Screen layout, interaction state, visual controls -> `ui`
- Persistence, sync, import/export -> `storage` or `sync` when those modules exist

For cross-module requirements, record:

- primary module: the owner for detailed design;
- impacted modules: secondary modules or areas affected by the change.

## Intake Fields

Capture enough information for `pm-design-requirement` to proceed:

- primary module;
- impacted modules or areas;
- modification summary as current-to-target behavior;
- scope and non-goals;
- impact points for workflows, data/state, API/contracts, UI, tests, operations, migration, or compatibility;
- assumptions and open questions.

## Clarification Gate

Ask targeted questions before recording when:

- two or more modules could own the design and the choice changes the solution;
- the requested modification is unclear;
- scope or non-goals are missing and likely to cause over-design;
- impact on data/state, API/contracts, UI, or compatibility is unclear.

If the user wants to record the requirement anyway, mark it `needs-clarification` and preserve the open questions.
