# Crimson Town Visual Runtime Contract

## Town-screen structures
The faction staging now declares a complete structure object for every visible Crimson building currently exposed in the Town Hall.

Each structure has:
- an animation resource path;
- x/y screen position;
- z draw order;
- selection border;
- selection area.

Upgrade structures are staged with `hidden: true` and `builds` pointing to their base visual, following the native VCMI replacement pattern. Final coordinates are art-production baselines, not locked pixel-perfect values.

Required resource family for each structure:
- `CRIMSON/TOWN/structures/<id>.DEF`
- `CRIMSON/TOWN/structures/<id>_border.png`
- `CRIMSON/TOWN/structures/<id>_area.png`

No staging resource path should be activated before the corresponding packaged file exists.

## Siege geometry
The previous all-zero siege coordinates were removed. Crimson now uses a complete known-good H3-compatible baseline geometry for:
- gate + arch;
- moat + bank;
- four destructible wall sections;
- three static wall/background sections;
- upper, keep and lower tower graphics;
- shooter positions.

Bloodstalker remains the siege shooter.

The geometry is intentionally a baseline. When original Crimson siege art exists, its rendered bounds must be measured and the coordinates tuned against that art.

## Siege resource contract
Prefix: `CRIMSON/SIEGE/CRSG`.

The final package must provide all suffix resources required by VCMI for intact/damaged/destroyed towers, walls, gate, moat and background. Tower queue icons must also exist.

## Visual acceptance test
Before activation:
1. every Town Hall building has a selectable town-screen structure;
2. base → upgrade visual replacement does not leave both animations visible;
3. z-order produces no impossible foreground/background overlaps;
4. selection area matches visible artwork;
5. all Fort/Citadel/Castle siege states open without missing resources;
6. wall destruction swaps through all required states;
7. Bloodstalker tower sprite is positioned inside battlements;
8. gate/moat do not cover battlefield units incorrectly;
9. Grail structure appears only after Grail construction;
10. no placeholder path reaches a release package.
