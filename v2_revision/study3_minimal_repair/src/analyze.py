"""Study 3 pre-registered analysis (PREREG.md sections 4-6). Frozen before calls."""
import json, random, re, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from frozen import protocol_construction as pc, parser as fp, scoring as fs
from run import CASES, RAW, MODELS, prompt_hash

BASE = HERE.parent
OUTD = BASE / "results"
PRIMARY = ("P1", "P2", "P3")
REPS = (0, 1, 2)


def lenient(text):
    if not isinstance(text, str): return text
    m = re.match(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", text, re.S)
    return m.group(1) if m else text


def load():
    cases = [json.loads(l) for l in CASES.open(encoding="utf-8")]
    raw = {}
    if RAW.exists():
        for l in RAW.open(encoding="utf-8"):
            r = json.loads(l)
            k = (r["model"], r["protocol"], r["rep"], r["prompt_hash"])
            if r.get("ok") or k not in raw:   # an ok record supersedes a failed one
                raw[k] = r
    return cases, raw


def score_rows(cases, raw, mode="strict"):
    rows, missing = [], 0
    for c in cases:
        rules = set(c["rules"])
        for p in ("P1", "P2", "P3", "P4"):
            ph = prompt_hash(pc.build_messages(c, p))
            for m in MODELS:
                for rep in REPS:
                    r = raw.get((m, p, rep, ph))
                    if r is None: missing += 1; continue
                    text = r.get("content") if r.get("ok") else None
                    if mode == "lenient": text = lenient(text)
                    parsed = fp.parse(text, rules, p) if text is not None else {"valid": False}
                    s = fs.score(c, parsed)
                    flags = set(parsed.get("flagged_rule_ids", [])) if parsed.get("valid") else set()
                    rows.append(dict(arm=c["arm"], case=c["base_case_id"], cond=c["condition"],
                                     version=c["version"], protocol=p, model=m, rep=rep,
                                     valid=s["valid"], detected=s["detected"],
                                     clean_target_fp=(c["condition"] == "CLEAN" and (not s["valid"] or c["rule_id"] in flags)),
                                     clean_any_fp=s["conservative_false_positive"]))
    return rows, missing


def mean(xs): xs = list(xs); return sum(xs) / len(xs) if xs else float("nan")


def unit_means(rows, arm, cond, version, field, protocols):
    u = defaultdict(list)
    for r in rows:
        if r["arm"] == arm and r["cond"] == cond and r["version"] == version and r["protocol"] in protocols:
            u[(r["case"], r["model"])].append(float(r[field]))
    return {k: mean(v) for k, v in u.items()}


def arm_stats(rows, arm, protocols=PRIMARY, seed=1733):
    Ro = unit_means(rows, arm, "OMISSION", "ORIG", "detected", protocols)
    Rr = unit_means(rows, arm, "OMISSION", "REPAIR", "detected", protocols)
    units = sorted(set(Ro) & set(Rr))
    d = {u: Rr[u] - Ro[u] for u in units}
    cases = sorted({u[0] for u in units}); models = sorted({u[1] for u in units})
    by_model = {m: mean(d[u] for u in units if u[1] == m) for m in models}
    by_case = {c: mean(d[u] for u in units if u[0] == c) for c in cases}
    fo = unit_means(rows, arm, "CLEAN", "ORIG", "clean_target_fp", protocols)
    fr = unit_means(rows, arm, "CLEAN", "REPAIR", "clean_target_fp", protocols)
    ao = unit_means(rows, arm, "CLEAN", "ORIG", "clean_any_fp", protocols)
    ar = unit_means(rows, arm, "CLEAN", "REPAIR", "clean_any_fp", protocols)
    co = unit_means(rows, arm, "COMMISSION", "ORIG", "detected", protocols)
    cr = unit_means(rows, arm, "COMMISSION", "REPAIR", "detected", protocols)
    s = dict(R_orig=mean(Ro.values()), R_rep=mean(Rr.values()), dR=mean(d.values()),
             models_dR_pos=sum(v > 0 for v in by_model.values()), n_models=len(models),
             cases_dR_nonneg=sum(v >= 0 for v in by_case.values()), n_cases=len(cases),
             dR_by_model=by_model, dR_by_case=by_case,
             clean_target_fpr_orig=mean(fo.values()), clean_target_fpr_rep=mean(fr.values()),
             clean_any_fpr_orig=mean(ao.values()), clean_any_fpr_rep=mean(ar.values()),
             comm_recall_orig=mean(co.values()), comm_recall_rep=mean(cr.values()), n_units=len(units))
    rng = random.Random(seed); bs = []
    for _ in range(10000):
        smp = [rng.choice(units) for _ in units]; bs.append(mean(d[u] for u in smp))
    bs.sort(); s["dR_boot95"] = [bs[249], bs[9749]] if units else None
    return s


def verdict(s):
    C0 = s["R_orig"] <= 0.85
    C1a = s["dR"] >= 0.20; C1b = s["models_dR_pos"] >= 4; C1c = s["cases_dR_nonneg"] == s["n_cases"]
    C2 = (s["clean_target_fpr_rep"] <= 0.10 and s["clean_target_fpr_rep"] - s["clean_target_fpr_orig"] <= 0.05
          and s["comm_recall_rep"] >= 0.90)
    C3 = s["R_rep"] >= 0.85
    crit = dict(C0=C0, C1a=C1a, C1b=C1b, C1c=C1c, C2=C2, C3=C3)
    if not C0: v = "NOT INFORMATIVE"
    elif C1a and C1b and C1c and C2 and C3: v = "SUPPORTED"
    elif C1a and not C2: v = "CONFOUNDED"
    elif C1a and C2: v = "PARTIAL"
    else: v = "NOT SUPPORTED"
    return v, crit


def main():
    cases, raw = load()
    out = {}
    for mode in ("strict", "lenient"):
        rows, missing = score_rows(cases, raw, mode)
        res = {"missing_calls": missing, "n_rows": len(rows),
               "invalid_rate": mean(not r["valid"] for r in rows)}
        for arm in ("TRIGGER", "STATE"):
            s = arm_stats(rows, arm); v, crit = verdict(s)
            res[arm] = dict(primary=s, verdict=v, criteria=crit, P4=arm_stats(rows, arm, ("P4",)))
        out[mode] = res
    out["cost_usd"] = sum(float(((r.get("usage") or {}).get("cost")) or 0) for r in raw.values())
    OUTD.mkdir(exist_ok=True)
    (OUTD / "summary.json").write_text(json.dumps(out, indent=1, default=str))
    for arm in ("TRIGGER", "STATE"):
        p = out["strict"][arm]; s = p["primary"]
        print(f"[{arm}] {p['verdict']}  R_orig={s['R_orig']:.3f} R_rep={s['R_rep']:.3f} dR={s['dR']:+.3f} "
              f"boot95={s['dR_boot95']} models+={s['models_dR_pos']}/{s['n_models']} cases>=0={s['cases_dR_nonneg']}/{s['n_cases']} "
              f"cleanFPR(t) {s['clean_target_fpr_orig']:.3f}->{s['clean_target_fpr_rep']:.3f} "
              f"anyFPR {s['clean_any_fpr_orig']:.3f}->{s['clean_any_fpr_rep']:.3f} "
              f"comm {s['comm_recall_orig']:.3f}->{s['comm_recall_rep']:.3f}  {p['criteria']}")
    print("missing calls:", out["strict"]["missing_calls"], " invalid rate:", round(out["strict"]["invalid_rate"], 4),
          " cost:", round(out["cost_usd"], 4))


if __name__ == "__main__":
    main()
