#!/usr/bin/env python3
"""Create JSON-animation scaffolds for Crimson T1/T2 without fake image frames."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production/generated-animation-scaffolds"
CONTRACT=ROOT/"production/animation-contracts.crimson-v0.1.json"
ap=argparse.ArgumentParser();ap.add_argument("--clean",action="store_true");a=ap.parse_args()
if a.clean and OUT.exists():
 import shutil;shutil.rmtree(OUT)
OUT.mkdir(parents=True,exist_ok=True)
d=json.loads(CONTRACT.read_text(encoding="utf-8"))
for cid,spec in d["creatures"].items():
 groups=[]
 for g in spec["requiredGroups"]:
  groups.append({"group":g,"frames":[],"productionState":"MISSING_FRAMES"})
 scaffold={"basepath":f"SPRITES/CRIMSON/frames/{cid}/","sequences":groups,"_production":{"creature":cid,"role":spec["role"],"note":"Empty frame arrays are production scaffolding only; do not register this file in VCMI until populated and validated."}}
 (OUT/f"{cid}.animation.scaffold.json").write_text(json.dumps(scaffold,indent=2)+"\n",encoding="utf-8")
print(f"Generated {len(d['creatures'])} non-runtime scaffolds in {OUT.relative_to(ROOT)}")
