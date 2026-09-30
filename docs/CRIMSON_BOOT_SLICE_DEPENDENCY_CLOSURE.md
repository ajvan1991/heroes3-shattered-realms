# Crimson T1/T2 Boot Slice — Dependency Closure

The candidate building set was traversed recursively through every master `requires` expression and `upgrades` edge.

## Result
- requested buildings: 22
- closed dependency set: 22
- additional buildings pulled in by closure: 0
- dangling building references: 0
- matching town-screen structures: 22
- pruned Hall layout: 4 non-empty rows / 9 slots

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

## Important VCMI compatibility note
The master Crimson town follows the normal seven-tier faction model. A two-tier faction representation may not be a valid production faction shape for every VCMI subsystem even if its references are closed. Therefore the first generated candidate must be treated as an experiment. If VCMI 1.7.5 requires seven creature tier entries, the safer candidate will keep seven data tiers while restricting the test surface/assets rather than fabricating an unsupported two-tier town format.

No activation is performed by this audit.
