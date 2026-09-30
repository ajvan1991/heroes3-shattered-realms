#!/usr/bin/env python3
"""Verify generated Crimson candidate packaging without launching VCMI."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/"build/crimson-v01-candidate"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
errors=[]
def safe_rel(v):
 if not isinstance(v,str) or not v or "\x00" in v or "\\" in v: return False
 # Resource/config paths are canonical POSIX-relative paths even when QA runs on Linux.
 if v.startswith("/") or v.startswith("//") or re.match(r"^[A-Za-z]:",v): return False
 parts=v.split("/")
 return all(part not in {"","..","."} for part in parts)
def ck(ok,msg):
 if not ok: errors.append(msg)
if not C.is_dir(): raise SystemExit("Candidate missing; run build_crimson_candidate.py first.")
mod=load(C/"mod.json")
expected={"factions":"config/factions.json","heroClasses":"config/heroClasses.json","heroes":"config/heroes.json","creatures":"config/creatures.json","skills":"config/skills.json","scripts":"config/combatScripts.json"}
for k,v in expected.items(): ck(mod.get(k)==[v],f"registration {k}: expected {[v]!r}, got {mod.get(k)!r}")
for k,v in expected.items():
 p=C/"Content"/v
 ck(p.is_file() and p.stat().st_size>0,f"registered config missing/empty for {k}: {v}")
# Production-style registration paths must stay relative and inside Content.
unsafeRegs=[]
for k,v in expected.items():
 if not safe_rel(v): unsafeRegs.append([k,v])
ck(not unsafeRegs,f"unsafe registration paths: {unsafeRegs}")
ck(not any(".staging." in str(x) for v in mod.values() for x in (v if isinstance(v,list) else [v])),"mod.json contains staging registration")
skills=load(C/"Content/config/skills.json")
ck(set(skills)=={"bloodCommand","crimsonDivination"},f"candidate skill surface leaked: {sorted(skills)}")
scripts=load(C/"Content/config/combatScripts.json").get("scripts",{})
for sid,s in scripts.items():
 sp=str(s.get("script",""))
 ck(safe_rel(sp),f"unsafe Lua script path for {sid}: {sp}")
 if safe_rel(sp):
  p=C/"Content/scripts"/(sp+".lua"); ck(p.is_file() and p.stat().st_size>0,f"missing Lua source for {sid}: {p}")
# Re-scan generated config independently so report counters cannot hide omissions.
exts=(".png",".def",".wav",".ogg",".pcx",".bmp",".webm",".mp3")
actualRefs=set(); unsafeMediaRefs=[]
def walk(v):
 if isinstance(v,str) and v.lower().endswith(exts):
  actualRefs.add(v)
  if not safe_rel(v): unsafeMediaRefs.append(v)
 elif isinstance(v,dict):
  for x in v.values(): walk(x)
 elif isinstance(v,list):
  for x in v: walk(x)
for p in (C/"Content/config").glob("*.json"): walk(load(p))
ck(not unsafeMediaRefs,f"unsafe media references: {sorted(set(unsafeMediaRefs))}")
actualMissing=sorted(r for r in actualRefs if not (C/"Content"/r).is_file() or (C/"Content"/r).stat().st_size==0)
report=load(C/"candidate-report.json")
manifest=load(C/"candidate-manifest.json")
# Reject path traversal / absolute paths before trusting package inventory.
unsafeManifest=[]
for x in manifest.get("files",[]):
 if not safe_rel(str(x.get("path",""))): unsafeManifest.append(x.get("path"))
ck(not unsafeManifest,f"unsafe candidate manifest paths: {unsafeManifest}")
manifestBad=[]
for x in manifest.get("files",[]):
 p=C/x["path"]
 if not p.is_file(): manifestBad.append([x["path"],"missing"]); continue
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 if p.stat().st_size!=x["bytes"] or h!=x["sha256"]: manifestBad.append([x["path"],"hash-or-size"])
ck(not manifestBad,f"candidate manifest mismatch: {manifestBad}")
ck(manifest.get("fileCount")==len(manifest.get("files",[])),"candidate manifest fileCount mismatch")
ck(report.get("manifestFiles")==manifest.get("fileCount"),"candidate report manifest count mismatch")
actualFiles=sorted(p.relative_to(C).as_posix() for p in C.rglob("*") if p.is_file() and p.name not in {"candidate-report.json","candidate-manifest.json"})
manifestFiles=sorted(str(x.get("path","")) for x in manifest.get("files",[]))
ck(len(manifestFiles)==len(set(manifestFiles)),"candidate manifest contains duplicate paths")
ck(actualFiles==manifestFiles,f"candidate manifest inventory mismatch: actual={len(actualFiles)} manifest={len(manifestFiles)}")
ck(report.get("directMediaReferences")==len(actualRefs),"candidate report direct-media count mismatch")
ck(report.get("missingDirectMedia")==len(actualMissing),"candidate report missing-media count mismatch")
ck(report.get("missing")==actualMissing,"candidate report direct missing list mismatch")
ck(report.get("registeredSkills")==["bloodCommand","crimsonDivination"],"candidate report skill list mismatch")
# Prefix-derived resources are independently reconstructed from generated faction data.
fac=load(C/"Content/config/factions.json")["crimsonCourt"]
siegePrefix=fac["town"]["siege"]["imagePrefix"]
suffixes=["BACK","TW21","TW22","TW2C","MAN1","MAN2","MANC","TW11","TW12","TW1C","DRW1","DRW2","DRW3","ARCH","WA61","WA62","WA63","WA41","WA42","WA43","WA31","WA32","WA33","WA11","WA12","WA13","MOAT","MLIP","WA2","WA5","TPWL"]
derivedSiege=[siegePrefix+s+".png" for s in suffixes]
puzzlePrefix=fac["puzzleMap"]["prefix"]
derivedPuzzle=[puzzlePrefix+f"{i:02d}.png" for i in range(48)]
actualMissingSiege=[r for r in derivedSiege if not (C/"Content"/r).is_file() or (C/"Content"/r).stat().st_size==0]
actualMissingPuzzle=[r for r in derivedPuzzle if not (C/"Content"/r).is_file() or (C/"Content"/r).stat().st_size==0]
ck(report.get("derivedSiegeReferences")==31,"candidate report siege reference count mismatch")
ck(report.get("missingDerivedSiege")==len(actualMissingSiege),"candidate report siege missing count mismatch")
ck(report.get("missingDerived")==actualMissingSiege,"candidate report siege missing list mismatch")
ck(report.get("derivedPuzzleReferences")==48,"candidate report puzzle reference count mismatch")
ck(report.get("missingDerivedPuzzle")==len(actualMissingPuzzle),"candidate report puzzle missing count mismatch")
ck(report.get("missingPuzzle")==actualMissingPuzzle,"candidate report puzzle missing list mismatch")
computedRuntimeReady=not actualMissing and not actualMissingSiege and not actualMissingPuzzle
ck(report.get("runtimeReady") is computedRuntimeReady,f"runtimeReady mismatch: report={report.get('runtimeReady')} computed={computedRuntimeReady}")
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
