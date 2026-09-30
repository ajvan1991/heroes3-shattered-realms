# VCMI Asset Runtime Contract — Shattered Realms v0.1

Verified against current upstream VCMI faction and animation documentation.

## Town core
- town background: **800 x 374**
- creature-screen backgrounds: **120 x 100** and **130 x 100**
- puzzle map: **48 pieces**
- adventure town states: village / town-castle / capitol animation resources
- town music: at least one track
- each visible town building needs an animation, selection highlight, selection area and Hall icon representation
- Hall GUI is limited to **5 rows x 4 columns**

## Town icons
A complete town icon set has eight state/size combinations:
- village normal small/large
- village built small/large
- fort normal small/large
- fort built small/large

Our current staging uses a legacy-style combined `buildingsIcons` animation for Hall building icons. Before production activation, the candidate must be checked against the exact VCMI 1.7.5 representation we choose; do not invent image dimensions not stated by the engine docs.

## Mage Guild
`guildWindow` and `guildBackground` may be arrays, one image per guild level; a one-element array is reused for every level. Crimson intentionally uses one visual for all five levels in the initial slice.

Town config must retain five rows of spell coordinates because Crimson Mage Guild maximum is 5.

## Siege image family
For prefix `CRIMSON/SIEGE/CRSG`, VCMI composes resources by suffix.

Required family:
- BACK — battlefield background
- TW21/TW22/TW2C — top tower
- MAN1/MAN2/MANC — keep
- TW11/TW12/TW1C — bottom tower
- DRW1/DRW2/DRW3 — gate states
- ARCH — gate arch
- WA61/WA62/WA63 — upper wall
- WA41/WA42/WA43 — upper-mid wall
- WA31/WA32/WA33 — bottom-mid wall
- WA11/WA12/WA13 — bottom wall
- MOAT / MLIP — moat and bank
- WA2 / WA5 / TPWL — static wall sections

Optional: DRWC drawbridge front overlay.

This is **31 required prefixed siege images** plus the two explicitly configured tower queue icons. These resources were not counted by the earlier direct-string scan because only the prefix occurs in JSON.

## Animation strategy
VCMI can replace legacy DEF animations with JSON animation definitions backed by modern PNG images. This is preferred for our original content where practical.

General animation JSON supports:
- base path
- sequences by numeric group
- individual frame overrides
- generated shadow
- generated outline overlay

This lets Shattered Realms avoid manufacturing legacy DEF binaries merely because older H3 content used DEF, provided the resource lookup/name and VCMI version behavior are validated locally.

## Creature animation groups
Core groups required by behavior include:
- 0 movement
- 1 mouse-over/random idle
- 2 idle
- 3 hit
- 4 defend
- 5 death
- 6 ranged death
- 7/8 turning
- 11/12/13 melee attack directions
- 14/15/16 ranged attack directions
- 17/18/19 special
- 20/21 movement start/end
- 22/23 dead states
- 24 resurrection
- 30/31/32 spellcasting
- 40/41/42 group attack
- 50/51 teleport start/end

Not every creature needs every optional group. Production requirements are derived from that creature's actual mechanics. Example: Scarlet Huntress/Bloodstalker need ranged attack groups; Hemomancer/Vein Oracle need casting groups; Eternal Blood Phoenix needs a coherent resurrection path.

## Acceptance
No resource is marked VALIDATED_VCMI until:
1. its exact lookup path resolves;
2. VCMI 1.7.5 loads it without resource errors;
3. relevant animation/state groups render in their actual UI/battle context;
4. save/reload and battle transitions do not expose missing frames.
