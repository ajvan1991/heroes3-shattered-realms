# v0.1 Spell Activation Matrix

This file separates authored spell concepts from effects safe enough to enter the first playable Crimson Court slice.

## Blood Rites
- Rite of the Open Vein — STAGED, activation gated by local marker compatibility test.
- Rite of Scarlet Shelter — STAGED, activation gated by local marker compatibility test.

They never enter ordinary Mage Guild generation; their gain chance remains zero.

## Universal counterplay set
The twelve faction-agnostic counterplay spells remain the intended first universal spell package. Effects that use native bonuses or the reviewed selective-dispel bridge may proceed to asset/schema testing. They still require icons and local VCMI validation before registration.

## Global spell concepts
- Leyline Convergence — RESERVED / DISABLED
- Echo of the Fallen — RESERVED / DISABLED
- Hour of Silence — RESERVED / DISABLED

All three now have default and per-faction gain chance zero for v0.1. Their unresolved effects are removed from level definitions. This prevents a spell with descriptive text but incomplete or ambiguous runtime behavior from entering Mage Guild generation.

Hour of Silence's custom `battleSpellCost` effect is unregistered from the v0.1 spell-effect manifest. The Lua prototype may remain as research source, but it is not part of the activation graph.

## Promotion rule
A reserved spell can move to STAGED only after:
1. exact VCMI bonus/effect semantics are proven from current upstream or a minimal local test;
2. target legality is deterministic;
3. AI valuation/behavior is acceptable;
4. save/load behavior is defined where stateful;
5. all four mastery entries have real effects and truthful descriptions;
6. required graphics exist.
