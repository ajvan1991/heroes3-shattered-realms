# Crimson Court Ability Matrix — Implementation Status

| Creature | Ability | v0.1 target | Status |
|---|---|---|---|
| Bloodbound | Bloodied | +1 Attack below 50% health | scripted staging |
| Crimson Dancer | Crimson Grace | first qualifying own-action melee attack blocks retaliation | scripted staging |
| Bloodwing | Blood Feast | 15% heal from valid damage on a killing attack; no resurrection | scripted staging |
| Vein Oracle | Bloodied + caster package | +1 Attack below 50%; bounded spellcasting | Bloodied staged / caster pending |
| Bloodstalker | Bloodied + Quarry Mark | +1 Attack below 50%; non-stacking mark | Bloodied staged / mark pending |
| Crimson Archon | Greater Bloodied + aura | +2 Attack below 50%; bounded nearby support | Bloodied staged / aura pending |
| Eternal Blood Phoenix | Greater Bloodied + Eternal Rebirth | +2 Attack below 50%; 20% once-per-battle rebirth | staged |

Base creatures remain intentionally simpler. Upgrade value comes from modest stats plus one meaningful mechanic rather than every tier receiving multiple high-impact abilities.

## Bloodied behavior
- health threshold is dynamic, not snapshotted at battle start
- healing back above the threshold removes the Attack bonus
- no bonus stacks on repeated event calls
- ordinary upgrades use +1 Attack
- Crimson Archon and Eternal Blood Phoenix use +2
- threshold is strictly below 50%, not at 50%
- effect has no Defense/Speed/damage multiplier component

## Remaining implementation order
1. validate Bloodied server bonus add/remove API against target VCMI
2. Quarry Mark
3. Noble/Archon aura
4. Hemomancer/Vein Oracle spell package
5. Blood Rite attach/transaction layer
6. Bloodlord/Seer class skill grants
7. local VCMI battle test


## Blood Rite runtime progress
- Rite of the Open Vein: executable server-side transaction script staged
- Rite of Scarlet Shelter: executable server-side transaction script staged
- both are nonlethal and target-limited once per battle
- both sacrifice HP before applying their benefit
- Hunt / Returning Embers / Red Moon remain gated on validated multi-target/action UI
- these scripts expose an apply() transaction; the player-facing action/spell bridge is still required before they are usable in a normal battle UI

## Caster runtime
- Hemomancer: SPELLCASTER Weakness mastery 1, 2 casts, enchant power 2
- Vein Oracle: Weakness mastery 2 + Stone Skin mastery 1, 3 shared casts, enchant power 3
- VCMI Battle AI already evaluates active SPELLCASTER bonuses; final AI quality remains a local-test gate
