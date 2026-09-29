# Crimson Court — Art & Animation Production Matrix

## Creature asset matrix

| Creature | Battle silhouette | Idle/Fidget | Move | Attack/Cast | Hit/Defend | Death | Adventure map | Icons |
|---|---|---|---|---|---|---|---|---|
| Veinling | thin initiate + hooked blade | tense breath / blade twitch | low stalk | diagonal slash | recoil / blade guard | kneel-collapse | hooded red-black initiate | L/S |
| Bloodbound | scarred half-mask + larger thorn blade | scars pulse subtly | confident stalk | two-stage hook slash | brace | ritual-kneel collapse | stronger thorn silhouette | L/S |
| Thorn Dancer | paired crescents + ribbons | footwork | dancer run | circular cross-cut | spin recoil | ribbon collapse | slim duelist | L/S |
| Crimson Dancer | crown + longer ribbons | blade flourish | gliding sprint | passing cut | evasive turn | controlled fall | crown readable | L/S |
| Gorewing | four-limbed crystal-vein predator | crouch/wing flex | flight | dive rake | wing shield | implosion/fall | flying loop | L/S |
| Bloodwing | broad translucent membranes | membrane shimmer | flight | dive + bite | recoil | crystal shatter | larger wing arc | L/S |
| Hemomancer | ritual needles + robe | orbiting needles | measured walk | blood glyph cast | ward gesture | sigils fall dark | robed caster | L/S |
| Vein Oracle | blindfold crown + chalice shards | shard orbit | float-step | prophecy glyph | shard ward | shards drop then body | distinct halo | L/S |
| Scarlet Huntress | recurved bloodwood launcher | aim check | hunter stride | ranged release | mantle guard | kneeling fall | long weapon silhouette | L/S |
| Bloodstalker | mask + segmented launcher | mark gesture | stalking sprint | marked shot | side recoil | cloak collapse | masked hunter | L/S |
| Sanguine Noble | glaive + floating cloak panels | regal stillness | deliberate march | sweeping glaive | plate brace | upright collapse | armored noble | L/S |
| Crimson Archon | crown-back ornament + heavy plate | aura pulse | heavy march | glaive + aura accent | shielded posture | crown light extinguishes | crown silhouette | L/S |
| Blood Phoenix | four crystal-leaf wings + dark core | continuous mote shedding | fast flight | body-to-arc strike | wing contraction | inward implosion | distinctive four-wing loop | L/S |
| Eternal Blood Phoenix | outer wing arc + heart halo | heart pulse + motes | fast flight | crimson arc reform | halo flare | implosion / rebirth cue | halo + four wings | L/S |

## Animation principles
- Readability first: attack anticipation and impact must be visible at normal combat speed.
- Avoid excessive particle coverage.
- Upgrade animation may share timing skeleton where sensible, but silhouette/material/VFX must visibly change.
- Death frames must end in a stable corpse/vanish state expected by the engine.
- Ranged projectiles and spell effects remain visually separate from unit body animation.
- Final frame counts/timings follow VCMI-supported animation metadata after first export tests.

## Hero portrait direction
### Bloodlords
Vaelor — weathered ritual master, pale skin, black-red ceremonial armor.
Seris — elegant duelist, thorn circlet, calm predatory gaze.
Khaeren — high-roost keeper, wing-shaped mantle.
Maelira — masked noble huntress, moonlit red markings.
Othrys — ancient court commander, severe silver-black plate.
Rhaevan — keeper of the ritual heart, crimson crystal reliquary.
Thalia Veyn — battlefield aristocrat, geometric scar over one cheek.
Ilyr Thorn — austere commander, visible ritual scars, restrained armor.

### Sanguine Seers
Aveline — scholar with floating ritual needles.
Sevrin — precise ritualist, minimal ornament, blood-measure instruments.
Miraleth — archivist with old chalice tablets.
Caelis — mnemonic scholar, layered script-cloth.
Vespera — battle sorceress, sharp crimson sigils.
Elyss Vane — meditative channel-reader.
Saereth — mystical hunter-scholar with thorn-ring motif.
Lysandra Noct — dark veil, branching divination sigil.

## Town animation layers
1. static painterly background
2. Bloodwood branch sway
3. slow ritual-channel pulse
4. moonlight atmospheric layer
5. dwelling-specific loops
6. occasional Gorewing flyby after T3 dwelling
7. T7 crimson motes
8. Grail red-moon halo + flowering canopy

## Asset acceptance
An asset is accepted only when it is:
- original/licensable
- readable at game scale
- stylistically compatible with classic Heroes III
- technically exportable for VCMI
- visually distinct from existing creatures/towns
- documented with source and export settings
