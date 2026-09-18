# Architecture decision log

Authority: Stage 1 audit approved by the user; Stage 2 product decisions explicitly approved. Recorded: 2026-09-18. Approved decisions below do not assert passing runtime evidence. No implementation execution is authorized by this log.

## D001 — Office-only V1

- **Status:** APPROVED.
- **Context:** Inherited repository spans many typologies.
- **Decision:** Limit the product to multi-storey office buildings.
- **Rationale:** Constrain qualification and product effort.
- **Consequences:** Residential fixtures remain technical tests, not product scope.
- **Revisit condition:** Explicitly approved future domain expansion.

## D002 — AI configures; deterministic software creates geometry

- **Status:** APPROVED.
- **Context:** AI output must not introduce arbitrary geometry.
- **Decision:** AI interprets/retrieves/proposes; deterministic code owns geometry and required-input checks.
- **Rationale:** Reproducibility and accountable constraints.
- **Consequences:** Missing mandatory data returns NEEDS_USER_INPUT.
- **Revisit condition:** Explicit product-policy change, not implementation convenience.

## D003 — First compiler boundary

- **Status:** APPROVED.
- **Context:** Multiple inherited entry points coexist.
- **Decision:** Qualify resolved spatial BOM → Java BOM compiler first.
- **Rationale:** Clearest inspected deterministic compilation boundary.
- **Consequences:** Candidate only; assets and contracts require proof.
- **Revisit condition:** Stage 3/5 evidence shows boundary cannot support the bounded slice.

## D004 — Order lifecycle

- **Status:** APPROVED.
- **Context:** Order walkers exist but main pipeline walks BOMs.
- **Decision:** C_Order/C_OrderLine initially record lifecycle/revision, not mandatory geometry authority.
- **Rationale:** Avoid documenting wiring that is not established.
- **Consequences:** Require causality proof before making orders authoritative.
- **Revisit condition:** Bounded integration plus G08 evidence.

## D005 — Legacy JSON/DSL

- **Status:** APPROVED.
- **Context:** IntentCompiler has defaults and a separate generation path.
- **Decision:** spec.json/DSL is not the primary V1 contract.
- **Rationale:** Strict structured intent needs explicit completeness.
- **Consequences:** Selectively reuse algorithms without inheriting legacy defaults.
- **Revisit condition:** Evidence-backed, explicitly approved contract change.

## D006 — Viewer candidate

- **Status:** APPROVED.
- **Context:** Substantive renderer source is under deploy/dev.
- **Decision:** Qualify deploy/dev through a narrow contract.
- **Rationale:** Reuse local functionality.
- **Consequences:** Compatibility remains UNPROVEN until Stage 3; BIMOOTB is not the renderer.
- **Revisit condition:** Stage 3 proves a material incompatibility requiring an approved alternative.

## D007 — No new V1 viewer

- **Status:** APPROVED.
- **Context:** A renderer already exists.
- **Decision:** Do not build a new viewer for V1.
- **Rationale:** Avoid unnecessary replacement effort.
- **Consequences:** New frontend integrates qualified renderer.
- **Revisit condition:** Explicit human authorization based on failed reuse evidence.

## D008 — One professional IFC first

- **Status:** APPROVED.
- **Context:** The office corpus is not yet supplied.
- **Decision:** After included-fixture proof, qualify one representative office IFC.
- **Rationale:** Find domain-specific failures before bulk ingestion.
- **Consequences:** No professional IFC request in Stage 2.
- **Revisit condition:** Human-approved change supported by qualification evidence.

## D009 — Variant before bulk corpus

- **Status:** APPROVED.
- **Context:** Reconstruction can masquerade as grammar readiness.
- **Decision:** Pass one meaningful new office variant before remaining IFC ingestion.
- **Rationale:** Prove generative reuse early.
- **Consequences:** Stage 5 precedes Stage 6.
- **Revisit condition:** Explicit scope decision; never silently bypass.

## D010 — Fail-closed acceptance

- **Status:** APPROVED.
- **Context:** Inherited code includes skips/log-only failures/stubs.
- **Decision:** Required failures or unavailable checks block accepted output.
- **Rationale:** Success must mean declared checks actually passed.
- **Consequences:** Add qualified acceptance enforcement without weakening checks.
- **Revisit condition:** Only explicit change in mandatory scope; not a failing output.

## D011 — Reconstruction is not generation

- **Status:** APPROVED.
- **Context:** Exact round trips prove replay fidelity.
- **Decision:** Require changed-brief and invariant evidence for generation.
- **Rationale:** Prevent overclaiming reusable knowledge.
- **Consequences:** Separate G06 and G07.
- **Revisit condition:** No automatic revisit; any changed definition needs human approval.

## D012 — Runtime freeze timing

- **Status:** APPROVED.
- **Context:** Java and browser generations coexist.
- **Decision:** Freeze runtime only after Stage 5F proof and human approval.
- **Rationale:** Choose with operational and generative evidence.
- **Consequences:** Product boundaries are approved now; runtime remains candidate.
- **Revisit condition:** Failed proof before freeze or explicit post-freeze decision change.

## Unresolved decision register

| ID | Matter | Status | Needed before |
|---|---|---|---|
| U001 | Source, rights, checksums and compatible versions of missing databases | UNKNOWN | Stage 3A |
| U002 | Exact dependency lock/version set and artifact bootstrap method | TBD | Stage 3A execution |
| U003 | Canonical schema/transform contract and numeric tolerances | TBD | Stage 3B–3E acceptance |
| U004 | Initial office archetype and qualified assembly/product set | TBD | Stages 4F–5A |
| U005 | Promised disciplines, generated/imported split, jurisdictions and professional signoff | TBD | Applicable design/acceptance work; final scope before Stage 8 |
| U006 | Exact current external PWA parity and whether it is needed | UNKNOWN; not presumed required | Only if local viewer qualification requires it |
| U007 | Final runtime architecture | PENDING Stage 5F | After new-variant proof |
| U008 | UI, hosting, security, tenancy and deployment | TBD | Stage 9 |

Resolve decisions once with evidence, then implement within their boundaries. Changes need recorded context, consequences and approval, not continuous redesign.
