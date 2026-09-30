#!/usr/bin/env python3
"""Recompute the committed Crimson structural reference-closure snapshot."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CFG=ROOT/"shattered-realms/Content/config/shattered-realms"
load=lambda p:json.loads(p.read_text(encoding="utf-8"))
fac=load(CFG/"crimson/faction.staging.json")["crimsonCourt"]; town=fac["town"]
b=load(CFG/"crimson/buildings.staging.json"); cr=load(CFG/"crimson/creatures.staging.json")
he=load(CFG/"crimson/heroes.staging.json"); hc=load(CFG/"crimson/heroClasses.staging.json")
scripts=load(CFG/"scripts/combatScripts.staging.json").get("scripts",{})
def reqrefs(v):
 out=[]
 if isinstance(v,str):
  if v not in {"allOf","anyOf","noneOf"}: out.append(v)
 elif isinstance(v,list):
  for x in v: out.extend(reqrefs(x))
 return out
requires=[r for x in b.values() for r in reqrefs(x.get("requires"))]
upgrades=[x["upgrades"] for x in b.values() if x.get("upgrades")]
townIds=[x for t in town["creatures"] for x in t]
army=[a["creature"] for h in he.values() for a in h.get("army",[])]
hall=[x for row in town["hallSlots"] for slot in row for x in slot]
events=[]
for x in cr.values():
 for a in (x.get("abilities") or {}).values():
  if isinstance(a,dict) and a.get("type")=="COMBAT_EVENT_TRIGGER" and a.get("subtype")!="rebirth": events.append(a.get("subtype"))
classRefs=[h.get("class") for h in he.values()]
spec=[h.get("specialty",{}).get("creature") for h in he.values() if h.get("specialty",{}).get("creature")]
checks={
 "buildingRequires":{"status":"PASS" if all(x in b for x in requires) else "FAIL","dangling":sum(x not in b for x in requires)},
 "buildingUpgrades":{"status":"PASS" if all(x in b for x in upgrades) else "FAIL","dangling":sum(x not in b for x in upgrades)},
 "townCreatureIds":{"status":"PASS" if all(x in cr for x in townIds) else "FAIL","dangling":sum(x not in cr for x in townIds)},
 "heroArmyCreatureIds":{"status":"PASS" if all(x in cr for x in army) else "FAIL","dangling":sum(x not in cr for x in army)},
 "hallBuildingIds":{"status":"PASS" if all(x in b for x in hall) else "FAIL","dangling":sum(x not in b for x in hall)},
 "buildingStructureCoverage":{"status":"PASS" if set(b)<=set(town["structures"]) else "FAIL","missing":len(set(b)-set(town["structures"]))},
 "combatEventScriptSubtypes":{"status":"PASS" if all(x in scripts for x in events) else "FAIL","references":len(events),"uniqueRegisteredScripts":len(set(events)),"dangling":sum(x not in scripts for x in events)},
 "heroClassIds":{"status":"PASS" if all(x in hc for x in classRefs) else "FAIL","references":len(classRefs),"dangling":sum(x not in hc for x in classRefs)},
 "heroCreatureSpecialties":{"status":"PASS" if all(x in cr for x in spec) else "FAIL","references":len(spec),"dangling":sum(x not in cr for x in spec)},
 "tavernClassLinks":{
  "status":"PASS" if all(hc.get(cid,{}).get("faction")=="crimsonCourt" and hc.get(cid,{}).get("defaultTavern")==5 and hc.get(cid,{}).get("tavern",{}).get("crimsonCourt")==100 for cid in ("bloodlord","sanguineSeer")) else "FAIL",
  "bloodlord":hc.get("bloodlord",{}).get("tavern",{}).get("crimsonCourt",0) if hc.get("bloodlord",{}).get("faction")=="crimsonCourt" else 0,
  "sanguineSeer":hc.get("sanguineSeer",{}).get("tavern",{}).get("crimsonCourt",0) if hc.get("sanguineSeer",{}).get("faction")=="crimsonCourt" else 0
 }
}
expected=load(ROOT/"production/crimson-reference-closure.v0.1.json")
snapshot={"buildings":len(b),"creatures":len(cr),"heroes":len(he),"townCreatureTiers":len(town["creatures"]),"hallRows":len(town["hallSlots"]),"townStructures":len(town["structures"])}
errors=[]
if snapshot!=expected.get("snapshot"): errors.append(["snapshot",snapshot,expected.get("snapshot")])
if checks!=expected.get("checks"): errors.append(["checks",checks,expected.get("checks")])
if any(v["status"]!="PASS" for v in checks.values()): errors.append(["closure","one-or-more checks failed"])
if expected.get("result")!="STRUCTURALLY_CLOSED": errors.append(["snapshot-result",expected.get("result")])
requiredLimitations={
 "Does not validate referenced media files.",
 "Does not prove VCMI 1.7.5 runtime behavior.",
 "Does not activate staging.",
 "Does not validate custom Lua semantics beyond separate audits."
}
if set(expected.get("limitations",[]))!=requiredLimitations: errors.append(["limitations",expected.get("limitations")])
print(json.dumps({"pass":not errors,"snapshot":snapshot,"checks":checks,"errors":errors},indent=2))
sys.exit(1 if errors else 0)
