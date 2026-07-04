# Modular Assessment

Use this rubric to judge how modular a project actually is. Directory structure alone proves nothing: a repo full of module folders can still be one tangled monolith. Every dimension below is judged from real code evidence.

## Evidence Requirements

- Every conclusion must point to concrete code locations (files, functions, call sites), not folder names.
- Mark each finding `verified` (you read the code / ran the command) or `inferred` (pattern suggests it); never present a guess as fact.
- Prefer a small number of load-bearing examples over exhaustive listings.
- An assessment that only describes the directory tree is a defect, not a deliverable.

## Assessment Dimensions

1. **Responsibility clarity** — can each module's job be stated in one sentence, plus what it does NOT do? Does its code serve one goal? Any god-modules?
2. **Contract clarity** — is there an explicit public entry? Is the public surface small and stable? Are internals leaked? Are inputs/outputs/errors defined?
3. **Dependency complexity** — how many dependencies per module; are they one-directional, explicit, acyclic; any hidden deps via globals or direct infrastructure calls?
4. **Change blast radius** — how many modules does an ordinary requirement touch? Does swapping a cache/database/format ripple into unrelated modules?
5. **Independent testability** — can a module be tested without booting the whole system, with external dependencies replaced, against its own behavior?
6. **Replaceability** — can the database, cache, an algorithm, or an external service implementation be swapped without editing callers?
7. **Independent comprehensibility** — can a newcomer understand one module by reading it alone? Clear entry point, concentrated core flow, few cross-module jumps?
8. **Data ownership clarity** — one owning module per core datum; no cross-module direct writes; state changes flow through one mechanism.
9. **Deployment/runtime independence** (large systems only) — independent deploy/scale/upgrade, fault isolation. A monolith can still score high overall; independent deployment is not a universal goal.
10. **Architecture constraint strength** — explicit dependency rules, tooling that catches illegal imports/cycles, module design docs, and adherence in new code.

## Maturity Levels

**Low** — many globals; files call each other freely; several modules mutate shared state; business code hits database/cache directly; widespread cycles; any change ripples globally; nothing testable in isolation. Directory splits exist but the system is one organism.

**Medium** — basic responsibility split and some public interfaces; parts testable in isolation; but shared state and cross-module reach-ins persist; infrastructure and business only partly separated; some changes still blast wide. Foundations exist; boundaries not yet stable.

**High** — clear responsibilities and dependency directions; stable contracts; replaceable internals; explicit data ownership; most modules independently testable; local blast radius; enforced constraints; new features land by composing or extending modules.

## Checklist

1. Can every module's responsibility be stated in one sentence?
2. Does every module state what it is NOT responsible for?
3. Does every module have a stable public contract?
4. Does anything outside access a module's internals directly?
5. Are there dependency cycles between modules?
6. Are dependencies explicitly declared?
7. Is there significant global mutable state?
8. Does every piece of core data have exactly one owning module?
9. Can modules be tested independently?
10. Can internal implementations be replaced?
11. Does changing one module force changes in many unrelated ones?
12. Does business code depend directly on database/cache/framework?
13. Are cross-module flows orchestrated by the application layer?
14. Is there a bloating common/shared/utils module?
15. Do tools or rules block illegal dependencies?
16. Can a new developer understand one module in isolation?
17. Can a new feature land by extending one module?
18. Can a module be replaced without touching its callers?

Score pragmatically: the more "healthy" answers with verified evidence, the higher the maturity. Report the 3-5 worst pain points ranked by blast radius, each with its evidence.
