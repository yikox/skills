# Diagram Validation Rules

Use these rules after creating or changing any Mermaid or SVG diagram in PM architecture docs.

## Accuracy Check

Validate the diagram against the source of truth available for the task:

- Existing repository code, entry points, package boundaries, tests, configs, and integration files.
- Existing PM architecture docs, `project-management.md`, and `knowledge-summary.md`.
- Requirement/change design docs when the diagram reflects an accepted implemented change.
- Explicit user-provided architecture facts for not-yet-built systems.

Check that:

- Every node or region represents a real or explicitly intended component.
- Every edge, arrow, dependency, or sequence step has a source fact.
- Module ownership and boundaries match the main design and module docs.
- Labels do not imply behavior, persistence, sync, authority, or implementation state that is not verified.
- UI schematic regions match the documented screen structure and do not introduce unapproved product behavior.
- Relative image paths from Markdown to SVG assets are correct.

## Repair Loop

If a diagram fails the accuracy check:

1. Identify the inaccurate nodes, edges, labels, paths, or regions.
2. Update the diagram and nearby prose so they describe the same architecture facts.
3. Run the syntax/rendering checks from the diagram-specific rules again.
4. Repeat the accuracy check until no known mismatch remains.

When a fact cannot be verified but the user wants it represented, mark it as an assumption in prose near the diagram.

## Completion Standard

Do not present a diagram as final until:

- Syntax or rendering checks pass for its format.
- The accuracy check has been performed against the relevant source facts.
- Any remaining uncertainty is called out explicitly as an assumption or open question.
