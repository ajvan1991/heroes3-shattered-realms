local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

local function qualifyingDamage(payload)
    local total = 0
    local killedAny = false
    for _, target in ipairs(payload.targets or {}) do
        if target.unit and target.unit:isLiving() then
            local before = target.healthBeforeAttack or 0
            local dealt = math.min(target.damage or 0, before)
            total = total + dealt
            if (target.killed or 0) > 0 then killedAny = true end
        end
    end
    return total, killedAny
end

function Script:onAfterAttack(server, battle, unit, other, payload)
    if not unit or not unit:isAlive() then return end
    if payload.isCounter and not self.allowCounter then return end

    local damage, killedAny = qualifyingDamage(payload)
    if self.requireKill and not killedAny then return end
    if damage <= 0 then return end
    if unit:getTotalHealth() == unit:getAvailableHealth() then return end

    local toHeal = math.floor(damage * (self.val or 0) / 100)
    if toHeal <= 0 then return end

    -- normal healing only: Bloodwing Feast does not resurrect dead creatures
    server:healUnit(battle, unit, toHeal, ENUM.HealLevel.heal, ENUM.HealPower.permanent)
end

return Script
