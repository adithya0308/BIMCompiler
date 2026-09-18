# V1 scope

Status: approved product scope; implementation and runtime qualification pending. Stage numbering is defined in [ROADMAP.md](ROADMAP.md). Approved decisions are recorded in [DECISIONS.md](DECISIONS.md).

## In scope

- Multi-storey office buildings, initially constrained to qualified configurations.
- Strict structured building intent and explicit missing-input handling.
- Qualified office configurations and versioned design revisions/orders.
- Deterministic assembly and spatial BOM materialization.
- Existing compiler reuse, initially qualifying the Java BOM boundary.
- Declared discipline coverage and provenance.
- Validation and acceptance reports, including failures and unavailable checks.
- Browser database and independently qualified IFC export.
- Existing deploy/dev viewer reuse through a narrow contract.
- Optional concept references after the strict intent contract exists.

These are product objectives, not a claim of current delivery.

## Out of scope for initial V1

Arbitrary building typologies; unrestricted AI architecture or geometry; CAD-to-BIM as the primary workflow; replacing Revit/Bonsai; a new BIM viewer; automatic professional engineering approval; unsupported compliance claims; guaranteed clash-free output; unrestricted MEP engineering.

An included residential fixture may be used in Stage 3 to qualify infrastructure. This does not expand the office-only product domain.

## Responsibility and completeness

AI may interpret requirements and optional concepts, identify ambiguity, retrieve qualified alternatives, propose configuration choices and explain unresolved requirements. Deterministic software owns required-input validation, constraints, dimensions, assembly/BOM creation, placement, geometry, enabled disciplines, compilation, checks and artifact generation.

Missing mandatory inputs yield `NEEDS_USER_INPUT`. Every input is explicitly supplied, derived by an approved deterministic rule, or unresolved. Silent mandatory defaults are prohibited.

## Claims and federation

Do not call output professionally approved, complete six-discipline, clash-free, code-compliant or constructible unless the relevant future acceptance gates establish that specific claim. A reported zero is meaningful only with a nonempty declared checked population.

“Federated BIM” is an accepted model state with explicit discipline coverage, shared coordinates, provenance and validation coverage. Generated, imported and omitted discipline content must be distinguishable. Initial discipline commitments, jurisdiction, engineering signoff and numeric tolerances are **TBD by human decision before their gates are applied**.

## Reference knowledge strategy

Included fixture → one representative professional office IFC → minimal curated office assemblies → one meaningfully changed office variant → remaining corpus.

Do not request or process the approximately 20 professional IFCs during Stage 2. Extraction supplies product/component candidates, spatial observations, repetitive patterns, discipline examples and test fixtures. It does not automatically supply regulatory rules, compatibility guarantees, structural design rules, professionally approved recipes or complete MEP knowledge.
