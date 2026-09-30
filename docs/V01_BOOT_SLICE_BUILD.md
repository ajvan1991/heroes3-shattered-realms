# Crimson v0.1 Candidate — Build & Validation

The production mod remains inert. Candidate generation writes only to `build/crimson-v01-candidate`.

## Windows
From repository root:

```powershell
py tools\validate_crimson_staging.py
py tools\build_crimson_candidate.py --allow-missing-assets
```

The first command is fail-closed and writes `production/crimson-static-validation.latest.json`.
The second creates an isolated structural candidate and `candidate-report.json`.

Do **not** interpret `--allow-missing-assets` as a playable build. It exists only so the generated registration tree can be inspected before art is complete.

A strict candidate is:

```powershell
py tools\build_crimson_candidate.py
```

It exits non-zero while direct media dependencies are missing.

## Candidate registration
The generated candidate uses stable names:
- `config/factions.json`
- `config/heroClasses.json`
- `config/heroes.json`
- `config/creatures.json`
- `config/combatScripts.json` via the VCMI `scripts` content category

It never registers a `*.staging.json` file and never edits `shattered-realms/mod.json`.

## VCMI rule confirmed upstream
Local mod content is registered through explicit arrays in `mod.json` such as `factions`, `heroClasses`, `heroes`, `creatures`, `skills`, and `spells`. Keeping these arrays out of the production manifest is therefore the current isolation boundary.

## Before local runtime
The candidate is not ready to copy into VCMI until strict build succeeds. Upstream VCMI's current `mod.json` schema explicitly provides a `scripts` content category, and `script.json` defines `combatEvent` scripts with required `description` and `priority`; the candidate generator now registers the Crimson combat script registry through that category. Local VCMI 1.7.5 still remains the final compatibility test. A structurally generated candidate is not proof of engine compatibility.


## Post-build verifier
After any structural or strict candidate build, run:

`py tools\verify_crimson_candidate.py`

This independently checks the generated registration tree, rejects staging-path leakage, requires the candidate skill surface to contain only Blood Command and Crimson Divination, verifies registered Lua sources, and cross-checks runtimeReady against direct and derived siege media counts.

The shared skill staging file may contain future faction design data; the generated Crimson candidate intentionally prunes it to the two Crimson passives.
