# v0.1 Asset Production Plan

Source of truth for the machine-readable queue: `production/asset-manifest.v0.1.json`.

## Queue snapshot
The current production manifest contains **530 deterministic asset jobs**:
- Priority A: **215**
- Priority B: **242**
- Priority C: **73**
- Boot-slice membership: **241 true / 289 false**

The 530 jobs are the closed production surface: **451 direct staging media references + 31 mandatory siege-prefix resources + 48 puzzle-prefix resources**. The historical 451 figure remains useful only when discussing direct quoted references; it is not the current production queue size.

Every job now records explicit resource path, file type, source, priority, status and boolean boot-slice membership.

## Priority meaning
### A — town/bootstrap
Town screen, map-town and siege resources needed to prove that a Crimson town can exist and its core UI/siege surfaces can load. These are produced first.

### B — playable content
Creature visual resources, hero portraits/animations, skill icons and spell icons. These are produced entity-by-entity so a controlled activation candidate can expand without requiring the whole final roster at once.

### C — presentation/audio
Creature sound suite and music. These remain mandatory for the finished faction but do not block early schema/identifier experiments if VCMI permits the candidate to omit the corresponding optional references.

## Production batches
1. **Town shell** — backgrounds, building-icons resource, Mage Guild window/background, map-town templates.
2. **Core town structures** — Village/Town/City/Capitol, Tavern, Marketplace, Silo, Blacksmith, Fort/Citadel/Castle, Mage Guild I–V.
3. **T1/T2 vertical slice** — Veinling/Bloodbound and Thorn/Crimson Dancer, their dwellings and Horde chain.
4. **Hero smoke-test pair** — one Bloodlord and one Sanguine Seer with valid portraits and class animation resources.
5. **Siege shell** — tower icons and the exact 31-image prefix-derived family required by VCMI.
6. **Puzzle family** — all 48 zero-based `CRP00.png`…`CRP47.png` resources.
7. **Remaining T3–T7** — creatures and dwellings in tier order.
8. **Remaining 14 heroes**.
9. **Validated spell/skill art**.
10. **Audio/music**.
11. **Polish/final replacement pass**.

## Asset acceptance rule
An item moves from MISSING only when the repository contains a structurally valid file at the exact referenced path. Concept art, a prompt, or a differently named source image does not satisfy a runtime asset job.

For DEF animation families, acceptance also requires the animation groups/frames needed by the relevant VCMI use case. A file that merely has a .DEF extension is not accepted.

## Boot candidate discipline
The first runnable candidate should reference only the content and assets actually present in that candidate. Master staging remains broader. We will not weaken master design merely to make a temporary smoke-test package load.

## Tracking
Statuses:
- MISSING
- CONCEPT
- SOURCE_READY
- CONVERTED
- VALIDATED_VCMI

Only `VALIDATED_VCMI` counts as release-ready.
