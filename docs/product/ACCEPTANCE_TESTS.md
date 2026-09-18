# V1 acceptance specification

These are required acceptance definitions, not newly implemented tests. Existing test source is supporting evidence, not a passing result. No build or test was run in Stage 2.

Every gate reports PASS, FAIL, INCONCLUSIVE or an explicitly approved NOT APPLICABLE, with artifact IDs, checked population, method, version, tolerance and reason. A mandatory FAIL/INCONCLUSIVE/unavailable check blocks acceptance. No silent skips or stub success.

| ID | Gate | Required result | Evidence / rejection condition |
|---|---|---|---|
| G01 | Asset | All required artifacts are nonempty, versioned and attributable; tools and licenses recorded. | Manifest, hashes, versions, source/rights records; missing required artifact blocks. |
| G02 | Schema | Every producer/consumer table, column, unit and transform convention is compatible. | Read-only schema comparison and contract checks; an empty compatibility table is not semantic repair. |
| G03 | Non-vacuity | Expected fixtures, elements, tests and mandatory checks actually execute. | Expected versus actual populations, test counts and skip reasons; zero/skip cannot pass a required gate. |
| G04 | Extraction | Every source element is extracted, explicitly excluded by approved scope, or reported failed. | Per-class/GUID accounting and exclusion reasons; unexplained omissions fail. |
| G05 | Coordinate | Units, axes, origin, site offset, storey elevation and rotation agree across consumers. | Numeric samples including rotated/offset elements and mesh-versus-bounds comparisons; tolerances approved before run. |
| G06 | Round-trip | Recompiled geometry and required semantics match the declared reference scope. | Per-element geometry/placement/identity/material/spatial comparisons; count agreement alone cannot pass. |
| G07 | Generative | A meaningful new office variant follows a changed brief through qualified parameterization. | Before/after brief, configuration/BOM provenance, intended effects and invariants; replay/renaming fails. |
| G08 | Order-causality | When order/configuration is authoritative, its change causally changes the intended compiled result. | Isolated revision mutation test without hidden direct BOM patching; immutable historical revision retained. |
| G09 | Completeness | All required assemblies, products, meshes, disciplines and system relationships exist. | Required-versus-produced inventory and topology/coverage; unresolved selections or missing geometry fail. |
| G10 | Validation | Required checks fail closed, including unavailable check implementations/data. | Injected bad/missing inputs are rejected or inconclusive; log-only failures and stub success fail. |
| G11 | Clash-coverage | Claims name checked populations, discipline pairs, method, clearance/tolerance and exclusions. | Nonempty pair counts and planted violations; zero reported clashes is not a universal clash-free proof. |
| G12 | IFC | An independent validation path parses export and confirms required classes, relationships and coordinates. | Schema/entity checks plus comparison; proxy substitution or exporter self-check alone cannot prove required fidelity. |
| G13 | Viewer | Qualified deploy/dev rendering matches accepted model placement, identity, bounds and selection. | Schema check, numeric scene assertions, rotated/offset samples and browser errors/network record; attractive screenshot alone fails. |
| G14 | Repeatability | Identical versioned inputs produce equivalent canonical model outputs. | Two isolated runs, canonical comparisons and documented volatile fields; timestamp differences distinguished from geometry drift. |
| G15 | Professional-scope | Every public claim is within declared rule, jurisdiction, discipline and signoff coverage. | Claim-to-evidence map, rule versions, exclusions and required professional review; unsupported claims fail. |

## Coverage and stage applicability

Stage 3 qualifies technical infrastructure with the included fixture: G01–G06, G09–G14 and bounded claim review G15. G07 is not passed by a fixture round trip; it is mandatory at Stage 5. G08 becomes mandatory when order/configuration is asserted to drive compilation, and must pass by Stage 7. Document the exact Stage 3 required discipline/class subset before execution.

Stage 4 adds real office evidence. Stage 5 adds generative proof before runtime freeze. Stage 6 adds holdout generalization. Stages 8–10 apply gates against the final promised discipline and professional scope. New claims require corresponding evidence, not reuse of a narrower earlier PASS.

## Existing evidence candidates and limitations

- [RosettaStoneGateTest](../../DAGCompiler/src/test/java/com/bim/compiler/contract/RosettaStoneGateTest.java): counts, bounds/digests and selected integrity checks; includes scope/skip behavior.
- [BuildingRegistryTest](../../DAGCompiler/src/test/java/com/bim/compiler/contract/BuildingRegistryTest.java): pipeline fixture assertions.
- [BomDropConfigureTest](../../BonsaiBIMDesigner/src/test/java/com/bim/designer/BomDropConfigureTest.java): manual BOM update means it does not alone prove order causality.
- [EyesProofRunner](../../BIMEyes/src/main/java/com/bim/eyes/proof/EyesProofRunner.java): bounded geometry/relational checks with availability limitations.
- [CheckClashVerb](../../BIM_COBOL/src/main/java/com/bim/cobol/verb/CheckClashVerb.java): selected AABB pairs; execution success is distinct from zero clashes.
- [Parent build configuration](../../pom.xml): pipeline tests default to skipped.

Numeric tolerances, expected fixture counts, required IFC entity subset, rule versions, discipline scope and professional signoff are **TBD** before their respective runs. They must not be selected retrospectively to make output pass.

## Required negative cases

Future tests must cover missing mandatory intent → NEEDS_USER_INPUT; missing product/mesh/rule; empty fixture/test populations; unknown assembly/verb; failed service provider; coordinate/unit mismatch; logged critical failure; unapproved proxy export; and missing required discipline content. Preserve the failure rather than weakening the test or injecting empty schema stubs.

Implementation of these tests requires a separately authorized bounded task.
