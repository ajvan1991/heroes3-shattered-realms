# v0.1 Asset Production Plan

Source of truth for the machine-readable queue: `production/asset-manifest.v0.1.json`.

## Queue snapshot
The current production manifest contains **530 deterministic asset jobs**:
- Priority A: **217**
- Priority B: **242**
- Priority C: **71**
- Boot-slice membership: **241 true / 289 false**

Two shared creature UI backgrounds are Priority A because the town/bootstrap shell directly requires them; this keeps their manifest priority aligned with executable batch A1.

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
The machine-readable plan currently has **16 executable batches**, and every one of the 530 manifest jobs has at least one owner:
- **A1–A5:** town shell, adventure-town shell, town structures, siege family and 48-piece puzzle family.
- **B1–B2:** T1/T2 creature smoke slice and Vaelor/Aveline hero smoke path.
- **B3–B4:** remaining T3–T7 creature visuals and the complete 16-hero Crimson portrait/specialty set.
- **B5–B8:** Crimson class-passive art, Blood Rite art, universal spell art, and the staged future-faction class-passive icon families.
- **C1–C3:** T1/T2 audio, town music, and remaining T3–T7 audio.

Production ownership is **exclusive**: every one of the 530 manifest jobs must resolve to exactly one batch. B2 owns the Vaelor/Aveline smoke-test hero resources; B4 explicitly owns the other 14 Crimson hero portrait/specialty families. Asset priority must match its owning batch. CI rejects unowned or multi-owned jobs.

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
