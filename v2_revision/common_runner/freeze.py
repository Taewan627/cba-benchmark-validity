import hashlib, json, sys, datetime
from pathlib import Path
V2 = Path(__file__).resolve().parents[1]
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
common = ["common_runner/run_calls.py", "common_runner/analyze.py", "study3_minimal_repair/src/frozen.py",
          "../public_release/code/protocol_construction.py", "../public_release/code/parser.py",
          "../public_release/code/deterministic_scoring.py"]
sets = {"study2c": ["study2c/PREREG.md", "study2c/data/study2c_cases.jsonl", "study2c/src/build_cases.py", "study2c/src/validate.py"] + common,
        "study2b_reruns": ["study2b_reruns/PREREG.md", "../public_release/data/study2b_scope_cases.jsonl"] + common}
now = datetime.datetime.now(datetime.timezone.utc)
for k, files in sets.items():
    d = {"frozen_at_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "frozen_at_kst": (now + datetime.timedelta(hours=9)).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
         "model_calls_before_freeze": 0, "sha256": {f: h(V2 / f) for f in files}}
    (V2 / k / "FREEZE.json").write_text(json.dumps(d, indent=1), encoding="utf-8")
    (V2 / k / "DEVIATIONS.md").write_text("# Deviations\n\nNone at freeze time.\n", encoding="utf-8")
    print(k, d["frozen_at_utc"]); [print(" ", a[:12], f) for f, a in d["sha256"].items()]
