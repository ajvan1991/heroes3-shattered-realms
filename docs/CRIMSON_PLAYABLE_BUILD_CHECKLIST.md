# Crimson Court — Playable Build Checklist

## Data
- [x] faction shell
- [x] seven creature tiers + upgrades
- [x] two hero classes
- [x] sixteen regular heroes
- [x] town building economy/prerequisites
- [x] five-level Mage Guild
- [x] Shattered Realms spell weighting draft
- [x] 48-piece puzzle-map data shape
- [x] siege data shape
- [x] twelve town names
- [ ] exact VCMI core identifiers revalidated on target 1.7.5 before activation
- [ ] building numeric IDs / dwelling semantics validated where required
- [x] map-object templates for village/castle/capitol staged (resource files still missing)
- [ ] structures coordinates after final town art
- [ ] siege coordinates after final siege art
- [ ] puzzle-piece coordinates after final puzzle art

## Art
- [ ] 14 creature battle animations
- [ ] 14 adventure-map animations where applicable
- [ ] 28 creature icons
- [ ] 16 hero portrait pairs
- [ ] 16 specialty icon pairs
- [ ] Bloodlord/Sanguine Seer battle/map hero art
- [ ] town background
- [ ] hall + guild screens
- [ ] building icon animation
- [ ] all building layers/highlights/areas
- [ ] village/fort map animations and town icons
- [ ] complete siege set
- [ ] 48 puzzle pieces
- [ ] 16 spell icon sets + VFX
- [ ] faction iconography

## Audio
- [ ] creature attack/defend/death/move/wince set
- [ ] spell SFX
- [ ] town music
- [ ] town ambient layer
- [ ] tavern asset

## Mechanics
- [ ] Bloodied
- [ ] Crimson Dancer retaliation rule
- [ ] Bloodwing capped kill-heal
- [ ] Hemomancer/Vein Oracle casting
- [ ] Quarry Mark
- [ ] Noble/Archon aura
- [ ] Eternal Phoenix rebirth
- [ ] Blood Rites
- [ ] Blood Command
- [ ] Crimson Divination
- [ ] complex spell counters/global effects

## QA
- [ ] launcher enable
- [ ] zero relevant schema/resource errors
- [ ] new-game faction selection
- [ ] all buildings construct
- [ ] all creatures recruit/upgrade
- [ ] all heroes tavern-spawn
- [ ] five Mage Guild levels
- [ ] siege
- [ ] save/load
- [ ] AI turn
- [ ] RMG generation
- [ ] week 1/2 economy benchmarks
- [ ] matchup tests against legacy towns

A checkmark means implemented or structurally staged, not necessarily locally proven. Only QA checkmarks establish playable status.


## Runtime blockers audit — current

### Engine paths now proven upstream
- custom unit spellEffect bridge: proven by VCMI spell scripts
- selective dispel: mirrors current VCMI dispel implementation
- battle-wide bonus injection: proven by BattleServer:addBattleBonus and VCMI moat script
- creature caster package: proven by core Ogre Mage configuration
- server-side HP sacrifice: BattleServer:damageUnit
- non-resurrecting Bloodwing healing: BattleServer:healUnit with heal/permanent mode

### Still blocking activation
- real creature DEF/PNG/WAV resources
- town screen / structure / siege resources
- hero portraits and map animations
- local VCMI 1.7.5 schema/load test of staging identifiers
- verification of dynamic Crimson Archon adjacency refresh
- verification of temporary-duration enum/turn handling in custom scripts
- Mortal Anchor is RESERVED/disabled until a verified anti-heal/rebirth hook exists
- final faction/town reference namespace pass
- all 16 regular heroes now use native creature/secondary-skill specialty shortcuts; local Tavern-spawn validation remains

The main mod manifest remains intentionally conservative until resource and local-load blockers are cleared.
