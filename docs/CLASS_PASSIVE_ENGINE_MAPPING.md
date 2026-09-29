# Class Passive Engine Mapping — VCMI 1.7.x

Current upstream schemas confirm that custom secondary skills can provide different effect maps at Basic, Advanced and Expert, and that the Bonus system supports limiters, propagators, durations, stacking keys, updaters and combat-event hooks.

## Important architectural decision
The ten class passives are authored as **real custom skills**, but their normal level-up gain chance is zero. They are class-exclusive progression assets and must be granted/advanced by the faction/class integration layer rather than appearing as ordinary random secondary skills.

## Native / mostly-native candidates
### Sacred Formation
Promising native pieces:
- UNIT_ADJACENT limiter
- faction/creature limiter
- additive primary-skill bonuses
- battle duration
Remaining proof: dynamic adjacency reevaluation during movement.

### Blood Command
Promising native pieces:
- primary-skill bonuses
- faction limiter
Remaining proof: reliable current-HP percentage limiter. Do not fake it with permanent stats.

### Dreamstep
Promising native pieces:
- N_TURNS / STACK_GETS_TURN duration
- Speed/Defense bonuses
Remaining proof: stance-change event and whitelist cleanse.

## Event-driven candidates
Current Bonus schema exposes COMBAT_EVENT_TRIGGER and ON_COMBAT_EVENT payloads capable of applying bonuses or spells. These are candidates for:
- Dread Dominion first-hit logic
- Deep Corruption threshold/refund
- Last Testament death triggers
- Celestial Alignment transitions
- once-per-battle portions of Crimson Divination and Broken Vow

They remain staging-only until exact event names, trigger scope and save/load behavior are validated against engine examples/source.

## Script-heavy candidates
- Oneiromancy control-expiration aftereffect
- Oath drawback suppression
- Alignment state machine
- Blood Rite sacrifice transaction

These require explicit state and therefore must not be represented as fragile collections of unrelated permanent bonuses.

## Save/load requirements
Every mechanic with charges, once-per-battle state, selected Oath, Alignment state, active mark or deferred trigger must survive:
1. battle quicksave/load where supported
2. adventure save/load before battle
3. hero transfer/town visit
4. AI turn serialization

## AI requirements
Every custom action needs either:
- native AI-understood bonus valuation, or
- conservative script valuation,
otherwise the effect is redesigned.

## Failure policy
If a mechanic cannot be made deterministic, serializable and AI-usable on the target VCMI version, preserve the fantasy but simplify the implementation.


## Crimson implementation status

### Blood Command
Native conservative v0.1 mapping is staged:
- Basic: +1 Attack
- Advanced: +1 Attack, +1 Defense
- Expert: +2 Attack, +1 Defense

This intentionally stays below the value of stacking full Offense + Armorer and is easy for AI to value.

### Crimson Divination
Native support layer is staged with current VCMI identifiers:
- Basic/Advanced: 110% mana per Knowledge baseline modifier
- Expert: 120% mana per Knowledge
- Advanced/Expert: small all-school spell-damage component

The signature Rite sacrifice reduction (8/10% toward a 4% floor) is implemented in the Blood Rite spell-effect configuration rather than pretending a generic native bonus can alter arbitrary scripted costs.

No other class passive receives runtime effects until its faction vertical slice is being implemented and the effect has an engine-safe mapping.
