# Crimson T1/T2 Boot Slice — Dependency Closure

The candidate building set was traversed recursively through every master `requires` expression and `upgrades` edge.

## Result
- requested buildings: 22
- closed dependency set: 22
- additional buildings pulled in by closure: 0
- dangling building references: 0
- matching town-screen structures: 22
- pruned Hall content: 9 non-empty slots, but candidate must preserve exactly **5 Hall rows**; empty content is represented inside the required five-row shape rather than deleting a row

The originally selected boot set is therefore already dependency-closed.

## Closed building set
Mage Guild I-V; Tavern; Fort/Citadel/Castle; Village/Town/City/Capitol; Marketplace; Resource Silo; Blacksmith; Vein House/Vein House Up; Thorn Gallery/Crimson Gallery; Horde Thorns/Horde Thorns Up.

## Candidate pruning rule
A reduced faction file must be generated from master data by:
1. retaining only closed buildings;
2. retaining only matching structures;
3. pruning every Hall slot to retained building IDs and removing empty slots/rows;
4. reducing recruitment to T1/T2 in the candidate representation only;
5. ensuring Horde indices remain meaningful for the candidate representation;
6. resolving every hero/creature/script reference before registration.

Master faction staging is never destructively reduced.

## VCMI schema decision — resolved
Current upstream `faction.json` explicitly requires `town.creatures` to contain **7 to 8 tier entries** and `hallSlots` to contain **exactly 5 rows**. Therefore a literal two-tier faction candidate and a four-row pruned Hall are invalid schema shapes.

The candidate will keep all seven Crimson creature tier entries at the faction-data level. T1/T2 remains the first **test and asset-production surface**, not a destructive reduction of the faction's tier vector. Likewise Hall pruning may remove building IDs/slots but must preserve a valid five-row container.

No activation is performed by this audit.
