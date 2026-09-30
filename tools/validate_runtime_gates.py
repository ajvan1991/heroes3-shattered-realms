#!/usr/bin/env python3
"""Fail closed if runtime-gate bookkeeping becomes internally inconsistent."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
doc=json.loads((ROOT/"production/runtime-gates.v0.1.json").read_text(encoding="utf-8"))
gates=doc.get("gates",[]); errors=[]
ids=[g.get("id") for g in gates]
if ids!=[f"G{i}" for i in range(1,11)]: errors.append(f"gate order/id contract mismatch: {ids}")
if len(ids)!=len(set(ids)): errors.append("duplicate gate id")
allowed={"PASS","BLOCKED","PENDING","FAIL"}
by={g["id"]:g for g in gates if g.get("id")}
for g in gates:
 if g.get("status") not in allowed: errors.append(f"invalid status {g.get('status')}: {g.get('id')}")
 for dep in g.get("dependsOn",[]):
  if dep not in by: errors.append(f"unknown dependency {dep}: {g.get('id')}")
  elif ids.index(dep)>=ids.index(g["id"]): errors.append(f"non-earlier dependency {dep}: {g.get('id')}")
 if g.get("status")=="PASS" and not g.get("evidence"): errors.append(f"PASS without evidence: {g.get('id')}")
 if g.get("status")=="BLOCKED" and not g.get("blocker"): errors.append(f"BLOCKED without blocker: {g.get('id')}")
# A passed gate cannot depend on a gate that is not itself passed.
for g in gates:
 if g.get("status")=="PASS":
  for dep in g.get("dependsOn",[]):
   if by[dep].get("status")!="PASS": errors.append(f"{g['id']} PASS depends on {dep}={by[dep].get('status')}")
# Current v0.1 truth: media prevents strict candidate/runtime gates.
if by.get("G3",{}).get("status")!="BLOCKED": errors.append("G3 must remain BLOCKED until real media evidence exists")
if by.get("G4",{}).get("status")!="BLOCKED": errors.append("G4 must remain BLOCKED until strict candidate succeeds")
for gid in ("G5","G6","G7","G8","G9","G10"):
 if by.get(gid,{}).get("status")!="PENDING": errors.append(f"{gid} must remain PENDING until local VCMI evidence is recorded")
ci=doc.get("ciEvidence",{})
if ci.get("conclusion")!="success" or not isinstance(ci.get("lastVerifiedRun"),int): errors.append("invalid CI evidence summary")
if not isinstance(ci.get("lastVerifiedRunId"),int) or ci.get("lastVerifiedRunId",0)<=0: errors.append("invalid CI run id")
sha=ci.get("headSha","")
if not isinstance(sha,str) or len(sha)!=40 or any(ch not in "0123456789abcdef" for ch in sha): errors.append("invalid CI head SHA")
if ci.get("lastVerifiedRun",0)<23: errors.append("CI evidence regressed behind executable reference-closure baseline run 23")
scope=str(ci.get("scope",""))
for token in ("structural","reference closure","production batches","candidate"):
 if token not in scope: errors.append(f"CI evidence scope missing contract token: {token}")
out={"pass":not errors,"gateStatuses":{g["id"]:g["status"] for g in gates},"errors":errors}
print(json.dumps(out,indent=2));sys.exit(1 if errors else 0)
