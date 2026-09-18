# Asset manifest

Snapshot: Stage 1 source audit, Stage 2 planning, baseline b4c31ad30aca974488fc3efca06d0d2e65d40f7a. Status is not runtime qualification. No assets were downloaded, generated or restored. Recheck existence, size, links and hashes at Stage 3A.

## A01 component_library.db

- **Purpose:** Meshes, product/image/geometry mappings
- **Expected consumer:** IFCtoBOM, MeshBinder, catalog/recovery scripts
- **Current status:** MISSING at library/component_library.db
- **Source/provenance:** UNKNOWN; schema snapshots exist, populated source not established
- **Required stage:** 3A before BOM/compiler
- **Rebuild possibility:** Partial schemas/extraction exist; complete curated content rebuild UNPROVEN
- **Blocking?:** YES for current compiler candidate
- **Notes:** An empty schema is not a geometry library.

## A02 ERP.db

- **Purpose:** Catalog/rules/recipes compatibility entry
- **Expected consumer:** Java pipeline, IFCtoERP, BackOffice
- **Current status:** MISSING at library/ERP.db
- **Source/provenance:** rebuild_erp.sh describes compatibility link to disc_patterns.db; original data provenance UNKNOWN
- **Required stage:** 3A/3C
- **Rebuild possibility:** Script exists but requires component library and applies migrations
- **Blocking?:** YES for current pipeline
- **Notes:** Do not replace with unrelated same-name DB.

## A03 disc_patterns.db

- **Purpose:** Prior-art discipline patterns and catalog data
- **Expected consumer:** ERP compatibility consumers and rules
- **Current status:** MISSING at library/disc_patterns.db
- **Source/provenance:** scripts/rebuild_erp.sh and migration SQL; curated row provenance UNKNOWN
- **Required stage:** 3A/3C
- **Rebuild possibility:** Conditional rebuild after library acquisition and migration review
- **Blocking?:** YES for candidate recipe/catalog path
- **Notes:** Rebuild writes DB and ERP.db compatibility link.

## A04 per-building BOM databases

- **Purpose:** Spatial hierarchy, offsets and registry
- **Expected consumer:** BOMWalker/CompilationPipeline
- **Current status:** MISSING; expected library/SH_BOM.db initially
- **Source/provenance:** IFCtoBOMPipeline from extraction/config/catalog
- **Required stage:** 3C
- **Rebuild possibility:** Candidate generation exists; qualification pending
- **Blocking?:** YES for compilation
- **Notes:** Temporary library/_SH_compile.db has additional schema handling.

## A05 extracted reference databases

- **Purpose:** Input geometry/metadata baseline
- **Expected consumer:** ExtractionPopulator, fidelity tests, viewer
- **Current status:** Usable populated reference DBs absent
- **Source/provenance:** Included IFCs exist; extraction version and output provenance to record
- **Required stage:** 3B
- **Rebuild possibility:** Rich Python extractor exists; schema compatibility to prove
- **Blocking?:** YES for round-trip evidence
- **Notes:** Expected DAGCompiler/lib/input/SampleHouse_extracted.db.

## A06 historical component library variants

- **Purpose:** Recovery of missing geometry/map rows
- **Expected consumer:** restore_generative_meshes.py and historical scripts
- **Current status:** component_library_pre_s173.db absent
- **Source/provenance:** UNKNOWN
- **Required stage:** Only if approved recovery path needs them
- **Rebuild possibility:** UNKNOWN; not assume replaceable from DDL
- **Blocking?:** CONDITIONAL
- **Notes:** Not an unconditional V1 dependency; avoid historical recovery if reproducible alternate approved.

## A07 browser rule databases

- **Purpose:** Discipline walker schedules/rules
- **Expected consumer:** build/disc_walker.js
- **Current status:** build/terminal_rules.db and build/duplex_rules.db absent
- **Source/provenance:** UNKNOWN
- **Required stage:** Only selected discipline/modelling path, potentially Stage 8
- **Rebuild possibility:** UNKNOWN
- **Blocking?:** NO for basic viewer; CONDITIONAL for walker
- **Notes:** Do not infer complete browser discipline runtime.

## A08 viewer fixture databases

- **Purpose:** Default demo and browser tests
- **Expected consumer:** deploy/dev loader and tests
- **Current status:** Default Duplex_extracted.db missing; four fixture links broken; several zero-byte placeholders
- **Source/provenance:** Historical distribution/extraction; exact matched assets UNKNOWN
- **Required stage:** 3D
- **Rebuild possibility:** Use qualified fixture via explicit db URL if contract passes
- **Blocking?:** YES for default demo; alternate fixture possible
- **Notes:** Tests/fixtures links samplehouse_library, duplex_library, duplex_extracted, samplehouse_extracted target absent assets.

## A09 placeholder databases

- **Purpose:** No usable proof content
- **Expected consumer:** Root/viewer/deploy historical paths
- **Current status:** Zero-byte output.db, validation.db, viewer/mep_rw.db, deploy/dev/ltu.db, deploy/dev/buildings/Clinic_extracted.db, Hospital_meta.db, city_index.db
- **Source/provenance:** UNKNOWN
- **Required stage:** Never acceptable as proof inputs
- **Rebuild possibility:** Generate only explicitly approved outputs later
- **Blocking?:** YES if mistaken for required inputs
- **Notes:** A filename is not evidence of a valid database.

## A10 external PWA

- **Purpose:** Potential newer runtime or feature parity
- **Expected consumer:** Historical active-PWA references
- **Current status:** External repository not retrieved or compared
- **Source/provenance:** README history references https://github.com/red1oon/bim-ootb; revision/rights/parity UNKNOWN
- **Required stage:** Only if local candidate proves insufficient
- **Rebuild possibility:** Local deploy/dev renderer exists
- **Blocking?:** NOT initially established as required
- **Notes:** Do not download during Stage 2; no assumption of source parity.

## A11 distributed viewer assets

- **Purpose:** Monolithic/split DB, geometry and positions
- **Expected consumer:** Cloud/browser streaming
- **Current status:** Not retrieved; exact versions/checksums UNKNOWN
- **Source/provenance:** deploy/OCI_UPLOAD.md documents OCI conventions, not artifact provenance
- **Required stage:** Only if distribution route chosen
- **Rebuild possibility:** Potential regeneration from qualified fixture; split compatibility UNKNOWN
- **Blocking?:** CONDITIONAL
- **Notes:** Matched _meta.db/_geo.db/_positions.bin sets required if split mode used.

## A12 included IFC fixture

- **Purpose:** First technical proof input
- **Expected consumer:** Rich extractor
- **Current status:** reference/residential/Ifc4_SampleHouse.ifc EXISTS
- **Source/provenance:** Tracked baseline fixture; upstream rights/source details still to record
- **Required stage:** 3B
- **Rebuild possibility:** Already available; do not regenerate
- **Blocking?:** NO availability block
- **Notes:** Residential technical test does not expand office product scope.

## A13 professional office corpus

- **Purpose:** Office reference and later grammar evidence
- **Expected consumer:** Stages 4–6 pipeline
- **Current status:** User possesses approximately 20 models; NOT supplied
- **Source/provenance:** User-held; per-file rights/version/provenance UNKNOWN
- **Required stage:** First at Stage 4; remainder at Stage 6
- **Rebuild possibility:** Not applicable
- **Blocking?:** NO for Stage 3; YES at relevant later stage
- **Notes:** Do not request/process now.

## A14 dependency/runtime artifacts

- **Purpose:** Java/Python/browser execution
- **Expected consumer:** Build, extractor, exporter, renderer
- **Current status:** Source declarations and local JS/WASM present; installed compatibility UNQUALIFIED
- **Source/provenance:** pom.xml and browser/Python imports; exact environment lock TBD
- **Required stage:** 3A
- **Rebuild possibility:** Install/restore only in later authorized environment
- **Blocking?:** YES until qualified
- **Notes:** IFC browser import has CDN dependencies; do not promise fully offline support.

## Acquisition and version requirements

Before use record source URI/person, rights, version, checksum, schema signature, producing tool/commit, coordinate convention and consumers. UNKNOWN provenance must remain explicit. Do not run SQLite in create mode against a missing input merely to inspect it. Distinguish source/library data from disposable build output.

Schema evidence: [library snapshots](../../library), [ERP rebuild script](../../scripts/rebuild_erp.sh), [IFCtoBOMPipeline](../../IFCtoBOM/src/main/java/com/bim/ifctobom/IFCtoBOMPipeline.java), [OCI conventions](../../deploy/OCI_UPLOAD.md). None establishes a fully reproducible populated bootstrap by itself.
