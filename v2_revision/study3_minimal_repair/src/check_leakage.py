import json, sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from frozen import protocol_construction as pc
D = Path(__file__).resolve().parents[1] / "data" / "study3_cases.jsonl"
cases = [json.loads(l) for l in D.open(encoding="utf-8")]
viol = []
for ver in ("ORIG", "REPAIR"):
    for bid in sorted({c["base_case_id"] for c in cases}):
        trip = [c for c in cases if c["base_case_id"] == bid and c["version"] == ver]
        viol += pc.check_triplet_leakage(trip)
print("leakage violations:", len(viol)); [print(" ", v) for v in viol]
# show one repaired prompt per arm for eyeballing
for bid, cond in (("b13", "OMISSION"), ("b18", "OMISSION")):
    c = next(x for x in cases if x["base_case_id"] == bid and x["condition"] == cond and x["version"] == "REPAIR")
    m = pc.build_messages(c, "P2")
    print("=====", bid, cond, "REPAIR P2\n", m[1]["content"][:900])
