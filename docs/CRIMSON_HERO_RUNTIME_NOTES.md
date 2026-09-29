# Crimson Court — Runtime Mapping Notes

Current staging follows the upstream VCMI hero and hero-class schemas rather than guessed field names.

## Hero classes
- Bloodlord: Might affinity; Attack/Defense weighted.
- Sanguine Seer: Magic affinity; Spell Power/Knowledge weighted.
- Secondary-skill weights intentionally differ by class.
- Tavern values are faction-local staging values.
- Battle animation paths are original-asset targets.

## Heroes
All **16 regular heroes** now have staging records:
- 8 Bloodlords
- 8 Sanguine Seers
- portraits and specialty-icon target paths
- starting armies
- starting skills
- biographies
- specialty text
- native VCMI creature-specialty shortcut where applicable
- native VCMI secondary-skill-specialty shortcut where applicable

## Important gate
Faction-mechanic specialties currently carry an empty bonus payload rather than a fake implementation. They are activated only after the relevant Blood Command, Blood Rite, Quarry Mark and Crimson Divination mechanics have an engine-safe Bonus/script representation.

## Starting-army QA
Current common staging army is deliberately temporary. Before activation, each hero receives one of several bounded starting-army patterns so tavern rerolling cannot reliably produce excessive T2 value.

## Commander field
The hero-class schema currently requires a commander identifier. Staging temporarily references a core creature solely to satisfy structural authoring while the project decides whether commanders are actually enabled in the target gameplay rules. This file must not be activated in a release with that placeholder intact.
