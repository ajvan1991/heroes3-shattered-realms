# Combat Script Architecture — Shattered Realms

VCMI's current combat-event system is the preferred implementation layer for stateful battle abilities. COMBAT_EVENT_TRIGGER attaches a Lua combat script to a unit. Handlers include battle setup/start, round start, before/after attack, before/after movement, spell hit, unit spellcast, death and action finished.

## Project scripts

### crimsonBloodwingDrain
Bearer: Bloodwing
Event: onAfterAttack
Rule: restore 15% of effective pre-hit health damage when the action produced at least one kill. Damage is clamped by `healthBeforeAttack`, so lethal hits count but overkill does not. Normal heal only; no resurrection.

### Eternal Blood Phoenix rebirth
No custom Crimson script is registered. The creature directly uses VCMI's built-in `COMBAT_EVENT_TRIGGER` subtype `rebirth` with `val: 20` and `guaranteed: true`. Returning Embers, if implemented later, must modify the existing result and never grant a second rebirth charge.

### crimsonDancerGrace
Bearer: Crimson Dancer
Event: onBeforeAttack
Rule: first eligible offensive melee attack in the stack's own action ignores retaliation. Counterattacks and additional attacks do not create extra charges.

### crimsonQuarryMark
Bearer/source: Bloodstalker and qualifying hero/Rite effects
Events: onAfterAttack or spell-applied combat script
Rule: apply one non-stacking mark with bounded duration. Follow-up benefit is modest.

### crimsonBloodied
Bearer: eligible Crimson creatures
Events: onActionFinished / onRoundStart, or native HP-based limiter if one is verified
Rule: below 50% HP of the surviving stack (`getCount() * getMaxHealth()`), grant the bounded Attack benefit; remove it when survivors heal back to at least half. Casualties alone do not trigger Bloodied.

### lastTestament
Source: Pale Oracle class passive
Event: onDeath
Rule: friendly Hollow stack death can create the bounded survivor buff. Trigger count is stored in a battle-state bonus.

### alignmentTransition
Source: Astral Hierophant
Events: spell hit/unit spellcast/action finished as appropriate
Rule: state-machine transitions are represented by explicit bonuses, not Lua table memory.

## State rule
Combat-event script implementations are stateless/shared. Persistent per-instance state must be stored as bonuses. Never rely on mutable Lua module fields for once-per-battle use, current Oath, Alignment step, mark owner or accumulated trigger count.

## Event safety
- Check whether the bearer is alive when required.
- Explicitly filter additional attacks and counterattacks.
- Do not rely on script-generated spells recursively firing onSpellHit.
- Rebirth resolves before final-death reactions.
- No unbounded event recursion.

## AI fallback
If MMAI cannot value a custom script reliably, expose conservative equivalent bonus metadata where possible or simplify the mechanic to an AI-understood effect.