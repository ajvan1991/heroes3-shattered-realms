local Base = require("combat/combatScript")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

-- v0.1 uses an explicit one-action marker bonus. The marker is attached for the
-- attack resolution only and removed by its short duration; this avoids a permanent
-- BLOCKS_RETALIATION creature ability.

function Script:onBeforeAttack(server, battle, unit, other, payload)
    if not unit or not unit:isAlive() then return end
    if payload.isCounter then return end
    if (payload.attackIndex or 0) ~= 0 then return end
    if not payload.targets or #payload.targets == 0 then return end

    server:addUnitBonus(battle, unit, {
        type = "BLOCKS_RETALIATION",
        val = 0,
        duration = ENUM.BonusDuration.untilAfterAttackSequence,
        stacking = "shattered-realms:crimsonGraceWindow"
    })
end

return Script
