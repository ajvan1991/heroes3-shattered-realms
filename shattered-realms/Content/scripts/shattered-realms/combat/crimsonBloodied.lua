local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

local FILTER = { stacking = "shattered-realms:bloodiedActive" }

local function update(server, battle, unit, val)
    if not unit or not unit:isAlive() then return end
    local available = unit:getAvailableHealth()
    local maxCurrentStackHealth = unit:getCount() * unit:getMaxHealth()
    if maxCurrentStackHealth <= 0 then return end

    -- Bloodied measures wounds in the surviving stack, not casualties against
    -- the original battle-start stack. Dead creatures alone must not trigger it.
    local shouldBeActive = available * 100 < maxCurrentStackHealth * 50
    local active = unit:hasBonuses(FILTER)
    local current = active and unit:getBonuses(FILTER) or nil

    if shouldBeActive and not active then
        server:addUnitBonus(battle, unit, {
            type = "PRIMARY_SKILL",
            subtype = "attack",
            val = val or 1,
            duration = ENUM.BonusDuration.oneBattle,
            stacking = "shattered-realms:bloodiedActive"
        }, false)
    elseif (not shouldBeActive) and active then
        server:removeUnitBonuses(battle, unit, current)
    end
end

function Script:onBattleStart(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onAfterAttacked(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onSpellHit(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onActionFinished(server,battle,unit) update(server,battle,unit,self.val) end
function Script:onRoundStart(server,battle,unit) update(server,battle,unit,self.val) end
return Script
