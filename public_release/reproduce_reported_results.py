"""Offline verification of the numerical results reported in the manuscript.

This script reads frozen scored rows and result manifests. It makes no network
request, does not call an evaluator, and does not alter any result artifact.
"""

from __future__ import annotations

import csv
import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def close(a, b, tol=5e-10):
    if abs(a - b) > tol:
        raise AssertionError(f"{a} != {b}")


def load_analysis_module():
    path = ROOT / "code" / "analysis.py"
    spec = importlib.util.spec_from_file_location("cba_frozen_analysis", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


analysis = load_analysis_module()
study1_rows = load_jsonl(ROOT / "results" / "study1_heldout" / "scores.jsonl")
study1 = analysis.analyze_run(study1_rows, {
    "analysis": {"bootstrap_seed": 1732, "bootstrap_replicates": 10000}
})

models = {
    "Gemini": "google/gemini-3.8-flash",
    "Claude": "anthropic/claude-sonnet-5",
}
expected_protocol = {
    ("Gemini", "P1"): (1.000, 0.900, 0.100, 0.150, 60, 0),
    ("Gemini", "P2"): (1.000, 0.750, 0.250, 0.150, 60, 0),
    ("Gemini", "P3"): (0.950, 0.850, 0.100, 0.150, 59, 1),
    ("Gemini", "P4"): (1.000, 0.700, 0.300, 0.000, 59, 1),
    ("Claude", "P1"): (1.000, 0.950, 0.050, 0.150, 60, 0),
    ("Claude", "P2"): (1.000, 0.850, 0.150, 0.100, 60, 0),
    ("Claude", "P3"): (1.000, 0.800, 0.200, 0.100, 59, 1),
    ("Claude", "P4"): (1.000, 0.850, 0.150, 0.050, 60, 0),
}

protocol_output = {}
for (label, protocol), expected in expected_protocol.items():
    model = models[label]
    cell = study1["cells"][(model, protocol)]
    subset = [r for r in study1_rows if r["model"] == model and r["protocol"] == protocol]
    actual = (cell["comm_recall"], cell["om_recall"], cell["gap"],
              cell["clean_conservative_fpr"], sum(r["valid"] for r in subset),
              sum(not r["valid"] for r in subset))
    for got, wanted in zip(actual[:4], expected[:4]):
        close(got, wanted)
    assert actual[4:] == expected[4:]
    protocol_output[f"{label}_{protocol}"] = actual

expected_ordinary = {
    "Gemini": (1.000, 0.825, 0.175, (0.050, 0.300), 0.150),
    "Claude": (1.000, 0.900, 0.100, (0.025, 0.175), 0.125),
}
ordinary_output = {}
for label, expected in expected_ordinary.items():
    row = study1["ordinary"][models[label]]
    actual = (row["comm_recall"], row["om_recall"], row["gap"],
              tuple(row["bootstrap_ci"]), row["clean_conservative_fpr"])
    for got, wanted in zip(actual[:3], expected[:3]):
        close(got, wanted)
    close(actual[3][0], expected[3][0]); close(actual[3][1], expected[3][1])
    close(actual[4], expected[4])
    ordinary_output[label] = actual

v1 = load_json(ROOT / "results" / "study2_v1" / "result_manifest.json")
assert v1["verdict"] == "INCONCLUSIVE"
assert v1["reasons"] == ["clean_fpr_exceeded"]
close((v1["primary"]["fpr_point"] + v1["primary"]["fpr_scope"]) / 2, 50 / 120)

with (ROOT / "results" / "study2_v1" / "clean_fpr_audit.csv").open(encoding="utf-8-sig", newline="") as fh:
    audit = list(csv.DictReader(fh))
assert len(audit) == 50
assert Counter(r["fp_status"] for r in audit) == {"B": 41, "C": 8, "A": 1}
assert Counter(r["benchmark_quality"] for r in audit) == {
    "LIKELY DEFECT": 25, "AMBIGUOUS": 17, "CLEAR CLEAN": 8
}

v2 = load_json(ROOT / "results" / "study2b" / "result_manifest.json")
assert v2["verdict"] == "KILL"
assert v2["reasons"] == ["delta_scope_ruled_out"]
close(v2["clean_quality"]["pooled"], 0.0083, tol=5e-5)
close(v2["primary"]["G_point"], -0.03333333333333333)
close(v2["primary"]["G_scope"], -0.016666666666666666)
close(v2["primary"]["Delta"], 0.016666666666666666)
close(v2["primary"]["delta_ci"][0], -0.03333333333333334)
close(v2["primary"]["delta_ci"][1], 0.06666666666666667)

report = {
    "study1_protocol_rows": protocol_output,
    "study1_ordinary": ordinary_output,
    "study1_frozen_verdict": load_json(ROOT / "results" / "study1_heldout" / "result_manifest.json")["verdict"],
    "study2_v1": {"clean_false_positives": 50, "clean_rows": 120, "verdict": v1["verdict"]},
    "study2_v1_diagnostic": {
        "fp_status": dict(Counter(r["fp_status"] for r in audit)),
        "quality": dict(Counter(r["benchmark_quality"] for r in audit)),
    },
    "study2b": {
        "clean_fpr": v2["clean_quality"]["pooled"],
        "G_point": v2["primary"]["G_point"],
        "G_scope": v2["primary"]["G_scope"],
        "Delta_scope": v2["primary"]["Delta"],
        "delta_ci": v2["primary"]["delta_ci"],
        "verdict": v2["verdict"],
    },
}
print(json.dumps(report, indent=2, sort_keys=True))
print("OFFLINE REPRODUCTION CHECK: PASS")
