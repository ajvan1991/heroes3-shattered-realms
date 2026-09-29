local Base = require("spells/unitEffect")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

function Script:apply(mechanics, server, target)
    local battle = mechanics:getBattle()
    local turns = mechanics:getEffectDuration()
    local key = mechanics:getSpell():getJsonKey()
    server:addBattleBonus(battle, {
        type = "CHANGES_SPELL_COST_FOR_ALLY",
        val = self.allyDelta or 0,
        duration = ENUM.BonusDuration.nTurns,
        turns = turns,
        sourceType = "SPELL_EFFECT",
        sourceID = key,
        stacking = key .. ":allyCost"
    })
    server:addBattleBonus(battle, {
        type = "CHANGES_SPELL_COST_FOR_ENEMY",
        val = self.enemyDelta or 0,
        duration = ENUM.BonusDuration.nTurns,
        turns = turns,
        sourceType = "SPELL_EFFECT",
        sourceID = key,
        stacking = key .. ":enemyCost"
    })
end

return Script
