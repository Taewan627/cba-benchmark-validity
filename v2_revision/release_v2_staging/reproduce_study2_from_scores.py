"""Recompute Study 2 v1 and Study 2b statistics directly from the released scored rows (reviewer request R2.4/R3.6).

Uses the frozen analysis functions verbatim: their source is read from code/study2_scope.py (lines 25-118:
per-case gaps, Delta_scope, the percentile cluster bootstrap with seed 1732 and 10,000 replicates, CLEAN FPR by
structure) and executed without the run-time imports, then the recomputed values are compared with the frozen
result manifests. Usage:  python reproduce_study2_from_scores.py <public_release_root>   (stdlib only)"""
import json, math, random, sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
src = (ROOT / "code" / "study2_scope.py").read_text(encoding="utf-8")
start = src.index("def _percentile(")
end = src.index("def analyze(")
ns = {"math": math, "random": random, "Counter": Counter, "PROTOCOL": "P2"}
exec(compile(src[start:end], "study2_scope.py[frozen functions]", "exec"), ns)
SEED, NB = 1732, 10000
jl = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
ok = True


def close(a, b, tol=1e-9):
    return (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= tol)


for name in ("study2_v1", "study2b"):
    rows = jl(ROOT / "results" / name / "scores.jsonl")
    man = json.loads((ROOT / "results" / name / "result_manifest.json").read_text(encoding="utf-8"))
    pooled = ns["_pooled_diffs"](rows)
    g_s, g_p, delta, n_s, n_p = ns["delta_scope"](pooled)
    ci = ns["bootstrap_delta"](pooled, SEED, NB)
    fpr_s, fpr_p = ns["fpr_by_structure"](pooled)
    clean = [r for r in rows if r["protocol"] == "P2" and r["condition"] == "CLEAN"]
    cfp = sum(r["conservative_false_positive"] for r in clean)
    invalid = sum(1 for r in rows if not r["valid"])
    print(f"== {name}: rows {len(rows)}, invalid {invalid}, conservative CLEAN FP {cfp}/{len(clean)}")
    print(f"   G_point {g_p:+.4f}  G_scope {g_s:+.4f}  Delta {delta:+.4f}  95% CI [{ci[0]:+.4f}, {ci[1]:+.4f}]  n_point {n_p} n_scope {n_s}")
    print(f"   CLEAN FPR point {fpr_p:.4f} scope {fpr_s:.4f}")
    for m in sorted({r["model"] for r in rows}):
        d = ns["per_case_diffs"](rows, model=m)
        gs, gp, dl, _, _ = ns["delta_scope"](d); c = ns["bootstrap_delta"](d, SEED, NB)
        print(f"   {m}: G_point {gp:+.4f} G_scope {gs:+.4f} Delta {dl:+.4f} CI [{c[0]:+.4f}, {c[1]:+.4f}]")
    p = man.get("primary", {})
    checks = [close(p.get("G_point"), g_p), close(p.get("G_scope"), g_s), close(p.get("Delta"), delta)]
    if p.get("delta_ci"): checks += [close(p["delta_ci"][0], ci[0]), close(p["delta_ci"][1], ci[1])]
    good = all(checks)
    ok &= good
    print("   matches frozen manifest:", "YES" if good else "NO", checks)
print("STUDY 2 RECOMPUTE FROM SCORED ROWS:", "PASS" if ok else "FAIL")
