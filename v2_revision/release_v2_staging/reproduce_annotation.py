"""Reproduce the independent-annotation statistics reported in the revised manuscript (Sec. IV-A, Table 7).

Inputs (all in the v2.0.0 release): annotation/coder1_labels.json, annotation/coder2_labels.json,
annotation/item_key.json, and the v1 scored rows results/study1_heldout/scores.jsonl and
results/study2_v1/clean_fpr_audit.csv. Usage:  python reproduce_annotation.py <v1_release_root> [<annotation_dir>]
Stdlib only."""
import csv, json, sys
from collections import Counter
from pathlib import Path

R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")  # folder holding results/ (the v1 release root)
A = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent / "annotation"
key = {k["item_id"]: k for k in json.load(open(A / "item_key.json", encoding="utf-8"))}
c1 = json.load(open(A / "coder1_labels.json", encoding="utf-8"))
c2 = json.load(open(A / "coder2_labels.json", encoding="utf-8"))
CATS = ["SATISFIED", "VIOLATED", "CANNOT TELL"]


def kappa(pairs, cats):
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
    return round(po, 3), round((po - pe) / (1 - pe), 3) if pe < 1 else 0.0


def alpha(pairs, cats):
    o = Counter()
    for a, b in pairs: o[(a, b)] += 1; o[(b, a)] += 1
    nc = {c: sum(o[(c, d)] for d in cats) for c in cats}; N = 2 * len(pairs)
    Do = sum(o[(c, d)] for c in cats for d in cats if c != d) / N
    De = sum(nc[c] * nc[d] for c in cats for d in cats if c != d) / (N * (N - 1))
    return round(1 - Do / De, 3)


att = lambda lab: sum(lab[i][r] == g for i, k in key.items() if k["study"] == "ATTN" for r, g in k["gold"].items())
print("attention checks (of 10): coder1", att(c1), "coder2", att(c2))
allp = [(c1[i][r], c2[i][r]) for i in key for r in key[i]["rule_order"]]
tp = [(c1[i][key[i]["target_rule"]], c2[i][key[i]["target_rule"]]) for i in key if key[i]["study"] != "ATTN"]
print("all 175 judgments: agreement, kappa", kappa(allp, CATS), "alpha", alpha(allp, CATS))
print("90 target rules:   agreement, kappa", kappa(tp, CATS), "alpha", alpha(tp, CATS))
by = {(k["study"], k["case"], k["condition"]): k["item_id"] for k in key.values() if k["study"] != "ATTN"}
s1 = [json.loads(l) for l in open(R / "results/study1_heldout/scores.jsonl", encoding="utf-8")]
M = {"VIOLATED": "genuine", "CANNOT TELL": "ambiguous", "SATISFIED": "label_defect"}
pairs = Counter()
for r in s1:
    if r["condition"] == "OMISSION" and not r["detected"]:
        o = by[("S1", r["base_case_id"], "OMISSION")]; t = key[o]["target_rule"]
        pairs[("artifact", "artifact") if not r["valid"] else (M[c1[o][t]], M[c2[o][t]])] += 1
print("Study 1 omission nondetections (coder1, coder2):", dict(pairs))


def derive(lab, it, invalid):
    if invalid: return "artifact"
    ls = list(lab[it].values())
    return "false_alarm" if all(x == "SATISFIED" for x in ls) else "defect" if "VIOLATED" in ls else "ambiguous"


fp = Counter()
for r in s1:
    if r["condition"] == "CLEAN" and r["conservative_false_positive"]:
        it = by[("S1", r["base_case_id"], "CLEAN")]; fp[(derive(c1, it, not r["valid"]), derive(c2, it, not r["valid"]))] += 1
print("Study 1 CLEAN false positives (coder1, coder2):", dict(fp))
aud = list(csv.DictReader(open(R / "results/study2_v1/clean_fpr_audit.csv", encoding="utf-8")))
s2 = Counter(); auth_c1 = []; auth_c2 = []
for r in aud:
    it = by[("S2v1", r["base_case_id"], "CLEAN")]; inv = r["fp_status"] == "C"
    d1, d2 = derive(c1, it, inv), derive(c2, it, inv)
    a = "artifact" if inv else "false_alarm" if r["fp_status"] == "A" else "defect" if r["benchmark_quality"] == "LIKELY DEFECT" else "ambiguous"
    s2[(d1, d2)] += 1
    if not inv: auth_c1.append((a, d1)); auth_c2.append((a, d2))
NC = ["false_alarm", "ambiguous", "defect"]
print("Study 2 v1 flagged CLEAN (coder1, coder2):", dict(s2))
print("author vs coder1 kappa", kappa(auth_c1, NC)[1], "; author vs coder2 kappa", kappa(auth_c2, NC)[1])

# Pre-registered statistic 2, second form (ANNOTATION_PREREG.md sec. 6): Study 1 author coding with the trigger cases
# (b08, b13, b16; the Study 3 TRIGGER arm) recoded as defects, all other valid rows "ambiguous" as recorded.
TRIG = {"b08", "b13", "b16"}
rec1, rec2 = [], []
for r in s1:
    if r["condition"] == "OMISSION" and not r["detected"] and r["valid"]:
        o = by[("S1", r["base_case_id"], "OMISSION")]; t = key[o]["target_rule"]
        a = "label_defect" if r["base_case_id"] in TRIG else "ambiguous"
        rec1.append((a, M[c1[o][t]])); rec2.append((a, M[c2[o][t]]))
S1C = ["genuine", "ambiguous", "label_defect"]
print("Study 1, author coding with trigger cases recoded as defects (n=%d): agreement, kappa  coder1" % len(rec1),
      kappa(rec1, S1C), " coder2", kappa(rec2, S1C))
# Pre-registered statistic 4: annotator-oracle agreement on target rules by study and condition.
orc = Counter(); tot = Counter()
for i, k in key.items():
    if k["study"] == "ATTN": continue
    exp = "VIOLATED" if k["oracle_target_violation"] else "SATISFIED"
    g = (k["study"], k["condition"]); tot[g] += 1
    orc[(g, 1)] += c1[i][k["target_rule"]] == exp; orc[(g, 2)] += c2[i][k["target_rule"]] == exp
print("annotator-oracle agreement on target rules by study and condition (coder1, coder2, n):")
for g in sorted(tot): print("  ", g[0], g[1], orc[(g, 1)], orc[(g, 2)], tot[g])
