local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

local STACKING = "shattered-realms:archonAura"

local function isAdjacentTo(battle, source, candidate)
    for _, hex in ipairs(source:getSurroundingHexes() or {}) do
        local found = battle:getUnitByPos(hex, true)
        if found and found == candidate then return true end
    end
    return false
end

local function refresh(server, battle, source)
    if not source or not source:isAlive() then return end
    local allies = battle:getUnitsIf(function(u)
        return u:isAlive() and u:getSide() == source:getSide()
    end)

    for _, ally in ipairs(allies or {}) do
        local current = ally:getBonuses({ stacking = STACKING })
        if current and #current > 0 then
            server:removeUnitBonuses(battle, ally, current)
        end
        if ally ~= source and isAdjacentTo(battle, source, ally) then
            server:addUnitBonus(battle, ally, {
                type = "PRIMARY_SKILL",
                subtype = "defence",
                val = self and self.val or 1,
                duration = ENUM.BonusDuration.oneBattle,
                stacking = STACKING
            }, false)
        end
    end
end

function Script:onBattleStart(server,battle,unit) refresh(server,battle,unit) end
function Script:onAfterMove(server,battle,unit) refresh(server,battle,unit) end
function Script:onActionFinished(server,battle,unit) refresh(server,battle,unit) end
function Script:onDeath(server,battle,unit) refresh(server,battle,unit) end
return Script
