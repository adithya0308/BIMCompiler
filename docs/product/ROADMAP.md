# V1 roadmap

Status at Stage 2: documentation prepared for review; no execution of the proof plan. Stage 0 and Stage 1 are COMPLETE. Stage 2 is CURRENT until human review. All later stages are PENDING, not authorized by this document.

## Stages and gates

| Stage | Input | Output | Test | Acceptance gate | Human input | Stop condition |
|---|---|---|---|---|---|---|
| 0 — Repository baseline — COMPLETE | Inherited checkout | Recorded tag/branch/commit and clean baseline | Git and case-sensitive path inspection | Authoritative WSL checkout identified | Baseline approval | Unexpected tracked changes or case loss |
| 1 — Architecture audit — COMPLETE | Source, tests, schemas, fixtures | Approved source-only audit | Call-path and evidence review | Claims distinguished from runtime proof | Audit approval received | Unsupported capability treated as proven |
| 2 — V1 authority/documentation + controlled proof plan — CURRENT | Approved audit and Stage 2 instructions | Ten authority/planning documents | Link, consistency, diff and scope checks | Human accepts documentation; no implementation changes | Review documents and unresolved matters | Scope expansion or contradictory authority |
| 3 — Technical vertical-slice qualification | Included fixture, qualified tools/assets | Reproducible extraction/BOM/output/viewer/IFC evidence | G01–G06, G09–G14 as applicable | All mandatory technical checks non-vacuous and passed | Approve bounded execution/assets/tolerances | Missing assets, incompatible schema, skipped mandatory gate |
| 4 — One professional office reference | First representative office IFC after Stage 3 | Qualified reference reconstruction plus minimal assembly candidates | Input/output accounting and spatial/semantic comparison | One office reconstructed within declared scope | First IFC, provenance, expected content and expert interpretation | Unexplained loss or reference not representative |
| 5 — One genuinely new office variant | Curated minimal assemblies and controlled changed brief | New variant plus runtime freeze decision | G07 and all applicable gates; G08 where order drives changes | Meaningful parameterized change passes, then human approves runtime | Changed brief, compatibility rules, freeze decision | Exact replay only, arbitrary geometry, failed mandatory check |
| 6 — Remaining professional IFC corpus | Qualified pipeline and remaining IFCs | Curated Office Building Grammar with held-out evidence | Per-model accounting, normalization and holdout tests | Corpus provenance and qualified reuse boundaries established | Remaining models and curation decisions | Bulk processing precedes Stage 5 or heuristics become guarantees |
| 7 — Product BuildingIntent + Configurator | Grammar and approved programming requirements | Product-level strict intent/configuration/revision flow | Missing/contradictory inputs, constraints, deterministic materialization and order causality | NEEDS_USER_INPUT and reproducible resolutions enforced | Programming fields, lifecycle and optional concept policy | Silent defaults, mutable revision or divergent BOM |
| 8 — Declared discipline completion + fail-closed acceptance | Agreed discipline scope and rules | Scoped systems and acceptance reports | Completeness, topology, validation, clash coverage and injected-failure tests | Every promised discipline/check demonstrated | Regulatory/engineering criteria and signoff | Incomplete systems or failure reported as success |
| 9 — Product frontend + reused viewer | Stable API, accepted artifact and viewer contracts | Product UI wrapping qualified deploy/dev | End-to-end requirements/issues/model/selection workflow | Correct model state visible; failures remain visible | UI, hosting, security and deployment choices | New viewer introduced without approval or failures hidden |
| 10 — V1 QA, demo and presentation | Frozen scope and release candidate | Repeatable demo/release evidence | Regression, holdout, independent IFC, viewer and deployment checks | Human accepts only evidenced product claims | Final acceptance and presentation scope | Mandatory gate failure or unsupported claim |

Gate IDs are defined in [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md). Applicability is declared before execution; exclusions cannot be invented after failure.

## Stage 3 substages

- **3A asset/environment bootstrap:** identify versions, provenance, dependencies and permitted output paths. No automatic restoration of unknown databases.
- **3B included fixture extraction:** begin with repository SampleHouse; account for every element and reconcile the extraction schema.
- **3C BOM/compiler round trip:** qualify catalog/BOM construction, placement and output using the existing compiler candidate.
- **3D viewer contract:** compare output schema, coordinates, bounds and actual rendering in deploy/dev.
- **3E IFC export qualification:** independently parse exported IFC and compare declared semantics and coordinates.

See [STAGE3_PROOF_PLAN.md](STAGE3_PROOF_PLAN.md) for command candidates, writes and stop points.

## Stage 4 substages

- **4A extraction:** ingest one supplied office with provenance and element accounting.
- **4B reconstruction:** establish an extracted reference and normalized spatial hierarchy.
- **4C compilation:** compile its resolved spatial BOM.
- **4D viewer:** verify the compiled office through the qualified viewer contract.
- **4E comparison:** measure losses, transforms, storeys, identity and declared disciplines.
- **4F minimal assembly curation:** qualify only the floor/core/bay/envelope/service candidates needed for Stage 5.

Request the first professional IFC only after Stage 3's gate. No request during Stage 2.

## Stage 5 substages

- **5A controlled changed brief:** specify a meaningful change and measurable expected effects before generation.
- **5B minimal configurator:** choose qualified assemblies and explicit parameters.
- **5C deterministic BOM materialization:** produce a new BOM with provenance, leaving reference inputs unchanged.
- **5D compilation:** use the candidate runtime with explicit inputs.
- **5E validation:** compare intended changes, unchanged invariants and mandatory coverage.
- **5F runtime architecture freeze:** record proof and human approval in DECISIONS; freeze only after the variant succeeds.

Reconstruction is not generation. Neither a renamed file nor an unchanged replay passes Stage 5.

## Stage 6 substages

- **6A batch extraction:** process remaining corpus only after Stage 5.
- **6B normalization:** identify units, families and semantic differences without silently merging incompatible products.
- **6C assembly/pattern mining:** generate candidates, not approved rules.
- **6D curated Office Building Grammar:** add compatibility, parameter ranges, provenance and professional constraints.
- **6E holdout testing:** reserve independent examples/variants and test generalization rather than memorized replay.

## Input timing

Asset source/rights and execution boundaries: before Stage 3. First professional IFC: Stage 4. Minimal component choices and controlled office brief: Stages 4–5. Remaining IFCs: Stage 6. Full programming requirements: Stage 7. Discipline/regulatory signoff: before Stage 8 acceptance claims. Optional concepts: after strict intent exists. UI/deployment: Stage 9, with contract decisions earlier only when technically necessary.

Do not continually redesign approved boundaries during implementation. Use explicit decision changes when evidence requires reconsideration.
