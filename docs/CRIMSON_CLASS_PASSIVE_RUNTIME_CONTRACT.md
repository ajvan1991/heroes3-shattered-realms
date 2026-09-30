# Crimson Class Passive Runtime Contract

## Resolved activation rule
Blood Command and Crimson Divination are implemented as VCMI secondary-skill entities with `gainChance.might=0` and `gainChance.magic=0`.

The skill-level `gainChance` is zero globally, so other classes do not receive the passive through the generic affinity fallback. VCMI hero classes have their own `secondarySkills` table, and missing skills there are banned. Crimson therefore explicitly gives its own passive a small positive class weight so an already-owned Basic passive can advance on level-up, while the opposite passive is omitted and remains banned.

Therefore every regular Crimson hero explicitly starts with the appropriate exclusive passive at Basic level:

- Bloodlord → Blood Command (Basic)
- Sanguine Seer → Crimson Divination (Basic)

The hero keeps its ordinary starting secondary skill as well (for example Vaelor keeps Basic Offense; Aveline keeps Basic Wisdom).

## Upgrade behavior
The passive is a normal registered skill for engine purposes, so once owned it can advance Basic → Advanced → Expert. The owning class has a positive class-level upgrade weight; the opposite class omits the passive entirely. Local VCMI testing must confirm that this produces the intended owned-skill upgrade behavior without unwanted cross-class acquisition.

## Candidate requirements
The Crimson candidate registers only `bloodCommand` and `crimsonDivination` from the shared class-passive staging file.

Static validation must fail when:
- either Crimson passive definition is missing;
- any Basic/Advanced/Expert effect set is empty;
- any Bloodlord lacks Blood Command;
- any Sanguine Seer lacks Crimson Divination;\n- either owning class has a non-positive class-level weight for its passive;\n- either class lists the opposite class passive.

## Local VCMI acceptance
Before G5/G7 can pass, verify:
1. Vaelor starts with Basic Offense + Basic Blood Command.
2. Aveline starts with Basic Wisdom + Basic Crimson Divination and a spellbook.
3. Blood Command and Crimson Divination display their icons/descriptions.
4. Level-up can upgrade an owned class passive.
5. The opposite class passive is not offered as a random new skill.
6. Save/reload preserves passive level and effects.

This contract is intentionally explicit because class exclusivity is a Shattered Realms design rule, not an automatic VCMI hero-class feature.


## offerCooldown correction

Upstream VCMI documents and implements `offerCooldown` as a number of following level-ups during which a gained or upgraded skill is withheld from being offered again unless no alternative upgrade exists. Skills present on the starting hero count as gained at the starting level. Because every Crimson hero explicitly starts with the class passive, a value of 99 would effectively suppress ordinary Basic -> Advanced -> Expert progression. The active Crimson passives therefore use `offerCooldown: 0`, and the static validator rejects a regression away from zero.

## Blood Command v0.1 truth-in-UI

The current v0.1 implementation is deliberately native and bounded: Basic grants +1 Attack; Advanced grants +1 Attack/+1 Defense; Expert grants +2 Attack/+1 Defense. Earlier descriptions referring to conditional low-health or blood-shed behavior overstated the implemented mechanic and have been replaced with exact runtime descriptions. A conditional Blood Command can be revisited only when it has an implemented and tested combat-event contract.
