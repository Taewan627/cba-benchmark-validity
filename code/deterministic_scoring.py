"""Scores parsed decisions only; no semantic judge or free-text parser.

``score`` consumes the intermediate representation produced by
``src.parser.parse`` (or an equivalent dict). The primary detection decision
depends only on whether the target ``rule_id`` is present in the flagged set and
on whether the output was valid. Evidence length, reason text, and violation
type never affect detection -- so verbosity cannot be rewarded.

Returned keys:

* ``valid``                         parser success
* ``abstained``                     explicit refusal / empty judgment list
* ``detected``                      target violation flagged on a corrupt case
* ``false_positive``                CLEAN with any flagged rule
* ``conservative_false_positive``   CLEAN, counting invalid as false positive
* ``off_target_count``              flagged rules other than the target
* ``expectation_present``           target rule explicitly enumerated (P3)
* ``violation_type``                reported type for the target, if any
* ``violation_type_correct``        whether it matches the case (secondary)
"""

from __future__ import annotations

EXPECTED_VIOLATION_TYPE = {
    "COMMISSION": "wrong_state",
    "OMISSION": "missing_state",
}


def score(case, output):
    valid = output.get("valid") is True
    flags = set(output.get("flagged_rule_ids", [])) if valid else set()
    expected = set(output.get("expectation_rule_ids", [])) if valid else set()
    clean = case["condition"] == "CLEAN"
    target = case["rule_id"]

    reported_type = None
    types = output.get("violation_types", {})
    if target in types:
        value = types[target]
        reported_type = value[1] if isinstance(value, tuple) else None

    type_correct = None
    if not clean and reported_type is not None:
        type_correct = reported_type == EXPECTED_VIOLATION_TYPE[case["condition"]]

    return {
        "valid": valid,
        "abstained": bool(output.get("abstained")) if valid else False,
        "detected": valid and not clean and target in flags,
        "false_positive": clean and valid and bool(flags),
        "conservative_false_positive": clean and (not valid or bool(flags)),
        "off_target_count": len(flags - {target}),
        "expectation_present": valid and target in expected,
        "violation_type": reported_type,
        "violation_type_correct": type_correct,
    }
