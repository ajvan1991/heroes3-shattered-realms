# Crimson Class Passive Runtime Contract

## Resolved activation rule
Blood Command and Crimson Divination are implemented as VCMI secondary-skill entities with `gainChance.might=0` and `gainChance.magic=0`.

A zero gain chance prevents normal random level-up offering. It does **not** grant the skill to a hero merely because the hero belongs to Bloodlord or Sanguine Seer.

Therefore every regular Crimson hero explicitly starts with the appropriate exclusive passive at Basic level:

- Bloodlord → Blood Command (Basic)
- Sanguine Seer → Crimson Divination (Basic)

The hero keeps its ordinary starting secondary skill as well (for example Vaelor keeps Basic Offense; Aveline keeps Basic Wisdom).

## Upgrade behavior
The passive is a normal registered skill for engine purposes, so once owned it can advance Basic → Advanced → Expert. It is not intended to be randomly offered to heroes that do not already own it.

## Candidate requirements
The Crimson candidate registers only `bloodCommand` and `crimsonDivination` from the shared class-passive staging file.

Static validation must fail when:
- either Crimson passive definition is missing;
- any Basic/Advanced/Expert effect set is empty;
- any Bloodlord lacks Blood Command;
- any Sanguine Seer lacks Crimson Divination.

## Local VCMI acceptance
Before G5/G7 can pass, verify:
1. Vaelor starts with Basic Offense + Basic Blood Command.
2. Aveline starts with Basic Wisdom + Basic Crimson Divination and a spellbook.
3. Blood Command and Crimson Divination display their icons/descriptions.
4. Level-up can upgrade an owned class passive.
5. The opposite class passive is not offered as a random new skill.
6. Save/reload preserves passive level and effects.

This contract is intentionally explicit because class exclusivity is a Shattered Realms design rule, not an automatic VCMI hero-class feature.
