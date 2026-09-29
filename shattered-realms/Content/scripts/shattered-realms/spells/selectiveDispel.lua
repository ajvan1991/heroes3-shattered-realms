local Base = require("spells/unitEffect")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

local function list(mechanics, unit, positive, negative, neutral)
    local current = mechanics:getSpell():getJsonKey()
    return unit:getBonuses({}):filter(function(bonus)
        if bonus:getSource() ~= ENUM.BonusSource.spellEffect then return false end
        if bonus:getSourceID() == current then return false end
        local spell = LIBRARY:getSpellByName(bonus:getSourceID())
        if not spell or spell:isPersistent() or spell:isAdventure() then return false end
        if positive and spell:isPositive() then return true end
        if negative and spell:isNegative() then return true end
        if neutral and spell:isNeutral() then return true end
        return false
    end)
end

function Script:applicableTarget(mechanics, problem, target)
    if #target ~= 1 or not target[1].unit then return false end
    return list(mechanics,target[1].unit,self.positive,self.negative,self.neutral):size() > 0
end

function Script:apply(mechanics, server, target)
    local unit = target[1].unit
    local bonuses = list(mechanics,unit,self.positive,self.negative,self.neutral)
    if bonuses:size() > 0 then server:removeUnitBonuses(mechanics:getBattle(),unit,bonuses) end
end

return Script
