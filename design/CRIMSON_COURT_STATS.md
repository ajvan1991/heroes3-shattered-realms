# Crimson Court — Creature Stats v0.1

Initial gameplay targets. These values are intentionally conservative and require combat testing.

| Tier | Creature | Atk | Def | Dmg | HP | Spd | Growth | Gold | Fight/AI target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Veinling | 4 | 4 | 1-2 | 4 | 5 | 14 | 55 | 55 |
| 1+ | Bloodbound | 5 | 5 | 1-3 | 5 | 6 | 14 | 75 | 80 |
| 2 | Thorn Dancer | 6 | 5 | 2-4 | 10 | 6 | 9 | 120 | 130 |
| 2+ | Crimson Dancer | 7 | 6 | 2-5 | 12 | 7 | 9 | 165 | 175 |
| 3 | Gorewing | 7 | 7 | 3-6 | 18 | 7 | 7 | 220 | 230 |
| 3+ | Bloodwing | 8 | 8 | 4-7 | 22 | 8 | 7 | 285 | 300 |
| 4 | Hemomancer | 9 | 8 | 6-9 | 30 | 6 | 4 | 390 | 410 |
| 4+ | Vein Oracle | 10 | 9 | 7-10 | 35 | 7 | 4 | 500 | 530 |
| 5 | Scarlet Huntress | 11 | 10 | 9-13 | 45 | 7 | 3 | 650 | 690 |
| 5+ | Bloodstalker | 12 | 11 | 10-15 | 55 | 8 | 3 | 825 | 870 |
| 6 | Sanguine Noble | 14 | 14 | 14-20 | 90 | 8 | 2 | 1200 | 1300 |
| 6+ | Crimson Archon | 16 | 16 | 16-23 | 105 | 9 | 2 | 1550 | 1650 |
| 7 | Blood Phoenix | 18 | 17 | 30-45 | 170 | 11 | 1 | 2800 + 1 crystal | 3000 |
| 7+ | Eternal Blood Phoenix | 20 | 19 | 35-50 | 210 | 12 | 1 | 3600 + 2 crystal | 3900 |

## Ability budget v0.1
- **Bloodbound:** Bloodied: +2 Attack while stack is below 50% HP. Base Veinling gets +1.
- **Crimson Dancer:** first offensive attack on its own turn ignores retaliation; once per turn.
- **Gorewing/Bloodwing:** flying. Bloodwing restores surviving-stack HP equal to at most 15% of damage dealt on a killing blow; no resurrection.
- **Hemomancer/Vein Oracle:** limited spell points/casts. Their best faction spell has an explicit vitality/resource cost.
- **Scarlet Huntress/Bloodstalker:** shooter. Quarry Mark provides bounded follow-up pressure; marks do not stack.
- **Sanguine Noble/Crimson Archon:** limited-radius support; no global aura.
- **Blood Phoenix:** flying.
- **Eternal Blood Phoenix:** one rebirth check per battle, returning a conservative fraction of the destroyed stack. Exact percentage is test-gated.

## Economy intent
Weekly full recruitment must be expensive enough that Crimson Court cannot simultaneously rush elite dwellings, maintain premium ranged power and buy every stack. Rare-resource pressure starts around T4/T5 and peaks at T7.
