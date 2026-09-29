# Crimson Activation Dependency Manifest

This file defines the intended registration/load order for the first Crimson Court playable vertical slice. It is not a claim that the slice is locally validated yet.

## Phase 0 — scripts
1. combat event registrations
2. combat Lua scripts
3. spellEffect registrations
4. spellEffect Lua scripts

No creature/spell may reference a custom subtype before its script registration is present in the activated mod content.

## Phase 1 — reusable gameplay entities
1. class passive skills
2. universal counterplay spells
3. Crimson Blood Rite spells

Universal spells must not depend on Crimson faction IDs for their effects. Blood Rites are separate faction/class actions.

## Phase 2 — faction foundation
1. Crimson creature definitions
2. Crimson hero classes
3. Crimson faction/town definition
4. Crimson buildings
5. Crimson heroes

Dependency rules:
- hero classes require a valid faction and commander creature;
- heroes require registered hero classes and creature identifiers;
- faction creature tiers require registered creature identifiers;
- town buildings require stable building IDs and requirement references.

## Stable Crimson building IDs
Core-compatible town slots:
- 0..4 Mage Guild I..V
- 5 Tavern
- 7 Fort
- 8 Citadel
- 9 Castle
- 10 Village Hall
- 11 Town Hall
- 12 City Hall
- 13 Capitol
- 14 Marketplace
- 15 Resource Silo
- 16 Blacksmith
- 26 Grail
- 30..36 base dwellings T1..T7
- 37..43 upgraded dwellings T1..T7

Crimson special buildings use 50..55 to avoid collisions with standard town slots.

## Economy baseline restored
The staging town now has the normal economic semantics needed for an actual town:
- Village Hall 500 gold/day
- Town Hall 1000 gold/day
- City Hall 2000 gold/day
- Capitol 4000 gold/day
- Grail 5000 gold/day
- Resource Silo +1 wood/+1 ore per day

Marketplace, Blacksmith and Tavern are explicitly present so City Hall and normal town gameplay do not depend on missing buildings.

## Phase 3 — visual town layer
Only after gameplay entities resolve:
- town screen background
- building structures and selection areas
- siege screen/fortifications
- puzzle map art
- creature dwelling map objects
- hero map/battle animations
- portraits/icons/sounds/music

## Activation gates
Before adding these staging configs to mod.json:
1. all referenced files physically exist;
2. all JSON passes VCMI 1.7.5 validation;
3. no unresolved identifier warnings in VCMI log;
4. new game can create Crimson town;
5. Tavern can recruit all 16 regular heroes;
6. all 14 creatures recruit/upgrade correctly;
7. Mage Guild opens without invalid spell references;
8. save/reload preserves custom combat state;
9. AI can recruit, build and fight with the town;
10. RMG can place the faction without fatal errors.

Until these gates pass, keepDisabled remains intentional.
