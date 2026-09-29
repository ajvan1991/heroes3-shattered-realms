# Crimson Court — Runtime Activation Manifest

This document defines the exact transition from staging data to a playable VCMI faction.

## Content registration target
When all required resources exist, the root mod manifest registers:
- factions: Crimson Court faction/town configuration
- creatures: 14 Crimson Court creature definitions
- heroClasses: Bloodlord and Sanguine Seer
- heroes: 16 regular Crimson Court heroes
- spells: 16 Shattered Realms spells
- objects: Crimson adventure dwellings and faction map objects
- skills/scripts: only mechanics proven against the target VCMI build

## Activation order
1. creature graphics/sounds/icons
2. creature config
3. hero portraits/specialty icons/battle animations
4. hero classes and heroes
5. town background and mandatory UI assets
6. building layers and town structures
7. siege assets and coordinates
8. 48-piece puzzle map
9. spell icons/VFX/sounds
10. faction/town config
11. map dwellings and RMG integration
12. custom mechanics/scripts
13. mod.json registration
14. schema/load test
15. controlled combat/economy test

## Required Crimson town asset set
- creature info backgrounds: 120px and 130px
- town background
- town hall background
- mage guild background + window
- building icon animation
- tavern video or technically valid original replacement
- music theme
- town map object animation/filter
- village/fort town icons, normal+built, small+large
- building animation/area/border assets
- siege background/walls/towers/gate/moat + tower icons
- 48 puzzle-map pieces

## Town names
Veyrath
Sanguinar
Thornveil
Caer Veyn
Redharrow
Nocthyr
Velisara
Bloodmere
Ilyrion
Scarlet Reach
Vael Noctis
Moonthorn

## Mage Guild policy
Mage Guild level: 5.
The town uses the shared game spell ecosystem plus Shattered Realms spells after activation.
Faction spell weighting favors tactical blood magic but does not guarantee counters to Crimson's own mechanics.

## Runtime quality gate
No staging file is promoted merely because it validates as JSON. Promotion requires:
- schema-valid entity references
- every referenced asset resolvable
- launcher enable succeeds
- no relevant VCMI error-log entries
- new game can select Crimson Court
- tavern can generate all 16 regular heroes
- all 14 creatures recruit and upgrade
- siege loads
- Mage Guild opens at all five levels
- save/load preserves custom state
- AI can recruit and use the faction without blocking
