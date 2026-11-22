from common import *
import parser as P, collections
cases = {(c["base_case_id"],c["condition"]): c for c in jl(ROOT/"data/confirmatory_cases.jsonl")}
raw = jl(ROOT/"results/study1_heldout/raw_model_outputs_public.jsonl")
scores = jl(ROOT/"results/study1_heldout/scores.jsonl")
print(len(cases), len(raw))
agg = collections.defaultdict(lambda: collections.Counter())
rows=[]
for r in raw:
    c = cases[(r["base_case_id"], r["condition"])]
    if r["condition"]!="CLEAN": continue
    known=set(c["rules"].keys())
    p = P.parse(r["response_text"] or "", known, r["protocol"])
    tgt=c["rule_id"]
    flags=set(p["flagged_rule_ids"]) if p["valid"] else set()
    any_fp = (not p["valid"]) or bool(flags)
    tgt_fp = (not p["valid"]) or (tgt in flags)
    tgt_fp_valid_only = p["valid"] and tgt in flags
    k=(r["model"].split("/")[1], r["protocol"])
    agg[k]["n"]+=1; agg[k]["any_cons"]+=any_fp; agg[k]["tgt_cons"]+=tgt_fp
    agg[k]["invalid"]+= (not p["valid"]); agg[k]["tgt_valid_only"]+=tgt_fp_valid_only
    agg[k]["any_valid_only"]+= (p["valid"] and bool(flags))
    if any_fp: rows.append((r["base_case_id"],k,p["valid"],sorted(flags),tgt))
for k in sorted(agg): print(k, dict(agg[k]))
tot=collections.Counter()
for k,v in agg.items(): tot.update(v)
print("TOTAL", dict(tot))
print("---flag rows")
for x in sorted(rows): print(x)
# consistency vs published scores
sc = [s for s in scores if s["condition"]=="CLEAN"]
print("published cons FP total", sum(s["conservative_false_positive"] for s in sc))
