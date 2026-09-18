# Controlled Stage 3 proof plan

**PLAN ONLY — NOT EXECUTION AUTHORIZATION.** No command below was executed during Stage 2. Builds, installs, migrations, IFC processing, database writes, serving applications and implementation fixes require a later bounded task. Commands shown are candidates, not a guaranteed working sequence.

Start with the included `reference/residential/Ifc4_SampleHouse.ifc`. Do not request the professional office IFC until Stage 3 is accepted; that input belongs to Stage 4.

## 1. Preconditions and execution boundary

Before any mutating command:

1. Approve a dedicated Linux disposable worktree/copy and one bounded qualification task. Resolve its absolute path; **TBD until that task**. Do not use the authoritative checkout or a Windows case-insensitive copy as the scratch workspace.
2. Record source commit, clean state, fixture checksum, all input asset checksums/rights, tool versions and schemas.
3. Acquire or reproducibly rebuild the required library/catalog from known provenance. See [ASSET_MANIFEST.md](ASSET_MANIFEST.md). Do not treat an empty schema as a populated library.
4. Define mandatory fixture class/discipline scope, exclusions, expected populations and numeric tolerances before execution. Values are **TBD**, not inherited silently from lenient fixture settings.
5. Approve the precise command, output inventory, dependency/cache location and network access. Maven may download plugins/dependencies; Python dependency installation commands/version lock are **TBD** and are not provided as a ready bootstrap.
6. Preserve immutable source IFC/reference assets separately from mutable working databases. Serialize jobs initially; compiler code uses process-global configuration.
7. Resolve known schema blockers first. If a code/schema change is necessary, report it and obtain a bounded fix task. Do not patch implementation under a proof-only authorization.

Expected write areas in the disposable workspace: module target/ directories, library working DBs, DAGCompiler/lib/input and lib/output, logs/, approved report/IFC output paths, and potentially the classification YAML. Legacy wrappers additionally write migration SQL and caches; they are not allowed by a narrow output-only boundary.

External writes: Maven local repository (normally ~/.m2), Python environment if separately approved, /tmp files from some scripts, browser downloads/cache and browser database storage. Prefer isolated caches with approved paths. Exact locations and retention are TBD before execution.

## 2. Candidate command register

Paths below are relative to the approved disposable repository root. The literal command interfaces were inspected in source; SampleHouse arguments instantiate those interfaces.

### C01 — Build modules

```bash
mvn -DskipTests install
```

Candidate reactor build based on pom.xml. Writes module target/ and installs reactor artifacts into the Maven local repository; may download dependencies/plugins. **Not a test pass.** Java 17 and compatible Maven required. Module ordering/classpath, including BIM_COBOL service implementations, must be checked. Do not interpret absent service providers as acceptable routing success.

The legacy wrapper instead explicitly installs orm-core/ORMSandbox and compiles DAGCompiler; that narrower sequence does not by itself establish all service providers are built.

### C02 — Included fixture extraction

```bash
python3 DAGCompiler/python/extractIFCtoDB.py --ifc reference/residential/Ifc4_SampleHouse.ifc -o DAGCompiler/lib/input/SampleHouse_extracted.db --building-type SampleHouse
```

Interface: [extractIFCtoDB.py](../../DAGCompiler/python/extractIFCtoDB.py). Requires qualified Python, IfcOpenShell and NumPy plus an approved existing output parent directory. Writes/replaces the extraction database; does not install dependencies. Without --library, geometry is intended to be self-contained. Shared-library mode is a separate mutation boundary and is not implied here.

Account for failed mesh extraction. Record units, offsets, transforms and source IDs. Do not substitute tools/extract.py: its rel_fills_host element_guid shape conflicts with the current reader's filling_guid expectation.

### C03 — Conditional ERP/catalog bootstrap

```bash
bash scripts/rebuild_erp.sh
```

Discovered existing command, **blocked pending asset/migration review**. Requires populated library/component_library.db and sqlite3. Writes library/disc_patterns.db, compatibility ERP.db link and temporary diagnostics; applies SQL migrations. Does not install dependencies by itself. Existing destination handling must be respected; never delete a user's database to make it run.

--full has broader pipeline effects and is not selected. This command is not a bootstrap from an empty repository.

### C04 — Populate and materialize BOM

Commands expanded from scripts/run_RosettaStones.sh:

```bash
mvn exec:java -pl IFCtoBOM -Dexec.mainClass=com.bim.ifctobom.IFCtoBOMMain "-Dexec.args=--populate --classify IFCtoBOM/src/main/resources/classify_sh.yaml"
```

```bash
mvn exec:java -pl IFCtoBOM -Dexec.mainClass=com.bim.ifctobom.IFCtoBOMMain "-Dexec.args=--classify IFCtoBOM/src/main/resources/classify_sh.yaml --bom-db library/SH_BOM.db"
```

Requires built modules, compatible extracted DB, component library, catalog and schema inputs. Maven may resolve plugins/dependencies. Populates/mutates library data; pipeline deletes/recreates target BOM, writes catalog/recipe/advisory data and can rewrite classification YAML counts. Logs are also outputs. Do not document the component connection as read-only merely because an old comment says so.

Expected outputs include library/SH_BOM.db and changes to component/catalog data; capture complete before/after inventory. IFCtoBOMPipeline embeds DDL; supplying a schema snapshot is not proof that the snapshot is the runtime DDL.

### C05 — Prepare compile database

Existing helper interface, instantiated from scripts/lib_rosetta_helpers.sh:

```bash
source scripts/lib_rosetta_helpers.sh
prepare_compile_db SH SampleHouse SH RE "Sample House" BUILDING_SH_STD IFCtoBOM/src/main/resources/classify_sh.yaml
```

Copies library/SH_BOM.db to library/_SH_compile.db and applies schema snapshot SQL. No dependency installation. It suppresses some SQL errors, so successful return is insufficient. Independently inspect resulting schema/data before C06. Preserve this DB through all test evidence; the wrapper's cleanup removes it.

### C06 — Compile and explicitly enable contract tests

Expanded compilation invocation from scripts/rosetta_compile.sh:

```bash
mvn test -pl DAGCompiler -Dtest=BuildingRegistryTest -Dbom.db=library/_SH_compile.db -Dproduct.category=RE -Dpipeline.tests.skip=false
```

Qualification variant of the discovered contract invocation, explicitly enabling tests:

```bash
mvn test -pl DAGCompiler -Dtest=RosettaStoneGateTest,TotalityContractTest,RotationContractTest -Dbom.db=library/_SH_compile.db -Dproduct.category=RE -Dpipeline.tests.skip=false
```

Writes target reports, logs, compile/work data and DAGCompiler/lib/output/samplehouse.db (registry-derived expected path). May resolve Maven dependencies. BuildingRegistryTest executes the pipeline; it is not a read-only inspection command. Verify actual executed tests and fixture populations from reports.

The inherited contract invocation omits pipeline.tests.skip=false, while the parent defaults it to true. The inherited wrapper also adds empty co_empty_space compatibility tables and updates output order bounds. **Do not count such patching as proof of correct semantic output.** If direct tests reveal missing-schema failures, stop and record them; do not weaken gates.

### C07 — IFC export

```bash
python3 scripts/export_building_to_ifc.py DAGCompiler/lib/output/samplehouse.db DAGCompiler/lib/output/samplehouse.ifc
```

Interface verified in exporter main(). Requires compatible output schema and IfcOpenShell. Writes IFC; does not install dependencies. Built-in verification is limited and not independent acceptance. Required classes may be converted to proxies; simple geometry may become boxes. Do not use the Java exporter's historical hardcoded script path.

### C08 — Viewer serving

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory .
```

Proposed standard-library serving command, **not an inherited wrapper command**. Use only inside the approved disposable workspace. No dependency installation or repository writes by the server itself; browser caches/downloads can write. Local-only exposure, stop after verification.

Candidate URL:
`http://127.0.0.1:8080/deploy/dev/index.html?db=/DAGCompiler/lib/output/samplehouse.db`

The loader accepts a db URL; this URL is a qualification proposal, not proven compatibility. Serving the disposable root avoids copying output into deploy/dev. Test console/network requests and schema/coordinates. Browser IFC import may contact CDN dependencies; network/offline policy requires prior decision.

### C09 — Broad inherited wrapper: reference only, not default execution

```bash
bash scripts/run_RosettaStones.sh classify_sh.yaml
```

This is the exact documented SH wrapper. It applies migrations/restoration, builds modules, populates libraries, materializes BOM, runs compilation/checks, removes temporary compile DBs and can write migration/DV_SH_rules.sql through rule mining. It may rewrite YAML and create reports/logs. It deliberately continues through individual failures.

Do not execute as the first controlled proof. Its “PASS”/exit status is not acceptance. A separate authorization covering all mutation surfaces and known skip behavior would be required.

## 3. Expected contracts to compare, not assume

| Artifact | Required inspection |
|---|---|
| Extraction DB | elements_meta, base_geometries, element_instances, element_transforms, bounds/spatial data; rel_fills_host with filling_guid/host_guid; source GUIDs and normalization metadata |
| Component library | component_geometries, I_Geometry_Map, M_Product_Image and the exact product lookup relationships read by selected code |
| ERP/catalog | M_Product, categories, selected recipe/rule tables; compatible ERP.db link and schema |
| Spatial BOM | m_bom, m_bom_line, m_bom_line_ma, product references, registry attributes and root metadata |
| Compile DB | BOM plus required order/registry/schema records; helper success is not proof of completeness |
| Output DB | elements_meta, instances, geometry, transforms, bounds/spatial containment, declared optional system graph and provenance |
| Viewer input | loader-required building field, mesh encoding, centers/rotations and local/world basis; compare against Java writer |
| IFC | schema, units, placements, expected classes, storeys, containment/aggregates and declared materials/identity |

Use actual source DDL/queries and read-only schema inspection. Never let SQLite create a missing “input” file. Numeric tolerances, required relationships and expected populations remain TBD until preflight review.

## 4. Substage verification

**3A:** verify assets, versions, rights, paths, schema signatures, provider availability and command write boundaries. Gate G01/G02. Missing populated libraries stop compilation work; extraction-only experimentation must be separately scoped.

**3B:** run included-fixture extraction; account for input/extracted/excluded/failed elements by class and identity. Verify representative rotations, storeys, material/host relationships, normalization and nonempty mesh data. G03–G05.

**3C:** register products/materialize BOM, inspect unresolved references, compile without hidden patches, run enabled tests, inspect counts/skips and compare mesh/placement/identity/semantics. Preserve inputs and repeat isolated runs for G14. Count-only agreement fails G06. Read proof findings, not just process exit.

**3D:** load the compiled DB in deploy/dev; verify schema contract, element population, positions, rotation, bounds, storey filtering and picking identity. Capture machine-checkable samples plus visual review for rendering defects. A screenshot alone is insufficient. Any needed adapter is a later bounded fix, not assumed installed.

**3E:** export IFC, then use an independent validation path/consumer to parse and compare classes, geometry, units, containment, transforms and required relationships. Validator/tool/version and exact command are **TBD before 3E execution**; exporter self-verification is not sufficient. Required proxy downgrades/omissions fail; explicitly excluded semantics remain reported.

Stage 3 completion requires a consolidated PASS/FAIL/INCONCLUSIVE report with checksums, commands, versions, populations, tolerances, skips, losses and applicable gate results. It proves a technical fixture slice, not office generation or professional compliance.

## 5. Rollback and cleanup — later execution only

Before a run, record exact canonical sandbox/cache/output paths and preserve immutable input copies/checksums. On failure stop processes, close DB handles, preserve logs/reports and failed artifacts for diagnosis. Do not overwrite the last good evidence.

Cleanup must target only run-created paths in the approved disposable workspace. Verify resolved paths, ownership and symlink destinations first. Do not use broad git clean/reset or recursive deletion against the authoritative checkout. Retain the evidence bundle before retiring the disposable worktree via a reviewed operation. Do not remove shared dependency caches or original assets.

If any authoritative file changed unexpectedly, stop, report exact paths/diff and obtain a recovery decision; do not automatically revert possible user changes. No cleanup commands are authorized in Stage 2.

## 6. Stop conditions

Missing/unknown-provenance required assets; incompatible schema; unexplained input loss; unavailable mandatory providers/checks; empty/skipped tests; stub success; critical log-only findings; order/BOM divergence; coordinate ambiguity; unapproved proxy export; viewer mismatch; dependency/network action outside authorization; or writes outside the approved sandbox.

Do not “fix” case-differing filenames, fabricate library contents, relax tests, inject empty tables to pass a gate, or claim professional/complete-six-discipline/clash-free/code-compliant/constructible BIM. Record findings first and request a bounded fix decision when needed.
