#!/usr/bin/env python3
"""Build an isolated Crimson activation candidate without touching production mod.json.

Generated output is intentionally ignored as release truth until local VCMI validation.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"shattered-realms"
CFG=SRC/"Content/config/shattered-realms"
OUT=ROOT/"build/crimson-v01-candidate"
FILES={
 "factions":CFG/"crimson/faction.staging.json",
 "heroClasses":CFG/"crimson/heroClasses.staging.json",
 "heroes":CFG/"crimson/heroes.staging.json",
 "creatures":CFG/"crimson/creatures.staging.json",
}
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def safe_rel(v):
 if not isinstance(v,str) or not v or "\\x00" in v or "\\\\" in v: return False
 if v.startswith("/") or v.startswith("//") or re.match(r"^[A-Za-z]:",v): return False
 return all(part not in {"","..","."} for part in v.split("/"))
def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+"\n",encoding="utf-8")

ap=argparse.ArgumentParser()
ap.add_argument("--allow-missing-assets",action="store_true",help="Structural build only; candidate is not runtime-ready.")
args=ap.parse_args()

for validator in ("validate_crimson_staging.py","validate_reference_closure.py"):
 v=subprocess.run([sys.executable,str(ROOT/"tools"/validator)])
 if v.returncode: raise SystemExit(v.returncode)
# Candidate construction validates gate bookkeeping but must not depend on the
# transient assertion that G3/G4 are still blocked; the strict build is itself future G4 evidence.
v=subprocess.run([sys.executable,str(ROOT/"tools/validate_runtime_gates.py"),"--pre-build"])
 if v.returncode: raise SystemExit(v.returncode)

if OUT.exists(): shutil.rmtree(OUT)
(OUT/"Content/config").mkdir(parents=True)

# Stable production-style names; never register *.staging.json.
for category,src in FILES.items():
    dump(OUT/f"Content/config/{category}.json",load(src))

# Candidate skill surface is deliberately Crimson-only. Future faction passives remain
# in shared staging but must not leak into the first activation candidate.
allSkills=load(CFG/"skills/classPassives.staging.json")
crimsonSkillIds=("bloodCommand","crimsonDivination")
missingSkills=[k for k in crimsonSkillIds if k not in allSkills]
if missingSkills: raise SystemExit(f"FAIL: missing required Crimson skills: {missingSkills}")
candidateSkills={k:allSkills[k] for k in crimsonSkillIds}
dump(OUT/"Content/config/skills.json",candidateSkills)

# Combat scripts are copied as source data because creature event triggers need them.
reg=load(CFG/"scripts/combatScripts.staging.json")
# VCMI mod schema exposes `scripts` as a first-class content registration category.
dump(OUT/"Content/config/combatScripts.json",reg)
script_src=SRC/"Content/scripts/shattered-realms"
if not script_src.is_dir(): raise SystemExit("FAIL: Crimson script source directory is missing")
registeredScriptPaths=[]
for sid,s in reg.get("scripts",{}).items():
 sp=s.get("script")
 if not safe_rel(sp): raise SystemExit(f"FAIL: unsafe registered Lua script path for {sid}: {sp!r}")
 src=SRC/"Content/scripts"/(sp+".lua")
 if not src.is_file() or src.stat().st_size==0: raise SystemExit(f"FAIL: missing registered Lua source for {sid}: {sp}.lua")
 registeredScriptPaths.append(sp)
# Package only scripts that are actually registered. Prototype/unregistered Lua stays
# in source staging and cannot silently expand the activation candidate surface.
for sp in sorted(set(registeredScriptPaths)):
 src=SRC/"Content/scripts"/(sp+".lua")
 dst=OUT/"Content/scripts"/(sp+".lua")
 dst.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src,dst)

base=load(SRC/"mod.json")
base.update({
 "name":"Shattered Realms — Crimson v0.1 Candidate",
 "keepDisabled":True,
 "factions":["config/factions.json"],
 "heroClasses":["config/heroClasses.json"],
 "heroes":["config/heroes.json"],
 "creatures":["config/creatures.json"],
 "skills":["config/skills.json"],
 "scripts":["config/combatScripts.json"],
})
dump(OUT/"mod.json",base)

# Asset preflight: direct quoted media paths from candidate JSON.
# Materialize every source-owned media resource into the isolated candidate; a strict
# build is only runtime-ready when the output itself contains every direct reference.
exts=(".png",".def",".wav",".ogg",".pcx",".bmp",".webm",".mp3")
refs=set()
for p in (OUT/"Content/config").glob("*.json"):
    def walk(v):
        if isinstance(v,str) and v.lower().endswith(exts): refs.add(v)
        elif isinstance(v,dict):
            for x in v.values(): walk(x)
        elif isinstance(v,list):
            for x in v: walk(x)
    walk(load(p))
missing=[]; copied=[]
for r in sorted(refs):
    if not safe_rel(r): raise SystemExit(f"FAIL: unsafe media reference: {r!r}")
    src=SRC/"Content"/r
    if not src.is_file() or src.stat().st_size==0:
        missing.append(r); continue
    dst=OUT/"Content"/r
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst); copied.append(r)
# Fail closed against the generated output, not merely the source tree.
outputMissing=[r for r in sorted(refs) if not (OUT/"Content"/r).is_file() or (OUT/"Content"/r).stat().st_size==0]
if outputMissing != missing: raise SystemExit("FAIL: candidate media materialization mismatch")

# Siege assets are convention-derived from faction town.siege.imagePrefix and therefore
# invisible to direct quoted-media scanning. Materialize the full VCMI-required family.
faction=load(OUT/"Content/config/factions.json")["crimsonCourt"]
prefix=faction["town"]["siege"]["imagePrefix"]
if not safe_rel(prefix): raise SystemExit(f"FAIL: unsafe siege imagePrefix: {prefix!r}")
siegeSuffixes=["BACK","TW21","TW22","TW2C","MAN1","MAN2","MANC","TW11","TW12","TW1C","DRW1","DRW2","DRW3","ARCH","WA61","WA62","WA63","WA41","WA42","WA43","WA31","WA32","WA33","WA11","WA12","WA13","MOAT","MLIP","WA2","WA5","TPWL"]
derivedSiege=[prefix+s+".png" for s in siegeSuffixes]

# Puzzle-map pieces are also prefix-derived by VCMI: <prefix><index>.png.
puzzle=faction["puzzleMap"]; puzzlePrefix=puzzle["prefix"]
if not safe_rel(puzzlePrefix): raise SystemExit(f"FAIL: unsafe puzzle prefix: {puzzlePrefix!r}")
# CTownHandler uses the zero-based vector position, padded to two digits (00..47),
# while piece.index controls uncover order only.
derivedPuzzle=[puzzlePrefix+f"{i:02d}.png" for i in range(48)]
missingDerived=[]; copiedDerived=[]
for r in derivedSiege:
    if not safe_rel(r): raise SystemExit(f"FAIL: unsafe derived siege resource: {r!r}")
    src=SRC/"Content"/r
    if not src.is_file() or src.stat().st_size==0:
        missingDerived.append(r); continue
    dst=OUT/"Content"/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); copiedDerived.append(r)
missingPuzzle=[]; copiedPuzzle=[]
for r in derivedPuzzle:
    if not safe_rel(r): raise SystemExit(f"FAIL: unsafe derived puzzle resource: {r!r}")
    src=SRC/"Content"/r
    if not src.is_file() or src.stat().st_size==0:
        missingPuzzle.append(r); continue
    dst=OUT/"Content"/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); copiedPuzzle.append(r)


lua=list((OUT/"Content/scripts").rglob("*.lua"))
expectedLuaFiles={Path(sp+".lua").as_posix() for sp in registeredScriptPaths}
actualLuaFiles={p.relative_to(OUT/"Content/scripts").as_posix() for p in lua}
if actualLuaFiles != expectedLuaFiles:
 raise SystemExit(f"FAIL: candidate Lua surface mismatch: actual={sorted(actualLuaFiles)} expected={sorted(expectedLuaFiles)}")
copiedRegisteredLua=[]
for sp in registeredScriptPaths:
 p=OUT/"Content/scripts"/(sp+".lua")
 if not p.is_file() or p.stat().st_size==0: raise SystemExit(f"FAIL: registered Lua not materialized: {sp}.lua")
 copiedRegisteredLua.append(sp)

# Deterministic package inventory for reproducibility and later local-test evidence.
def sha256(p):
 h=hashlib.sha256()
 with p.open("rb") as fh:
  for chunk in iter(lambda:fh.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
inventory=[]
for p in sorted(x for x in OUT.rglob("*") if x.is_file() and x.name not in {"candidate-report.json","candidate-manifest.json"}):
 inventory.append({"path":p.relative_to(OUT).as_posix(),"bytes":p.stat().st_size,"sha256":sha256(p)})
dump(OUT/"candidate-manifest.json",{"format":1,"files":inventory,"fileCount":len(inventory),"totalBytes":sum(x["bytes"] for x in inventory)})
skillIds=sorted(load(OUT/"Content/config/skills.json").keys())
report={"candidate":str(OUT.relative_to(ROOT)),"registeredSkills":skillIds,"directMediaReferences":len(refs),"missingDirectMedia":len(missing),"missing":missing,"derivedSiegeReferences":len(derivedSiege),"missingDerivedSiege":len(missingDerived),"missingDerived":missingDerived,"derivedPuzzleReferences":len(derivedPuzzle),"missingDerivedPuzzle":len(missingPuzzle),"missingPuzzle":missingPuzzle,"registeredLuaScripts":len(registeredScriptPaths),"copiedRegisteredLuaScripts":len(copiedRegisteredLua),"copiedLuaFiles":len(lua),"manifestFiles":len(inventory),"copiedMediaFiles":len(copied),"copiedDerivedSiegeFiles":len(copiedDerived),"copiedDerivedPuzzleFiles":len(copiedPuzzle),"runtimeReady":not outputMissing and not missingDerived and not missingPuzzle}
dump(OUT/"candidate-report.json",report)
if (missing or missingDerived or missingPuzzle) and not args.allow_missing_assets:
    print(f"FAIL: {len(missing)} direct media and {len(missingDerived)} derived siege and {len(missingPuzzle)} puzzle resources are missing. Use --allow-missing-assets only for structural inspection.")
    raise SystemExit(2)
print(json.dumps({k:v for k,v in report.items() if k not in ("missing","missingDerived","missingPuzzle")},indent=2))
