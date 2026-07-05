# Modular Methodology

Use this corpus when reasoning about module boundaries: proposing a new-project modular design, planning legacy modularization, or judging whether a split is real modularization or just file shuffling. `modular-advisor` treats this as its core thinking material; other skills may cite specific sections.

Modularization is not splitting code into files. It is dividing responsibility, controlling dependencies, and defining stable contracts so each module can be independently understood, tested, changed, and replaced. The end goal is containing change propagation, not increasing module count.

## Core Mindset

1. **Divide responsibility before dividing code.** First decide what capabilities the system has, who owns each, which belong together, and who owns which data. Splitting one big file into many files that still share global state and call each other's internals is not modularization.
2. **A module is a complete capability**, not a code-type bucket. Prefer capability modules (task scheduling, model loading, cache management) over type-only layers (controllers/services/utils); layer inside a module when needed.
3. **High cohesion, low coupling.** Inside a module everything serves one goal; between modules only necessary, explicit dependencies remain. Changing internals must not ripple outward; replacing a module must not rewrite the system.
4. **Expose capability, hide implementation** (information hiding, Parnas 1972: a module hides one design decision likely to change). Outsiders may know what a module does, how to call it, inputs, outputs, and errors — never its classes, storage, algorithms, or internal state.
5. **Dependencies must be explicit and controlled**: mostly one-directional, few, declared (not fetched via globals or implicit imports), replaceable, acyclic.
6. **Every piece of core data has exactly one owning module.** Others read or request changes through the owner's contract. Shared mutable data across modules is the fastest path to inconsistent state (the bounded-context rule from DDD: one authoritative owner per model).
7. **Modules collaborate through contracts** — public interfaces, input/output shapes, error definitions, state constraints, call ordering, event formats — never through each other's internals. Prefer data coupling; treat shared-global (common) coupling and reach-into-internals (content) coupling as defects (structured-design coupling scale).
8. **Composition over mutual penetration.** Cross-module flows are orchestrated by the application layer that composes modules; a module must not remote-control the internals of its peers.
9. **Not finer is better.** Over-splitting produces long call chains, interface explosion, and debugging pain. A module should be independently understandable yet express a complete responsibility.
10. **The goal is controlling change**: one requirement touches few modules; swapping a technical implementation leaves business logic alone; one module's failure does not cascade; new features come from composing or extending.

## New Project Design Rules

1. **List system capabilities first** (e.g. request intake, task management, scheduling, model management, inference, cache, storage, monitoring). Capabilities seed the module map — never start from file-type directories.
2. **Define each module's boundary**: what it owns, what it explicitly does NOT own, the data it owns, its public contract, its declared dependencies, its error surface. "Not responsible for" prevents boundary creep.
3. **Set dependency direction early** (dependency inversion: high-level policy never depends on low-level detail; both depend on abstractions). Interface layer -> application layer -> business modules -> abstract capabilities <- infrastructure implementations. Core business must not depend on concrete frameworks.
4. **Separate business rules from technical implementation.** Business modules state the capability they need; infrastructure modules implement it. Swapping the database or cache must not rewrite business rules.
5. **One assembly entry point** creates infrastructure objects, chooses implementations, injects dependencies, and boots the app. Modules never construct their own external dependencies.
6. **Keep public contracts small and stable.** Do not export internals for convenience; contract surface is coupling surface.
7. **No global mutable state**: no global connections, caches, config objects, or user context. Globals make dependencies invisible and break testing and initialization order.
8. **Meet real needs first, extract abstractions later.** No factories/plugin systems/registries while there is exactly one implementation. Extract the abstraction when the second real implementation arrives (YAGNI).
9. **Every module must be testable in isolation** — external dependencies replaceable, no full-system boot required. Untestable usually means over-dependent or badly bounded.
10. **Standardize cross-module communication** (direct call, events, queue, RPC, state query) — pick the allowed set once; don't let each module improvise.
11. **Guard the commons.** `common`/`shared`/`utils`/`core` directories become boundary-less landfills; admit only genuinely generic, stable, business-free code. Business rules live in their business module.
12. **Establish architecture constraints early**: forbid business-to-infrastructure direct access, cross-module internal imports, cycles, low-level-depends-on-high-level; back them with tooling where possible.

## Legacy Refactoring Rules

1. **Do not move directories first.** First map call graphs, data flow, state mutation sites, globals, shared objects, cycles, infrastructure calls, and high-risk core flows. Moving files without a dependency map relocates the mess.
2. **Establish a behavior baseline before refactoring**: core-flow tests, key input/output samples, performance baseline, error behavior, logs, production metrics. Without it you cannot tell whether behavior changed.
3. **Identify boundaries opportunistically, not perfectly.** Peel off the easy capabilities first (config, logging, cache, storage, process management, external service access); refine boundaries iteratively.
4. **Wrap before replacing.** Put a seam (interface) around direct database/cache/filesystem/third-party calls; route new code through it; replace the implementation only after call sites stabilize.
5. **Migrate one module at a time, full loop each**: confirm responsibility -> define contract -> move implementation -> update callers -> add tests -> delete old logic -> re-check dependencies -> commit independently.
6. **Replace progressively** (strangler-fig migration, Fowler): keep the old path, build the new module, shift a slice of traffic, verify equivalence, widen coverage, then delete the old path. No big-bang rewrites.
7. **Eliminate hidden dependencies first**: globals, singletons, statics, implicit init, cross-module shared caches, direct env reads, import-time side effects. Convert them to explicit parameters.
8. **Settle data ownership early.** If several modules mutate the same data, decide the owner, who may write, who may only read, which interface mediates writes, and how changes are announced. Boundaries stay unstable until ownership is settled.
9. **Treat cycles as responsibility confusion**, not import puzzles. Fix by extracting the shared capability, lifting the flow to the application layer, decoupling via events, redrawing boundaries, or merging over-split modules — never just lazy imports.
10. **Keep external behavior stable; separate refactoring commits from feature commits.** Changing logic, contract semantics, and data shapes at once makes failures undiagnosable.
11. **Watch performance.** Modularization adds call layers, conversions, serialization. Benchmark critical paths before and after; balance maintainability against hot-path cost.
12. **Delete old code at each milestone** — old entry points, duplicated helpers, temporary adapters, dead compatibility layers. Two coexisting structures are worse than one bad one.
13. **Prevent regression after refactoring**: import-path restrictions, no cross-module internal access, cycle checks, commons limits, data-ownership rules, "new code goes into a named module". Without constraints the mess grows back.

## Attribution

Supplemented concepts and their sources: information hiding (D. L. Parnas, *On the Criteria to Be Used in Decomposing Systems into Modules*, 1972); coupling/cohesion scale (structured design, Constantine & Myers); dependency inversion (R. C. Martin); strangler-fig progressive replacement (M. Fowler); bounded contexts and data ownership (E. Evans, *Domain-Driven Design*).
