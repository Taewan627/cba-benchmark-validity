"""Study-2b: run plan, manifest, freeze, and preflight (offline).

Reuses the Study-2 scope Delta_scope analysis (structure labels are the same
"point"/"scope"); only the benchmark source differs.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from src.run_plan import (
    load_evaluator_config, expand_matrix, project_cost,
    PROJECTED_OUTPUT_TOKENS_PER_CALL,
)
from src.study2b_scope_cases import BASES, all_triplets, manifest as cases_manifest
from src.study2_scope import analyze, decide, per_case_diffs, delta_scope, \
    bootstrap_delta, fpr_by_structure, DELTA_THRESHOLD, MAX_CLEAN_FPR, MAX_INVALID
from src.freeze import write_study2b_scope_freeze, verify_study2b_scope_freeze

ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = "P2"


def run_plan(evaluators=None):
    if evaluators is None:
        evaluators = load_evaluator_config()["evaluators"]
    return expand_matrix(evaluators, bases=list(BASES), protocols=(PROTOCOL,))


def run_manifest(calls):
    man = {
        "total_calls": len(calls),
        "by_model": dict(Counter(c["model"] for c in calls)),
        "by_protocol": {"P2": len(calls)},
        "by_condition": dict(Counter(c["condition"] for c in calls)),
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
        verify_study2b_scope_freeze()
        report["checks"]["freeze"] = "PASS"
    except (RuntimeError, FileNotFoundError):
        report["checks"]["freeze"] = "NOT_YET_FROZEN"

    report["checks"]["call_count"] = "PASS" if len(calls) == 360 else "FAIL: %d" % len(calls)
    ids = [c["call_id"] for c in calls]
    report["checks"]["unique_call_ids"] = "PASS" if len(ids) == len(set(ids)) else "FAIL"
    by_model = Counter(c["model"] for c in calls)
    report["checks"]["model_balance"] = "PASS" if (
        by_model.get("google/gemini-3.8-flash") == 180
        and by_model.get("anthropic/claude-sonnet-5") == 180) else "FAIL"
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
    with open(ROOT / "data" / "study2b_scope_manifest.json", "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2, sort_keys=True)
    return man


def freeze():
    write_study2b_scope_freeze(extra={
        "note": "Study-2b frozen benchmark; author QA pending; no paid API executed."})


if __name__ == "__main__":
    calls = run_plan()
    print(json.dumps(run_manifest(calls), indent=2, sort_keys=True))
