local Base = require("spells/unitEffect")
local Script = setmetatable({}, {__index = Base})
Script.__index = Script

local function sacrifice(unit, percent)
    local hp = unit:getAvailableHealth()
    local amount = math.max(1, math.floor(hp * percent / 100))
    return math.min(amount, hp - 1)
end

function Script:applicableTarget(mechanics, problem, target)
    if #target ~= 1 or not target[1].unit then return false end
    local unit = target[1].unit
    if not unit:isAlive() or not unit:isLiving() then return false end
    if unit:getAvailableHealth() <= 1 then return false end
    if self.usedMarker and unit:hasBonuses({ type = self.usedMarker }) then return false end
    return true
end

function Script:getHealthChange(mechanics, target)
    if #target ~= 1 or not target[1].unit then return { hpDelta = 0, unitsDelta = 0 } end
    local amount = sacrifice(target[1].unit, self.sacrifice or 8)
    return { hpDelta = -amount, unitsDelta = 0 }
end

function Script:apply(mechanics, server, target)
    local unit = target[1].unit
    local battle = mechanics:getBattle()
    local amount = sacrifice(unit, self.sacrifice or 8)
    if amount <= 0 then return end

    server:damageUnit(battle, unit, amount)

    server:addUnitBonus(battle, unit, {
        type = "PRIMARY_SKILL",
        subtype = self.stat or "attack",
        val = self.statValue or 2,
        duration = "N_TURNS",
        turns = mechanics:getEffectDuration(),
        sourceType = "SPELL_EFFECT",
        sourceID = mechanics:getSpell():getJsonKey(),
        stacking = mechanics:getSpell():getJsonKey()
    }, false)

    if self.rangedReduction and self.rangedReduction > 0 then
        server:addUnitBonus(battle, unit, {
            type = "GENERAL_DAMAGE_REDUCTION",
            subtype = "damageTypeRanged",
            val = self.rangedReduction,
            effectRange = "ONLY_DISTANCE_FIGHT",
            duration = "N_TURNS",
            turns = mechanics:getEffectDuration(),
            sourceType = "SPELL_EFFECT",
            sourceID = mechanics:getSpell():getJsonKey(),
            stacking = mechanics:getSpell():getJsonKey() .. ":ranged"
        }, false)
    end

    if self.usedMarker then
        server:addUnitBonus(battle, unit, {
            type = self.usedMarker, val = 1, duration = "ONE_BATTLE"
        }, false)
    end
end

return Script
