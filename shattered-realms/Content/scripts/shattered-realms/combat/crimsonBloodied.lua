local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

local function bonus(unit)
    for _, b in ipairs(unit:getBonuses() or {}) do
        if b.stacking == "shattered-realms:bloodiedActive" then return b end
    end
    return nil
end

local function update(server, battle, unit, val)
    if not unit or not unit:isAlive() then return end
    local available = unit:getAvailableHealth()
    local total = unit:getTotalHealth()
    if total <= 0 then return end
    local shouldBeActive = available * 100 < total * 50
    local current = bonus(unit)

    if shouldBeActive and not current then
        server:addUnitBonus(battle, unit, {
            type = "PRIMARY_SKILL",
            subtype = "attack",
            val = val or 1,
            duration = ENUM.BonusDuration.oneBattle,
            stacking = "shattered-realms:bloodiedActive"
        }, false)
    elseif (not shouldBeActive) and current then
        server:removeUnitBonuses(battle, unit, { current })
    end
end

function Script:onBattleStart(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onAfterAttacked(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onActionFinished(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onRoundStart(server,battle,unit) update(server,battle,unit,self.val) end
return Script
