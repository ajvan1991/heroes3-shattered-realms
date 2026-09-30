#!/usr/bin/env python3
"""Shattered Realms asset manifest QA / batch planner.

This tool never fabricates placeholder art. It turns the manifest into deterministic
production batches and verifies status claims against files that actually exist.
"""
from __future__ import annotations
import argparse,json,sys
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/"production/asset-manifest.v0.1.json"
CONTENT=ROOT/"shattered-realms/Content"
VALID={"MISSING","CONCEPT","SOURCE_READY","CONVERTED","VALIDATED_VCMI"}

def load(): return json.loads(MAN.read_text(encoding="utf-8"))
def exists(resource):
    p=CONTENT/resource
    return p.exists() and p.is_file() and p.stat().st_size>0

ap=argparse.ArgumentParser()
ap.add_argument("--boot-slice",action="store_true")
ap.add_argument("--priority",choices=["A","B","C"])
ap.add_argument("--strict",action="store_true")
ap.add_argument("--report",default="production/asset-pipeline.latest.json")
args=ap.parse_args()
m=load(); assets=m["assets"]; errors=[]
summary=m.get("summary",{})
actualPri=Counter(a.get("priority") for a in assets)
if summary.get("total")!=len(assets): errors.append(f"manifest summary total mismatch: {summary.get('total')} != {len(assets)}")
for pri in ("A","B","C"):
    if summary.get(pri)!=actualPri.get(pri,0): errors.append(f"manifest summary {pri} mismatch: {summary.get(pri)} != {actualPri.get(pri,0)}")
seen=set()
# VCMI derives puzzle filenames from zero-based vector positions, padded to 00..47.
expectedPuzzle={f"CRIMSON/PUZZLE/CRP{i:02d}.png" for i in range(48)}
manifestResources={a.get("resource") for a in assets}
missingPuzzle=sorted(expectedPuzzle-manifestResources)
extraPuzzle=sorted(r for r in manifestResources if isinstance(r,str) and r.startswith("CRIMSON/PUZZLE/CRP") and r not in expectedPuzzle)
if missingPuzzle: errors.append(f"missing derived puzzle manifest entries: {missingPuzzle}")
if extraPuzzle: errors.append(f"unexpected derived puzzle manifest entries: {extraPuzzle}")
for a in assets:
    r=a["resource"]
    if r in seen: errors.append(f"duplicate resource: {r}")
    seen.add(r)
    if a.get("status") not in VALID: errors.append(f"invalid status {a.get('status')}: {r}")
    if a.get("status") in {"SOURCE_READY","CONVERTED","VALIDATED_VCMI"} and not exists(r):
        errors.append(f"status claims file but resource is absent/empty: {r}")

sel=[a for a in assets if (not args.boot_slice or a.get("bootSlice")) and (not args.priority or a.get("priority")==args.priority)]
by_status=Counter(a["status"] for a in sel); by_type=Counter(a["type"] for a in sel); by_pri=Counter(a["priority"] for a in sel)
missing=[a["resource"] for a in sel if not exists(a["resource"])]
report={
 "scope":{"bootSlice":args.boot_slice,"priority":args.priority},
 "manifestAssets":len(assets),"selected":len(sel),
 "byPriority":dict(sorted(by_pri.items())),"byStatus":dict(sorted(by_status.items())),"byType":dict(sorted(by_type.items())),
 "physicalFilesPresent":len(sel)-len(missing),"physicalFilesMissing":len(missing),
 "manifestErrors":errors,"strictPass":not errors and not missing,
 "nextMissing":missing[:100]
}
out=ROOT/args.report;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="nextMissing"},indent=2))
if errors or (args.strict and missing): sys.exit(1)
