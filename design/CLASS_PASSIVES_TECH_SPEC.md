# Exclusive Class Passives — Technical Contract

The ten Shattered Realms hero classes each own a three-rank exclusive passive. Presentation is **Basic / Advanced / Expert**, matching Heroes III skill readability.

## Implementation contract
1. Prefer native VCMI Bonus-system representation.
2. If a passive needs event state, use a supported scripted mechanism only after verifying lifecycle/savegame behavior.
3. Every trigger specifies scope: hero, stack, turn, round or battle.
4. Every effect specifies whether it stacks.
5. Every once-per-battle state must serialize correctly.
6. AI valuation must be supplied or approximated conservatively.
7. Unsupported mechanics are redesigned, not silently approximated.

## Ten passives
- Bloodlord — Blood Command
- Sanguine Seer — Crimson Divination
- Deep Sovereign — Dread Dominion
- Voidcaller — Deep Corruption
- Lucid Warden — Dreamstep
- Somnomancer — Oneiromancy
- Oathbreaker — Broken Vow
- Pale Oracle — Last Testament
- Halo Warden — Sacred Formation
- Astral Hierophant — Celestial Alignment

## Rank budget
**Basic:** roughly a modest specialty/partial secondary-skill effect; introduces the class loop.
**Advanced:** adds one tactical dimension or improves consistency.
**Expert:** adds a capped payoff, not a global raw-stat explosion.

## Anti-abuse gates
- no infinite spell-point/resource refunds
- no repeated resurrection loops
- no permanent fear/sleep locks
- no uncapped stat stacking
- no sacrifice whose discount reaches zero cost
- no stance/alignment cycling for repeated free buffs
- no Oath implementation that permanently removes its downside
