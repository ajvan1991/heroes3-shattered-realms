# Crimson Court — Town Dependency Audit

Status: data-level dependency graph clean; runtime/assets still gated.

## Verified against current upstream VCMI
- Rampart uses `horde: [1,4]`, matching Crimson T2/T5 selection.
- Native horde buildings use base + upgraded pairs linked through `upgrades` to base/upgraded dwellings.
- Native Blacksmith war-machine identifiers are unscoped strings such as `firstAidTent`.
- Five-level Mage Guild layout and spell-position counts match the upstream five-level pattern.

## Automated graph audit
Current canonical Crimson building graph: **41 definitions**.

Results:
- duplicate numeric building IDs: 0
- dangling `requires` references: 0
- dangling `upgrades` references: 0
- dependency/upgrade cycles: 0
- Hall-slot references to missing buildings: 0
- Hall-slot buildings missing town-screen structures: 0
- canonical building file vs embedded faction buildings: exact match
- town structures: 41 definitions
- Hall slots expose 38 unique building IDs

## Stable ID bands
- Mage Guild: 0–4
- Tavern: 5
- Fort/Citadel/Castle: 7–9
- economy/services: 10–16
- Grail: 26
- base dwellings: 30–36
- upgraded dwellings: 37–43
- horde chains: 44–47
- faction specials: 50–55

## Horde chains
- 44 `hordeThorns` -> T2 base dwelling
- 45 `hordeThornsUp` -> T2 upgraded dwelling; requires 44
- 46 `hordeHunt` -> T5 base dwelling
- 47 `hordeHuntUp` -> T5 upgraded dwelling; requires 46

## Remaining activation gates
This audit does **not** mark the town playable. Still required in local VCMI 1.7.5:
1. all referenced town/map/siege/structure resources physically exist;
2. build-screen coordinates/masks are visually tested;
3. Mage Guild spell generation works in a live Crimson town;
4. Grail construction/income and later faction bonus work;
5. siege shooter, moat and wall geometry work in a live siege;
6. dwelling recruitment, upgrades and horde growth survive week rollover;
7. save/reload preserves complete town build state.

Staging remains disabled until these gates pass.
