"""Offline check of the Study 2b exact case-level permutation sensitivity analysis.

Reads results/study2b/scores.jsonl (stored scored rows). No network access.
Standard library only. Run from the repository root:

    python scripts/verify_study2b_permutation.py
"""
import json
from collections import defaultdict
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in
        (ROOT / "results" / "study2b" / "scores.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

cell = defaultdict(dict)   # case -> {(model, condition): detected}
structure = {}
for r in rows:
    if r["condition"] in ("COMMISSION", "OMISSION"):
        cell[r["base_case_id"]][(r["model"], r["condition"])] = int(bool(r["detected"]))
        structure[r["base_case_id"]] = r["structure"]

d = {}
for case, c in cell.items():
    models = sorted({m for m, _ in c})
    d[case] = sum(c[(m, "COMMISSION")] - c[(m, "OMISSION")] for m in models) / len(models)

point = sorted(k for k, s in structure.items() if s == "point")
scope = sorted(k for k, s in structure.items() if s == "scope")
assert len(point) == len(scope) == 30 and len(d) == 60

mean = lambda xs: sum(xs) / len(xs)
observed = mean([d[k] for k in scope]) - mean([d[k] for k in point])

# Exact enumeration via the multiset of d_i values: only the nonzero cases matter.
nonzero = [v for v in d.values() if v != 0]
zeros = len(d) - len(nonzero)
total = comb(60, 30)
dist = defaultdict(int)   # permuted Delta -> number of allocations
total_d = sum(d.values())
for k in range(len(nonzero) + 1):
    for sub in combinations(range(len(nonzero)), k):
        scope_sum = sum(nonzero[i] for i in sub)
        ways = comb(zeros, 30 - k)
        delta = scope_sum / 30 - (total_d - scope_sum) / 30
        dist[round(delta, 10)] += ways
assert sum(dist.values()) == total
p_one = sum(w for x, w in dist.items() if x >= round(observed, 10) - 1e-12) / total
p_two = sum(w for x, w in dist.items() if abs(x) >= abs(observed) - 1e-12) / total

print(f"observed Delta_scope = {observed:+.4f}")
print(f"one-sided p = {p_one:.4f}; two-sided p = {p_two:.4f}")
print(f"attainable range = [{min(dist):+.4f}, {max(dist):+.4f}]")
assert abs(observed - 1 / 60) < 1e-9
assert abs(p_one - 0.5) < 1e-9 and abs(p_two - 1.0) < 1e-9
assert abs(min(dist) + 0.05) < 1e-9 and abs(max(dist) - 0.05) < 1e-9
print("PERMUTATION SENSITIVITY CHECK: PASS")
