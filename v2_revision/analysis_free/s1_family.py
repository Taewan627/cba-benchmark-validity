from common import *
import collections
rows=jl(ROOT/"results/study1_heldout/scores.jsonl")
fam={r["base_case_id"]:r["rule_family"] for r in rows}
print(collections.Counter(fam.values()))
print({f:sorted(b for b in fam if fam[b]==f) for f in set(fam.values())})
# per family
T=collections.defaultdict(collections.Counter)
miss=collections.defaultdict(list)
for r in rows:
    f=r["rule_family"]; c=r["condition"]
    if c in("COMMISSION","OMISSION"):
        T[(f,c)]["n"]+=1; T[(f,c)]["det"]+=r["detected"]; T[(f,c)]["inv"]+=(not r["valid"])
        if not r["detected"]: miss[(f,c)].append((r["base_case_id"],r["model"].split('/')[1][:6],r["protocol"],"INV" if not r["valid"] else ""))
    else:
        T[(f,c)]["n"]+=1; T[(f,c)]["fp"]+=r["conservative_false_positive"]
print("family  cond n det(recall) inv")
for f in sorted(set(fam.values())):
    cr=T[(f,"COMMISSION")]; om=T[(f,"OMISSION")]; cl=T[(f,"CLEAN")]
    print(f"{f:18s} comm {cr['det']}/{cr['n']}={cr['det']/cr['n']:.3f} om {om['det']}/{om['n']}={om['det']/om['n']:.3f} gap {(cr['det']-om['det'])/cr['n']:.3f} cleanFP(any) {cl['fp']}/{cl['n']}")
for k,v in sorted(miss.items()): print(k,len(v),v)
# omission misses by case
bc=collections.Counter(); 
for (f,c),v in miss.items():
    if c=="OMISSION":
        for x in v: bc[(f,x[0])]+=1
print(sorted(bc.items()))
print("omission misses total", sum(bc.values()), "invalid among", sum(1 for (f,c),v in miss.items() if c=="OMISSION" for x in v if x[3]))
