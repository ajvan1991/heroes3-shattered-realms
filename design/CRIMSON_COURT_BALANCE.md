# Crimson Court — v0.1 Balance Baseline

This document is a design baseline, not final game data. Values must be tested in VCMI before release.

| Tier | Base / Upgrade | Role | HP target | Speed target | Growth target | Cost target |
|---|---|---|---:|---:|---:|---:|
| 1 | Veinling / Bloodbound | fragile scaling melee | 4 / 5 | 5 / 6 | 14 / 14 | 55 / 75 |
| 2 | Thorn Dancer / Crimson Dancer | mobile duelist | 10 / 12 | 6 / 7 | 9 / 9 | 120 / 160 |
| 3 | Gorewing / Bloodwing | flying sustain | 18 / 22 | 7 / 8 | 7 / 7 | 220 / 280 |
| 4 | Hemomancer / Vein Oracle | fragile caster | 30 / 35 | 6 / 7 | 4 / 4 | 400 / 500 |
| 5 | Scarlet Huntress / Bloodstalker | ranged mark specialist | 45 / 55 | 7 / 8 | 3 / 3 | 650 / 800 |
| 6 | Sanguine Noble / Crimson Archon | elite sustain/support | 90 / 105 | 8 / 9 | 2 / 2 | 1200 / 1500 |
| 7 | Blood Phoenix / Eternal Blood Phoenix | fast high-risk apex | 170 / 210 | 11 / 12 | 1 / 1 | 2800 / 3600 + rare resource |

## Ability budget

### Veinling / Bloodbound
**Bloodied:** gains a modest Attack bonus only while below 50% HP.
Counterplay: eliminate the stack or avoid leaving it damaged.

### Thorn Dancer / Crimson Dancer
Mobility-focused melee. Upgrade may avoid retaliation on the first attack of its own turn.
Counterplay: modest HP and no permanent damage multiplier.

### Gorewing / Bloodwing
Flying attacker. Upgrade heals a capped fraction after kills.
Counterplay: healing cannot exceed casualties inflicted and must not resurrect lost creatures by default.

### Hemomancer / Vein Oracle
Limited battle spellcasting. Stronger effects consume a defined resource/HP budget.
Counterplay: deliberately weak physical profile.

### Scarlet Huntress / Bloodstalker
Ranged specialist. Mark improves follow-up pressure rather than dealing free burst damage.
Counterplay: vulnerable when engaged in melee.

### Sanguine Noble / Crimson Archon
Sustain/support aura with conservative radius and value.
Counterplay: expensive and only two weekly growth before external modifiers.

### Blood Phoenix / Eternal Blood Phoenix
Fast apex creature. Upgrade receives a tightly limited rebirth mechanic.
Counterplay: rebirth is once per battle and resurrection percentage must be substantially below a full second stack.

## Town economy philosophy
Crimson Court must not combine premium speed, premium ranged power and cheap development.
- Early dwellings: affordable.
- T4-T5 transition: above-average rare-resource pressure.
- T6-T7: expensive.
- Blood Rite buildings compete with economic development.
- Capitol / Castle / Mage Guild remain comparable to core-town opportunity costs.

## Test gates
1. Week-1 creature value must not clearly exceed strong base-faction openings.
2. Week-2 T6/T7 access should require meaningful economic sacrifice.
3. AI value must be checked against actual combat performance.
4. Blood Rite cannot create net-positive resources without a hard opportunity cost.
5. Rebirth, lifesteal and healing effects need caps to prevent exponential sustain.
