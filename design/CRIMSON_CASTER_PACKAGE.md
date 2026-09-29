# Crimson Court Caster Package — v0.1

## Hemomancer
Role: tier-4 utility caster. The base creature should not become a second hero.
- limited casts
- low spell power
- one simple blood-themed debuff/support spell
- no mass spell
- no direct resurrection
- no hard disable

Initial candidate: a creature-cast version of Weakness or a future low-level blood debuff implemented through a validated VCMI ability spell.

## Vein Oracle
Role: upgraded tactical caster.
- more casts than Hemomancer
- slightly stronger effect
- Bloodied +1 Attack remains its separate upgrade identity
- may receive one support and one debuff option, but not a broad spellbook

Initial candidates:
- Weakness-style attack reduction
- defensive blood ward with short duration

## Spellcasting guardrails
1. creature spellcasting cannot duplicate a full hero turn in value
2. no percentage HP sacrifice unless the AI can understand it
3. spell effects must respect immunity
4. script-triggered spell casts must not recursively fire combat-event spell handlers
5. number of casts must be visible and finite
6. auto-cast behavior requires explicit AI testing

## Activation gate
Do not wire SPELLCASTER/CASTS until the exact current VCMI ability-spell configuration and target semantics are verified against upstream examples.
