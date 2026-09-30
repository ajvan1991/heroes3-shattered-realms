# Crimson v0.1 Candidate Content Closure

The isolated candidate must be self-contained. A source-tree resource existing somewhere outside the generated candidate is not sufficient runtime evidence.

## Registered categories
- factions
- heroClasses
- heroes
- creatures
- skills
- scripts

The production `mod.json` remains inert; these registrations are generated only under `build/crimson-v01-candidate`.

## Class-passive policy
The shared staging file currently contains all ten planned class passives. The Crimson candidate needs Blood Command and Crimson Divination as real implemented passives; the other eight are future-faction definitions and currently contain empty effects.

The static validator therefore explicitly requires Basic/Advanced/Expert effects for the two Crimson passives and does **not** interpret empty future-faction effects as implemented mechanics.

A later cleanup may split class-passive staging by faction. Until then, registration of the shared skill file is acceptable for structural testing because all passives have zero gain chance, but only the Crimson pair is part of v0.1 acceptance.

## Media materialization
The candidate builder now:
1. discovers direct media references from generated candidate config;
2. requires a non-empty source file;
3. copies it into the same resource path under candidate `Content`;
4. re-checks the generated output;
5. reports `copiedMediaFiles`;
6. refuses strict runtime-ready status while any direct reference is absent from the candidate.

This closes the earlier false-positive risk where strict preflight could see source assets while the generated mod itself did not contain them.

## Remaining derived resources
Resources implied by conventions rather than direct quoted JSON paths (notably the siege `imagePrefix` family) remain governed by the asset manifest/runtime gate and must be added to candidate materialization before siege acceptance can pass.


## Puzzle-map filename contract
Upstream `CTownHandler::loadPuzzle` constructs puzzle filenames from the **zero-based vector position**, formatted as two digits: `<prefix>00` through `<prefix>47`. The JSON `piece.index` field controls reveal order; it is not the filename number. For Crimson prefix `CRIMSON/PUZZLE/CRP`, the candidate therefore requires `CRP00.png ... CRP47.png`.
