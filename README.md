# Heroes III: Shattered Realms

A mythology-first expansion for **VCMI / Heroes of Might and Magic III**.

## Vision

Shattered Realms adds five original factions designed to feel at home in Heroes III while avoiding direct creature duplication and power creep:

- **Crimson Court** — Blood Elves; Blood Rites; aggressive risk/reward.
- **Abyss** — eldritch depths; corruption, fear, curses and spatial control.
- **Veil** — Dreamborn; Dream/Nightmare stances, illusion and control.
- **Hollow** — Forsaken Court; Oaths, attrition and gothic dark fantasy.
- **Starfall** — mythic celestials; sacred geometry and astral magic.

Planned expansion scope:
- 5 towns / 10 hero classes
- 70 faction creatures (7 tiers + upgrades)
- 20 neutral mythic creatures
- 30 artifacts
- 30 adventure-map objects
- 5 distinct environmental identities
- unique town screens, buildings, Grails, dwellings and siege presentation
- RMG integration
- balance against the base Heroes III ecosystem

## Current milestone

**v0.1 — Crimson Court vertical slice**

Goal: load cleanly in VCMI, expose Crimson Court as a playable faction, then iterate on creatures, heroes, buildings, assets and balance.

## Development rules

1. Gameplay before final art.
2. Every strong mechanic has a measurable cost or weakness.
3. No faction should dominate the base factions by raw efficiency.
4. Avoid reusing existing creature concepts as simple reskins.
5. New content must remain readable in classic Heroes III combat.
6. Configuration is validated before a feature is marked playable.

## Repository layout

- `shattered-realms/` — installable VCMI mod root
- `design/` — faction, creature, artifact and balance specifications
- `docs/` — development/testing documentation
- `assets/` — source artwork and production assets when added

## Target

Initial development target: **VCMI 1.7.x**.
