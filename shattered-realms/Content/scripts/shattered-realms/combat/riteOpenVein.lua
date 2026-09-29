local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

local USED = "shattered-realms:riteOpenVeinUsed"

function Script:apply(server, battle, unit)
    if not unit or not unit:isAlive() then return false end
    if unit:hasBonuses({ type = USED }) then return false end

    local hp = unit:getAvailableHealth()
    local sacrifice = math.max(1, math.floor(hp * (self.sacrifice or 8) / 100))
    sacrifice = math.min(sacrifice, hp - 1)
    if sacrifice <= 0 then return false end

    server:damageUnit(battle, unit, sacrifice)
    server:addUnitBonus(battle, unit, {
        type = "PRIMARY_SKILL", subtype = "attack", val = self.val or 2,
        duration = ENUM.BonusDuration.nTurns, turns = self.turns or 2,
        stacking = "shattered-realms:riteOpenVeinBuff"
    }, false)
    server:addUnitBonus(battle, unit, {
        type = USED, val = 1, duration = ENUM.BonusDuration.oneBattle
    }, false)
    return true
end

return Script
