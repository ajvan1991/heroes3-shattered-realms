#!/usr/bin/env python3
"""Build an isolated Crimson activation candidate without touching production mod.json.

Generated output is intentionally ignored as release truth until local VCMI validation.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
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
def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+"\n",encoding="utf-8")

ap=argparse.ArgumentParser()
ap.add_argument("--allow-missing-assets",action="store_true",help="Structural build only; candidate is not runtime-ready.")
args=ap.parse_args()

v=subprocess.run([sys.executable,str(ROOT/"tools/validate_crimson_staging.py")])
if v.returncode: raise SystemExit(v.returncode)

if OUT.exists(): shutil.rmtree(OUT)
(OUT/"Content/config").mkdir(parents=True)

# Stable production-style names; never register *.staging.json.
for category,src in FILES.items():
    dump(OUT/f"Content/config/{category}.json",load(src))

# Combat scripts are copied as source data because creature event triggers need them.
reg=load(CFG/"scripts/combatScripts.staging.json")
dump(OUT/"Content/config/combatScripts.json",reg)
script_src=SRC/"Content/scripts/shattered-realms"
if script_src.exists(): shutil.copytree(script_src,OUT/"Content/scripts/shattered-realms")

base=load(SRC/"mod.json")
base.update({
 "name":"Shattered Realms — Crimson v0.1 Candidate",
 "keepDisabled":True,
 "factions":["config/factions.json"],
 "heroClasses":["config/heroClasses.json"],
 "heroes":["config/heroes.json"],
 "creatures":["config/creatures.json"],
})
dump(OUT/"mod.json",base)

# Asset preflight: direct quoted media paths from candidate JSON.
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
missing=[]
for r in sorted(refs):
    # VCMI resource lookup is richer than filesystem lookup; this is a conservative local preflight.
    if not any((SRC/"Content"/r).exists() for _ in [0]): missing.append(r)

report={"candidate":str(OUT.relative_to(ROOT)),"directMediaReferences":len(refs),"missingDirectMedia":len(missing),"missing":missing,"runtimeReady":not missing}
dump(OUT/"candidate-report.json",report)
if missing and not args.allow_missing_assets:
    print(f"FAIL: {len(missing)} direct media resources are missing. Use --allow-missing-assets only for structural inspection.")
    raise SystemExit(2)
print(json.dumps({k:v for k,v in report.items() if k!="missing"},indent=2))
