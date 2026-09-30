#!/usr/bin/env python3
"""Static fail-closed validator for Crimson Court staging.

No VCMI runtime is emulated here. This validates the repository-side contracts that
must be true before an activation candidate is generated.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/"shattered-realms/Content/config/shattered-realms"
P={
 "faction":CFG/"crimson/faction.staging.json",
 "buildings":CFG/"crimson/buildings.staging.json",
 "creatures":CFG/"crimson/creatures.staging.json",
 "classes":CFG/"crimson/heroClasses.staging.json",
 "heroes":CFG/"crimson/heroes.staging.json",
 "scripts":CFG/"scripts/combatScripts.staging.json",
 "skills":CFG/"skills/classPassives.staging.json",
 "bloodRites":CFG/"spells/bloodRites.staging.json",
 "counterplay":CFG/"spells/counterplay.staging.json",
 "spellEffects":CFG/"scripts/spellEffects.staging.json",
 "mod":ROOT/"shattered-realms/mod.json",
}
load=lambda p: json.loads(p.read_text(encoding="utf-8"))
D={k:load(v) for k,v in P.items()}
fac=D["faction"]["crimsonCourt"]; town=fac["town"]; b=D["buildings"]; cr=D["creatures"]; hc=D["classes"]; he=D["heroes"]; scripts=D["scripts"].get("scripts",{}); skills=D["skills"]; rites=D["bloodRites"]; counterplay=D["counterplay"]; spellEffects=D["spellEffects"]
errors=[]; checks={}

def reqrefs(v):
    out=[]
    if isinstance(v,str):
        if v not in {"allOf","anyOf","noneOf"}: out.append(v)
    elif isinstance(v,list):
        for x in v: out.extend(reqrefs(x))
    return out

def ck(name, ok, detail):
    checks[name]={"status":"PASS" if ok else "FAIL","detail":detail}
    if not ok: errors.append(f"{name}: {detail}")

ck("townTierCount",7<=len(town.get("creatures",[]))<=8,len(town.get("creatures",[])))
ck("hallRowCount",len(town.get("hallSlots",[]))==5,len(town.get("hallSlots",[])))
hallWidths=[len(row) for row in town.get("hallSlots",[])]
ck("hallRowWidths",all(1<=n<=4 for n in hallWidths),hallWidths)
pm=fac.get("puzzleMap",{}); pieces=pm.get("pieces",[])
indices=[x.get("index") for x in pieces]
ck("puzzleMapPieceCount",len(pieces)==48,len(pieces))
ck("puzzleMapIndices",sorted(indices)==list(range(1,49)),indices)
requiredTown={"mapObject","buildingsIcons","buildings","creatures","guildWindow","names","hallBackground","hallSlots","horde","mageGuild","moatAbility","defaultTavern","tavernVideo","guildBackground","musicTheme","siege","structures","townBackground"}
missingTown=sorted(requiredTown-set(town))
ck("townRequiredFields",not missingTown,missingTown)
ck("buildingCount",len(b)==41,len(b))
ck("creatureCount",len(cr)==14,len(cr))
ck("heroCount",len(he)==16,len(he))
ck("structureCoverage",set(b)<=set(town.get("structures",{})),sorted(set(b)-set(town.get("structures",{}))))

dang=[]
for i,x in b.items():
    for r in reqrefs(x.get("requires")):
        if r not in b: dang.append([i,"requires",r])
    r=x.get("upgrades")
    if r and r not in b: dang.append([i,"upgrades",r])
ck("buildingGraph",not dang,dang)

# Upgrade edges must be acyclic; otherwise town construction can become impossible.
cycles=[]
for start in b:
    seen=[]; cur=start
    while cur in b and b[cur].get("upgrades"):
        if cur in seen:
            cycles.append(seen[seen.index(cur):]+[cur]); break
        seen.append(cur); cur=b[cur]["upgrades"]
ck("buildingUpgradeCycles",not cycles,cycles)

# Numeric building IDs are part of the town contract and must remain unique.
ids=[x.get("id") for x in b.values()]
dupeIds=sorted({x for x in ids if ids.count(x)>1})
ck("buildingIds",all(isinstance(x,int) for x in ids) and not dupeIds,{"duplicates":dupeIds,"count":len(ids)})

hall=[x for row in town.get("hallSlots",[]) for slot in row for x in slot]
ck("hallReferences",all(x in b for x in hall),[x for x in hall if x not in b])
tiers=[x for tier in town.get("creatures",[]) for x in tier]
ck("townCreatureReferences",all(x in cr for x in tiers),[x for x in tiers if x not in cr])
tierShape=[]; upgradeErrors=[]
for n,tier in enumerate(town.get("creatures",[]),1):
 if len(tier)!=2: tierShape.append([n,len(tier)])
 else:
  base,up=tier
  if cr.get(base,{}).get("level")!=n or cr.get(up,{}).get("level")!=n: upgradeErrors.append([n,"level",base,up])
  if cr.get(base,{}).get("upgrades")!=[up]: upgradeErrors.append([n,"upgrade",base,cr.get(base,{}).get("upgrades"),up])
  if cr.get(up,{}).get("upgrades"): upgradeErrors.append([n,"upgrade-has-upgrades",up])
ck("townCreaturePairShape",not tierShape,tierShape)
ck("townCreatureUpgradeChains",not upgradeErrors,upgradeErrors)

creatureNumeric=[]
for cid,x in cr.items():
 dmg=x.get("damage",{}); cost=x.get("cost",{})
 if not (1<=x.get("level",0)<=7): creatureNumeric.append([cid,"level",x.get("level")])
 for key in ("speed","hitPoints","attack","defense","fightValue","aiValue","growth"):
  if not isinstance(x.get(key),(int,float)) or x.get(key)<=0: creatureNumeric.append([cid,key,x.get(key)])
 if not isinstance(dmg.get("min"),(int,float)) or not isinstance(dmg.get("max"),(int,float)) or dmg.get("min",0)<=0 or dmg.get("max",0)<dmg.get("min",0): creatureNumeric.append([cid,"damage",dmg])
 if not isinstance(cost,dict) or not cost or any(not isinstance(v,(int,float)) or v<=0 for v in cost.values()): creatureNumeric.append([cid,"cost",cost])
ck("creatureNumericContracts",not creatureNumeric,creatureNumeric)

shooterErrors=[]
for cid,x in cr.items():
 abilities=x.get("abilities",{}) or {}
 isShooter=any(isinstance(a,dict) and a.get("type")=="SHOOTER" for a in abilities.values())
 shots=x.get("shots")
 if isShooter and (not isinstance(shots,int) or shots<=0): shooterErrors.append([cid,"shooter-without-shots",shots])
 if not isShooter and shots is not None: shooterErrors.append([cid,"shots-without-shooter",shots])
ck("creatureShooterContracts",not shooterErrors,shooterErrors)

badclass=[]; badarmy=[]; badspec=[]
for i,h in he.items():
    if h.get("class") not in hc: badclass.append([i,h.get("class")])
    for a in h.get("army",[]):
        if a.get("creature") not in cr: badarmy.append([i,a.get("creature")])
    s=h.get("specialty",{})
    if isinstance(s,dict) and s.get("creature") and s["creature"] not in cr: badspec.append([i,s["creature"]])
ck("heroClassReferences",not badclass,badclass)
badCommander=[[i,x.get("commander")] for i,x in hc.items() if x.get("commander") not in cr]
badFaction=[[i,x.get("faction")] for i,x in hc.items() if x.get("faction")!="crimsonCourt"]
badAffinity=[[i,x.get("affinity")] for i,x in hc.items() if x.get("affinity") not in {"might","magic"}]
ck("heroClassCommanders",not badCommander,badCommander)
ck("heroClassFaction",not badFaction,badFaction)
ck("heroClassAffinity",not badAffinity,badAffinity)

# Crimson class-passive contract: each hero class must actually start with its exclusive
# passive. gainChance=0 only prevents random level-up offers; it does not grant the skill.
exclusiveByClass={"bloodlord":"bloodCommand","sanguineSeer":"crimsonDivination"}
missingExclusive=[]
for heroId,h in he.items():
 expected=exclusiveByClass.get(h.get("class"))
 if expected and not any(x.get("skill")==expected for x in h.get("skills",[])):
  missingExclusive.append([heroId,expected])
ck("heroExclusiveClassPassives",not missingExclusive,missingExclusive)
badExclusiveChance=[]
for classId,skillId in exclusiveByClass.items():
 chance=hc.get(classId,{}).get("secondarySkills",{}).get(skillId)
 if not isinstance(chance,(int,float)) or chance<=0: badExclusiveChance.append([classId,skillId,chance])
ck("classPassiveUpgradeChance",not badExclusiveChance,badExclusiveChance)

# Keep the exclusive passive absent from the opposite class table.
crossExclusive=[]
if "crimsonDivination" in hc.get("bloodlord",{}).get("secondarySkills",{}): crossExclusive.append(["bloodlord","crimsonDivination"])
if "bloodCommand" in hc.get("sanguineSeer",{}).get("secondarySkills",{}): crossExclusive.append(["sanguineSeer","bloodCommand"])
ck("classPassiveCrossClassBan",not crossExclusive,crossExclusive)
ck("heroArmyReferences",not badarmy,badarmy)
ck("heroCreatureSpecialties",not badspec,badspec)
heroShape=[]
classCounts={k:0 for k in hc}
for hid,h in he.items():
 if h.get("class") in classCounts: classCounts[h["class"]]+=1
 army=h.get("army",[])
 if not (1<=len(army)<=3): heroShape.append([hid,"army-size",len(army)])
 for a in army:
  if not isinstance(a.get("min"),int) or not isinstance(a.get("max"),int) or a.get("min",0)<=0 or a.get("max",0)<a.get("min",0): heroShape.append([hid,"army-range",a])
 skillsList=h.get("skills",[])
 if len({x.get("skill") for x in skillsList})!=len(skillsList): heroShape.append([hid,"duplicate-skill"])
 if h.get("class")=="sanguineSeer" and "spellbook" not in h: heroShape.append([hid,"missing-spellbook"])
ck("heroRuntimeShape",not heroShape,heroShape)
ck("heroClassRosterBalance",classCounts=={"bloodlord":8,"sanguineSeer":8},classCounts)

# Specialty shortcuts must point to something the hero can actually use/grow.
specialtySkillErrors=[]
for hid,h in he.items():
    sec=h.get("specialty",{}).get("secondary")
    if sec:
        allowed=hc.get(h.get("class"),{}).get("secondarySkills",{})
        if sec not in allowed or allowed.get(sec,0)<=0:
            specialtySkillErrors.append([hid,sec,"not-positive-in-class-table"])
ck("heroSecondarySpecialtyClassAvailability",not specialtySkillErrors,specialtySkillErrors)

# Keep the v0.1 roster from silently collapsing into accidental duplicate native
# specialties. Duplicates are allowed only when explicitly recorded here.
expectedDuplicateSecondary={
    "offence":{"ilyrThorn","thaliaVeyn"},
    "intelligence":{"caelis","miraleth"},
    "mysticism":{"elyssVane","saereth"},
    "sorcery":{"lysandraNoct","vespera"},
}
actualSecondary={}
for hid,h in he.items():
    sec=h.get("specialty",{}).get("secondary")
    if sec: actualSecondary.setdefault(sec,set()).add(hid)
actualDuplicates={k:v for k,v in actualSecondary.items() if len(v)>1}
ck("heroSecondarySpecialtyDuplicateContract",actualDuplicates==expectedDuplicateSecondary,{k:sorted(v) for k,v in actualDuplicates.items()})

badscript=[]
for i,c in cr.items():
    for a in (c.get("abilities") or {}).values():
        if isinstance(a,dict) and a.get("type")=="COMBAT_EVENT_TRIGGER":
            sub=a.get("subtype")
            if sub!="rebirth" and sub not in scripts: badscript.append([i,sub])
ck("combatScriptReferences",not badscript,badscript)

abilityContracts=[]
for cid,x in cr.items():
 abilities=x.get("abilities",{}) or {}
 for aid,a in abilities.items():
  if not isinstance(a,dict) or not isinstance(a.get("type"),str): abilityContracts.append([cid,aid,"type"])
  if isinstance(a,dict) and a.get("type")=="COMBAT_EVENT_TRIGGER":
   if not isinstance(a.get("subtype"),str) or not a.get("subtype"): abilityContracts.append([cid,aid,"subtype"])
   if not isinstance(a.get("val"),(int,float)): abilityContracts.append([cid,aid,"val"])
ck("creatureAbilityShape",not abilityContracts,abilityContracts)

# Explicit regression gates for the four custom Crimson combat mechanics plus native rebirth.
expectedTriggers={
 "bloodbound":{"crimsonBloodied"},
 "crimsonDancer":{"crimsonDancerGrace","crimsonBloodied"},
 "bloodwing":{"crimsonBloodwingDrain","crimsonBloodied"},
 "veinOracle":{"crimsonBloodied"},
 "bloodstalker":{"crimsonBloodied","crimsonQuarryMark"},
 "crimsonArchon":{"crimsonBloodied"},
 "eternalBloodPhoenix":{"rebirth","crimsonBloodied"},
}
triggerMismatch=[]
for cid,expected in expectedTriggers.items():
 actual={a.get("subtype") for a in (cr.get(cid,{}).get("abilities",{}) or {}).values() if isinstance(a,dict) and a.get("type")=="COMBAT_EVENT_TRIGGER"}
 if actual!=expected: triggerMismatch.append([cid,sorted(expected),sorted(actual)])
ck("crimsonTriggerRegression",not triggerMismatch,triggerMismatch)

# Validate the subset of VCMI script.json that is critical for combat-event registration.
badscriptdefs=[]
for sid,s in scripts.items():
    if s.get("implements")!="combatEvent": badscriptdefs.append([sid,"implements"])
    if not isinstance(s.get("script"),str) or not s.get("script"): badscriptdefs.append([sid,"script"])
    if not isinstance(s.get("patches"),list): badscriptdefs.append([sid,"patches"])
    if not isinstance(s.get("schema"),dict): badscriptdefs.append([sid,"schema"])
    if not isinstance(s.get("description"),str) or not s.get("description"): badscriptdefs.append([sid,"description"])
    if not isinstance(s.get("priority"),(int,float)): badscriptdefs.append([sid,"priority"])
    scriptfile=ROOT/"shattered-realms/Content/scripts"/(str(s.get("script",""))+".lua")
    if not scriptfile.is_file(): badscriptdefs.append([sid,"lua",str(scriptfile.relative_to(ROOT))])
ck("combatScriptDefinitions",not badscriptdefs,badscriptdefs)

# Crimson class-passive activation contract: only the two Crimson passives belong
# in the first candidate; future-faction empty passives must not be accidentally
# treated as implemented Crimson runtime mechanics.
crimsonSkills={"bloodCommand","crimsonDivination"}
missingCrimsonSkills=sorted(crimsonSkills-set(skills))
ck("crimsonClassPassiveDefinitions",not missingCrimsonSkills,missingCrimsonSkills)
emptyCrimson=[]
for sid in crimsonSkills:
    s=skills.get(sid,{})
    for tier in ("basic","advanced","expert"):
        if not s.get(tier,{}).get("effects"): emptyCrimson.append([sid,tier])
ck("crimsonClassPassiveEffects",not emptyCrimson,emptyCrimson)

# VCMI counts a starting skill as newly gained for offerCooldown. These two
# passives start on every Crimson hero, so cooldown must stay zero or normal
# Basic -> Advanced -> Expert progression can be withheld for many levels.
passiveCooldown=[]
for sid in crimsonSkills:
    if skills.get(sid,{}).get("offerCooldown",0)!=0:
        passiveCooldown.append([sid,skills.get(sid,{}).get("offerCooldown")])
ck("crimsonClassPassiveOfferCooldown",not passiveCooldown,passiveCooldown)

# Future-faction passive definitions are design staging only. Keep them inert and
# explicitly non-random until their faction runtime contracts exist.
futureSkills=set(skills)-crimsonSkills
futurePassiveErrors=[]
for sid in sorted(futureSkills):
 s=skills.get(sid,{})
 if s.get("gainChance")!={"might":0,"magic":0}: futurePassiveErrors.append([sid,"gainChance",s.get("gainChance")])
 for tier in ("basic","advanced","expert"):
  if s.get(tier,{}).get("effects"): futurePassiveErrors.append([sid,tier,"effects-not-empty"])
ck("futureClassPassivesRemainInert",not futurePassiveErrors,futurePassiveErrors)

# Spell staging must not silently enable reserved mechanics. Blood Rites are
# candidate-local and generation-disabled; universal counterplay spells are either
# deliberately available to all five factions or deliberately reserved everywhere.
spellStageErrors=[]
for sid,s in rites.items():
 if s.get("defaultGainChance")!=0: spellStageErrors.append([sid,"blood-rite-defaultGainChance",s.get("defaultGainChance")])
 if any(v!=0 for v in (s.get("gainChance") or {}).values()): spellStageErrors.append([sid,"blood-rite-gainChance",s.get("gainChance")])
for sid,s in counterplay.items():
 gc=s.get("gainChance") or {}; dg=s.get("defaultGainChance")
 vals=[gc.get(fid) for fid in ("crimsonCourt","abyss","veil","hollow","starfall")]
 if dg==0:
  if any(v!=0 for v in vals): spellStageErrors.append([sid,"reserved-spell-enabled",gc])
 elif dg>0:
  if any(v!=dg for v in vals): spellStageErrors.append([sid,"universal-gainChance-not-equal",dg,gc])
 else: spellStageErrors.append([sid,"invalid-defaultGainChance",dg])
ck("spellGenerationContract",not spellStageErrors,spellStageErrors)

# Custom spell-effect references must resolve to the staged spell-effect registry.
effectIds=set()
if isinstance(spellEffects,dict):
 effectIds=set(spellEffects.get("scripts",spellEffects.get("effects",spellEffects)).keys())
customEffectErrors=[]
for family,doc in (("bloodRites",rites),("counterplay",counterplay)):
 for sid,s in doc.items():
  for lvl,lvlDoc in (s.get("levels") or {}).items():
   for eid,e in (lvlDoc.get("effects") or {}).items():
    typ=e.get("type") if isinstance(e,dict) else None
    if isinstance(typ,str) and typ.startswith("shattered-realms:"):
     ref=typ.split(":",1)[1]
     if ref not in effectIds: customEffectErrors.append([family,sid,lvl,eid,ref])
ck("customSpellEffectReferences",not customEffectErrors,customEffectErrors)

# Siege prefix is a derived resource contract: VCMI composes filenames from it.
siege=town["siege"]
prefix=siege.get("imagePrefix")
ck("siegeImagePrefix",isinstance(prefix,str) and bool(prefix),prefix)
siegeSuffixes=["BACK","TW21","TW22","TW2C","MAN1","MAN2","MANC","TW11","TW12","TW1C","DRW1","DRW2","DRW3","ARCH","WA61","WA62","WA63","WA41","WA42","WA43","WA31","WA32","WA33","WA11","WA12","WA13","MOAT","MLIP","WA2","WA5","TPWL"]
ck("siegeDerivedFamilyCount",len(siegeSuffixes)==31,len(siegeSuffixes))

# Production manifest must remain inert until activation is explicitly approved.
game_keys={"factions","heroClasses","heroes","skills","creatures","artifacts","objects","spells","terrains","roads","rivers","battlefields","obstacles","mapLayers","templates","scripts"}
active=sorted(game_keys & set(D["mod"]))
ck("productionModInert",not active,active)

report={"result":"PASS" if not errors else "FAIL","checks":checks,"errors":errors}
out=ROOT/"production/crimson-static-validation.latest.json"
out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
