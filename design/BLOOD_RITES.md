# Blood Rite System — v0.1 Gameplay Contract

Blood Rites are Crimson Court's strategic identity. They exchange something tangible for a short, bounded advantage. They are not free passive bonuses.

## Rite resource model
Initial implementation should prefer **HP/casualty, gold/rare-resource, or once-per-battle state** over introducing a brand-new global resource. A dedicated Blood resource is deferred unless playtesting proves it necessary.

## Five initial Rites

### Rite of the Open Vein
**Cost:** selected living Crimson stack loses 8% current HP, never killing the last creature.
**Effect:** +2 Attack for 2 rounds.
**Advanced faction support:** may also grant +1 Speed for the first round only.
**Cap:** once per target stack per battle.

### Rite of Scarlet Shelter
**Cost:** 10% current HP from target.
**Effect:** +3 Defense and 10% ranged damage reduction for 2 rounds.
**Purpose:** defensive alternative to pure Bloodied aggression.

### Rite of the Hunt
**Cost:** modest hero mana + 5% current HP from the selected Crimson ranged/hunter stack.
**Effect:** target enemy receives a non-stacking Quarry-style mark for 2 rounds; follow-up bonus is capped.
**Cap:** one active Rite-of-the-Hunt mark per caster.

### Rite of Returning Embers
**Cost:** significant mana plus a meaningful HP sacrifice from one surviving Crimson stack.
**Effect:** improves the *existing* Eternal Blood Phoenix rebirth result if its one-per-battle rebirth later triggers.
**Hard rule:** never creates a second rebirth and never resurrects a currently destroyed Phoenix stack on cast.

### Rite of the Red Moon
**Cost:** once per battle; caster pays mana and two selected Crimson stacks each lose 6% current HP.
**Effect:** all living Crimson stacks gain +1 Attack and +1 Defense for 2 rounds.
**Hard rule:** cannot be recast; no Speed bonus; no healing.

## Interaction with Crimson Divination
Basic/Advanced/Expert cost reduction applies only to the sacrifice component explicitly tagged as reducible.
Minimum sacrifice floors:
- HP rite: never below 4% current HP
- resource rite: never below 50% listed non-HP cost
- once-per-battle charge: never refundable

## AI rules
AI should cast a Rite only when estimated short-term value exceeds sacrifice by a safety margin.
Avoid:
- sacrificing a stack into one-hit range for a marginal buff
- using Red Moon with fewer than two meaningful stacks
- Return Embers without Eternal Blood Phoenixes
- Hunt on a target expected to die before follow-up

## Counterplay
Quiet the Blood offsets offensive rites.
Veil of Still Water mitigates marked burst.
Wash Away can remove explicitly removable Rite-applied marks/buffs.
Mortal Anchor limits sustain/rebirth value.
No counter spell deletes the Blood Rite system itself.
