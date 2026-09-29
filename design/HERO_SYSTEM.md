# Hero System — 100 Heroes & Class Passives

## Global roster rule
Every Shattered Realms faction follows the standard Heroes III town roster: **16 regular heroes** split evenly between its two native classes.

5 factions × 16 heroes = **80 regular new heroes** total.
Each faction therefore has **8 Might-class heroes + 8 Magic-class heroes**.

Every hero requires:
- unique name and portrait direction
- biography
- starting secondary skills
- specialty with explicit scaling/limits
- class-appropriate primary/secondary skill weights
- map/battle presentation required by VCMI
- balance review against comparable Heroes III specialties

Specialty families deliberately mirror the readable Heroes III model while adding faction identity:
1. **Creature specialty** — improves a named faction creature or upgrade pair, using level-scaled Attack/Defense and only a carefully bounded faction-specific rider where technically supported.
2. **Spell specialty** — improves a specific spell/effect.
3. **Secondary-skill specialty** — improves an existing skill.
4. **Faction-mechanic specialty** — improves Blood Rites, Corruption, Dream/Nightmare, Oaths or Celestial Alignments within hard limits.
5. **Economic/logistics specialty** — narrow adventure-map advantage; no runaway resource engines.

Each 8-hero class should contain multiple creature specialists plus a balanced mix of the other specialty families, following the recognizable Heroes III roster pattern.

# Exclusive class passives

Each new class has one exclusive progression:
**Basic -> Advanced -> Expert**.

These are class identity systems, not free universal bonuses. They must be implemented as a VCMI-supported skill/bonus system or scripted equivalent after technical validation. Numerical values below are initial balance targets.

## Crimson Court

### Bloodlord — Blood Command
- **Basic:** Crimson Court creatures below 50% stack HP gain +1 Attack.
- **Advanced:** bonus becomes +2 Attack; once per battle the first Crimson stack to fall below 25% gains +1 Speed until end of its next turn.
- **Expert:** +2 Attack and +1 Defense below 50%; the low-HP Speed trigger may occur once for up to two different stacks.
**Limits:** no stacking with itself; no resurrection; trigger state is per battle.

### Sanguine Seer — Crimson Divination
- **Basic:** first Blood Rite/cost-bearing faction spell in battle costs 10% less HP/resource, rounded conservatively.
- **Advanced:** 15% reduction; first friendly Crimson spell target gains +1 Spell Defense-equivalent protection for one round where supported.
- **Expert:** 20% reduction; once per battle, using a Blood Rite grants a small temporary spell-power effect to the hero's next faction spell.
**Limits:** cannot reduce a sacrifice below its defined minimum; cannot create resources.

## Abyss

### Deep Sovereign — Dread Dominion
- **Basic:** first successful melee hit by each eligible Abyss stack applies a small one-round morale/attack pressure effect.
- **Advanced:** pressure is stronger or lasts one additional bounded round, depending on implementation.
- **Expert:** affected enemies also suffer a small Defense penalty while adjacent to an Abyss creature.
**Limits:** no permanent fear lock; bosses/fear-immune targets retain immunity.

### Voidcaller — Deep Corruption
- **Basic:** faction Corruption effects gain +1 effective potency step within their own cap.
- **Advanced:** first Corruption application each round lasts +1 round.
- **Expert:** once per battle, reaching a defined Corruption threshold refunds a small bounded amount of spell points.
**Limits:** one refund per battle; no infinite spell-point cycle.

## Veil

### Lucid Warden — Dreamstep
- **Basic:** after changing Dream/Nightmare stance, affected friendly stack gains +1 Defense until its next turn.
- **Advanced:** stance change grants +1 Speed for that turn as well.
- **Expert:** first stance change by each eligible stack per battle also removes one minor movement/accuracy debuff.
**Limits:** speed does not stack; cleanse whitelist only.

### Somnomancer — Oneiromancy
- **Basic:** sleep/dream control effects gain a small resistance-piercing bonus against non-immune targets.
- **Advanced:** first successful dream-control spell costs slightly less spell points.
- **Expert:** once per battle, when a dream-control effect naturally expires, the target receives a one-round mild accuracy/attack penalty.
**Limits:** no bypass of absolute immunity; no chain sleep.

## Hollow

### Oathbreaker — Broken Vow
- **Basic:** selecting an Oath slightly increases its benefit **and** its stated drawback.
- **Advanced:** once per battle the hero may suppress the drawback of one Oath for one round.
- **Expert:** Oath benefit improves again; after the suppression round, the drawback returns normally.
**Limits:** Oaths always retain an opportunity cost; no permanent drawback removal.

### Pale Oracle — Last Testament
- **Basic:** when the first friendly stack dies, remaining Hollow stacks gain +1 Defense for one round.
- **Advanced:** also grants a small spell-resistance bonus for that round.
- **Expert:** may trigger a second time on a different stack death, but the second trigger is weaker.
**Limits:** no resurrection and no intentional-sacrifice resource loop.

## Starfall

### Halo Warden — Sacred Formation
- **Basic:** adjacent Starfall stacks gain +1 Defense while at least two eligible stacks maintain formation.
- **Advanced:** formation also grants a small ranged/spell damage reduction.
- **Expert:** groups of three or more eligible adjacent stacks gain +1 Attack in addition.
**Limits:** positional, non-stacking, immediately lost when formation breaks.

### Astral Hierophant — Celestial Alignment
- **Basic:** faction Alignment effect receives a small bounded improvement.
- **Advanced:** first Alignment transition in battle grants a minor spell-point discount to the next spell.
- **Expert:** once per battle, a completed Alignment grants a one-round faction-wide minor resistance effect.
**Limits:** no free repeated transitions; no multiplicative global damage stacking.

# Balance rules for class passives
- A class passive must be useful but weaker than combining two full Expert secondary skills.
- Basic level should change decisions, not determine battles.
- Advanced adds identity; Expert adds tactical payoff rather than a raw-stat explosion.
- Class passive effects never scale without a cap.
- Creature specialty + class passive interactions are explicitly tested.
- AI must receive sensible value estimates for passive effects.
- If a mechanic cannot be represented reliably by VCMI, it is redesigned rather than implemented as a fragile hack.
