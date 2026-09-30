# Crimson Court — Current Runtime Snapshot

## Creature roster
| Tier | Base | Upgrade | Implemented/staged mechanics |
|---|---|---|---|
| 1 | Veinling | Bloodbound | Bloodbound: Bloodied +1 |
| 2 | Thorn Dancer | Crimson Dancer | Dancer: Bloodied +1, Crimson Grace |
| 3 | Gorewing | Bloodwing | Flying; Bloodwing: Bloodied +1, Blood Feast |
| 4 | Hemomancer | Vein Oracle | Hemomancer: 2× Basic Weakness; Oracle: Bloodied +1, 3 casts from Weakness/Stone Skin package |
| 5 | Scarlet Huntress | Bloodstalker | Shooter; Bloodstalker: Bloodied +1, Quarry Mark |
| 6 | Sanguine Noble | Crimson Archon | Archon: Bloodied +2, Crimson Presence adjacency aura |
| 7 | Blood Phoenix | Eternal Blood Phoenix | Flying; Eternal: Bloodied +2, once-per-battle 20% Rebirth |

## Engine-backed mechanics now selected
- active creature spellcasting: SPELLCASTER
- shared creature cast count: CASTS
- enchant duration: CREATURE_ENCHANT_POWER
- scripted event abilities: COMBAT_EVENT_TRIGGER
- Phoenix resurrection: built-in combat/rebirth script
- authoritative healing/damage/bonus mutation: BattleServer
- Crimson Archon adjacency: native UNIT_ADJACENT limiter
- siege moat baseline: verified core:spell.castleMoat

## Recently hardened
- Blood Feast now counts lethal hits through pre-hit health and clamps overkill
- Bloodied now measures wounds in the surviving stack rather than counting dead creatures toward the threshold
- all 16 regular heroes have engine-backed specialties and are Tavern-eligible at the data level
- T2/T5 horde base+upgrade chains and firstAidTent Blacksmith identifier match upstream town patterns

## Still gated
- final validation of every custom Lua call on local VCMI 1.7.5
- Blood Rite active-action UI
- Blood Command / Crimson Divination class grant progression
- final spell implementations
- assets
- faction activation in mod.json

This file is a development snapshot, not a claim of a playable release.


## Hero availability safety
All sixteen regular Crimson heroes now have engine-backed creature or secondary-skill specialties and are eligible for the regular Tavern pool. Empty spellbook arrays on Sanguine Seers are valid VCMI and intentionally grant a spellbook.

Archon adjacency now uses the native UNIT_ADJACENT limiter. Creature caster spell weights are explicit rather than relying on omitted defaults.
