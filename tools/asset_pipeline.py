#!/usr/bin/env python3
"""Shattered Realms asset manifest QA / batch planner.

This tool never fabricates placeholder art. It turns the manifest into deterministic
production batches and verifies status claims against files that actually exist.
"""
from __future__ import annotations
import argparse,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/"production/asset-manifest.v0.1.json"
BATCHES=ROOT/"production/asset-batches.v0.1.json"
CONTENT=ROOT/"shattered-realms/Content"
VALID={"MISSING","CONCEPT","SOURCE_READY","CONVERTED","VALIDATED_VCMI"}
VALID_PRI={"A","B","C"}
EXT_TYPE={".png":"PNG",".def":"DEF",".wav":"WAV",".ogg":"OGG",".pcx":"PCX",".bmp":"BMP",".webm":"WEBM",".mp3":"MP3"}

def safe_resource(resource):
    if not isinstance(resource,str) or not resource: return False
    p=Path(resource)
    return not p.is_absolute() and ".." not in p.parts and "\\x00" not in resource

def load(): return json.loads(MAN.read_text(encoding="utf-8"))
def exists(resource):
    p=CONTENT/resource
    return p.exists() and p.is_file() and p.stat().st_size>0

ap=argparse.ArgumentParser()
ap.add_argument("--boot-slice",action="store_true")
ap.add_argument("--priority",choices=["A","B","C"])
ap.add_argument("--batch",help="Select one production batch ID from asset-batches.v0.1.json")
ap.add_argument("--strict",action="store_true")
ap.add_argument("--report",default="production/asset-pipeline.latest.json")
args=ap.parse_args()
m=load(); assets=m["assets"]; errors=[]
summary=m.get("summary",{})
actualPri=Counter(a.get("priority") for a in assets)
if summary.get("total")!=len(assets): errors.append(f"manifest summary total mismatch: {summary.get('total')} != {len(assets)}")
for pri in ("A","B","C"):
    if summary.get(pri)!=actualPri.get(pri,0): errors.append(f"manifest summary {pri} mismatch: {summary.get(pri)} != {actualPri.get(pri,0)}")
bootCount=sum(1 for a in assets if a.get("bootSlice"))
declaredBoot=m.get("bootSlice",{}).get("directAndDerivedAssetJobs")
if declaredBoot!=bootCount: errors.append(f"boot-slice count mismatch: {declaredBoot} != {bootCount}")
seen=set()
# VCMI derives puzzle filenames from zero-based vector positions, padded to 00..47.
expectedPuzzle={f"CRIMSON/PUZZLE/CRP{i:02d}.png" for i in range(48)}
manifestResources={a.get("resource") for a in assets}
missingPuzzle=sorted(expectedPuzzle-manifestResources)
extraPuzzle=sorted(r for r in manifestResources if isinstance(r,str) and r.startswith("CRIMSON/PUZZLE/CRP") and r not in expectedPuzzle)
if missingPuzzle: errors.append(f"missing derived puzzle manifest entries: {missingPuzzle}")
if extraPuzzle: errors.append(f"unexpected derived puzzle manifest entries: {extraPuzzle}")
siegeSuffixes={"BACK","TW21","TW22","TW2C","MAN1","MAN2","MANC","TW11","TW12","TW1C","DRW1","DRW2","DRW3","ARCH","WA61","WA62","WA63","WA41","WA42","WA43","WA31","WA32","WA33","WA11","WA12","WA13","MOAT","MLIP","WA2","WA5","TPWL"}
expectedSiege={f"CRIMSON/SIEGE/CRSG{s}.png" for s in siegeSuffixes}
missingSiege=sorted(expectedSiege-manifestResources)
extraDerivedSiege=sorted(r for r in manifestResources if isinstance(r,str) and r.startswith("CRIMSON/SIEGE/CRSG") and r not in expectedSiege)
if missingSiege: errors.append(f"missing derived siege manifest entries: {missingSiege}")
if extraDerivedSiege: errors.append(f"unexpected derived siege manifest entries: {extraDerivedSiege}")
# Batch definitions are executable production contracts, not documentation-only labels.
batchDoc=json.loads(BATCHES.read_text(encoding="utf-8"))
batches=batchDoc.get("batches",[])
batchIds=[b.get("id") for b in batches]
required=batchDoc.get("validation",{}).get("requiredBatchIds",[])
if len(batchIds)!=len(set(batchIds)): errors.append("duplicate asset batch id")
if sorted(batchIds)!=sorted(required): errors.append(f"asset batch id contract mismatch: {batchIds} vs {required}")
for b in batches:
    for selector in b.get("selectors",[]):
        if not any(isinstance(r,str) and r.startswith(selector) for r in manifestResources):
            errors.append(f"batch selector matches no manifest asset: {b.get('id')}:{selector}")
batchById={b.get("id"):b for b in batches}
if args.batch and args.batch not in batchById:
    errors.append(f"unknown asset batch: {args.batch}; expected one of {sorted(batchById)}")
for a in assets:
    r=a.get("resource")
    if not safe_resource(r):
        errors.append(f"unsafe/invalid resource path: {r!r}")
        continue
    if r in seen: errors.append(f"duplicate resource: {r}")
    seen.add(r)
    if a.get("priority") not in VALID_PRI: errors.append(f"invalid priority {a.get('priority')}: {r}")
    if not isinstance(a.get("bootSlice"),bool): errors.append(f"bootSlice must be boolean: {r}")
    if a.get("status") not in VALID: errors.append(f"invalid status {a.get('status')}: {r}")
    ext=Path(r).suffix.lower(); expectedType=EXT_TYPE.get(ext)
    if expectedType and str(a.get("type","")).upper()!=expectedType:
        errors.append(f"type/extension mismatch {a.get('type')} vs {expectedType}: {r}")
    if not expectedType: errors.append(f"unsupported asset extension {ext}: {r}")
    if a.get("status") in {"SOURCE_READY","CONVERTED","VALIDATED_VCMI"} and not exists(r):
        errors.append(f"status claims file but resource is absent/empty: {r}")

def in_batch(a):
    if not args.batch or args.batch not in batchById: return not args.batch
    return any(a["resource"].startswith(s) for s in batchById[args.batch].get("selectors",[]))
sel=[a for a in assets if (not args.boot_slice or a.get("bootSlice")) and (not args.priority or a.get("priority")==args.priority) and in_batch(a)]
by_status=Counter(a["status"] for a in sel); by_type=Counter(a["type"] for a in sel); by_pri=Counter(a["priority"] for a in sel)
missing=[a["resource"] for a in sel if not exists(a["resource"])]
report={
 "scope":{"bootSlice":args.boot_slice,"priority":args.priority,"batch":args.batch},
 "manifestAssets":len(assets),"selected":len(sel),
 "byPriority":dict(sorted(by_pri.items())),"byStatus":dict(sorted(by_status.items())),"byType":dict(sorted(by_type.items())),
 "physicalFilesPresent":len(sel)-len(missing),"physicalFilesMissing":len(missing),
 "manifestErrors":errors,"strictPass":not errors and not missing,
 "nextMissing":missing[:100]
}
out=ROOT/args.report;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="nextMissing"},indent=2))
if errors or (args.strict and missing): sys.exit(1)
