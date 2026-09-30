# Crimson Court v0.1 — Activation Gate

This gate separates structurally valid staging from content that is safe to register in VCMI.

## Structural state
PASS:
- 41/41 building definitions resolve their requires/upgrades graph.
- 41/41 buildings have matching town structures.
- 14/14 town creatures resolve.
- 16/16 hero class references resolve.
- all hero starting armies resolve.
- 7/7 creature-specialist references resolve.
- 10 custom combat-event uses resolve to the four registered Crimson combat scripts.
- town has the schema-required seven creature tiers and five Hall rows.

## Creature activation rule
Current master creatures are staged with `special: true`. VCMI documents this as "special and not available by default".

When a creature is changed to normal availability (`special: false`), the schema additionally requires a valid:
`advMapAmount: { min, max }`.

Therefore **do not mass-flip special to false** until:
1. real battle animation and icons resolve;
2. sounds resolve or candidate deliberately uses a validated legal fallback;
3. adventure-map behavior has an explicit policy;
4. advMapAmount is balanced and supplied;
5. the creature passes local battle/recruit/save tests.

Recruitment validation can begin with special creatures only if VCMI local behavior confirms explicit town dwelling references can recruit them. Otherwise candidate-only availability fields are required.

## Asset gate
The master staging graph is structurally closed but its referenced original media is not present yet. Structural closure is not runtime readiness.

No asset may be called VALIDATED_VCMI until its resource path resolves in VCMI 1.7.5 and its real context renders without missing-resource errors.

## Registration gate
Production `mod.json` remains without gameplay registration arrays.

Activation order:
1. materialize real Priority-A shell assets;
2. materialize T1/T2 battle/icon assets;
3. create a candidate registration manifest separate from production mod.json;
4. schema/identifier boot;
5. town-screen boot;
6. T1/T2 recruitment and combat;
7. Tavern/Mage Guild;
8. siege;
9. save/reload + week rollover;
10. only then widen the candidate toward T3-T7.

## Stop conditions
Do not merge candidate registration into production if any of these occurs:
- missing media/resource lookup;
- unresolved identifier;
- schema warning/error caused by Shattered Realms;
- combat script leaves temporary bonus state behind;
- save/reload changes town/army state incorrectly;
- week rollover produces invalid growth;
- siege references incomplete image-prefix family.
