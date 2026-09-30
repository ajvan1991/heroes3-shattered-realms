# Crimson Court v0.1 Static Invariants

These invariants are repository-side gates. They do not replace VCMI 1.7.5 runtime testing.

## Creature progression
- exactly seven town tiers;
- exactly one base and one upgrade in every tier;
- both members report the correct tier level;
- each base creature upgrades to exactly its paired upgraded creature;
- upgraded creatures do not declare a further upgrade;
- all combat/economy numeric fields are positive and damage min <= max;
- SHOOTER implies a positive shot count and shot counts are not allowed on non-shooters.

## Crimson combat trigger regression matrix
Expected combat-event subtypes:
- Bloodbound: crimsonBloodied
- Crimson Dancer: crimsonDancerGrace + crimsonBloodied
- Bloodwing: crimsonBloodwingDrain + crimsonBloodied
- Vein Oracle: crimsonBloodied
- Bloodstalker: crimsonBloodied + crimsonQuarryMark
- Crimson Archon: crimsonBloodied
- Eternal Blood Phoenix: native rebirth + crimsonBloodied

Any accidental removal/addition fails static validation.

## Hero roster
- exactly 16 regular Crimson heroes;
- exactly 8 Bloodlords and 8 Sanguine Seers;
- 1–3 starting army stacks with valid positive min/max ranges;
- no duplicate starting secondary-skill identifiers;
- every Sanguine Seer explicitly has a spellbook;
- every hero carries the class-exclusive passive defined by the class-passive runtime contract.

## Why these checks exist
The candidate build already validates references and packaging. These invariants catch a different class of regression: structurally valid JSON that silently changes gameplay topology, such as breaking an upgrade pair, removing a signature combat trigger, losing a Seer's spellbook, or unbalancing the 8/8 class roster.

A PASS means the authored data still matches the locked Crimson v0.1 design contract. It does not mean the mechanics have passed engine execution.
