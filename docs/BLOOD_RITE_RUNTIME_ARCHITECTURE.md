# Blood Rite Runtime Architecture

Blood Rites are active hero-side combat decisions. They must not be implemented as passive creature abilities because the player chooses the target and accepts an explicit sacrifice.

## Runtime contract
Each Rite is modeled as a combat spell/action with:
1. target validation
2. sacrifice transaction
3. effect application
4. once-per-target / once-per-battle marker where required
5. AI valuation
6. combat log + VFX

## Sacrifice safety
The transaction is server-authoritative.
For an HP sacrifice:
- read target available health
- calculate percentage using integer-safe rounding
- cap damage so at least one HP remains where the Rite says it cannot kill
- call BattleServer:damageUnit
- only after successful sacrifice apply the benefit
- never refund the sacrifice because the target later becomes invalid

## Rite mapping

### Open Vein
Target: friendly living Crimson stack.
Sacrifice: 8% current HP, nonlethal.
Effect: +2 Attack, 2 turns.
Marker: target cannot receive Open Vein again that battle.

### Scarlet Shelter
Target: friendly living Crimson stack.
Sacrifice: 10% current HP, nonlethal.
Effect: +3 Defense plus 10% ranged mitigation, 2 turns.
Marker: target-specific, no stacking.

### Hunt
Target model: two-stage action is required — friendly source + enemy quarry — and therefore needs a dedicated action/script rather than pretending a normal one-target spell can perform both selections.
Cost: hero mana plus 5% source HP.
Effect: Quarry Mark family, 2 turns.
Fallback if two-stage UI is not practical: hero casts directly on enemy for mana only; HP sacrifice is removed rather than hidden.

### Returning Embers
Target: friendly Eternal Blood Phoenix.
Sacrifice: significant mana + HP from a separate surviving Crimson stack.
Because this is multi-target, implement only after two-stage action support is validated.
Effect: modifies the existing rebirth percentage/marker; never adds a second rebirth trigger.

### Red Moon
Target: no enemy target; requires two valid friendly Crimson stacks.
Sacrifice: 6% current HP from each.
Effect: +1 Attack/+1 Defense to living Crimson stacks for 2 rounds.
Marker: hero/battle once-only.

## Crimson Divination integration
Cost reduction is computed before damage but after validating minimum sacrifice floors.
Basic/Advanced/Expert modifiers must never reduce HP sacrifice below 4%.

## AI
Rites expose explicit estimated benefit and sacrifice values. If custom action valuation cannot be integrated reliably, v0.1 AI uses only Open Vein and Scarlet Shelter; multi-target rites remain player-only until proper AI support exists.

## Network/save rule
No Rite state is stored in Lua globals. Use engine bonuses/markers so clients and saves receive authoritative state.
