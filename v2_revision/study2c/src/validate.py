"""Validate Study 2c cases: structure, leakage, oracle consistency, length balance."""
import json, re, sys, collections
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "data" / "study2c_cases.jsonl"
cases = [json.loads(l) for l in P.open(encoding="utf-8")]
BAD = re.compile(r"\b(wrong|incorrect|empty|absent|missing|instead|fails?|failed|forgets?|forgot|omits?|violat\w*|mistak\w*|error|never|not|no one|nobody|nothing|without|skips?|skipped)\b", re.I)
errs = []
for c in cases:
    cid = (c["base_case_id"], c["condition"])
    if len(c["beats"]) != 6:
        errs.append((cid, "beats != 6"))
    for b in c["beats"]:
        if BAD.search(b):
            errs.append((cid, "cue word in beat: " + b))
    if len(c["rules"]) != 3:
        errs.append((cid, "rules != 3"))
    txt = c["script"]
    hasA = c["A"] in txt
    hasB = c["B"] in txt
    cond = c["condition"]
    exp = {"CLEAN": (True, False), "COMMISSION": (False, True), "OMISSION": (False, False), "ADD": (True, True)}[cond]
    if (hasA, hasB) != exp:
        errs.append((cid, "A/B presence %s expected %s" % ((hasA, hasB), exp)))
    if c["oracle_label"] != (cond != "CLEAN"):
        errs.append((cid, "oracle label"))
    for r in ("r02", "r03"):
        pass
    if "bg1" not in " ".join(c["observed_events"]):
        errs.append((cid, "bg"))
# length balance per base case (word counts across variants)
by = collections.defaultdict(dict)
for c in cases:
    by[c["base_case_id"]][c["condition"]] = c["word_count"]
spread = max(max(v.values()) - min(v.values()) for v in by.values())
# POINT vs SCOPE same obligation: target slot must match
slot = collections.defaultdict(set)
for c in cases:
    slot[c["obligation_id"]].add(c["target_position"])
for k, v in slot.items():
    if len(v) != 1:
        errs.append((k, "target slot differs"))
# no actor/place cue-free check for OMISSION: nothing mentions rule object
for c in cases:
    if c["condition"] == "OMISSION":
        obj = c["rules"]["r01"].split("must ")[1].split(",")[0]
        key = obj.split(" to ")[0].split(" on ")[0].split(" in ")[0]
        if key.split()[-1] in c["script"] and key.split()[-1] not in ("the", "name"):
            errs.append(((c["base_case_id"], "OMISSION"), "object noun in script: " + key))
print("cases", len(cases), "errors", len(errs), "max word-count spread within base case", spread)
for e in errs[:40]:
    print(e)
sys.exit(1 if errs else 0)
