# Four Global Spells — World Magic v0.1

These four spells are **global Shattered Realms spells**: they are not faction-exclusive and are designed to enter the shared Mage Guild / scroll ecosystem. Each fills a strategic niche without replacing Town Portal, Dimension Door, Resurrection, Implosion or the strongest existing battlefield staples.

## 13. Leyline Convergence
**School:** Earth + Air • **Level:** 4 • **Type:** Combat • **Target:** NO_TARGET
**Fantasy:** The hero briefly aligns invisible currents beneath the battlefield; pale geometric lines connect every living stack.
**None/Basic:** for 2 rounds, both sides receive +10% spell resistance and all temporary Speed bonuses are reduced by 1 (never below the unit's printed/base speed because of this spell).
**Advanced:** 3 rounds; +15% spell resistance.
**Expert:** 3 rounds; +20% spell resistance.
**Purpose:** a symmetrical reset tool against buff-heavy, speed-combo and magic-burst armies.
**Why fair:** affects the caster too; does not dispel effects, cause damage or grant immunity.

## 14. Echo of the Fallen
**School:** Water + Earth • **Level:** 3 • **Type:** Combat • **Target:** CREATURE (friendly)
**Fantasy:** A translucent memory of the stack's fallen warriors appears for a single instant.
**None/Basic:** target gains +2 Defense for 2 rounds if it has already suffered casualties this battle.
**Advanced:** +3 Defense.
**Expert:** +3 Defense and +1 Morale where morale is applicable.
**Purpose:** comeback/attrition support without resurrection.
**Why fair:** restores no creatures or HP; useless before casualties; modest temporary stats.

## 15. Fateful Exchange
**School:** Fire + Water • **Level:** 4 • **Type:** Combat • **Target:** CREATURE (friendly)
**Fantasy:** The hero burns one advantage away to wash another weakness from fate.
**None/Basic:** removes one ordinary removable positive spell and one ordinary removable negative spell from the target.
**Advanced:** player-facing design target: removes up to one of each, then grants +1 Defense for one round.
**Expert:** same exchange plus +2 Defense for one round.
**Purpose:** deliberate counterplay when a crucial stack is both heavily buffed and disabled/debuffed.
**Why fair:** the price is sacrificing one of your own buffs; no mass cleanse; no persistent/absolute removal.

## 16. Hour of Silence
**School:** Air + Water • **Level:** 4 • **Type:** Combat • **Target:** NO_TARGET
**Fantasy:** Sound, ritual words and magical resonance disappear for one heartbeat of the battle.
**None/Basic:** design target: until the start of the caster hero's next spell opportunity, both heroes' next combat spell costs +3 mana.
**Advanced:** +4 mana.
**Expert:** +5 mana.
**Purpose:** symmetrical tempo spell against spell-chain pressure and faction spell bursts.
**Why fair:** caster pays the initial spell plus suffers the same global tax; does not prevent casting or drain existing mana.
**Implementation fallback:** if a safe next-cast cost modifier cannot be represented/serialized in VCMI, redesign as a short symmetrical Spell Power reduction rather than using brittle scripting.

# Global spell rules
- Available to old and new factions unless map/mod compatibility requires otherwise.
- Multi-school spells count as belonging to both listed schools where VCMI rules support this cleanly.
- Mage Guild appearance rates are deliberately below common level-equivalent spells until balance tests.
- No global spell permanently changes hero stats.
- No global spell grants extra turns, resurrects units, teleports armies on the adventure map, or generates resources.
- Global effects must clearly indicate that **both armies** are affected.
