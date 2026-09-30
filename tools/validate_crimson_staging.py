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
 "mod":ROOT/"shattered-realms/mod.json",
}
load=lambda p: json.loads(p.read_text(encoding="utf-8"))
D={k:load(v) for k,v in P.items()}
fac=D["faction"]["crimsonCourt"]; town=fac["town"]; b=D["buildings"]; cr=D["creatures"]; hc=D["classes"]; he=D["heroes"]; scripts=D["scripts"].get("scripts",{})
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

hall=[x for row in town.get("hallSlots",[]) for slot in row for x in slot]
ck("hallReferences",all(x in b for x in hall),[x for x in hall if x not in b])
tiers=[x for tier in town.get("creatures",[]) for x in tier]
ck("townCreatureReferences",all(x in cr for x in tiers),[x for x in tiers if x not in cr])

badclass=[]; badarmy=[]; badspec=[]
for i,h in he.items():
    if h.get("class") not in hc: badclass.append([i,h.get("class")])
    for a in h.get("army",[]):
        if a.get("creature") not in cr: badarmy.append([i,a.get("creature")])
    s=h.get("specialty",{})
    if isinstance(s,dict) and s.get("creature") and s["creature"] not in cr: badspec.append([i,s["creature"]])
ck("heroClassReferences",not badclass,badclass)
ck("heroArmyReferences",not badarmy,badarmy)
ck("heroCreatureSpecialties",not badspec,badspec)

badscript=[]
for i,c in cr.items():
    for a in (c.get("abilities") or {}).values():
        if isinstance(a,dict) and a.get("type")=="COMBAT_EVENT_TRIGGER":
            sub=a.get("subtype")
            if sub!="rebirth" and sub not in scripts: badscript.append([i,sub])
ck("combatScriptReferences",not badscript,badscript)

# Production manifest must remain inert until activation is explicitly approved.
game_keys={"factions","heroClasses","heroes","skills","creatures","artifacts","objects","spells","terrains","roads","rivers","battlefields","obstacles","mapLayers","templates","scripts"}
active=sorted(game_keys & set(D["mod"]))
ck("productionModInert",not active,active)

report={"result":"PASS" if not errors else "FAIL","checks":checks,"errors":errors}
out=ROOT/"production/crimson-static-validation.latest.json"
out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
