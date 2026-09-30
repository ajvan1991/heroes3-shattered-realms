# v0.1 Registration Tree Audit

Status: staging intentionally disconnected from `mod.json`.

## Critical finding
VCMI loads gameplay entity files through explicit content arrays in the local `mod.json` such as `factions`, `heroClasses`, `heroes`, `skills`, `creatures`, `spells`, and other supported categories.

The current Shattered Realms `mod.json` contains **none** of those arrays. This is intentional at the present safety stage: every `*.staging.json` file is therefore inert even if the user manually enables the mod in Launcher. `keepDisabled: true` only prevents automatic enabling on install; it is not the mechanism that disconnects staging content.

This distinction is now part of the activation contract.

## Staged entity files
- Crimson faction/town
- Crimson hero classes
- Crimson heroes
- Crimson creatures
- class passives
- universal/counterplay spells
- Blood Rites
- combat-event script registry
- spell-effect script registry

The separate Crimson `buildings.staging.json` is an authoring source. Town buildings are embedded in `faction.staging.json`; it must not be registered as an independent VCMI content category.

## Script source inventory
Registered by the staged registries:
- combat/crimsonBloodwingDrain.lua
- combat/crimsonDancerGrace.lua
- combat/crimsonBloodied.lua
- combat/crimsonQuarryMark.lua
- spells/bloodRiteUnitEffect.lua
- spells/selectiveDispel.lua

Unregistered research/legacy source:
- combat/crimsonArchonAura.lua — superseded by native UNIT_ADJACENT
- spells/battleSpellCost.lua — research prototype; no active registration

Transaction helpers currently present:
- combat/riteOpenVein.lua
- combat/riteScarletShelter.lua

These are not independent combatEvent registrations; their production use depends on the Blood Rite bridge architecture.

## Activation rule
Do not point production `mod.json` at files whose filenames still contain `.staging`. First create an activation candidate set with stable production filenames and only the subset whose assets/references have passed local validation.

Recommended first activation order:
1. script registrations + required Lua sources
2. only validated skills/spells
3. creatures
4. faction/town + hero classes
5. heroes

The first activation candidate should exclude reserved spells and any player-facing mechanic without a validated runtime bridge.

## Asset gate
Config registration alone is insufficient. Crimson currently references placeholder/nonexistent media for town screen, siege, puzzle map, heroes, creatures, skills and spells. The full faction must remain disconnected until a minimum placeholder asset pack using valid VCMI resource formats exists.

## Local-test definition of success
A registration candidate passes only when VCMI 1.7.5:
- starts without schema/identifier errors;
- creates a map containing Crimson;
- opens the town screen;
- recruits every tier and upgrade;
- opens Tavern and Mage Guild;
- enters and exits a normal battle;
- enters and exits a siege;
- saves and reloads;
- reaches a week rollover;
- lets AI own/build/recruit from Crimson without a fatal error.

Passing JSON review is not equivalent to this runtime gate.
