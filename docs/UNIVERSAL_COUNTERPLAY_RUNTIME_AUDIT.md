# Universal Counterplay Runtime Audit — v0.1

Audit target: current upstream VCMI bonus semantics and the Shattered Realms counterplay staging file.

## Native-effect spells retained in generation
The following currently use engine bonus types with upstream evidence and retain normal generation chance:
- Sever Formation — PRIMARY_SKILL / STACKS_SPEED
- Clear Mind — MIND_IMMUNITY
- Unbound Step — STACKS_SPEED
- Grounding Sigil — STACKS_SPEED
- Burden Stone — PRIMARY_SKILL
- Brand the Frail — PRIMARY_SKILL
- Flare of Waking — MORALE / STACKS_SPEED
- Quiet the Blood — PRIMARY_SKILL
- Veil of Still Water — GENERAL_DAMAGE_REDUCTION, subtype damageTypeAll

For numeric stat/damage modifiers, staging now declares BASE_NUMBER explicitly where appropriate instead of relying on implicit defaults.

Upstream confirms GENERAL_DAMAGE_REDUCTION + damageTypeAll as the all-damage reduction form used by the engine and Armorer path. Upstream also confirms MIND_IMMUNITY as the standard mind-spell targeting immunity.

## Reviewed custom-effect spells
These still depend on the Shattered Realms selective-dispel bridge and therefore require the custom-effect registration plus a local cast test:
- Scorch the Oath
- Wash Away
- Fateful Exchange

They remain generated because the bridge is intentionally modeled on the official dispel implementation, but they are not considered activation-proven until the local test passes.

## Disabled / reserved
The following are excluded from normal v0.1 generation:
- Mortal Anchor — no verified healing/resurrection suppression effect is currently staged.
- Leyline Convergence — unresolved global mechanic.
- Echo of the Fallen — unresolved corpse/death mechanic.
- Hour of Silence — battle-side spell-cost semantics require live validation.

An effectless spell must never retain a positive generation chance.

## Activation assertions
1. generated spell has at least one executable effect at every mastery;
2. native bonus identifiers resolve without warnings;
3. numeric value type produces the documented magnitude;
4. positive/negative targeting matches flags;
5. Clear Mind blocks mind-spell targeting rather than merely adding resistance;
6. Still Water reduces incoming damage by its stated percentage;
7. selective dispel never strips permanent creature abilities;
8. no RESERVED spell appears in Mage Guild, shrine, scroll or random-spell generation.
