# v0.1 Asset Dependency Audit

Status: **hard activation blocker**.

This audit scans every quoted media resource referenced by the current `*.staging.json` files and compares it with files physically present under `shattered-realms/Content`.

## Result

- unique media references: **451**
- physically present referenced media files: **0**
- missing referenced media files: **451**

By extension:
- DEF: **68**
- PNG: **312**
- WAV: **70**
- OGG: **1**

By resource area:
- `SPRITES/CRIMSON`: 48
- `SOUNDS/CRIMSON`: 70
- `CRIMSON/UI`: 2
- `CRIMSON/MAP`: 6
- `CRIMSON/TOWN`: 128
- `CRIMSON/MUSIC`: 1
- `CRIMSON/SIEGE`: 2
- `HEROES/CRIMSON`: 64
- `SKILLS/SHATTERED`: 40
- `SPELLS/CRIMSON`: 10
- `SPELLS/SHATTERED`: 80

This count covers direct media strings visible in staging JSON. It does not yet count resource families implied by prefixes (for example every siege frame implied by a siege prefix) unless an explicit filename is present.

## Interpretation

The current configuration is a gameplay/data prototype, not an installable faction asset pack. Registering the full Crimson staging set in production `mod.json` now would create a large unresolved-resource surface.

No fake zero-byte DEF/PNG/WAV files should be created merely to make this count disappear. A placeholder is acceptable only if it is a structurally valid resource VCMI can actually load.

## Minimum boot-slice strategy

Do not try to produce all 451 final assets before the first runtime test. Build a deliberately reduced **boot slice** whose goal is engine validation, not presentation quality.

Priority A — boot-critical:
1. valid hero class map/battle animation resources;
2. valid creature battle animation/icon resources for the creatures included in the boot slice;
3. valid town map object resources;
4. valid town background/building icon/guild/hall resources;
5. valid town structures and masks for buildings exposed in the boot slice;
6. valid siege resources required to enter a siege;
7. valid portraits for Tavern heroes included in the boot slice.

Priority B — feature validation:
- skill icons for the two Crimson class passives;
- spell icons for only spells included in the activation candidate;
- creature sounds;
- music;
- full 16-hero specialty art;
- puzzle-map final art.

Priority C — final production:
- bespoke final animations for all 14 creatures;
- final hero animation variants;
- final building construction states/masks;
- final audio/music;
- final spell/skill art;
- polished siege and puzzle map.

## Activation invariant

The production candidate manifest must never reference a resource absent from the candidate Content tree. Asset completeness is checked against the exact subset being registered, not against the long-term master staging set.

## Next engineering gate

Create a machine-readable asset manifest grouped by entity and priority, then build the smallest valid VCMI candidate capable of:
- loading the mod;
- spawning one Crimson town;
- recruiting a controlled subset;
- opening town/Tavern/Mage Guild;
- entering a battle and siege;
- saving/reloading.

Only after that boot slice works should the activation candidate expand toward all 14 creatures and 16 heroes.


## Prefix-derived closure update

The production manifest now includes the full convention-derived resource surface used by the Crimson candidate. In addition to the 451 directly quoted media references, the package requires the 31 mandatory siege-prefix images and the 48 puzzle-prefix images `CRP00.png` through `CRP47.png`. These derived entries are explicit production jobs rather than hidden builder-only requirements.

The current machine-readable manifest contains **530 asset jobs** total: **215 Priority A**, **242 Priority B**, and **73 Priority C**. This is the production-job count after adding the 48 puzzle pieces; it should not be confused with the original 451 direct-reference count.

`tools/asset_pipeline.py` now rejects a stale summary and rejects any missing or unexpected member of the exact 48-piece puzzle family.
