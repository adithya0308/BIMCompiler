# BIM Compiler V1

A new product built from selected inherited BIM Compiler technology, scoped to **multi-storey office buildings**.

## Target product

Structured requirements → strict building intent → office configurator → resolved configuration → immutable design revision/order → deterministic spatial BOM → qualified existing compiler → fail-closed acceptance → accepted model → browser database and IFC → reused web viewer.

AI interprets and proposes configuration decisions. Deterministic software owns dimensions, constraints, placement and geometry. Missing mandatory information returns `NEEDS_USER_INPUT`.

## Current status

Stage 0 baseline and Stage 1 source architecture audit are complete. Stage 2 establishes V1 documentation and a controlled proof plan; human review is pending. No Stage 3 execution has been performed under this plan.

Source inspection established implementations for extraction, spatial BOM construction/traversal, placement, geometry binding, bounded validation and browser rendering. Existing test source supports some of these mechanisms; it is not evidence that those tests passed in this checkout.

End-to-end runtime readiness, populated asset availability, compiler/viewer compatibility, office generation, complete discipline coverage and IFC fidelity remain **UNPROVEN**. Several required databases are missing. Current code does not justify automatic professional approval, complete six-discipline, clash-free, compliant or constructible BIM claims.

The first runtime candidate is **resolved spatial BOM → Java BOM compiler**. It is not permanently frozen until Stage 5. C_Order records lifecycle/revision information initially; BomDrop is not a requirements-to-BOM generator. The legacy JSON/DSL route is not the primary V1 contract.

The preferred viewer candidate is **deploy/dev/**. We will reuse it, not build a new viewer. BIMOOTB is not the substantive renderer; viewer/ is legacy. Compatibility is unproven until Stage 3.

## Developer starting point

Read [AGENTS.md](AGENTS.md), then:

- [V1 scope](docs/product/V1_SCOPE.md)
- [Architecture](docs/product/ARCHITECTURE.md)
- [Roadmap](docs/product/ROADMAP.md)
- [Acceptance gates](docs/product/ACCEPTANCE_TESTS.md)
- [Architecture decisions](docs/product/DECISIONS.md)
- [Asset manifest](docs/product/ASSET_MANIFEST.md)
- [Controlled Stage 3 plan](docs/product/STAGE3_PROOF_PLAN.md)
- [Legacy evidence index](docs/legacy/README.md)

AGENTS.md and docs/product govern V1. Inherited instructions and roadmaps are historical evidence. Source remains the evidence for actual behavior.

## Development environment

Use the authoritative WSL/Linux checkout at `/home/s_adithya/projects/BIMCompiler`. Case-sensitive tracked filenames cannot be represented reliably by a normal Windows checkout; preserve both case-differing migration files.

Baseline: tag `legacy-redhuan-baseline`, commit `b4c31ad30aca974488fc3efca06d0d2e65d40f7a`, V1 branch `v1-development`.

Java 17/Maven, Python/IfcOpenShell/NumPy, SQLite and browser/WASM tooling appear in the inherited implementation. Installed versions and a reproducible dependency set are not yet qualified. Do not run inherited “quick start” scripts as a bootstrap: some migrate databases, rewrite configuration or generate SQL. Follow the Stage 3 plan only after execution authorization.

## Inherited technology and license

Inherited BIM Compiler technology: Copyright (c) 2025-2026 Redhuan D. Oon. The existing [MIT license](LICENSE) and attribution are preserved.
