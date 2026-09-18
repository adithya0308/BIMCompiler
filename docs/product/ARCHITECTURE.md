# V1 architecture

## Product architecture — approved

Requirements → Strict BuildingIntent → Office Configurator → Resolved BuildingConfiguration → Immutable design revision/order → Deterministic BOM materialization → Spatial BOM → Qualified existing BIM compiler → Fail-closed acceptance → Accepted model → Browser database + IFC → Reused viewer.

The browser database and IFC are parallel deliverables. Database viewing need not wait for IFC export. A failed or inconclusive mandatory gate prevents an accepted-model result.

| Boundary | Required contract | Current status |
|---|---|---|
| Intent | Typed requirements, explicit units, provenance, unresolved fields; NEEDS_USER_INPUT | New product contract; implementation TBD |
| Configuration | Qualified assembly/product/recipe versions, compatible dimensions, selected disciplines | Minimal implementation in Stage 5; product implementation in Stage 7 |
| Revision/order | Immutable input revision and artifact association | Existing order models are candidates; immutability enforcement TBD |
| Materialization | Deterministic configuration → complete spatial BOM | Adapter/configuration logic unproven |
| Compilation | Explicit BOM/catalog/geometry inputs → placed model and diagnostics | Existing Java candidate |
| Acceptance | Pass/fail/inconclusive, coverage and reasons, mandatory-stage enforcement | Existing checks need qualification and fail-closed integration |
| Artifacts | Versioned schemas, coordinates, identity/provenance and checksums | Canonical contracts TBD in Stage 3 |
| Viewer | Accepted database → verified rendering and selection | deploy/dev candidate; compatibility UNPROVEN |

## Current runtime candidate — not permanently frozen

First qualify resolved spatial BOM → existing Java BOM compiler. Runtime selection freezes only at Stage 5F after a genuinely new office variant passes acceptance.

Source anchors:

- [CompilationPipeline](../../DAGCompiler/src/main/java/com/bim/compiler/dsl/CompilationPipeline.java): CompileStage calls BOMWalker; writer and optional route/proof stages follow.
- [BOMWalker](../../DAGCompiler/src/main/java/com/bim/compiler/bom/walker/BOMWalker.java) and [PlacementCollectorVisitor](../../DAGCompiler/src/main/java/com/bim/compiler/bom/walker/PlacementCollectorVisitor.java): hierarchy and placement.
- [BomDropper](../../DAGCompiler/src/main/java/com/bim/compiler/bom/BomDropper.java): existing BOM → C_Order/C_OrderLine.
- [PlacementLoader](../../DAGCompiler/src/main/java/com/bim/compiler/dsl/PlacementLoader.java): separate order-walker path; not proof that order edits control the principal CompileStage.
- [IFCtoBOMPipeline](../../IFCtoBOM/src/main/java/com/bim/ifctobom/IFCtoBOMPipeline.java): extracted data → products/spatial BOM and related catalog writes.
- [EyesProofRunner](../../BIMEyes/src/main/java/com/bim/eyes/proof/EyesProofRunner.java): bounded checks.
- [Browser application](../../deploy/dev/index.html): local renderer candidate.

C_Order/C_OrderLine may record lifecycle/revision data; they are not initially mandatory geometry authority. BomDrop is not a requirements-to-BOM generator. spec.json → IntentCompiler → DSL is legacy/selective reference, not the primary product contract. BIM COBOL is reusable Java verb/recipe machinery, not a promise of complete discipline engineering.

Spatial BOM databases, catalog/recipe databases, mesh libraries and output databases are separate contracts. Do not conflate similarly named tables or infer distinct SQLite schemas from capitalization.

## Unproven components and known integration gaps

- Missing populated libraries and reference databases; see [assets](ASSET_MANIFEST.md).
- Older tools/extract.py host schema differs from ExtractionPopulator's filling_guid expectation.
- Main BOM and order-walker integration is not one authoritative execution chain.
- Some paths log failures, skip unavailable checks or return stub success.
- Java output and browser schema/transform conventions require comparison.
- IFC exporters need independent semantic and coordinate validation.
- Selected MEP routing graphs do not prove complete emitted physical systems.
- Professional office configuration and product compatibility remain unqualified.
- Browser reference-editing code is an alternative source of bounded reuse, not a second geometry authority.

The Stage 1 audit was source-only. Existing test source is not a passing runtime result. No current professional/clash/compliance guarantee follows from the existence of a class or gate.

## Protected boundaries

Preserve compiler, extraction, ORM, validation and renderer implementations until a bounded task authorizes change. Prefer adapters around existing qualified behavior. Do not create a second BIM compiler or a new viewer. Reuse deploy/dev; BIMOOTB is a launch/documentation shell and viewer/ is legacy.

AI proposes qualified decisions; deterministic software validates and materializes them. Preserve provenance through source IFC, extraction version, product/recipe, configuration, BOM, compilation and acceptance. Regulatory knowledge must be separately sourced and approved.

## Freeze policy

Product boundaries above are approved now. Numeric contracts, discipline scope and runtime compatibility are unresolved, not silently frozen. Stage 5F requires recorded evidence and human approval. Later implementation tasks must not continually redesign the frozen architecture; changes require an explicit decision-log update.
