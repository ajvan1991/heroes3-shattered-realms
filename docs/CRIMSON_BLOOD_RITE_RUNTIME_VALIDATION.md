# Crimson Blood Rite Runtime Validation

## Duration contract
Open Vein and Scarlet Shelter are designed as exactly two-turn effects. Their Lua spell effect no longer derives this promise from spell Power or `getEffectDuration()`.

Each mastery level now sends `turns: 2` explicitly and the spellEffect schema requires a bounded integer duration. Runtime bonuses use `ENUM.BonusDuration.nTurns`, matching current official VCMI Lua examples.

The once-per-target marker uses `ENUM.BonusDuration.oneBattle`.

## Marker contract
VCMI's own rebirth combat script demonstrates that script-only state can be represented as a bonus type string and queried through `hasBonuses({ type = ... })`. Blood Rite markers therefore remain isolated state bonuses rather than visible stat modifiers:
- shattered-realms:riteOpenVeinUsed
- shattered-realms:riteScarletShelterUsed

This still requires a local VCMI 1.7.5 load/cast/save test before activation because custom namespaced bonus-type resolution is the remaining compatibility question.

## Spell-cost field
The Hour of Silence helper was also normalized to the canonical Lua duration enum. Its ally/enemy perspective semantics remain gated pending a live two-player-side combat test; enum correctness alone does not prove which side receives each battle-wide cost modifier.

## Required local tests
1. cast each Rite on a healthy living stack;
2. verify HP sacrifice is nonlethal;
3. verify buff lasts exactly two unit turns;
4. verify same Rite cannot be recast on the same stack that battle;
5. verify the other Rite can still be used independently;
6. verify dispel interaction does not clear the once-per-battle marker unless intentionally designed;
7. save/reload during battle if supported by the test harness and confirm marker state;
8. verify undead/nonliving target rejection;
9. verify Open Vein and Shelter do not resurrect killed creatures;
10. verify Hour of Silence cost direction independently for caster and opponent before enabling it.
