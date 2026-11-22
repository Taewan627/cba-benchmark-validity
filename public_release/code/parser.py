"""Deterministic evaluator-output parser.

The evaluator is instructed to return a single JSON object. This module parses
that object into a fixed intermediate representation and *never* uses an LLM or
free-text scoring to interpret it. Determinism means: the same raw text and the
same rule catalog always produce the same parse result.

Contract (evaluator-facing output):

    {
      "judgments": [
        {
          "rule_id": "r01",               // must be a known catalog key
          "violation_detected": true,     // must be a JSON boolean
          "violation_type": "commission", // optional; "commission"|"omission"
          "evidence_line_ids": ["L3"],    // optional; evaluator-facing line ids
          "reason": "short justification" // optional; never scored
        }
      ],
      "expectations": [                    // P3 only; may be absent/empty
        {"rule_id": "r01", "expected_requirement": "..."}
      ]
    }

P4 instead returns a single judgment with ``fulfilled`` (boolean). The parser
maps ``fulfilled`` to ``violation_detected = not fulfilled`` for the supplied
target rule and does not infer anything from prose.

Handling rules (all deterministic):

* Malformed JSON / not an object / missing ``judgments``        -> invalid
* ``judgments`` not a list                                      -> invalid
* judgment missing ``rule_id`` or ``violation_detected``        -> invalid
* ``violation_detected`` not a JSON boolean (e.g. "maybe",
  "uncertain", 1) -> invalid (hedged answers are not silently
  coerced)
* unknown ``rule_id``                                           -> invalid
* the same ``rule_id`` reported twice with conflicting boolean  -> invalid
* unknown ``violation_type`` is NOT invalid; it is recorded as
  ``violation_type`` but never affects primary detection
* an explicit ``abstained: true`` with an empty judgment list is
  valid and yields zero flags (nondetection / no false positive)

The parse result is the single input to ``deterministic_scoring.score``.
"""

from __future__ import annotations

import json

VIOLATION_TYPES = ("wrong_state", "missing_state")


class ParserFailure(ValueError):
    """Raised internally for any deterministic parse failure."""


def _json_bool(value):
    return type(value) is bool


def parse(raw, known_rule_ids, protocol=None):
    """Parse raw evaluator text into the intermediate representation.

    ``known_rule_ids`` is the rule catalog for the case (a set of ids). A
    ``ParserFailure`` is converted to ``{"valid": False}`` rather than raised,
    so callers treat malformed output uniformly.
    """
    try:
        return _parse(raw, known_rule_ids, protocol)
    except ParserFailure:
        return {
            "valid": False,
            "flagged_rule_ids": [],
            "expectation_rule_ids": [],
            "fulfilled": None,
            "abstained": False,
            "violation_types": {},
            "error": "parser_failure",
        }


def _parse(raw, known_rule_ids, protocol):
    if isinstance(raw, bytes):
        try:
            raw = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise ParserFailure("undecodable bytes")

    if not isinstance(raw, str):
        raise ParserFailure("raw output is not text")

    try:
        obj = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        raise ParserFailure("invalid JSON")

    if not isinstance(obj, dict):
        raise ParserFailure("output is not a JSON object")

    if "judgments" not in obj:
        raise ParserFailure("missing judgments")

    judgments = obj["judgments"]
    if not isinstance(judgments, list):
        raise ParserFailure("judgments is not a list")

    flagged = set()
    violation_types = {}
    for j in judgments:
        if not isinstance(j, dict):
            raise ParserFailure("judgment is not an object")
        if "rule_id" not in j or "violation_detected" not in j:
            raise ParserFailure("judgment missing rule_id or violation_detected")
        rule_id = j["rule_id"]
        if not isinstance(rule_id, str) or rule_id not in known_rule_ids:
            raise ParserFailure("unknown rule_id %r" % rule_id)
        if not _json_bool(j["violation_detected"]):
            raise ParserFailure("violation_detected is not a boolean")
        if rule_id in violation_types and violation_types[rule_id] != j["violation_detected"]:
            raise ParserFailure("conflicting judgments for rule %r" % rule_id)
        violation_types[rule_id] = j["violation_detected"]
        if j["violation_detected"]:
            flagged.add(rule_id)
        if "violation_type" in j and j["violation_type"] is not None:
            violation_types[rule_id] = (j["violation_detected"],
                                        j["violation_type"])

    expectations = _parse_expectations(obj.get("expectations"), known_rule_ids)

    fulfilled = None
    if protocol == "P4":
        if len(judgments) != 1:
            raise ParserFailure("P4 requires exactly one judgment")
        only = judgments[0]
        if "fulfilled" not in only or not _json_bool(only["fulfilled"]):
            raise ParserFailure("P4 requires a boolean fulfilled")
        fulfilled = only["fulfilled"]
        if only["violation_detected"] != (not fulfilled):
            raise ParserFailure("P4 violation_detected contradicts fulfilled")

    abstained = obj.get("abstained") is True and not judgments

    return {
        "valid": True,
        "flagged_rule_ids": sorted(flagged),
        "expectation_rule_ids": sorted(expectations),
        "fulfilled": fulfilled,
        "abstained": bool(abstained),
        "violation_types": violation_types,
        "error": None,
    }


def _parse_expectations(raw, known_rule_ids):
    if raw is None:
        return set()
    if not isinstance(raw, list):
        raise ParserFailure("expectations is not a list")
    out = set()
    for entry in raw:
        if not isinstance(entry, dict) or "rule_id" not in entry:
            raise ParserFailure("expectation entry missing rule_id")
        rid = entry["rule_id"]
        if not isinstance(rid, str) or rid not in known_rule_ids:
            raise ParserFailure("unknown expectation rule_id %r" % rid)
        out.add(rid)
    return out


def violation_type_of(parsed, rule_id):
    """Return the recorded violation_type string, or None if absent/unknown."""
    value = parsed.get("violation_types", {}).get(rule_id)
    if isinstance(value, tuple):
        return value[1]
    return None
