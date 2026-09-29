# Crimson Growth and Recruitment Contract

## Base growth
Base weekly growth is owned by creature definitions. Current v0.1 values remain:
- T1 Veinling/Bloodbound: 14
- T2 Thorn Dancer/Crimson Dancer: 9
- T3 Gorewing/Bloodwing: 7
- T4 Hemomancer/Vein Oracle: 4
- T5 Scarlet Huntress/Bloodstalker: 3
- T6 Sanguine Noble/Crimson Archon: 2
- T7 Blood Phoenix/Eternal Blood Phoenix: 1

Upgrades do not create a second independent growth pool; they share their dwelling tier.

## Horde tiers
VCMI town `horde` uses zero-based creature-tier indices. Crimson keeps the planned Rampart-like distribution:
- index 1 = T2
- index 4 = T5

Two explicit horde buildings occupy stable custom IDs:
- 44 Garden of Red Thorns — T2 horde building
- 45 Scarlet Hunting Grounds — T5 horde building

The town horde mechanism, not an invented custom creature-growth bonus, is the source of the horde behavior.

## Dwelling ID contract
VCMI's town creature mapping expects dwelling IDs by tier:
- base: 30..36
- first upgrade: 37..43

Crimson follows this exactly. The faction creature arrays and building IDs therefore line up T1 through T7 without a custom recruitment bridge.

## Mage Guild UI contract
The faction now stages the standard five-level H3 spell icon coordinate layout and guild window position. These are UI coordinates only; actual universal-spell availability remains controlled by the spell distribution layer.

## Test assertions
Local activation test must verify:
1. each base dwelling recruits only its matching base creature;
2. each upgrade replaces/unlocks the matching upgraded creature;
3. weekly growth is not duplicated between base and upgrade;
4. Citadel/Castle growth modifiers apply normally;
5. horde slot 0 affects T2 and horde slot 1 affects T5;
6. no horde building affects an unrelated tier;
7. Mage Guild levels 1–5 render spell slots without overlap;
8. universal spells can appear according to their configured availability, independent of hero class.
