local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

function Script:onAfterAttack(server, battle, unit, other, payload)
    if not unit or not unit:isAlive() then return end
    if payload.isCounter then return end
    if (payload.attackIndex or 0) ~= 0 then return end

    for _, entry in ipairs(payload.targets or {}) do
        local target = entry.unit
        if target and target:isAlive() and target:getSide() ~= unit:getSide() and (entry.damage or 0) > 0 then
            server:addUnitBonus(battle, target, {
                type = "PRIMARY_SKILL",
                subtype = "defence",
                val = -(self.val or 1),
                duration = ENUM.BonusDuration.nTurns,
                turns = self.turns or 2,
                stacking = "shattered-realms:quarryMark"
            }, false)
        end
    end
end

return Script
