# Module Authoring Rules

Use these rules when writing or updating `architecture/modules/*.md`. They define what deserves a module doc and what a good one contains. Frontmatter schema is in `storage-schema.md`; kind taxonomy is in `module-kind-classification.md`.

## Granularity

- Aim for 4-9 top-level modules. Fewer usually means boundaries are hidden; more usually means implementation details leaked into the map.
- An atomic module is one technical responsibility that can be understood and verified independently. Anything smaller is internal implementation: describe it inside its owner's Internal Design, do not give it a doc.
- Use a composite module when outsiders only need the whole but the parts are strongly related inside. A composite with one child, or children that never collaborate, is a boundary smell.

## Section Rules

**Responsibility** — at most 3 sentences. What the module owns, not how it works. If you cannot state it without "and also", consider splitting.

**Public Contract** — the surfaces other modules actually depend on: function signatures, file formats, CLI arguments, directory conventions, message shapes. Be concrete enough that a consumer could code against it. If nothing external depends on this module, write "No external contract" explicitly — do not leave the section vague.

**Internal Design** — only what someone must know before reading the code: key structures, state, non-obvious flows, where the internal docs live. Do not restate code line by line; link deeper material instead.

**Dependencies** — a subset of the architecture graph relations, plus reasons. The graph is authoritative (see the graph format reference).

**Constraints** — only constraints that cannot be derived from the code: compatibility promises, environment limits, performance floors, conventions with external reasons.

**Validation** — executable commands or concrete checks that prove the module works. "Run the tests" is too vague; give the command and the expected signal.

## Fact Confidence

Mark uncertain statements inline as `(inferred)` or `(unclear)`; unmarked statements are treated as `verified`. Never present a guess as fact — review treats disguised guesses as defects. This applies to all module docs, not only migration output.

## Update Triggers

Update the module doc in the same change when any of these shift:

- public contract (signatures, formats, CLI, conventions others rely on);
- dependencies (graph relations touching this module);
- constraints;
- `code_paths` ownership.

Pure internal implementation changes do not force a doc update. When in doubt: would the current doc mislead the next change? If yes, update.

## Length Guidance

Target 30-80 lines per module doc. A doc that keeps growing past that is a signal: split the module, or move detail into code comments or linked internal docs.

## Kind Templates

Start from `module-design-template.md`. When the module kind's main design subject needs dedicated sections (e.g. `function-flow` steps and sequencing, `data-state` state machines, `layout-style` regions), pull those sections in from the kind's template in `module-kind-classification.md`. Keep the generic sections; kind sections are additions, not replacements.
