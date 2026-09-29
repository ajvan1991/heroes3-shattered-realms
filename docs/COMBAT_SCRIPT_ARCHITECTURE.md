# Combat Script Architecture — Shattered Realms

VCMI's current combat-event system is the preferred implementation layer for stateful battle abilities. COMBAT_EVENT_TRIGGER attaches a Lua combat script to a unit. Handlers include battle setup/start, round start, before/after attack, before/after movement, spell hit, unit spellcast, death and action finished.

## Project scripts

### crimsonBloodwingDrain
Bearer: Bloodwing
Event: onAfterAttack
Rule: restore 15% of valid living-target damage only when the action produced at least one kill. Hard cap by damage actually dealt.

### crimsonPhoenixRebirth
Bearer: Eternal Blood Phoenix
Event: onDeath
Rule: once per battle, restore a conservative percentage of initial stack count.
Implementation: prefer a dedicated configuration of VCMI's built-in rebirth combat script rather than custom code.
Rite interaction: Returning Embers modifies the one existing rebirth result; never grants another charge.

### crimsonDancerGrace
Bearer: Crimson Dancer
Events: onBeforeAttack / onActionFinished
Rule: first eligible offensive melee attack in the stack's own action ignores retaliation. Counterattacks and additional attacks do not create extra charges.

### crimsonQuarryMark
Bearer/source: Bloodstalker and qualifying hero/Rite effects
Events: onAfterAttack or spell-applied combat script
Rule: apply one non-stacking mark with bounded duration. Follow-up benefit is modest.

### crimsonBloodied
Bearer: eligible Crimson creatures
Events: onActionFinished / onRoundStart, or native HP-based limiter if one is verified
Rule: below 50% current stack health relative to its current maximum, grant the bounded Attack benefit; remove it when threshold is no longer met.

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