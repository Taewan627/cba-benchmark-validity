"""Recompute the Study 2c and Study 2b-rerun results from the released raw outputs (no API calls, no key needed)
and check them against the stored analysis files. Run: python reproduce_followups.py   (from anywhere)"""
import json, subprocess, sys
from pathlib import Path
V2 = Path(__file__).resolve().parents[1]
ok = True
for study, d in (("2c", "study2c"), ("2brerun", "study2b_reruns")):
    f = V2 / d / "results" / "analysis.json"
    before = json.loads(f.read_text(encoding="utf-8"))
    subprocess.run([sys.executable, str(V2 / "common_runner" / "analyze.py"), "--study", study], check=True, capture_output=True)
    after = json.loads(f.read_text(encoding="utf-8"))
    same = before == after
    p = after["strict"]["pooled"]
    print(study, "reproduced" if same else "MISMATCH", "| omission recall %.3f | delta %.3f CI %s | %s" % (p["pooled_omission_recall"], p["delta"], [round(x, 3) for x in p["delta_ci"]], p["decision"]))
    ok &= same
sys.exit(0 if ok else 1)
