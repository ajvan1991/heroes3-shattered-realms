# Crimson Court T1/T2 Boot Slice

Purpose: define the first mechanically representative Crimson subset for local VCMI validation without weakening the master roster.

## Included creatures
### T1
- Veinling — baseline melee/control creature, no custom combat script
- Bloodbound — upgrade, Bloodied custom combat-event trigger

### T2
- Thorn Dancer — baseline melee
- Crimson Dancer — upgrade, Crimson Grace + Bloodied

This four-creature slice deliberately exercises:
- base -> upgrade resolution on two tiers;
- one ordinary tier and one Horde tier;
- custom combat-event registration;
- dynamic add/remove unit bonus through Bloodied;
- pre-attack retaliation suppression through Crimson Grace;
- weekly growth 14 / 9;
- hero starting-army references.

## Included heroes
### Bloodlord smoke-test hero: Vaelor
- Might class
- starts with Offense
- creature specialty: Veinling/Bloodbound
- army: Veinling + Thorn Dancer

### Sanguine Seer smoke-test hero: Aveline
- Magic class
- starts with Wisdom
- has spellbook
- creature specialty remains Hemomancer/Vein Oracle in master data

Aveline's specialty target is outside T1/T2. For the reduced boot candidate, either include the referenced T4 pair as data-only dependencies or use a candidate-only hero copy whose specialty is a validated native secondary-skill specialty. **Do not mutate master Aveline merely for the smoke test.**

## Required town buildings for recruitment
- Vein House / Vein House Up
- Thorn Gallery / Crimson Gallery
- Horde Thorns / Horde Thorns Up

Required economic/GUI shell:
- Village Hall / Town Hall / City Hall / Capitol
- Tavern
- Marketplace
- Resource Silo
- Blacksmith
- Fort / Citadel / Castle
- Mage Guild I-V structures

## Runtime assertions
1. Vein House recruits Veinling.
2. upgraded T1 dwelling recruits Bloodbound.
3. Thorn Gallery recruits Thorn Dancer.
4. upgraded T2 dwelling recruits Crimson Dancer.
5. T2 Horde base/upgraded chain increases the intended T2 growth without creating a duplicate recruitment path.
6. Bloodbound gains Bloodied only while survivors are below 50% HP.
7. casualties with fully healed survivors do not trigger Bloodied.
8. Crimson Dancer's first normal attack receives Crimson Grace behavior.
9. retaliation/additional-attack behavior does not leave BLOCKS_RETALIATION behind.
10. Vaelor appears in Tavern and starts with legal T1/T2 army.
11. at least one Sanguine Seer appears with a spellbook.
12. save/reload preserves town construction, growth and hero armies.

## Expansion gate
T3 is added only after this slice boots and survives the assertions above. The master staging files remain the full 14-creature / 16-hero design source throughout.
