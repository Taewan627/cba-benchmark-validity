"""Paired analysis, finite-sample intervals, and gate decision logic.

Every comparison is paired within base case. Commission and omission variants
of the same base case are never treated as independent observations; the
bootstrap resamples whole base-case clusters (stratified by rule family), and
the finite-sample interval conditions on the paired 2x2 table.

Primary estimand (per model x protocol cell): mean over base cases of
(commission_detection - omission_detection).

Uncertainty:
* Newcombe paired interval (method 10) -- a finite-sample paired interval that
  never degenerates to zero width; used for cell-level gate decisions.
* Stratified cluster bootstrap -- reported alongside as a robustness interval.

The ordinary-audit summary G_ordinary(m) = mean(G_P1(m), G_P2(m)) is computed
as a paired quantity over base cases (average of the two within-case protocol
gaps); its interval is the cluster bootstrap on those per-case differences.
The KILL ordinary-equivalence route uses this same G_ordinary aggregate (its
bootstrap interval, ordinary recalls, and ordinary conservative CLEAN FPR),
not the individual P1/P2 cells.

Data-quality gating: an invalid-output fraction strictly exceeding
``max_invalid_fraction`` (0.05), at global or per-(model, protocol, condition)
granularity, forces INCONCLUSIVE with reason
``invalid_output_fraction_exceeded``. Rows must carry a boolean ``valid`` field;
invalid rows are included in the denominator.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

Z95 = 1.959963984540054


# --------------------------------------------------------------------------
# Finite-sample paired interval (Newcombe 1998, method 10)
# --------------------------------------------------------------------------

def _wilson(x, n, z=Z95):
    if n == 0:
        return (0.0, 0.0)
    p = x / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (center - half, center + half)


def newcombe_paired_ci(a, b, c, d, z=Z95):
    """95% CI for p_comm - p_om from paired counts.

    Cells: a = both detected, b = commission only, c = omission only,
    d = neither. Returns (lower, upper).
    """
    n = a + b + c + d
    if n == 0:
        return (0.0, 0.0)
    p1 = (a + b) / n
    p2 = (a + c) / n
    delta = (b - c) / n
    l1, u1 = _wilson(a + b, n, z)
    l2, u2 = _wilson(a + c, n, z)
    denom = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    phi = ((a * d - b * c) / denom) if denom > 0 else 0.0
    lower = delta - math.sqrt(
        (p1 - l1) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2) + (u2 - p2) ** 2)
    upper = delta + math.sqrt(
        (u1 - p1) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2) + (p2 - l2) ** 2)
    return (lower, upper)


def _percentile(values, q):
    if not values:
        raise ValueError("empty sample")
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return s[lo]
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


# --------------------------------------------------------------------------
# Point estimate
# --------------------------------------------------------------------------

def paired_gap(commission, omission):
    """Inputs map independent case IDs to binary detections for ONE cell."""
    if not commission or commission.keys() != omission.keys():
        raise ValueError("Nonempty, identical case IDs required; no silent dropping")
    if any(type(v) not in (bool, int) or v not in (0, 1)
           for v in [*commission.values(), *omission.values()]):
        raise ValueError("Detection outcomes must be binary")
    return sum(commission[k] - omission[k] for k in commission) / len(commission)


# --------------------------------------------------------------------------
# Cell summarization
# --------------------------------------------------------------------------

def _group(rows, model, protocols):
    return [r for r in rows
            if r["model"] == model and r["protocol"] in protocols]


def _per_case_pairs(rows):
    pairs = {}
    for r in rows:
        bid = r["base_case_id"]
        entry = pairs.setdefault(bid, {})
        if r["condition"] == "COMMISSION":
            entry.setdefault("comm", []).append(int(bool(r["detected"])))
        elif r["condition"] == "OMISSION":
            entry.setdefault("om", []).append(int(bool(r["detected"])))
        elif r["condition"] == "CLEAN":
            entry.setdefault("clean_fp", []).append(int(bool(r["conservative_false_positive"])))
    return pairs


def _mean(seq):
    return sum(seq) / len(seq) if seq else None


def _cell_summary(rows):
    """Summarize one model x protocol cell (binary paired detections)."""
    pairs = _per_case_pairs(rows)
    a = b = c = d = 0
    clean_fp = 0
    clean_total = 0
    missing = []
    for bid, entry in pairs.items():
        if "comm" not in entry or "om" not in entry:
            missing.append(bid)
            continue
        comm = int(round(_mean(entry["comm"])))
        om = int(round(_mean(entry["om"])))
        if comm and om:
            a += 1
        elif comm:
            b += 1
        elif om:
            c += 1
        else:
            d += 1
        if "clean_fp" in entry:
            clean_fp += sum(entry["clean_fp"])
            clean_total += len(entry["clean_fp"])

    n = a + b + c + d
    return {
        "n_base": n,
        "missing": missing,
        "a": a, "b": b, "c": c, "d": d,
        "comm_recall": (a + b) / n if n else None,
        "om_recall": (a + c) / n if n else None,
        "gap": (b - c) / n if n else None,
        "newcombe_ci": newcombe_paired_ci(a, b, c, d) if n else None,
        "clean_conservative_fpr": (clean_fp / clean_total) if clean_total else None,
        "clean_total": clean_total,
    }


def _ordinary_summary(rows, families, seed, n_boot):
    """Per-model ordinary-audit summary: mean of P1 and P2, paired.

    G_ordinary = mean over base cases of (mean(P1,P2 commission detection) -
    mean(P1,P2 omission detection)). The KILL ordinary-equivalence route needs
    the ordinary recalls and ordinary conservative CLEAN FPR too.
    """
    pairs = _per_case_pairs(rows)
    diffs = {}
    comms = []
    oms = []
    clean_fps = []
    for bid, entry in pairs.items():
        if "comm" not in entry or "om" not in entry:
            continue
        comm = _mean(entry["comm"])
        om = _mean(entry["om"])
        diffs[bid] = comm - om
        comms.append(comm)
        oms.append(om)
        if "clean_fp" in entry:
            clean_fps.append(_mean(entry["clean_fp"]))
    n = len(diffs)
    gap = sum(diffs.values()) / n if n else None
    ci = _bootstrap_diffs(diffs, families, seed, n_boot) if n else None
    return {
        "gap": gap,
        "bootstrap_ci": ci,
        "n_base": n,
        "comm_recall": sum(comms) / len(comms) if comms else None,
        "om_recall": sum(oms) / len(oms) if oms else None,
        "clean_conservative_fpr": (sum(clean_fps) / len(clean_fps)
                                   if clean_fps else None),
    }


def _bootstrap_diffs(diffs, families, seed, n_boot):
    by_family = {}
    for bid in diffs:
        by_family.setdefault(families.get(bid, "unassigned"), []).append(bid)
    rng = random.Random(seed)
    means = []
    for _ in range(n_boot):
        sample = []
        for fam_ids in by_family.values():
            sample.extend(rng.choices(fam_ids, k=len(fam_ids)))
        means.append(sum(diffs[b] for b in sample) / len(sample))
    return (_percentile(means, 0.025), _percentile(means, 0.975))


def _binary_pairs(rows):
    """Reduce rows to per-base-case binary (comm, om) ints."""
    pairs = _per_case_pairs(rows)
    out = {}
    for bid, entry in pairs.items():
        if "comm" not in entry or "om" not in entry:
            continue
        out[bid] = (int(round(_mean(entry["comm"]))),
                    int(round(_mean(entry["om"]))))
    return out


def _bootstrap_binary(pairs, families, seed, n_boot):
    by_family = {}
    for bid in pairs:
        by_family.setdefault(families.get(bid, "unassigned"), []).append(bid)
    rng = random.Random(seed)
    gaps = []
    for _ in range(n_boot):
        sample = []
        for fam_ids in by_family.values():
            sample.extend(rng.choices(fam_ids, k=len(fam_ids)))
        gaps.append(sum(
            (pairs[b][0] - pairs[b][1]) for b in sample) / len(sample))
    return (_percentile(gaps, 0.025), _percentile(gaps, 0.975))


# --------------------------------------------------------------------------
# Invalid-output quality gate
# --------------------------------------------------------------------------

def _invalid_exceeds(invalid, total, max_frac):
    """Strictly-greater-than comparison, exact under floating point.

    ``invalid / total > max_frac`` evaluated with ``fractions.Fraction`` so a
    fraction of exactly 0.05 (e.g. 1/20) is NOT flagged while 0.0501 is.
    """
    if total <= 0:
        return False
    return Fraction(invalid, total) > Fraction(str(max_frac))


def _invalid_summary(rows):
    """Invalid-output counts/fractions at every reporting granularity.

    A row is invalid when its ``valid`` field is false. The denominator always
    includes invalid rows (they are never silently dropped)."""
    def stats(subset):
        total = len(subset)
        invalid = sum(1 for r in subset if not r.get("valid", True))
        return {"invalid": invalid, "total": total,
                "fraction": (invalid / total) if total else None}

    models = sorted({r["model"] for r in rows})
    protocols = sorted({r["protocol"] for r in rows})
    conditions = sorted({r["condition"] for r in rows})

    summary = {
        "global": stats(rows),
        "by_model": {m: stats([r for r in rows if r["model"] == m])
                     for m in models},
        "by_protocol": {p: stats([r for r in rows if r["protocol"] == p])
                        for p in protocols},
        "by_condition": {c: stats([r for r in rows if r["condition"] == c])
                         for c in conditions},
        "cells": {},
    }
    for m in models:
        for p in protocols:
            for c in conditions:
                subset = [r for r in rows
                          if r["model"] == m and r["protocol"] == p
                          and r["condition"] == c]
                summary["cells"][(m, p, c)] = stats(subset)
    return summary


# --------------------------------------------------------------------------
# Full-run analysis
# --------------------------------------------------------------------------

def analyze_run(rows, config):
    """Return {"cells": {(model, protocol): summary}, "ordinary": {model: ...}}."""
    seed = config.get("analysis", {}).get("bootstrap_seed", 1732)
    n_boot = config.get("analysis", {}).get("bootstrap_replicates", 10000)

    families = {r["base_case_id"]: r["rule_family"] for r in rows}
    models = sorted({r["model"] for r in rows})

    cells = {}
    for m in models:
        for p in ("P1", "P2", "P3", "P4"):
            cell_rows = _group(rows, m, (p,))
            if not cell_rows:
                cells[(m, p)] = None
                continue
            summary = _cell_summary(cell_rows)
            pairs = _binary_pairs(cell_rows)
            summary["bootstrap_ci"] = _bootstrap_binary(pairs, families, seed, n_boot)
            cells[(m, p)] = summary

    ordinary = {}
    for m in models:
        ordinary[m] = _ordinary_summary(
            _group(rows, m, ("P1", "P2")), families, seed, n_boot)

    return {"cells": cells, "ordinary": ordinary,
            "invalid": _invalid_summary(rows)}


# --------------------------------------------------------------------------
# Gate decision
# --------------------------------------------------------------------------

def _inside(ci, lo, hi):
    return ci is not None and lo <= ci[0] and ci[1] <= hi


def _excludes_zero(ci):
    return ci is not None and (ci[1] < 0 or ci[0] > 0)


def decide(result, config):
    """Apply frozen gate rules to an ``analyze_run`` result."""
    th = config.get("thresholds_provisional", {})
    gap_th = th.get("ordinary_gap", 0.20)
    margin = th.get("equivalence_margin", 0.10)
    residual = th.get("residual_gap", 0.10)
    max_fpr = th.get("max_clean_conservative_fpr", 0.10)
    min_recall = th.get("rescue_min_recall", 0.80)
    max_invalid = th.get("max_invalid_fraction", 0.05)

    cells = result["cells"]
    ordinary = result["ordinary"]
    models = sorted(ordinary.keys())
    if len(models) != 2:
        return ("INCONCLUSIVE", ["decision requires exactly two models"])

    reasons = []

    # Data-quality: any missing cell or unrecovered base case -> INCONCLUSIVE.
    for m in models:
        for p in ("P1", "P2", "P3", "P4"):
            s = cells.get((m, p))
            if s is None or s["missing"]:
                reasons.append("missing/incomplete cell %s/%s" % (m, p))
                return ("INCONCLUSIVE", reasons)

    # Data-quality: invalid-output fraction gate (global and per-cell).
    invalid = result.get("invalid", {})
    if _invalid_exceeds(invalid.get("global", {}).get("invalid", 0),
                        invalid.get("global", {}).get("total", 0), max_invalid):
        reasons.append("invalid_output_fraction_exceeded")
        return ("INCONCLUSIVE", reasons)
    for cell in invalid.get("cells", {}).values():
        if _invalid_exceeds(cell["invalid"], cell["total"], max_invalid):
            reasons.append("invalid_output_fraction_exceeded")
            return ("INCONCLUSIVE", reasons)

    def ci(m, p):
        s = cells[(m, p)]
        nc = s["newcombe_ci"]
        bc = s["bootstrap_ci"]
        if nc is None:
            return bc
        if bc is not None and (bc[1] - bc[0]) > (nc[1] - nc[0]):
            return bc
        return nc

    # ---- KILL (evaluated first) ------------------------------------------
    kill_checklist = True
    kill_equiv = True
    for m in models:
        p3 = cells[(m, "P3")]
        if not (_inside(ci(m, "P3"), -margin, margin)
                and p3["comm_recall"] >= min_recall
                and p3["om_recall"] >= min_recall
                and p3["clean_conservative_fpr"] <= max_fpr):
            kill_checklist = False

        # KILL route 2 uses G_ordinary (mean of P1 and P2), matching the
        # frozen spec: ordinary-gap interval inside [-margin, +margin],
        # ordinary recalls >= min_recall, ordinary conservative CLEAN FPR.
        ord_summary = ordinary[m]
        if not (_inside(ord_summary["bootstrap_ci"], -margin, margin)
                and ord_summary["comm_recall"] >= min_recall
                and ord_summary["om_recall"] >= min_recall
                and ord_summary["clean_conservative_fpr"] <= max_fpr):
            kill_equiv = False

    if kill_checklist:
        reasons.append("KILL: precise high-recall checklist rescue in both models")
        return ("KILL", reasons)
    if kill_equiv:
        reasons.append("KILL: precise ordinary-audit equivalence in both models")
        return ("KILL", reasons)

    # ---- GO --------------------------------------------------------------
    go_ordinary = True
    go_retain = True
    for m in models:
        g1 = cells[(m, "P1")]["gap"]
        g2 = cells[(m, "P2")]["gap"]
        ord_gap = ordinary[m]["gap"]
        ord_ci = ordinary[m]["bootstrap_ci"]
        sign_conflict = (g1 * g2) < 0
        fpr_ok = (cells[(m, "P1")]["clean_conservative_fpr"] <= max_fpr
                  and cells[(m, "P2")]["clean_conservative_fpr"] <= max_fpr)
        if not (ord_gap >= gap_th and _excludes_zero(ord_ci)
                and not sign_conflict and fpr_ok):
            go_ordinary = False

        p3 = cells[(m, "P3")]
        if not (p3["gap"] >= residual and _excludes_zero(ci(m, "P3"))
                and p3["clean_conservative_fpr"] <= max_fpr):
            go_retain = False

    if go_ordinary and go_retain:
        reasons.append("GO: ordinary gap >= %.2f in both models with checklist "
                       "persistence" % gap_th)
        return ("GO", reasons)

    reasons.append("INCONCLUSIVE: no KILL or GO pattern met")
    return ("INCONCLUSIVE", reasons)
