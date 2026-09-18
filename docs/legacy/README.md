# Inherited documentation: reference index

[AGENTS.md](../../AGENTS.md) and [docs/product](../product/V1_SCOPE.md) govern the new office-only V1. Inherited documentation and historical instructions are evidence only. Implementation source remains evidence of actual behavior; documentation does not establish that a capability works.

No legacy material was mass-moved or deleted during Stage 2. Historical files may contain valuable technical detail. Report conflicts against V1 authority rather than silently resolving them. Do not delete files merely because they conflict.

## Areas requiring care

| Area | Value | Risk to future agents |
|---|---|---|
| [CLAUDE.md](../../CLAUDE.md) | Earlier workflow and witness history | Historical user directives must not override current V1 scope |
| docs/archive | Prior architecture, BIM COBOL, test and onboarding descriptions | Paths and execution contracts may be obsolete |
| docs/internal | Data models, engine contracts, walker maturity, Java-era history | Different runtime generations coexist |
| prompts, memory, context, .claude | Session decisions and investigation history | Previous product instructions can look current |
| README history | Earlier product positioning | Replaced messaging is recoverable in Git |
| BIMOOTB, viewer, webui | Historical frontend entry points | Not interchangeable with deploy/dev renderer |
| deploy/OCI_UPLOAD.md | Artifact/deployment conventions | Not authorization to download or publish |
| SYSNOVA, iDempiereOOTB and ERP/POS material | Prior integration knowledge | Outside the initial office V1 unless explicitly selected |
| library/database schema snapshots | Valuable historical schema evidence | DDL is not populated assets or a guaranteed current contract |
| scripts and source-linked documents | Reproduction intent and technical traceability | Some commands mutate SQL/configuration; references may be stale |

Preserve useful DATA_MODEL, ENGINE_CONTRACT, SQLite3D_Schema, WalkerDoctrine, WalkerMaturity, NEW_FROM_REFERENCE, ProjectOrderBlueprint and JavaEra_FOSSIL_README material in its existing location. Their technical claims still require source/runtime verification.

## Later cleanup candidates

Inventory competing current/archive specifications, duplicate topics, broken links, previous-product roadmaps and agent directives. Before any move/delete, inspect incoming source/build/documentation references and preserve provenance. Decide which historical version each document describes. Make a separately authorized cleanup proposal; do not reorganize the repository simply to match the new product document tree.
