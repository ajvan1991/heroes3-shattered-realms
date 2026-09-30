# Crimson Static QA CI

GitHub Actions runs the repository-side Crimson QA chain on relevant pushes, pull requests, and manual dispatch.

## Executed order
1. compile every Python file under `tools/`;
2. run `validate_crimson_staging.py`;
3. run `validate_reference_closure.py` against the committed structural snapshot;
4. run `validate_runtime_gates.py` in full mode so committed evidence/status claims remain fail-closed;
5. run `validate_runtime_gates.py --pre-build` to validate the build-safe gate contract without transient G3/G4 locks;
6. run `asset_pipeline.py` in non-strict production-contract mode and assert 530 jobs, zero unowned resources, zero unowned boot-slice resources, zero priority mismatches and zero manifest errors;
7. execute all 16 production batches independently: A1–A5, B1–B8, C1–C3;
8. build the isolated candidate with `--allow-missing-assets`;
9. run `verify_crimson_candidate.py`;
10. publish paths to the generated QA reports in the GitHub job summary.

The candidate build is deliberately structural while real art/audio are missing. CI passing does **not** change G3/G4 runtime readiness and does not claim that VCMI can load the release candidate without missing resources.

The compile step is intentionally first: it catches syntax damage in QA/build scripts before those scripts can incorrectly report success.

## Asset-contract checks
Asset QA is non-strict only with respect to files that are honestly still marked missing. Structural errors remain fatal, including stale manifest counts, invalid status/type/path data, malformed siege or puzzle families, broken/unsafe batch selectors, missing production-batch ownership for any of the 530 jobs, missing boot-slice ownership, and asset-to-batch priority mismatches.

Current manifest contract: 530 jobs = 451 direct references + 31 derived siege resources + 48 derived puzzle resources. Current priority snapshot is A 217 / B 242 / C 71, with 241 boot-slice jobs.

## Candidate integrity
The builder consumes staging, reference-closure and runtime-gate validators before packaging. The candidate merges the staged combat-event and spell-effect registries into one production-style `config/scripts.json`. Its v0.1 script surface is exact: four Crimson `combatEvent` scripts plus `bloodRiteUnitEffect` and `selectiveDispel` as `spellEffect` scripts. Registered Lua sources must exist, be non-empty and be copied; duplicate script IDs across registries are fatal. The independent verifier checks the exact six-script IDs, their `implements` kinds, media references, siege/puzzle families, runtime readiness, manifest hashes/file inventory and registered Lua materialization rather than trusting the builder report.

No placeholder or zero-byte asset may be used to satisfy a gate.

## Evidence policy
The workflow no longer uploads a generated artifact as release evidence. Generated report locations are written to the GitHub job summary. The committed runtime-gate document records only a specifically verified successful run; a later green run is not automatically promoted to committed evidence.

A future asset-complete gate may switch the asset pipeline/candidate build to strict mode only after real resources exist. It must never be made green by fabricating placeholder files.
