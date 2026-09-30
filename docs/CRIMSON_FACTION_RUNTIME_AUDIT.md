# Crimson Court — Faction Runtime Audit

Status: namespace/data audit advanced; local VCMI 1.7.5 and real assets still required.

## Upstream schema verification
Current VCMI faction schema requires a town to define mapObject, buildingsIcons, buildings, creatures, guildWindow, names, hallBackground, hallSlots, horde, mageGuild, moatAbility, defaultTavern, tavernVideo, guildBackground, musicTheme, siege, structures and townBackground.

Crimson currently supplies every required town field.

## Recruitment mapping
Exactly seven creature tiers are mapped, each with base + upgrade:
1. Veinling -> Bloodbound
2. Thorn Dancer -> Crimson Dancer
3. Gorewing -> Bloodwing
4. Hemomancer -> Vein Oracle
5. Scarlet Huntress -> Bloodstalker
6. Sanguine Noble -> Crimson Archon
7. Blood Phoenix -> Eternal Blood Phoenix

The town mapping therefore covers all 14 Crimson creature definitions without an extra or missing recruitment tier.

## Mage Guild
- maximum level: 5
- five spell-position rows are present
- position counts match the upstream five-level layout: 6 / 5 / 4 / 3 / 2
- guild window/background resources are staged placeholders
- normal universal spells may enter generation according to their gain chances
- Blood Rites remain gainChance 0 and are not ordinary Mage Guild spells
- reserved spells remain gainChance 0

## Primary resource
Crimson explicitly uses `crystal` as its primary resource. This is compatible with the faction schema and the intended crystal-heavy high-tier economy.

## Moat
The previous guessed `core:spell.moat` reference was invalid for current core identifiers. Upstream VCMI defines the generic/default siege moat spell as `castleMoat`, whose fully qualified core identifier is `core:spell.castleMoat`.

Crimson now uses:
`"moatAbility": "core:spell.castleMoat"`

A bespoke Crimson moat spell can replace this later, after its runtime and visuals exist.

## Grail
Heart of the Red Moon is staged with native `mode: grail`, ID 26 and 5000 gold production. This audit intentionally does not invent an unverified faction-specific Grail bonus. The base construction/income behavior must be proven in a live Crimson town before extra bonuses are added.

## Activation gates
- referenced media resources still need real files;
- live Mage Guild generation must be checked;
- Blood Rite unlock path remains custom and gated;
- Grail build/income must be checked;
- moat geometry/damage must be checked in a siege;
- all 14 recruit/upgrade paths and T2/T5 horde rollover must be checked;
- save/reload and AI town usage must be checked.

Staging remains disabled.
