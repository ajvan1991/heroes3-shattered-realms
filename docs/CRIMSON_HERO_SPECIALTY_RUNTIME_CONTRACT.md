# Crimson Hero Specialty Runtime Contract

VCMI's current hero schema provides native specialty shortcuts for creatures, secondary skills, and spell specialties. Crimson v0.1 deliberately uses only implemented native shortcuts in the regular 16-hero Tavern roster.

## Runtime roster

### Bloodlords
- Vaelor — Veinling creature specialty
- Seris — Thorn Dancer
- Khaeren — Gorewing
- Maelira — Scarlet Huntress
- Othrys — Sanguine Noble
- Rhaevan — Blood Phoenix
- Thalia Veyn — Offense
- Ilyr Thorn — Offense

### Sanguine Seers
- Aveline — Hemomancer
- Sevrin — Wisdom
- Miraleth — Intelligence
- Caelis — Intelligence
- Vespera — Sorcery
- Elyss Vane — Mysticism
- Saereth — Mysticism
- Lysandra Noct — Sorcery

The duplicate skill-specialist pairs are intentional temporary v0.1 substitutions for custom specialties that are not yet implemented. They are not the desired final diversity target.

## Static guarantees

The Crimson validator now requires every secondary-skill specialty to have a positive weight in that hero class's `secondarySkills` table. This prevents a hero from specializing in a skill their class cannot normally receive.

The exact temporary duplicate-specialty set is also locked. An accidental fifth duplicate or silent reassignment fails CI instead of quietly changing the roster.

## Upgrade policy

Custom Blood Command, Blood Rite, Quarry Mark, Crimson Divination or similar hero specialties should return only when their actual runtime bonus/script contract exists and is tested. Narrative design text alone is not sufficient to activate a specialty.

## Local acceptance

VCMI runtime testing must still confirm:
- all 16 heroes can appear under the intended Tavern rules;
- native creature and secondary specialties display the correct name/description/icon;
- specialty scaling behaves as expected through multiple hero levels;
- save/reload preserves the specialty;
- no custom placeholder specialty is exposed to the player.
