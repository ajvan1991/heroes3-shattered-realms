# Crimson Creature Runtime Audit — v0.1

## Engine-native abilities
Verified against current upstream VCMI documentation:
- Gorewing / Bloodwing / Blood Phoenix / Eternal Blood Phoenix: FLYING.
- Scarlet Huntress / Bloodstalker: SHOOTER with explicit shot pools.
- Hemomancer / Vein Oracle: SPELLCASTER + CASTS + CREATURE_ENCHANT_POWER.
- Eternal Blood Phoenix: native combat-event subtype `rebirth`, value 20, `guaranteed: true`.
- Crimson Archon: PRIMARY_SKILL defence aura limited by UNIT_ADJACENT.

The Archon limiter is represented as an array, matching the documented bonus limiter form.

## Creature casters
SPELLCASTER `val` is spell mastery. `addInfo` is the weighted spell-selection chance. Both Hemomancer and Vein Oracle spell entries now use explicit weight 100 rather than relying on omission/default behavior.

Hemomancer:
- Weakness, mastery 1
- 2 casts
- enchant duration 2 turns

Vein Oracle:
- Weakness, mastery 2, weight 100
- Stone Skin, mastery 1, weight 100
- 3 shared casts
- enchant duration 3 turns

The two Oracle spells therefore enter the chooser at equal weight. This is intentional for v0.1 and must be AI-tested.

## Eternal Blood Phoenix
The previous custom alias `crimsonPhoenixRebirth` added no unique behavior and only wrapped the official `combat/rebirth` implementation. It has been removed from the custom script registry. The creature now calls upstream `rebirth` directly.

Runtime contract:
- once-per-battle semantics come from VCMI rebirth;
- val 20 means the rebirth script's configured magnitude;
- guaranteed true selects the guaranteed variant;
- no duplicate custom registration exists.

## Custom combat-event abilities still requiring live validation
- Bloodied — Bloodbound, Crimson Dancer, Bloodwing, Vein Oracle, Bloodstalker, Crimson Archon, Eternal Blood Phoenix.
- Crimson Grace — Crimson Dancer.
- Blood Feast — Bloodwing.
- Quarry Mark — Bloodstalker.

These scripts use current combat-event hooks and canonical Lua duration enums, but event payload semantics, multi-action edge cases and stacking/removal must still be tested in VCMI 1.7.5.

## Balance metadata
fightValue and aiValue are resynchronized to the current design baseline for all 14 creatures. This is provisional AI metadata, not a claim of final balance.

## Required creature test matrix
1. all 14 creatures load with no unknown bonus/subtype warnings;
2. four flyers path over occupied/blocked hexes correctly;
3. both shooters consume shots and suffer normal melee/range rules;
4. Hemomancer gets exactly two casts and correct Weakness mastery/duration;
5. Oracle gets three shared casts and can select both configured spells;
6. Eternal Phoenix rebirth occurs no more than once per battle and at intended magnitude;
7. Bloodied activates below 50%, does not activate at exactly 50%, and is removed after healing above threshold;
8. Grace blocks only the intended retaliation window;
9. Blood Feast never resurrects dead members of its own stack;
10. Blood Feast obeys kill and counterattack restrictions;
11. Quarry Mark applies only to enemy targets, lasts exactly two turns and does not stack unexpectedly;
12. Archon aura affects only intended adjacent allied stacks and disappears immediately when adjacency ends;
13. save/load does not duplicate transient bonuses;
14. AI can use both creature casters and does not hang on scripted abilities.
