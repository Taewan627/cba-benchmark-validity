import importlib.util, copy, yaml, collections, json
from common import *
import parser as P
spec=importlib.util.spec_from_file_location("an", ROOT/"code/analysis.py"); an=importlib.util.module_from_spec(spec); spec.loader.exec_module(an)
cfg=yaml.safe_load(open(ROOT/"config/pilot.yaml",encoding="utf-8"))
rows=jl(ROOT/"results/study1_heldout/scores.jsonl")
cases={(c["base_case_id"],c["condition"]):c for c in jl(ROOT/"data/confirmatory_cases.jsonl")}
raw={(r["base_case_id"],r["condition"],r["protocol"],r["model"]):r for r in jl(ROOT/"results/study1_heldout/raw_model_outputs_public.jsonl")}
def run(rows,label):
    res=an.analyze_run(rows,cfg); v=an.decide(res,cfg)
    print("==",label,v)
    for m in sorted(res["ordinary"]):
        o=res["ordinary"][m]; print(m.split('/')[1],"ord gap %.3f ci %s fpr %.3f"%(o["gap"],tuple(round(x,3) for x in o["bootstrap_ci"]),o["clean_conservative_fpr"]))
        for p in ("P1","P2","P3","P4"):
            c=res["cells"][(m,p)]; print("  ",p,"gap %.3f fpr %.3f comm %.3f om %.3f ci %s boot %s"%(c["gap"],c["clean_conservative_fpr"],c["comm_recall"],c["om_recall"],tuple(round(x,3) for x in c["newcombe_ci"]),tuple(round(x,3) for x in c["bootstrap_ci"])))
    return res,v
run(rows,"AS PUBLISHED (any-rule conservative FPR)")
rows2=copy.deepcopy(rows)
for r in rows2:
    if r["condition"]!="CLEAN": continue
    rw=raw[(r["base_case_id"],r["condition"],r["protocol"],r["model"])]
    c=cases[(r["base_case_id"],"CLEAN")]
    p=P.parse(rw["response_text"] or "",set(c["rules"]),r["protocol"])
    r["conservative_false_positive"]=(not p["valid"]) or (c["rule_id"] in p["flagged_rule_ids"])
run(rows2,"TARGET-ONLY conservative FPR")
