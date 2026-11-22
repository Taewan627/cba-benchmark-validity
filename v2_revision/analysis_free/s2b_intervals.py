"""B5: Study 2b interaction with zero-event-robust intervals + design sensitivity. Also lenient-parser variant."""
from common import *
import numpy as np, json, collections
from scipy import stats
rows=jl(ROOT/"results/study2b/scores.jsonl")
# lenient override: q001 Claude COMMISSION becomes detected (see rescore_all.json)
def load(lenient):
    cell=collections.defaultdict(dict); struct={}
    for r in rows:
        if r["condition"] not in("COMMISSION","OMISSION"): continue
        det=int(bool(r["detected"]))
        if lenient and r["base_case_id"]=="q001" and r["condition"]=="COMMISSION" and "claude" in r["model"]: det=1
        cell[r["base_case_id"]][(r["model"],r["condition"])]=det; struct[r["base_case_id"]]=r["structure"]
    return cell,struct
def case_arrays(cell,struct):
    P=[];S=[]
    for k,c in sorted(cell.items()):
        ms=sorted({m for m,_ in c})
        rec=[[c[(m,"COMMISSION")] for m in ms],[c[(m,"OMISSION")] for m in ms]]
        (P if struct[k]=="point" else S).append(np.array(rec))  # shape 2(cond) x 2(models)
    return np.array(P),np.array(S)  # n x 2 x 2
def delta(P,S):
    g=lambda A:(A[:,0,:]-A[:,1,:]).mean()
    return g(S)-g(P), g(P), g(S)
def boot(P,S,B=10000,seed=1732):
    rng=np.random.default_rng(seed); dP=(P[:,0,:]-P[:,1,:]).mean(1); dS=(S[:,0,:]-S[:,1,:]).mean(1)
    n=len(dP); iP=rng.integers(0,n,(B,n)); iS=rng.integers(0,n,(B,n))
    D=dS[iS].mean(1)-dP[iP].mean(1); return np.percentile(D,[2.5,97.5])
def wilson(x,n,z=1.959964):
    p=x/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return p,max(0,c-h),min(1,c+h)
def mover(cells,signs):
    th=sum(s*p for (p,l,u),s in zip(cells,signs))
    L=th-np.sqrt(sum(((p-l) if s>0 else (u-p))**2 for (p,l,u),s in zip(cells,signs)))
    U=th+np.sqrt(sum(((u-p) if s>0 else (p-l))**2 for (p,l,u),s in zip(cells,signs)))
    return th,L,U
def jeffreys(P,S,N=200000,seed=7,unit=1):
    rng=np.random.default_rng(seed)
    def post(x,n): return rng.beta(x+.5,n-x+.5,N)
    def cnt(A,cond): 
        return A[:,cond,:].sum(), A[:,cond,:].size
    if unit==0: # case-level (n=30 clusters; a case counts as detected if mean>=.5 ... use proportion*30)
        pass
    out={}
    pc_p=post(*cnt(P,0)); po_p=post(*cnt(P,1)); pc_s=post(*cnt(S,0)); po_s=post(*cnt(S,1))
    D=(pc_s-po_s)-(pc_p-po_p)
    return np.percentile(D,[2.5,97.5]), (D>=0.15).mean()
res={}
for lenient in (False,True):
    cell,struct=load(lenient); P,S=case_arrays(cell,struct)
    d,gp,gs=delta(P,S)
    out={"Delta":d,"G_point":gp,"G_scope":gs}
    out["percentile_cluster_bootstrap_10000_seed1732"]=boot(P,S).tolist()
    # score-type (MOVER-Wilson) for Delta = (pcS-poS)-(pcP-poP); cell proportion over model-responses n=60 (optimistic) and n_eff=30 cases (conservative)
    for tag,fac in(("mover_wilson_n60",1),("mover_wilson_neff30",2)):
        cells=[]
        for A,cond in((S,0),(S,1),(P,0),(P,1)):
            x=A[:,cond,:].sum(); n=A[:,cond,:].size
            x2=x/fac; n2=n/fac   # n_eff scaling keeps proportion
            cells.append(wilson(x2,n2))
        th,L,U=mover(cells,[1,-1,-1,1]); out[tag]=[L,U]
    ci,pge=jeffreys(P,S); out["jeffreys_bayes_95"]=ci.tolist(); out["jeffreys_P(Delta>=0.15)"]=float(pge)
    # exclusion rule check
    res["lenient" if lenient else "strict"]=out
    # per model
    for mi,mn in enumerate(("gemini","claude")): pass
print(json.dumps(res,indent=1))
# check per-cell counts
cell,struct=load(False); P,S=case_arrays(cell,struct)
print("comm det P",P[:,0,:].sum(0),"om det P",P[:,1,:].sum(0),"comm det S",S[:,0,:].sum(0),"om det S",S[:,1,:].sum(0), "(columns: models sorted)")
# ---- design sensitivity
def sim(delta_true,pc=0.967,po_p=1.0,n=30,reps=2000,B=1000,rho=0.0,seed=11,go_thr=0.15):
    rng=np.random.default_rng(seed); po_s=po_p-delta_true  # omission harder in SCOPE by delta_true (commission recall same in both)
    exc=0; go=0; ci_excl0=0
    for r in range(reps):
        def gen(po):
            # case random effect via shared uniform per case (rho: prob that both models share the case outcome)
            comm=(rng.random((n,2))<pc).astype(int); om=(rng.random((n,2))<po).astype(int)
            return np.stack([comm,om],1)
        Pm=gen(po_p); Sm=gen(po_s)
        dP=(Pm[:,0,:]-Pm[:,1,:]).mean(1); dS=(Sm[:,0,:]-Sm[:,1,:]).mean(1)
        iP=rng.integers(0,n,(B,n)); iS=rng.integers(0,n,(B,n))
        D=dS[iS].mean(1)-dP[iP].mean(1); lo,hi=np.percentile(D,[2.5,97.5]); est=dS.mean()-dP.mean()
        exc+= hi<go_thr; go+= (est>=go_thr and lo>0)
    return exc/reps, go/reps
print("\ntrue_delta  P(bootstrap upper<0.15)  P(detect: est>=.15 & CI excludes 0)")
sens=[]
for dl in (0,0.05,0.10,0.15,0.20,0.25,0.30,0.40):
    e,g=sim(dl); sens.append((dl,e,g)); print(dl,e,g)
json.dump({"intervals":res,"design_sensitivity":sens},open("s2b_intervals.json","w"),indent=1)
