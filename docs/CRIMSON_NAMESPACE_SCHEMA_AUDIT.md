# Crimson Namespace and Schema Audit

## Faction schema corrections
Validated against current VCMI `config/schemas/faction.json`.

- Puzzle map now contains exactly 48 pieces.
- Puzzle indices are 1..48; the previous index 0 placeholder was invalid.
- Town `defaultTavern` uses 5, matching normal core behavior.
- Experimental `guildSpells` entries for Shattered Realms spells were removed from the faction staging file until spell entities are actually registered. Universal spell availability belongs in the activated spell pool/distribution layer, not as dangling faction references.

## Hero staging corrections
- Empty `specialty.bonuses: {}` placeholders were removed from Ilyr Thorn, Sevrin, Miraleth, Saereth and Lysandra Noct.
- Their narrative specialty intent remains in hero text/design docs, but runtime specialty data will only return when an actual engine-safe bonus/script mapping exists.
- Existing creature and secondary-skill specialty shortcuts remain staged.

## Identifier policy
Inside one mod scope, local identifiers should remain local where the target is another Shattered Realms entity. Explicit `core:` identifiers are retained only for core VCMI/H3 entities such as secondary skills, boat/moat references, and core spells.

Do not create references to staging-only spells from an activated faction before the spell config itself is activated.

## Remaining namespace gates
- Validate town building requirement identifiers against final activated building source.
- Validate creature identifiers in faction creature tiers after config registration order is fixed.
- Validate class identifiers in hero files after heroClass registration.
- Validate all image/animation/music paths against actual packaged resources.
- Run local VCMI 1.7.5 load and inspect mod validation log before removing `keepDisabled`.


## Secondary-skill identifier correction
A deeper comparison with current VCMI content/test data showed that core secondary-skill identifiers are resolved canonically as local/global identifiers such as `offence`, `armorer`, `wisdom`, `earthMagic`, etc. The previous `core:offence`-style values in Crimson hero-class and hero staging were normalized.

Updated surfaces:
- Bloodlord/Sanguine Seer level-up skill-weight maps
- all Crimson starting secondary skills
- Thalia Veyn / Caelis / Vespera / Elyss Vane secondary-skill specialties

This removes a likely identifier-resolution failure before activation.
