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
 "spellContract":ROOT/"production/crimson-spell-contract.v0.1.json",
 "mod":ROOT/"shattered-realms/mod.json",
}
load=lambda p: json.loads(p.read_text(encoding="utf-8"))
D={k:load(v) for k,v in P.items()}
fac=D["faction"]["crimsonCourt"]; town=fac["town"]; b=D["buildings"]; cr=D["creatures"]; hc=D["classes"]; he=D["heroes"]; scripts=D["scripts"].get("scripts",{}); skills=D["skills"]; rites=D["bloodRites"]; counterplay=D["counterplay"]; spellEffects=D["spellEffects"]; spellContract=D["spellContract"]
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

# Hero starting-kit contract: every regular hero starts its class-exclusive
# passive at Basic; Seers explicitly own an empty spellbook and no hero starts
# the opposite class passive.
heroKitErrors=[]
classPassive={"bloodlord":"bloodCommand","sanguineSeer":"crimsonDivination"}
for hid,h in he.items():
 cls=h.get("class"); expected=classPassive.get(cls)
 skillsList=h.get("skills") or []
 pairs=[(x.get("skill"),x.get("level")) for x in skillsList]
 if pairs.count((expected,"basic"))!=1: heroKitErrors.append([hid,"exclusive-passive",pairs,expected])
 opposite="crimsonDivination" if expected=="bloodCommand" else "bloodCommand"
 if any(x.get("skill")==opposite for x in skillsList): heroKitErrors.append([hid,"cross-class-passive",opposite])
 if cls=="sanguineSeer" and h.get("spellbook")!=[]: heroKitErrors.append([hid,"seer-spellbook-must-be-explicit-empty",h.get("spellbook")])
 if cls=="bloodlord" and "spellbook" in h: heroKitErrors.append([hid,"bloodlord-unexpected-spellbook",h.get("spellbook")])
 if not isinstance(h.get("female"),bool): heroKitErrors.append([hid,"female-flag"])
 texts=h.get("texts") or {}; specText=texts.get("specialty") or {}
 if not texts.get("name") or not texts.get("biography"): heroKitErrors.append([hid,"missing-name-or-biography"])
 if not all(specText.get(k) for k in ("name","description","tooltip")): heroKitErrors.append([hid,"incomplete-specialty-text"])
ck("heroStartingKitContract",not heroKitErrors,heroKitErrors)

# Exact v0.1 specialty distribution: six Bloodlord creature specialists, one
# Seer creature specialist, and conservative native secondary specialists.
specialtyDistributionErrors=[]
expectedCreature={
 "vaelor":"veinling","seris":"thornDancer","khaeren":"gorewing","maelira":"scarletHuntress",
 "othrys":"sanguineNoble","rhaevan":"bloodPhoenix","aveline":"hemomancer",
}
expectedSecondary={
 "thaliaVeyn":"offence","ilyrThorn":"offence","sevrin":"wisdom",
 "miraleth":"intelligence","caelis":"intelligence","vespera":"sorcery",
 "elyssVane":"mysticism","saereth":"mysticism","lysandraNoct":"sorcery",
}
for hid,h in he.items():
 spec=h.get("specialty") or {}
 expected={"creature":expectedCreature[hid]} if hid in expectedCreature else {"secondary":expectedSecondary.get(hid)}
 if spec!=expected: specialtyDistributionErrors.append([hid,spec,expected])
 # Creature specialties deliberately name the base creature of an upgrade pair.
 if hid in expectedCreature and expectedCreature[hid] not in cr: specialtyDistributionErrors.append([hid,"unknown-creature-specialty",expectedCreature[hid]])
ck("heroSpecialtyDistributionSnapshot",not specialtyDistributionErrors,specialtyDistributionErrors)

# Starting armies are deliberately restricted to early Crimson troops so no
# hero can accidentally begin with a high-tier unit through a data edit.
armyTierErrors=[]
allowedStarting={"veinling","thornDancer"}
for hid,h in he.items():
 for stack in h.get("army",[]) or []:
  if stack.get("creature") not in allowedStarting: armyTierErrors.append([hid,stack.get("creature")])
ck("heroStartingArmyTierContract",not armyTierErrors,armyTierErrors)

# Hero-class identity snapshot. These values control level-up identity and must
# not drift while balancing individual heroes.
classIdentityErrors=[]
expectedClass={
 "bloodlord":{"affinity":"might","commander":"bloodstalker","primarySkills":{"attack":2,"defence":2,"spellpower":1,"knowledge":1},"lowLevelChance":{"attack":40,"defence":35,"spellpower":15,"knowledge":10},"highLevelChance":{"attack":30,"defence":30,"spellpower":20,"knowledge":20},"passive":"bloodCommand"},
 "sanguineSeer":{"affinity":"magic","commander":"bloodstalker","primarySkills":{"attack":1,"defence":1,"spellpower":2,"knowledge":2},"lowLevelChance":{"attack":15,"defence":15,"spellpower":35,"knowledge":35},"highLevelChance":{"attack":20,"defence":20,"spellpower":30,"knowledge":30},"passive":"crimsonDivination"},
}
for cid,exp in expectedClass.items():
 cls=hc.get(cid,{})
 for field in ("affinity","commander","primarySkills","lowLevelChance","highLevelChance"):
  if cls.get(field)!=exp[field]: classIdentityErrors.append([cid,field,cls.get(field),exp[field]])
 if cls.get("faction")!="crimsonCourt" or cls.get("defaultTavern")!=5 or cls.get("tavern")!={"crimsonCourt":100}: classIdentityErrors.append([cid,"faction-tavern-contract"])
 if cls.get("secondarySkills",{}).get(exp["passive"])!=1: classIdentityErrors.append([cid,"exclusive-passive-weight",cls.get("secondarySkills",{}).get(exp["passive"])])
 for chanceField in ("lowLevelChance","highLevelChance"):
  if sum(cls.get(chanceField,{}).values())!=100: classIdentityErrors.append([cid,chanceField+"-sum",sum(cls.get(chanceField,{}).values())])
ck("heroClassIdentitySnapshot",not classIdentityErrors,classIdentityErrors)

# Active Crimson class passives are native, fully populated three-tier skills.
# Future faction passives remain inert elsewhere in this validator.
passiveRuntimeErrors=[]
expectedPassive={
 "bloodCommand":{
  "basic":{"bloodCommandAttack":("PRIMARY_SKILL","attack",1)},
  "advanced":{"bloodCommandAttack":("PRIMARY_SKILL","attack",1),"bloodCommandDefence":("PRIMARY_SKILL","defence",1)},
  "expert":{"bloodCommandAttack":("PRIMARY_SKILL","attack",2),"bloodCommandDefence":("PRIMARY_SKILL","defence",1)},
 },
 "crimsonDivination":{
  "basic":{"riteDiscipline":("MANA_PER_KNOWLEDGE_PERCENTAGE",None,10)},
  "advanced":{"riteDiscipline":("MANA_PER_KNOWLEDGE_PERCENTAGE",None,15),"riteFocus":("SPELL_DAMAGE","any",5)},
  "expert":{"riteDiscipline":("MANA_PER_KNOWLEDGE_PERCENTAGE",None,20),"riteFocus":("SPELL_DAMAGE","any",10)},
 },
}
for sid,tiers in expectedPassive.items():
 s=skills.get(sid,{})
 if s.get("gainChance")!={"might":0,"magic":0} or s.get("offerCooldown")!=0: passiveRuntimeErrors.append([sid,"availability-contract",s.get("gainChance"),s.get("offerCooldown")])
 if s.get("tags",{}).get("classExclusive") is not True: passiveRuntimeErrors.append([sid,"classExclusive-tag"])
 for tier,expectedEffects in tiers.items():
  node=s.get(tier,{})
  actual={}
  for eid,e in (node.get("effects") or {}).items(): actual[eid]=(e.get("type"),e.get("subtype"),e.get("val"))
  if actual!=expectedEffects: passiveRuntimeErrors.append([sid,tier,"effects",actual,expectedEffects])
  images=node.get("images") or {}
  if set(images)!={"small","medium","large","scenarioBonus"} or not all(images.values()): passiveRuntimeErrors.append([sid,tier,"images"])
  if not node.get("description"): passiveRuntimeErrors.append([sid,tier,"description"])
ck("activeClassPassiveRuntimeSnapshot",not passiveRuntimeErrors,passiveRuntimeErrors)

# Town roster/UI/siege identity snapshot. This complements graph/reference
# closure by detecting semantically valid but unintended town-layout drift.
townIdentityErrors=[]
fac=D["faction"].get("crimsonCourt",{}); town=fac.get("town",{})
expectedTiers=[["veinling","bloodbound"],["thornDancer","crimsonDancer"],["gorewing","bloodwing"],["hemomancer","veinOracle"],["scarletHuntress","bloodstalker"],["sanguineNoble","crimsonArchon"],["bloodPhoenix","eternalBloodPhoenix"]]
if town.get("creatures")!=expectedTiers: townIdentityErrors.append(["creature-tiers",town.get("creatures")])
slots=town.get("hallSlots") or []
if len(slots)!=5 or any(not (1<=len(row)<=4) for row in slots): townIdentityErrors.append(["hall-shape",[len(x) for x in slots]])
expectedHall0=[["villageHall","townHall","cityHall","capitol"],["fort","citadel","castle"],["tavern","blacksmith"],["marketplace","resourceSilo"]]
if not slots or slots[0]!=expectedHall0: townIdentityErrors.append(["hall-core-row",slots[0] if slots else None])
if len(town.get("structures") or {})!=41: townIdentityErrors.append(["structure-count",len(town.get("structures") or {})])
siege=town.get("siege") or {}
if siege.get("shooter")!="bloodstalker" or siege.get("imagePrefix")!="CRIMSON/SIEGE/CRSG": townIdentityErrors.append(["siege-identity",siege.get("shooter"),siege.get("imagePrefix")])
if fac.get("alignment")!="neutral" or fac.get("nativeTerrain")!="dirt": townIdentityErrors.append(["faction-identity",fac.get("alignment"),fac.get("nativeTerrain")])
ck("townRuntimeIdentitySnapshot",not townIdentityErrors,townIdentityErrors)

# Puzzle/Grail/horde families are exact runtime-facing town contracts.
townFamilyErrors=[]
puzzle=fac.get("puzzleMap") or {}
pieces=puzzle.get("pieces") or []
if puzzle.get("prefix")!="CRIMSON/PUZZLE/CRP": townFamilyErrors.append(["puzzle-prefix",puzzle.get("prefix")])
if len(pieces)!=48 or [p.get("index") for p in pieces]!=list(range(1,49)): townFamilyErrors.append(["puzzle-index-family",len(pieces),[p.get("index") for p in pieces]])
grail=(town.get("buildings") or {}).get("grail",{})
if (grail.get("id"),grail.get("mode"),grail.get("produce"))!=(26,"grail",{"gold":5000}): townFamilyErrors.append(["grail-contract",grail])
expectedHorde={"hordeThorns":(44,"thornGallery"),"hordeThornsUp":(45,"crimsonGallery"),"hordeHunt":(46,"scarletLodge"),"hordeHuntUp":(47,"bloodstalkerLodge")}
for bid,(eid,upgrade) in expectedHorde.items():
 bld=(town.get("buildings") or {}).get(bid,{})
 if (bld.get("id"),bld.get("upgrades"))!=(eid,upgrade): townFamilyErrors.append([bid,bld.get("id"),bld.get("upgrades"),eid,upgrade])
specialIds={k:v.get("id") for k,v in (town.get("buildings") or {}).items() if isinstance(v,dict) and 50<=v.get("id",-1)<=55}
if specialIds!={"courtVeins":50,"scarletConservatory":51,"firstChalice":52,"moonlitMenagerie":53,"thornTribunal":54,"redMoonObservatory":55}: townFamilyErrors.append(["special-building-ids",specialIds])
ck("townSpecialFamiliesSnapshot",not townFamilyErrors,townFamilyErrors)

# Building economy/progression safety: IDs and costs must remain sane and
# canonical staging must stay synchronized with the faction-embedded copy.
buildingEconomyErrors=[]
embedded=town.get("buildings") or {}
if embedded!=b: buildingEconomyErrors.append(["embedded-buildings-drift"])
ids=[x.get("id") for x in b.values()]
if len(ids)!=len(set(ids)): buildingEconomyErrors.append(["duplicate-building-ids",ids])
allowedResources={"wood","ore","mercury","sulfur","crystal","gems","gold"}
for bid,x in b.items():
 cost=x.get("cost") or {}
 if any(k not in allowedResources or not isinstance(v,int) or v<0 for k,v in cost.items()): buildingEconomyErrors.append([bid,"invalid-cost",cost])
 prod=x.get("produce") or {}
 if any(k not in allowedResources or not isinstance(v,int) or v<0 for k,v in prod.items()): buildingEconomyErrors.append([bid,"invalid-produce",prod])
 if x.get("upgrades")==bid: buildingEconomyErrors.append([bid,"self-upgrade"])
# Exact economic backbone protects classic H3 town pacing.
expectedIncome={"villageHall":500,"townHall":1000,"cityHall":2000,"capitol":4000,"grail":5000}
for bid,gold in expectedIncome.items():
 if b.get(bid,{}).get("produce",{}).get("gold")!=gold: buildingEconomyErrors.append([bid,"gold-income",b.get(bid,{}).get("produce"),gold])
if b.get("resourceSilo",{}).get("produce")!={"wood":1,"ore":1}: buildingEconomyErrors.append(["resourceSilo","produce",b.get("resourceSilo",{}).get("produce")])
ck("buildingEconomyAndSyncContract",not buildingEconomyErrors,buildingEconomyErrors)

# Dwelling progression snapshot protects the seven-tier economic curve and
# prevents a valid dependency edit from silently flattening town development.
dwellingErrors=[]
dwellingPairs=[
 ("veinHouse","veinHouseUp",400,900),("thornGallery","crimsonGallery",1000,1500),
 ("gorewingRoost","bloodwingRoost",1800,2200),("hallVeins","oracleHall",2500,3000),
 ("scarletLodge","bloodstalkerLodge",3500,4500),("sanguinePalace","archonPalace",7000,9000),
 ("heartAviary","eternalAviary",12000,16000),
]
lastBaseGold=-1
for baseId,upId,baseGold,upGold in dwellingPairs:
 base=b.get(baseId,{}); up=b.get(upId,{})
 if base.get("cost",{}).get("gold")!=baseGold or up.get("cost",{}).get("gold")!=upGold: dwellingErrors.append([baseId,upId,"gold-cost",base.get("cost",{}).get("gold"),up.get("cost",{}).get("gold"),baseGold,upGold])
 if up.get("upgrades")!=baseId: dwellingErrors.append([upId,"upgrade-target",up.get("upgrades"),baseId])
 if baseGold<=lastBaseGold: dwellingErrors.append([baseId,"base-tier-gold-not-increasing",baseGold,lastBaseGold])
 if upGold<baseGold: dwellingErrors.append([upId,"upgrade-cheaper-than-base",upGold,baseGold])
 lastBaseGold=baseGold
# High-tier gates are intentional pacing anchors.
if b.get("sanguinePalace",{}).get("requires")!=["allOf",["scarletLodge"],["cityHall"],["mageGuild2"]]: dwellingErrors.append(["sanguinePalace","gate-drift"])
if b.get("heartAviary",{}).get("requires")!=["allOf",["sanguinePalace"],["castle"],["mageGuild3"]]: dwellingErrors.append(["heartAviary","gate-drift"])
ck("dwellingProgressionSnapshot",not dwellingErrors,dwellingErrors)

# Fortification progression is combat-critical and must remain monotonic.
fortErrors=[]
expectedFort={
 "fort":{"wallsHealth":2,"citadelHealth":0,"upperTowerHealth":0,"lowerTowerHealth":0,"hasMoat":False},
 "citadel":{"wallsHealth":2,"citadelHealth":2,"upperTowerHealth":0,"lowerTowerHealth":0,"hasMoat":True,"citadelShooter":"bloodstalker"},
 "castle":{"wallsHealth":3,"citadelHealth":2,"upperTowerHealth":2,"lowerTowerHealth":2,"hasMoat":True,"citadelShooter":"bloodstalker","upperTowerShooter":"bloodstalker","lowerTowerShooter":"bloodstalker"},
}
for bid,exp in expectedFort.items():
 actual=b.get(bid,{}).get("fortifications") or {}
 if actual!=exp: fortErrors.append([bid,actual,exp])
if b.get("citadel",{}).get("upgrades")!="fort" or b.get("castle",{}).get("upgrades")!="citadel": fortErrors.append(["fort-upgrade-chain"])
# Every configured tower shooter must resolve to the town's intended ranged unit.
for bid in ("citadel","castle"):
 for k,v in (b.get(bid,{}).get("fortifications") or {}).items():
  if k.endswith("Shooter") and v!="bloodstalker": fortErrors.append([bid,k,v])
ck("fortificationProgressionSnapshot",not fortErrors,fortErrors)

# Town presentation coordinates are runtime-sensitive: require complete,
# nonnegative clickable structures and exact top-level presentation anchors.
presentationErrors=[]
structures=town.get("structures") or {}
if set(structures)!=set(b): presentationErrors.append(["structure-building-membership",sorted(set(structures)^set(b))])
for sid,node in structures.items():
 for field in ("animation","border","area"):
  if not isinstance(node.get(field),str) or not node.get(field): presentationErrors.append([sid,"missing-"+field])
 for field in ("x","y","z"):
  if not isinstance(node.get(field),int): presentationErrors.append([sid,"invalid-"+field,node.get(field)])
 if isinstance(node.get("x"),int) and node["x"]<0: presentationErrors.append([sid,"negative-x",node["x"]])
 if isinstance(node.get("y"),int) and node["y"]<0: presentationErrors.append([sid,"negative-y",node["y"]])
if town.get("musicTheme")!=["CRIMSON/MUSIC/crimson_court.ogg"]: presentationErrors.append(["musicTheme",town.get("musicTheme")])
if town.get("moatAbility")!="core:spell.castleMoat": presentationErrors.append(["moatAbility",town.get("moatAbility")])
if town.get("primaryResource")!="crystal" or town.get("mageGuild")!=5: presentationErrors.append(["town-resource-guild",town.get("primaryResource"),town.get("mageGuild")])
if town.get("defaultTavern")!=5 or town.get("tavern")!={"bloodlord":100,"sanguineSeer":100}: presentationErrors.append(["town-tavern",town.get("defaultTavern"),town.get("tavern")])
ck("townPresentationStructureContract",not presentationErrors,presentationErrors)

# Creature upgrade balance regression: every base->upgrade pair must remain a
# strict combat improvement without silently reducing core values.
creatureUpgradeErrors=[]
for baseId,base in cr.items():
 for upId in base.get("upgrades",[]) or []:
  up=cr.get(upId)
  if not up: continue
  for field in ["attack","defense","hitPoints","speed","fightValue","aiValue"]:
   bv=base.get(field); uv=up.get(field)
   if isinstance(bv,(int,float)) and isinstance(uv,(int,float)) and uv<bv:
    creatureUpgradeErrors.append([baseId,upId,field,bv,uv])
  bd=base.get("damage") or {}; ud=up.get("damage") or {}
  for field in ["min","max"]:
   if isinstance(bd.get(field),(int,float)) and isinstance(ud.get(field),(int,float)) and ud[field]<bd[field]:
    creatureUpgradeErrors.append([baseId,upId,"damage."+field,bd[field],ud[field]])
  if up.get("growth")!=base.get("growth"):
   creatureUpgradeErrors.append([baseId,upId,"growth",base.get("growth"),up.get("growth")])
  if up.get("fightValue")!=up.get("aiValue"):
   creatureUpgradeErrors.append([upId,"fightValue-aiValue",up.get("fightValue"),up.get("aiValue")])
ck("creatureUpgradeProgression",not creatureUpgradeErrors,creatureUpgradeErrors)

# v0.1 activation safety and ranged/flying identity are explicit contracts.
creatureActivationErrors=[]
expectedShooters={"scarletHuntress":12,"bloodstalker":16}
expectedFlyers={"gorewing","bloodwing","bloodPhoenix","eternalBloodPhoenix"}
for cid,x in cr.items():
 if x.get("special") is not True: creatureActivationErrors.append([cid,"must-remain-special-before-G3/G4"])
 abilities=x.get("abilities") or {}
 isShooter="shooter" in abilities
 if (cid in expectedShooters)!=isShooter: creatureActivationErrors.append([cid,"shooter-contract",isShooter])
 if cid in expectedShooters and x.get("shots")!=expectedShooters[cid]: creatureActivationErrors.append([cid,"shots",x.get("shots"),expectedShooters[cid]])
 if cid not in expectedShooters and x.get("shots") not in (None,0): creatureActivationErrors.append([cid,"unexpected-shots",x.get("shots")])
 isFlyer="canFly" in abilities
 if (cid in expectedFlyers)!=isFlyer: creatureActivationErrors.append([cid,"flying-contract",isFlyer])
ck("creatureActivationAndRoleContract",not creatureActivationErrors,creatureActivationErrors)

# Ability topology is a gameplay-facing contract: custom triggers must stay on
# the intended creatures and native spellcaster/rebirth/aura parameters must
# not drift silently.
abilityErrors=[]
expectedCustom={
 "bloodbound":{"bloodied":"crimsonBloodied"},
 "crimsonDancer":{"crimsonGrace":"crimsonDancerGrace","bloodied":"crimsonBloodied"},
 "bloodwing":{"bloodFeast":"crimsonBloodwingDrain","bloodied":"crimsonBloodied"},
 "veinOracle":{"bloodied":"crimsonBloodied"},
 "bloodstalker":{"bloodied":"crimsonBloodied","quarryMark":"crimsonQuarryMark"},
 "crimsonArchon":{"bloodied":"crimsonBloodied"},
 "eternalBloodPhoenix":{"bloodied":"crimsonBloodied"},
}
for cid,x in cr.items():
 abilities=x.get("abilities") or {}
 actual={k:v.get("subtype") for k,v in abilities.items() if isinstance(v,dict) and v.get("type")=="COMBAT_EVENT_TRIGGER" and str(v.get("subtype","")).startswith("crimson")}
 if actual!=expectedCustom.get(cid,{}): abilityErrors.append([cid,"custom-trigger-topology",actual,expectedCustom.get(cid,{})])
# Lock the current native contracts that materially define T4/T6/T7 roles.
hemo=cr["hemomancer"]["abilities"]; oracle=cr["veinOracle"]["abilities"]; arch=cr["crimsonArchon"]["abilities"]; phoenix=cr["eternalBloodPhoenix"]["abilities"]
if (hemo.get("castsWeakness",{}).get("subtype"),hemo.get("castsWeakness",{}).get("val"),hemo.get("castsCount",{}).get("val"),hemo.get("castLength",{}).get("val"))!=("weakness",1,2,2): abilityErrors.append(["hemomancer","spellcaster-contract"])
if (oracle.get("castsWeakness",{}).get("val"),oracle.get("castsStoneSkin",{}).get("subtype"),oracle.get("castsStoneSkin",{}).get("val"),oracle.get("castsCount",{}).get("val"),oracle.get("castLength",{}).get("val"))!=(2,"stoneSkin",1,3,3): abilityErrors.append(["veinOracle","spellcaster-contract"])
if (arch.get("crimsonPresence",{}).get("type"),arch.get("crimsonPresence",{}).get("subtype"),arch.get("crimsonPresence",{}).get("val"))!=("PRIMARY_SKILL","defence",1): abilityErrors.append(["crimsonArchon","presence-contract"])
if (phoenix.get("eternalRebirth",{}).get("subtype"),phoenix.get("eternalRebirth",{}).get("val"),phoenix.get("eternalRebirth",{}).get("addInfo",{}).get("guaranteed"))!=("rebirth",20,True): abilityErrors.append(["eternalBloodPhoenix","rebirth-contract"])
ck("creatureAbilityTopology",not abilityErrors,abilityErrors)

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

# Lock the exact v0.1 spell surface so generation status cannot drift silently.
sc=spellContract
cp=sc.get("counterplay",{})
br=sc.get("bloodRites",{})
expectedNative=set(cp.get("activeNative",[])); expectedCustom=set(cp.get("activeCustomBridge",[])); expectedReserved=set(cp.get("reservedDisabled",[]))
actualActive={sid for sid,s in counterplay.items() if s.get("defaultGainChance",0)>0}
actualReserved={sid for sid,s in counterplay.items() if s.get("defaultGainChance")==0}
customIds=set()
for sid,s in counterplay.items():
 for lvlDoc in (s.get("levels") or {}).values():
  for e in (lvlDoc.get("effects") or {}).values():
   if isinstance(e,dict) and e.get("type")==f"shattered-realms:{cp.get('customEffect')}": customIds.add(sid)
spellSnapshotErrors=[]
if actualActive != expectedNative|expectedCustom: spellSnapshotErrors.append(["active",sorted(actualActive),sorted(expectedNative|expectedCustom)])
if actualReserved != expectedReserved: spellSnapshotErrors.append(["reserved",sorted(actualReserved),sorted(expectedReserved)])
if customIds != expectedCustom: spellSnapshotErrors.append(["customBridge",sorted(customIds),sorted(expectedCustom)])
if set(counterplay) != expectedNative|expectedCustom|expectedReserved: spellSnapshotErrors.append(["counterplayMembership",sorted(counterplay)])
if set(rites) != set(br.get("ids",[])): spellSnapshotErrors.append(["bloodRiteMembership",sorted(rites),sorted(br.get("ids",[]))])
for sid in actualActive:
 s=counterplay[sid]
 if s.get("defaultGainChance")!=cp.get("activeDefaultGainChance"): spellSnapshotErrors.append([sid,"activeChance",s.get("defaultGainChance")])
for sid in actualReserved:
 if counterplay[sid].get("defaultGainChance")!=cp.get("reservedDefaultGainChance"): spellSnapshotErrors.append([sid,"reservedChance"])
ck("spellActivationSnapshot",not spellSnapshotErrors,spellSnapshotErrors)

# Spell text must remain truthful to the implementation class recorded by the
# activation snapshot. Native spells may not contain custom Shattered effects;
# bridge spells must contain the declared custom effect on every mastery level.
spellEffectClassErrors=[]
for sid in sorted(expectedNative):
 for lvl,lvlDoc in (counterplay.get(sid,{}).get("levels") or {}).items():
  custom=[e.get("type") for e in (lvlDoc.get("effects") or {}).values() if isinstance(e,dict) and isinstance(e.get("type"),str) and e.get("type").startswith("shattered-realms:")]
  if custom: spellEffectClassErrors.append([sid,lvl,"native-has-custom",custom])
for sid in sorted(expectedCustom):
 for lvl,lvlDoc in (counterplay.get(sid,{}).get("levels") or {}).items():
  types=[e.get("type") for e in (lvlDoc.get("effects") or {}).values() if isinstance(e,dict)]
  if f"shattered-realms:{cp.get('customEffect')}" not in types: spellEffectClassErrors.append([sid,lvl,"bridge-effect-missing",types])
ck("spellImplementationClassContract",not spellEffectClassErrors,spellEffectClassErrors)

# Active universal spells must be complete VCMI spell records, not merely IDs with
# generation chances. Lock mastery coverage, one school, graphics, target/flags and
# non-empty executable effects at every mastery.
spellShapeErrors=[]
requiredLevels={"none","basic","advanced","expert"}
requiredGraphics={"iconBook","iconScroll","iconEffect","iconImmune","iconScenarioBonus"}
for sid in sorted(actualActive):
 s=counterplay[sid]
 levels=s.get("levels") or {}
 if set(levels)!=requiredLevels: spellShapeErrors.append([sid,"levels",sorted(levels)])
 schools=[k for k,v in (s.get("school") or {}).items() if v is True]
 schoolContract=cp.get("schoolContract",{})
 minSchools=schoolContract.get("minimumActiveSchools",1)
 exceptions=schoolContract.get("multiSchoolExceptions",{})
 expectedSchools=exceptions.get(sid)
 if len(schools)<minSchools: spellShapeErrors.append([sid,"school",schools])
 elif expectedSchools is not None and sorted(schools)!=sorted(expectedSchools): spellShapeErrors.append([sid,"schoolException",schools,expectedSchools])
 elif expectedSchools is None and len(schools)!=1: spellShapeErrors.append([sid,"unexpectedMultiSchool",schools])
 if s.get("type")!="combat": spellShapeErrors.append([sid,"type",s.get("type")])
 if s.get("targetType")!="CREATURE": spellShapeErrors.append([sid,"targetType",s.get("targetType")])
 flags=s.get("flags") or {}
 if sum(v is True for v in flags.values())!=1: spellShapeErrors.append([sid,"flags",flags])
 graphics=s.get("graphics") or {}
 if not requiredGraphics.issubset(graphics) or any(not isinstance(graphics.get(k),str) or not graphics.get(k) for k in requiredGraphics): spellShapeErrors.append([sid,"graphics"])
 for lvl in requiredLevels:
  d=levels.get(lvl,{})
  if not isinstance(d.get("cost"),int) or d.get("cost")<0: spellShapeErrors.append([sid,lvl,"cost",d.get("cost")])
  if not isinstance(d.get("description"),str) or not d.get("description").strip(): spellShapeErrors.append([sid,lvl,"description"])
  if not isinstance(d.get("effects"),dict) or not d.get("effects"): spellShapeErrors.append([sid,lvl,"effects"])
ck("activeSpellRecordShape",not spellShapeErrors,spellShapeErrors)

# Lock user-visible spell identity: level, school assignment and polarity are
# balance-facing API and must change only through an intentional snapshot update.
spellIdentityErrors=[]
shapeContract=cp.get("activeShape",{})
if set(shapeContract)!=actualActive: spellIdentityErrors.append(["membership",sorted(shapeContract),sorted(actualActive)])
for sid in sorted(actualActive):
 s=counterplay[sid]; exp=shapeContract.get(sid,{})
 schools=sorted(k for k,v in (s.get("school") or {}).items() if v is True)
 flags=sorted(k for k,v in (s.get("flags") or {}).items() if v is True)
 if s.get("level")!=exp.get("level"): spellIdentityErrors.append([sid,"level",s.get("level"),exp.get("level")])
 if schools!=sorted(exp.get("schools",[])): spellIdentityErrors.append([sid,"schools",schools,exp.get("schools")])
 if flags!=[exp.get("flag")]: spellIdentityErrors.append([sid,"polarity",flags,exp.get("flag")])
ck("activeSpellIdentitySnapshot",not spellIdentityErrors,spellIdentityErrors)

# Mastery must not become cheaper and native numeric effects must not silently
# weaken as skill mastery increases. This is a conservative balance regression
# guard; intentional non-monotonic designs should use a custom-effect contract.
spellProgressionErrors=[]
levelOrder=["none","basic","advanced","expert"]
for sid in sorted(actualActive):
 s=counterplay[sid]; lv=s.get("levels") or {}
 costs=[lv.get(k,{}).get("cost") for k in levelOrder]
 if all(isinstance(x,int) for x in costs) and any(costs[i]>costs[i+1] for i in range(3)): spellProgressionErrors.append([sid,"cost-regression",costs])
 if sid in expectedNative:
  signatures={}
  for mastery in levelOrder:
   for key,e in (lv.get(mastery,{}).get("effects") or {}).items():
    if not isinstance(e,dict) or not isinstance(e.get("val"),(int,float)): continue
    sig=(key,e.get("type"),e.get("subtype"))
    signatures.setdefault(sig,[]).append(e.get("val"))
  for sig,vals in signatures.items():
   if len(vals)!=4: continue
   # Effects should not move toward zero at higher mastery.
   mags=[abs(v) for v in vals]
   if any(mags[i]>mags[i+1] for i in range(3)): spellProgressionErrors.append([sid,"effect-regression",list(sig),vals])
ck("activeSpellMasteryProgression",not spellProgressionErrors,spellProgressionErrors)

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

# Spell-effect registry entries must themselves be executable and their Lua sources
# must exist. This mirrors the combat-script closure instead of trusting a name match.
spellEffectDefs=spellEffects.get("scripts",{}) if isinstance(spellEffects,dict) else {}
badSpellEffectDefs=[]
for sid,s in spellEffectDefs.items():
 if s.get("implements")!="spellEffect": badSpellEffectDefs.append([sid,"implements",s.get("implements")])
 if not isinstance(s.get("script"),str) or not s.get("script"): badSpellEffectDefs.append([sid,"script"])
 if not isinstance(s.get("patches"),list): badSpellEffectDefs.append([sid,"patches"])
 if not isinstance(s.get("schema"),dict): badSpellEffectDefs.append([sid,"schema"])
 scriptfile=ROOT/"shattered-realms/Content/scripts"/(str(s.get("script",""))+".lua")
 if not scriptfile.is_file() or scriptfile.stat().st_size<=0: badSpellEffectDefs.append([sid,"lua",str(scriptfile.relative_to(ROOT))])
ck("spellEffectDefinitions",not badSpellEffectDefs,badSpellEffectDefs)

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
