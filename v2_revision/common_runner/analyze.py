"""Pre-specified analysis for Study 2c and the Study 2b reruns (frozen before any call).
Usage: python analyze.py --study 2c|2brerun
Strict frozen parser (primary). Lenient parser reported as sensitivity.
Cluster bootstrap: 10,000 reps, seed 1734. 2c clusters = obligation (paired POINT/SCOPE);
2b reruns = base case, resampled independently within structure."""
import argparse, json, random, re, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_calls import STUDIES, ph, pc, V2
from frozen import parser as fp, scoring as fs

THRESH = 0.15
CEIL = 0.95
B = 10000
SEED = 1734


def lenient(text):
    if not isinstance(text, str):
        return text
    t = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text, flags=re.S)
    i = t.find("{")
    if i < 0:
        return text
    d = 0
    for j in range(i, len(t)):
        d += (t[j] == "{") - (t[j] == "}")
        if d == 0:
            return t[i:j + 1]
    return text


def rows_for(study, mode="strict"):
    cfg = STUDIES[study]
    cases = [json.loads(l) for l in cfg["cases"].open(encoding="utf-8")]
    cmap = {"%s|%s" % (c["base_case_id"], c["condition"]): c for c in cases}
    raw = {}
    for l in cfg["raw"].open(encoding="utf-8"):
        r = json.loads(l)
        k = (r["case"], r["model"], r["rep"], r["mode"])
        if r.get("ok") or k not in raw:
            raw[k] = r
    rows = []
    for (cid, model, rep, md), r in raw.items():
        c = cmap[cid]
        text = r.get("content") if r.get("ok") else None
        if mode == "lenient":
            text = lenient(text)
        try:
            parsed = fp.parse(text, set(c["rules"]), "P2") if text is not None else {"valid": False}
        except RecursionError:  # pathologically nested output: frozen parser crashes; counted as invalid
            parsed = {"valid": False}
        s = fs.score(dict(c, condition="COMMISSION") if c["condition"] == "ADD" else c, parsed)
        flags = set(parsed.get("flagged_rule_ids", [])) if parsed.get("valid") else set()
        cond = c["condition"]
        rows.append(dict(case=c["base_case_id"], cluster=c.get("obligation_id", c["base_case_id"]),
                         structure=c["structure"], cond=cond, model=model, rep=rep, mode=md,
                         valid=bool(s["valid"]), detected=bool(s["detected"]),
                         target_fp=(cond == "CLEAN" and (not s["valid"] or c["rule_id"] in flags)),
                         any_fp=bool(s.get("conservative_false_positive")) if cond == "CLEAN" else False,
                         finish=r.get("finish_reason")))
    return rows, len(cases) * 0


def mean(x):
    x = list(x)
    return sum(x) / len(x) if x else float("nan")


def cell(rows, structure, cond, field="detected"):
    return mean(r[field] for r in rows if r["structure"] == structure and r["cond"] == cond)


def gap(rows, structure, comm="COMMISSION"):
    return cell(rows, structure, comm) - cell(rows, structure, "OMISSION")


def delta(rows, comm="COMMISSION"):
    return gap(rows, "scope", comm) - gap(rows, "point", comm)


def boot(rows, paired, comm="COMMISSION"):
    rng = random.Random(SEED)
    byc = defaultdict(list)
    for r in rows:
        byc[(r["structure"], r["cluster"])].append(r)
    cl = defaultdict(list)
    for (s, c) in byc:
        cl[s].append(c)
    out = []
    for _ in range(B):
        sample = []
        if paired:
            ids = [rng.choice(cl["point"]) for _ in cl["point"]]
            for s in ("point", "scope"):
                for c in ids:
                    sample += byc[(s, c)]
        else:
            for s in ("point", "scope"):
                ids = [rng.choice(cl[s]) for _ in cl[s]]
                for c in ids:
                    sample += byc[(s, c)]
        d = delta(sample, comm)
        if d == d:
            out.append(d)
    out.sort()
    return out[int(0.025 * len(out))], out[int(0.975 * len(out))]


def summarize(rows, paired, label):
    res = {"label": label, "n_rows": len(rows)}
    res["invalid_rate"] = 1 - mean(r["valid"] for r in rows)
    res["truncation_rate"] = mean(r["finish"] == "length" for r in rows)
    for s in ("point", "scope"):
        res[s] = {c: cell(rows, s, c) for c in ("COMMISSION", "OMISSION", "ADD") if any(r["cond"] == c for r in rows)}
        res[s]["CLEAN_target_fpr"] = cell(rows, s, "CLEAN", "target_fp")
        res[s]["CLEAN_any_fpr"] = cell(rows, s, "CLEAN", "any_fp")
        res[s]["G"] = gap(rows, s)
    res["delta"] = delta(rows)
    res["delta_ci"] = boot(rows, paired)
    pooled_om = mean(r["detected"] for r in rows if r["cond"] == "OMISSION")
    res["pooled_omission_recall"] = pooled_om
    res["ceiling"] = pooled_om > CEIL
    res["clean_target_fpr_pooled"] = mean(r["target_fp"] for r in rows if r["cond"] == "CLEAN")
    lo, hi = res["delta_ci"]
    res["decision"] = ("CEILING_UNINFORMATIVE" if res["ceiling"] else
                       "EXCLUDES_+0.15" if hi < THRESH else "REACHES_+0.15" if lo > THRESH else "INCONCLUSIVE")
    if "ADD" in res["point"]:
        res["add_vs_commission_gap_point"] = res["point"]["COMMISSION"] - res["point"]["ADD"]
        res["add_vs_commission_gap_scope"] = res["scope"]["COMMISSION"] - res["scope"]["ADD"]
        res["delta_ADD_based"] = delta(rows, "ADD")
        res["delta_ADD_ci"] = boot(rows, paired, "ADD")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--study", required=True, choices=list(STUDIES))
    a = ap.parse_args()
    paired = a.study == "2c"
    out = {}
    for mode in ("strict", "lenient"):
        rows, _ = rows_for(a.study, mode)
        out[mode] = {"pooled": summarize(rows, paired, "pooled")}
        for m in sorted({r["model"] for r in rows}):
            sub = [r for r in rows if r["model"] == m]
            out[mode][m] = summarize(sub, paired, m)
        if a.study == "2brerun":
            sub = [r for r in rows if r["mode"] == "orig"]
            out[mode]["orig_body_two_models"] = summarize(sub, paired, "orig_body_two_models")
    d = V2 / ("study2c" if a.study == "2c" else "study2b_reruns") / "results"
    d.mkdir(exist_ok=True)
    (d / "analysis.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    p = out["strict"]["pooled"]
    print(json.dumps({k: p[k] for k in ("n_rows", "invalid_rate", "pooled_omission_recall", "clean_target_fpr_pooled", "delta", "delta_ci", "decision")}, indent=1, default=str))


if __name__ == "__main__":
    main()
