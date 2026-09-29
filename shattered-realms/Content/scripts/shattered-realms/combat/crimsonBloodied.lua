local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script
local KEY = "shattered-realms:bloodiedActive"

local function update(server, battle, unit, val)
    if not unit or not unit:isAlive() then return end
    local available = unit:getAvailableHealth()
    local total = unit:getTotalHealth()
    if total <= 0 then return end
    local active = available * 100 < total * 50
    server:removeUnitBonus(battle, unit, { stacking = KEY })
    if active then
        server:addUnitBonus(battle, unit, {
            type = "PRIMARY_SKILL",
            subtype = "attack",
            val = val or 1,
            duration = ENUM.BonusDuration.oneBattle,
            stacking = KEY
        })
    end
end
function Script:onBattleStart(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onAfterAttacked(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onActionFinished(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onRoundStart(server,battle,unit) update(server,battle,unit,self.val) end
return Script
