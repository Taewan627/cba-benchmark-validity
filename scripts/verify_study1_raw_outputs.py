"""Check that the published Study 1 raw model outputs reproduce the frozen parse status.

Re-parses each stored response text with code/parser.py and compares the result with
the frozen `valid` flag in results/study1_heldout/scores.jsonl. Offline, stdlib only.

    python scripts/verify_study1_raw_outputs.py
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("cba_parser", ROOT / "code" / "parser.py")
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

def jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

rules = {}
for c in jsonl(ROOT / "data" / "confirmatory_cases.jsonl"):
    rules[c["base_case_id"]] = set(re.findall(r"\((r\d+)\)", c["setup"]))
scores = {(s["model"], s["protocol"], s["condition"], s["base_case_id"]): s["valid"]
          for s in jsonl(ROOT / "results" / "study1_heldout" / "scores.jsonl")}
raw = jsonl(ROOT / "results" / "study1_heldout" / "raw_model_outputs_public.jsonl")

mismatch = 0
for r in raw:
    key = (r["model"], r["protocol"], r["condition"], r["base_case_id"])
    valid = parser.parse(r["response_text"], rules[r["base_case_id"]], r["protocol"])["valid"]
    if valid != scores[key] or valid != r["frozen_parse_valid"]:
        mismatch += 1
        print("MISMATCH:", key)
print(f"rows: {len(raw)}; transport failures: {sum(r['error_type'] is not None for r in raw)}; mismatches: {mismatch}")
print("RAW OUTPUT PARSE CHECK:", "PASS" if mismatch == 0 and len(raw) == 480 else "FAIL")
raise SystemExit(mismatch)
