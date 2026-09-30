# Crimson Custom Combat Event Hardening

Upstream combat-event documentation was rechecked against all four v0.1 custom creature scripts.

## Event guarantees used
- `attackIndex == 0` is the first attack by that side in the action; counterattacks also report zero, so scripts that exclude counters must check both fields.
- `payload.targets` contains `unit`, `damage`, `killed`, `damageBeforeDefense` and `healthBeforeAttack` after attack resolution.
- `onActionFinished` runs once after the complete action, including counterattacks/additional attacks.
- `onSpellHit` runs for deliberate hero/unit casts and provides an immediate post-spell refresh point.
- handlers may run with dead bearers after lethal attack resolution, so scripts must explicitly guard `unit:isAlive()`.

## Blood Feast
Drain is now calculated from effective damage to living targets:
`min(target.damage, target.healthBeforeAttack)`.

This prevents overkill damage from increasing healing. The existing rules remain:
- qualifying target must be living;
- at least one creature must be killed when `requireKill` is true;
- counterattacks are excluded when configured;
- healing is normal/permanent healing and cannot resurrect the Bloodwing stack.

## Bloodied
Threshold remains strict: below 50%, not at 50%.

In addition to attack/action/round hooks, Bloodied now refreshes on `onSpellHit`, so direct healing or damage spells do not need to wait for a later round to update the bonus. `onActionFinished` remains the catch-all for the complete resolved action.

## Quarry Mark
The mark now requires positive actual damage on the target. A zero-damage or otherwise non-damaging attack cannot mark a target merely because it appears in the attack target list.

Counterattacks and repeated attacks after attack index zero remain excluded. Duration remains two turns.

## Crimson Grace
The retaliation bypass remains:
- offensive only;
- first attack index only;
- duration `untilAfterAttackSequence`.

An explicit target-list guard was added so the script does not create a retaliation-blocking window for a malformed/empty attack event.

## Remaining live-test questions
1. confirm `untilAfterAttackSequence` expires after the intended attack/counterattack sequence on VCMI 1.7.5;
2. confirm Quarry Mark's stacking key refreshes/replaces rather than accumulating Defense penalties;
3. confirm Bloodied removal receives a bonus list accepted by `removeUnitBonuses`;
4. test Bloodied after Resurrection/heal/script damage paths that do not emit `onSpellHit`;
5. test Blood Feast with area/multi-target attacks if Bloodwing ever gains one from external mods;
6. test all scripts with Additional Attack, First Strike and Retaliation modifiers;
7. test dead-attacker reactions such as Fire Shield against Blood Feast ordering.
