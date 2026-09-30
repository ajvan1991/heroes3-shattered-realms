#!/usr/bin/env python3
"""Verify generated Crimson candidate packaging without launching VCMI."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/"build/crimson-v01-candidate"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
errors=[]
def ck(ok,msg):
 if not ok: errors.append(msg)
if not C.is_dir(): raise SystemExit("Candidate missing; run build_crimson_candidate.py first.")
mod=load(C/"mod.json")
expected={"factions":"config/factions.json","heroClasses":"config/heroClasses.json","heroes":"config/heroes.json","creatures":"config/creatures.json","skills":"config/skills.json","scripts":"config/combatScripts.json"}
for k,v in expected.items(): ck(mod.get(k)==[v],f"registration {k}: expected {[v]!r}, got {mod.get(k)!r}")
ck(not any(".staging." in str(x) for v in mod.values() for x in (v if isinstance(v,list) else [v])),"mod.json contains staging registration")
skills=load(C/"Content/config/skills.json")
ck(set(skills)=={"bloodCommand","crimsonDivination"},f"candidate skill surface leaked: {sorted(skills)}")
scripts=load(C/"Content/config/combatScripts.json").get("scripts",{})
for sid,s in scripts.items():
 p=C/"Content/scripts"/(s["script"]+".lua"); ck(p.is_file() and p.stat().st_size>0,f"missing Lua source for {sid}: {p}")
report=load(C/"candidate-report.json")
ck(report.get("registeredSkills")==["bloodCommand","crimsonDivination"],"candidate report skill list mismatch")
if report.get("runtimeReady"):
 ck(report.get("missingDirectMedia")==0,"runtimeReady with missing direct media")
 ck(report.get("missingDerivedSiege")==0,"runtimeReady with missing derived siege")
 ck(report.get("copiedMediaFiles")==report.get("directMediaReferences"),"runtimeReady direct media copy mismatch")
 ck(report.get("copiedDerivedSiegeFiles")==report.get("derivedSiegeReferences")==31,"runtimeReady siege copy mismatch")
 ck(report.get("missingDerivedPuzzle")==0,"runtimeReady with missing puzzle-map pieces")
 ck(report.get("copiedDerivedPuzzleFiles")==report.get("derivedPuzzleReferences")==48,"runtimeReady puzzle copy mismatch")
out={"pass":not errors,"errors":errors,"runtimeReady":report.get("runtimeReady",False),"registeredSkills":sorted(skills),"registeredScripts":sorted(scripts)}
print(json.dumps(out,indent=2))
sys.exit(0 if not errors else 1)
