# Crimson Static QA CI

GitHub Actions now runs the repository-side Crimson QA chain on relevant pushes, pull requests, and manual dispatch.

Order:
1. compile every Python file under `tools/`;
2. run `validate_crimson_staging.py`;
3. run `asset_pipeline.py` in non-strict production-contract mode;
4. build the isolated candidate with `--allow-missing-assets`;
5. run the independent candidate verifier.

The candidate build is deliberately structural while real art/audio are missing. CI passing does **not** change G3/G4 runtime readiness and does not claim that VCMI can load the release candidate without missing resources.

The compile step is intentionally first: it catches syntax damage in QA/build scripts before those scripts can incorrectly report success.

Asset pipeline is non-strict in CI because missing real assets are currently expected. Manifest inconsistencies, invalid statuses, broken batch selectors, stale counts, or malformed derived siege/puzzle families still fail.

A future asset-complete gate should switch the asset pipeline/candidate build to strict mode; that change must happen only after real resources exist, never by creating fake placeholder files.
