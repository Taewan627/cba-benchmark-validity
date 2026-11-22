"""Study-2 (scope): Delta_scope analysis, run plan, manifest, freeze (offline)."""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from pathlib import Path

from src.run_plan import (
    load_evaluator_config, expand_matrix, project_cost,
    PROJECTED_OUTPUT_TOKENS_PER_CALL,
)
from src.study2_scope_cases import BASES, all_triplets, manifest as cases_manifest
from src.freeze import write_study2_scope_freeze, verify_study2_scope_freeze

ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = "P2"
DELTA_THRESHOLD = 0.15
MAX_CLEAN_FPR = 0.10
MAX_INVALID = 0.05


def _percentile(values, q):
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    return s[lo] if lo == hi else s[lo] + (s[hi] - s[lo]) * (pos - lo)


def per_case_diffs(rows, model=None):
    diffs = {}
    for r in rows:
        if r["protocol"] != PROTOCOL:
            continue
        if model is not None and r["model"] != model:
            continue
        bid = r["base_case_id"]
        e = diffs.setdefault(bid, {"structure": r["structure"],
                                   "comm": None, "om": None, "clean_fp": None})
        if r["condition"] == "COMMISSION":
            e["comm"] = int(r["detected"])
        elif r["condition"] == "OMISSION":
            e["om"] = int(r["detected"])
        elif r["condition"] == "CLEAN":
            e["clean_fp"] = int(r["conservative_false_positive"])
    out = {}
    for bid, e in diffs.items():
        if e["comm"] is None or e["om"] is None:
            continue
        e["diff"] = e["comm"] - e["om"]
        out[bid] = e
    return out


def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def delta_scope(diffs):
    scope = [e["diff"] for e in diffs.values() if e["structure"] == "scope"]
    point = [e["diff"] for e in diffs.values() if e["structure"] == "point"]
    g_s = _mean(scope)
    g_p = _mean(point)
    delta = (g_s - g_p) if (g_s is not None and g_p is not None) else None
    return g_s, g_p, delta, len(scope), len(point)


def bootstrap_delta(diffs, seed, n_boot=10000):
    scope_ids = [b for b, e in diffs.items() if e["structure"] == "scope"]
    point_ids = [b for b, e in diffs.items() if e["structure"] == "point"]
    rng = random.Random(seed)
    deltas = []
    for _ in range(n_boot):
        ss = rng.choices(scope_ids, k=len(scope_ids))
        ps = rng.choices(point_ids, k=len(point_ids))
        gs = sum(diffs[b]["diff"] for b in ss) / len(ss)
        gp = sum(diffs[b]["diff"] for b in ps) / len(ps)
        deltas.append(gs - gp)
    return (_percentile(deltas, 0.025), _percentile(deltas, 0.975))


def fpr_by_structure(diffs):
    scope = [e["clean_fp"] for e in diffs.values()
             if e["structure"] == "scope" and e["clean_fp"] is not None]
    point = [e["clean_fp"] for e in diffs.values()
             if e["structure"] == "point" and e["clean_fp"] is not None]
    return (_mean(scope), _mean(point))


def _pooled_diffs(rows):
    acc = {}
    for r in rows:
        if r["protocol"] != PROTOCOL:
            continue
        bid = r["base_case_id"]
        e = acc.setdefault(bid, {"structure": r["structure"],
                                 "comm": [], "om": [], "clean_fp": []})
        if r["condition"] == "COMMISSION":
            e["comm"].append(int(r["detected"]))
        elif r["condition"] == "OMISSION":
            e["om"].append(int(r["detected"]))
        elif r["condition"] == "CLEAN":
            e["clean_fp"].append(int(r["conservative_false_positive"]))
    out = {}
    for bid, e in acc.items():
        if not e["comm"] or not e["om"]:
            continue
        comm = sum(e["comm"]) / len(e["comm"])
        om = sum(e["om"]) / len(e["om"])
        out[bid] = {"structure": e["structure"], "comm": comm, "om": om,
                    "clean_fp": (sum(e["clean_fp"]) / len(e["clean_fp"])
                                 if e["clean_fp"] else None),
                    "diff": comm - om}
    return out


def analyze(rows, config=None):
    config = config or {}
    seed = config.get("study2", {}).get("bootstrap_seed", 1732)
    n_boot = config.get("study2", {}).get("bootstrap_replicates", 10000)
    models = sorted({r["model"] for r in rows})
    per_model = {}
    for m in models:
        diffs = per_case_diffs(rows, model=m)
        g_s, g_p, delta, ns, np_ = delta_scope(diffs)
        ci = bootstrap_delta(diffs, seed, n_boot)
        fpr_s, fpr_p = fpr_by_structure(diffs)
        per_model[m] = {
            "G_scope": g_s, "G_point": g_p, "Delta": delta,
            "delta_ci": list(ci), "n_scope": ns, "n_point": np_,
            "fpr_scope": fpr_s, "fpr_point": fpr_p,
            "comm_scope": _mean([e["comm"] for e in diffs.values()
                                 if e["structure"] == "scope"]),
            "om_scope": _mean([e["om"] for e in diffs.values()
                               if e["structure"] == "scope"]),
            "comm_point": _mean([e["comm"] for e in diffs.values()
                                 if e["structure"] == "point"]),
            "om_point": _mean([e["om"] for e in diffs.values()
                               if e["structure"] == "point"]),
        }
    pooled = _pooled_diffs(rows)
    g_s, g_p, delta, ns, np_ = delta_scope(pooled)
    ci = bootstrap_delta(pooled, seed, n_boot)
    fpr_s, fpr_p = fpr_by_structure(pooled)
    primary = {"G_scope": g_s, "G_point": g_p, "Delta": delta,
               "delta_ci": list(ci), "n_scope": ns, "n_point": np_,
               "fpr_scope": fpr_s, "fpr_point": fpr_p}
    total = len(rows)
    invalid = sum(1 for r in rows if not r["valid"])
    return {"primary": primary, "per_model": per_model, "models": models,
            "invalid_fraction": (invalid / total) if total else None}


def decide(result):
    if result.get("invalid_fraction") is not None and \
            result["invalid_fraction"] > MAX_INVALID:
        return ("INCONCLUSIVE", ["invalid_output_fraction_exceeded"])
    primary = result["primary"]
    delta = primary["Delta"]
    lo, hi = primary["delta_ci"]
    fpr_ok = (primary["fpr_scope"] is not None
              and primary["fpr_point"] is not None
              and primary["fpr_scope"] <= MAX_CLEAN_FPR
              and primary["fpr_point"] <= MAX_CLEAN_FPR)
    if not fpr_ok:
        return ("INCONCLUSIVE", ["clean_fpr_exceeded"])
    if delta is None:
        return ("INCONCLUSIVE", ["missing_observations"])
    if delta >= DELTA_THRESHOLD and lo > 0:
        consistent = all(p["Delta"] is not None and p["Delta"] > 0
                         for p in result["per_model"].values())
        if consistent:
            return ("GO", ["delta_scope_positive_consistent"])
        return ("INCONCLUSIVE", ["model_disagreement"])
    if hi < DELTA_THRESHOLD:
        return ("KILL", ["delta_scope_ruled_out"])
    return ("INCONCLUSIVE", ["no_delta_pattern"])


def run_plan(evaluators=None):
    if evaluators is None:
        evaluators = load_evaluator_config()["evaluators"]
    return expand_matrix(evaluators, bases=list(BASES), protocols=(PROTOCOL,))


def run_manifest(calls):
    by_model = Counter(c["model"] for c in calls)
    by_condition = Counter(c["condition"] for c in calls)
    man = {
        "total_calls": len(calls),
        "by_model": dict(by_model),
        "by_protocol": {"P2": len(calls)},
        "by_condition": dict(by_condition),
        "call_id_example": calls[0]["call_id"] if calls else None,
    }
    man.update(cases_manifest())
    return man


def preflight(calls, evaluators):
    report = {"ok": True, "checks": {}}

    def fail(name, msg):
        report["checks"][name] = "FAIL: %s" % msg
        report["ok"] = False

    try:
        verify_study2_scope_freeze()
        report["checks"]["freeze"] = "PASS"
    except (RuntimeError, FileNotFoundError):
        report["checks"]["freeze"] = "NOT_YET_FROZEN"

    if len(calls) != 360:
        fail("call_count", len(calls))
    else:
        report["checks"]["call_count"] = "PASS"
    ids = [c["call_id"] for c in calls]
    report["checks"]["unique_call_ids"] = "PASS" if len(ids) == len(set(ids)) else "FAIL"
    by_model = Counter(c["model"] for c in calls)
    ok = (by_model.get("google/gemini-3.8-flash") == 180
          and by_model.get("anthropic/claude-sonnet-5") == 180)
    report["checks"]["model_balance"] = "PASS" if ok else "FAIL: %s" % dict(by_model)
    leaked = [c["call_id"] for c in calls if c["leakage_violations"]]
    report["checks"]["leakage"] = "PASS" if not leaked else "FAIL: %s" % leaked
    pinned = {ev["requested_model"] for ev in evaluators}
    report["checks"]["models"] = "PASS" if pinned == {
        "google/gemini-3.8-flash", "anthropic/claude-sonnet-5"} else "FAIL"
    pricing = load_evaluator_config()["pricing"]
    projected = project_cost(calls, pricing, PROJECTED_OUTPUT_TOKENS_PER_CALL)
    report["projected_cost_usd"] = projected["total_usd"]
    report["checks"]["budget"] = "PASS" if projected["total_usd"] < 5.0 else "FAIL"
    return report


def write_run_plan_manifest():
    calls = run_plan()
    man = run_manifest(calls)
    with open(ROOT / "data" / "study2_scope_manifest.json", "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2, sort_keys=True)
    return man


def freeze():
    write_study2_scope_freeze(extra={
        "note": "Study-2 scope frozen benchmark; no paid API executed."})


if __name__ == "__main__":
    calls = run_plan()
    print(json.dumps(run_manifest(calls), indent=2, sort_keys=True))
