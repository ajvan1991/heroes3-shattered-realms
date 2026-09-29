# Crimson Court v0.1 — Implementation Gate

## Completed
- [x] 14-creature roster and upgrade graph
- [x] baseline combat/economy stats
- [x] descriptions and visual identities
- [x] 16 regular heroes (8 Might / 8 Magic)
- [x] hero specialty distribution
- [x] Bloodlord and Sanguine Seer class-passive specifications
- [x] town building dependency design
- [x] creature animation production matrix
- [x] VCMI creature staging JSON with native FLYING/SHOOTER bonuses where verified

## Engine-validation work before activation
- [ ] produce game-ready battle animation files for all 14 creatures
- [ ] produce large/small creature icons
- [ ] produce required creature sounds
- [ ] validate custom Bloodied implementation
- [ ] validate first-attack no-retaliation state
- [ ] validate capped kill-heal without resurrection
- [ ] validate Hemomancer/Vein Oracle caster payload
- [ ] validate Quarry Mark
- [ ] validate Sanguine aura propagation/radius
- [ ] validate Eternal Blood Phoenix once-per-battle rebirth state
- [ ] create faction/town art dependencies required by faction schema
- [ ] create hero portraits and class animation dependencies
- [ ] register staging configs in mod.json only after dependencies exist
- [ ] run VCMI log/schema test
- [ ] run controlled map test

## Activation policy
The main mod manifest stays conservative. Staging content is not referenced until it can load without missing-resource errors. This prevents a repository milestone from being mistaken for a playable build.

## Current engine-safe abilities
The VCMI Bonus-system forms for FLYING and SHOOTER have been verified against current upstream creature definitions and are already represented in staging data. More complex custom mechanics remain gated until their exact savegame/AI/stacking behavior is proven.
