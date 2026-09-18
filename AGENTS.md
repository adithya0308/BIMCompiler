# V1 development authority

## Read first

Read this file and all documents in docs/product before implementation. Start with the [scope](docs/product/V1_SCOPE.md), [architecture](docs/product/ARCHITECTURE.md), [roadmap](docs/product/ROADMAP.md), [acceptance gates](docs/product/ACCEPTANCE_TESTS.md), [decisions](docs/product/DECISIONS.md), [assets](docs/product/ASSET_MANIFEST.md) and [Stage 3 plan](docs/product/STAGE3_PROOF_PLAN.md).

User instructions govern the authorized task. This file and docs/product govern V1 repository work. Inherited CLAUDE.md, prompts, memory, archived specifications and earlier product directives are historical/reference evidence, not independent V1 authority. Implementation source is evidence of behavior, not permission to expand scope. Report conflicts; do not silently reconcile them or delete their evidence.

## Baseline and environment

- Baseline tag: `legacy-redhuan-baseline`.
- V1 branch: `v1-development`.
- Baseline commit: `b4c31ad30aca974488fc3efca06d0d2e65d40f7a`.
- Authoritative development checkout: `/home/s_adithya/projects/BIMCompiler` in WSL/Linux.
- Preserve independently tracked case-differing paths, including `migration/DV_CA_rules.sql` and `migration/DV_ca_rules.sql`. Never “repair,” merge or rename them for Windows compatibility.

The baseline tag, branch and commit were verified during Stage 2. Work on one bounded task per worktree/branch. Do not create a new branch or commit merely because this guidance exists; follow the current task's authorization.

## Approved product boundaries

V1 is multi-storey office buildings only. AI interprets requirements, identifies ambiguity, retrieves qualified alternatives and proposes configuration choices. AI must not directly invent arbitrary BIM geometry.

Deterministic software owns required-input validation, constraints, dimensional calculations, assembly materialization, BOM creation, placement, geometry, enabled discipline generation, compilation, validation and artifact generation. Missing mandatory intent returns `NEEDS_USER_INPUT`, never an undocumented default.

The first runtime candidate is resolved spatial BOM → existing Java BOM compiler. Runtime architecture is not permanently frozen until Stage 5's new-variant proof. C_Order/C_OrderLine initially represent lifecycle/revision data, not mandatory geometry authority. BomDrop expands an existing BOM into order lines; it is not a requirements-to-BOM generator. The spec.json/DSL route is legacy/selective reference, not the V1 contract.

Reuse the deploy/dev renderer through a narrow contract; compatibility remains UNPROVEN until Stage 3. No new BIM viewer during V1 without explicit approval. No second BIM compiler.

## Working rules

- Inspect before modifying; findings before fixes; specifications before implementation.
- Reuse existing working source before creating replacements.
- Do not redesign approved product boundaries or, after Stage 5, frozen runtime architecture during implementation. Propose a bounded decision change with evidence and obtain human approval.
- Tests and declared acceptance evidence precede completion claims. Documentation-only work uses document/link/diff checks, not builds. Never run prohibited tests or generators merely to satisfy this rule.
- Do not weaken validation to make output pass, silently skip mandatory stages, or return stub success.
- Preserve source, product, recipe, rule, configuration and artifact provenance.
- Geometry and placement must be deterministic; record versions and declared tolerances.
- Reconstruction is not proof of generation.
- Never claim clash-free, professional, compliant or constructible BIM without declared acceptance evidence. “Federated BIM” requires explicit discipline and validation coverage.
- Protect DAGCompiler, IFCtoBOM, BIM_COBOL, BIMEyes, orm-core, ORMSandbox, designer/viewer implementations, schemas, migrations, scripts and tests unless a bounded task explicitly authorizes changes.
- Do not mass-delete or mass-move inherited code/docs. Preserve CLAUDE.md pending separate cleanup authorization.
- Stop when acceptance/stop conditions require a human decision. Missing required data is a blocked/inconclusive result, not success.

## Current stage boundary

Stage 2 is documentation and controlled proof planning only. No builds, dependency installation, migrations, IFC processing, database generation or implementation fixes. Stage 3 commands are proposals, not authorization. Stop after documentation review; do not commit without instruction.
