# Twelve New Spells — Counterplay Set v0.1

Goal: add **12 new combat spells** that create answers to Shattered Realms class passives, faction buffs and positional mechanics without invalidating them. All numbers are initial balance targets.

## Distribution
- 3 Air
- 3 Earth
- 3 Fire
- 3 Water
- Mostly levels 2–4; no level-5 auto-win spell.
- Expert versions favor better efficiency/range or modest area use, not extreme magnitude.

---

## AIR

### 1. Sever the Formation
**Level:** 3 Air • **Role:** counter to Starfall formation and adjacency-based support.
**Target:** enemy creature.
**None/Basic:** -2 Defense and -1 Speed for 2 rounds.
**Advanced:** -3 Defense, -1 Speed.
**Expert:** small 0-1 hex area; -3 Defense, -1 Speed.
**Counterplay purpose:** makes maintaining Sacred Formation harder without turning the formation off by script.
**Why fair:** weaker than stacking Slow + Disrupting Ray and temporary.

### 2. Clear Mind
**Level:** 2 Air • **Role:** anti-dream/fear/soft-control protection.
**Target:** friendly creature.
**None/Basic:** +20% resistance against mind-affecting magic for 3 rounds.
**Advanced:** +30%.
**Expert:** all friendly stacks, +30%, but higher mana cost.
**Counterplay purpose:** Veil dream control and Abyss fear pressure.
**Why fair:** resistance, not immunity; does not erase already-applied effects by default.

### 3. Unbound Step
**Level:** 3 Air • **Role:** mobility restoration.
**Target:** friendly creature.
**None/Basic:** +1 Speed and removes one ordinary movement-reduction spell where supported.
**Advanced:** +2 Speed.
**Expert:** +2 Speed and stronger cleanse whitelist.
**Counterplay purpose:** answers slows, snares and positioning pressure.
**Why fair:** below Haste's raw speed swing; cleanse is narrow.

---

## EARTH

### 4. Grounding Sigil
**Level:** 3 Earth • **Role:** anti-teleport / anti-high-mobility pressure.
**Target:** enemy creature.
**None/Basic:** -1 Speed and +15% incoming penalty to teleport-like reposition resistance check where technically supported.
**Advanced:** -2 Speed.
**Expert:** 0-1 area, -2 Speed.
**Fallback implementation:** temporary -Speed plus anti-flight/teleport-specific bonus only if VCMI exposes a safe native bonus.
**Counterplay purpose:** Abyss repositioning and extreme mobility.
**Why fair:** never roots a unit completely.

### 5. Mortal Anchor
**Level:** 4 Earth • **Role:** anti-rebirth / anti-resurrection preparation.
**Target:** enemy creature.
**None/Basic:** for 2 rounds, resurrection/healing received is reduced by 25%.
**Advanced:** 35%.
**Expert:** 40%.
**Counterplay purpose:** Eternal Blood Phoenix and other sustain strategies.
**Why fair:** never prevents healing entirely and does not deal damage itself.

### 6. Burden of Stone
**Level:** 2 Earth • **Role:** answer to low-HP berserker/risk-reward stacks.
**Target:** enemy creature.
**None/Basic:** -2 Attack for 3 rounds.
**Advanced:** -3 Attack.
**Expert:** -3 Attack to a small area.
**Counterplay purpose:** Blood Command/Bloodied pressure.
**Why fair:** simple temporary debuff; does not specifically disable Crimson mechanics.

---

## FIRE

### 7. Brand of Frailty
**Level:** 3 Fire • **Role:** anti-aura / elite-stack pressure.
**Target:** enemy creature.
**None/Basic:** -2 Defense for 3 rounds; healing received -10% if engine-safe.
**Advanced:** -3 Defense; -15% healing.
**Expert:** -4 Defense; -15% healing.
**Counterplay purpose:** Sanguine Noble sustain and other defensive elite anchors.
**Why fair:** single-target at all ranks; no permanent stat loss.

### 8. Scorch the Oath
**Level:** 3 Fire • **Role:** Hollow counter.
**Target:** enemy creature.
**None/Basic:** -2 Attack for 2 rounds.
**Advanced:** -2 Attack and -1 Defense.
**Expert:** -3 Attack and -1 Defense.
**Special interaction:** if a clean, engine-safe Oath tag exists, magnitude may receive only a small conditional bonus against an Oath-buffed target.
**Why fair:** remains useful outside Hollow matchups; does not delete the Oath.

### 9. Flare of Waking
**Level:** 2 Fire • **Role:** wake/clarity utility.
**Target:** friendly creature.
**None/Basic:** dispels one dream/sleep-like negative effect from an approved whitelist and gives +1 Attack for one round.
**Advanced:** +2 Attack.
**Expert:** small allied area if engine-safe; otherwise single target with lower cost.
**Counterplay purpose:** Veil control.
**Why fair:** requires a hero action and has a narrow cleanse list.

---

## WATER

### 10. Quiet the Blood
**Level:** 3 Water • **Role:** Crimson risk-reward counter.
**Target:** enemy creature.
**None/Basic:** -2 Attack for 2 rounds.
**Advanced:** -3 Attack.
**Expert:** -3 Attack and -1 Speed.
**Special interaction:** does not remove Bloodied/Blood Command; it offsets their offensive payoff.
**Why fair:** normal dispellable debuff.

### 11. Wash Away
**Level:** 3 Water • **Role:** broad anti-mark/corruption utility.
**Target:** friendly creature.
**None/Basic:** removes one approved removable faction debuff (Quarry Mark, minor Corruption, dream residue, similar tags) or one ordinary negative spell.
**Advanced:** removes up to two approved effects.
**Expert:** small allied area, one approved effect each.
**Counterplay purpose:** prevents new mechanics from becoming mandatory snowball states.
**Why fair:** consumes a cast and does not remove persistent/absolute effects.

### 12. Veil of Still Water
**Level:** 4 Water • **Role:** anti-burst defensive buff.
**Target:** friendly creature.
**None/Basic:** +3 Defense for 2 rounds.
**Advanced:** +4 Defense.
**Expert:** +4 Defense and 10% ranged damage reduction.
**Counterplay purpose:** helps survive marked focus fire, Blood Command burst and celestial formation attacks.
**Why fair:** single-target even at Expert; does not grant immunity.

---

# Counter Matrix

| Mechanic | Primary counters |
|---|---|
| Bloodied / Blood Command | Burden of Stone, Quiet the Blood, Veil of Still Water |
| Blood Phoenix rebirth/sustain | Mortal Anchor, Brand of Frailty |
| Quarry Mark | Wash Away, Veil of Still Water |
| Abyss fear/control | Clear Mind, Wash Away |
| Abyss mobility | Grounding Sigil, Unbound Step |
| Veil sleep/dream control | Clear Mind, Flare of Waking, Wash Away |
| Dreamstep mobility | Grounding Sigil |
| Hollow Oaths | Scorch the Oath, Wash Away where the applied effect is removable |
| Hollow death-trigger pressure | Veil of Still Water / ordinary mitigation rather than mechanic deletion |
| Starfall Sacred Formation | Sever the Formation, Grounding Sigil |
| Celestial Alignment buffs | Wash Away only for removable sub-effects; otherwise normal mitigation |

# Balance rules
1. Counter spells remain useful in ordinary matchups.
2. No spell says “disable faction mechanic”.
3. No new dispel removes absolute/persistent effects.
4. Expert mass targeting is used sparingly and costs significantly more mana.
5. No new spell combines mass hard-control with damage.
6. New spells compete with existing H3 spells for hero actions and Mage Guild slots.
7. AI valuation and Mage Guild appearance rates are tuned after test maps.
