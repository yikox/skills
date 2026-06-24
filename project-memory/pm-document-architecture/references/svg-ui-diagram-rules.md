# SVG UI Diagram Rules

Use these rules for durable UI schematic, wireframe, screen-region, and layout diagrams in PM architecture docs.

## When To Use SVG

Use SVG-first for:

- Window or page layout diagrams.
- Screen-region maps.
- Sidebar, toolbar, tab, modal, panel, or split-pane schematics.
- UI composition diagrams where spatial placement matters.

Use Mermaid instead for module relationships, sequence flows, state machines, and data movement. Do not use ASCII box drawings for durable UI layout docs.

## Paths

Default root:

```text
architecture/assets/ui/
```

Suggested file names:

```text
architecture/assets/ui/main-window-layout.svg
architecture/assets/ui/editor-layout.svg
architecture/assets/ui/ai-chat-layout.svg
```

Reference from `architecture/main-design.md`:

```markdown
![Main window layout](assets/ui/main-window-layout.svg)
```

Reference from `architecture/modules/<module>.md`:

```markdown
![Editor layout](../assets/ui/editor-layout.svg)
```

## Authoring Rules

- Keep one diagram per SVG file.
- Use plain SVG with `viewBox`; avoid external fonts, external CSS, JavaScript, `foreignObject`, raster images, filters, and network assets.
- Use basic shapes: `rect`, `line`, `path`, `text`, and `g`.
- Include `<title>` and `<desc>` for accessibility.
- Keep labels short and readable. Prefer 12-16 px text.
- Use a restrained neutral palette with a small number of semantic accents.
- Use stable ids for major groups, such as `top-bar`, `sidebar`, `main-area`, or `modal`.
- Keep diagrams at a documentation abstraction level. Show regions and responsibilities, not pixel-perfect product UI.
- Represent only current or accepted baseline architecture. Plans and pending changes belong to `pm-design-requirement`.

## Markdown Integration

- Link SVG files from Markdown instead of inlining SVG code.
- Add a short table or bullet list near the image when the labels need explanation.
- Keep the image path relative to the document.
- If the target Markdown renderer cannot display SVG, create a PNG export only as a secondary artifact and keep the SVG source canonical.

## Verification

Before finishing:

- Inspect the SVG text for balanced tags and a valid `viewBox`.
- Confirm all referenced SVG paths exist.
- If the diagram is complex, render or preview the SVG with a browser or local viewer and check that labels do not overlap.
- Run the diagram accuracy check from [diagram-validation-rules.md](diagram-validation-rules.md). Fix any inaccurate regions, labels, paths, or implied UI behavior, then repeat the SVG checks.
