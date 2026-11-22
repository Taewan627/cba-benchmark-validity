"""Concrete prompt rendering and leakage screening.

Prompts are rendered deterministically from the frozen case representation.
Only the assigned protocol changes across calls. All protocols see the setup
(which embeds the requirements with neutral keys) and the script; P2/P3 add an
explicit rule catalog; P4 adds the privileged target requirement as a
verification cue. Oracle-only fields are never rendered.

Leakage checks verify, per message, that:

* no condition label (CLEAN / COMMISSION / OMISSION) appears,
* no oracle event id (expected, incompatible, or observed) appears,
* no sibling-variant text appears,
* the target requirement is not singled out in P1-P3 (it appears only as part
  of the setup / catalog), and
* the condition word never occurs in system or user text.
"""

from __future__ import annotations

from src.spec import CONDITIONS

PROTOCOLS = ("P1", "P2", "P3", "P4")

_SYSTEM = (
    "You are a meticulous auditor of a short, bounded narrative scene. "
    "Judge only the events explicitly described in the scene; do not invent "
    "events, assume events outside the described beats, or rely on external "
    "knowledge. Every line is labeled with an id such as L1, L2. "
    "Respond with a single JSON object and nothing else, using the schema "
    "described in the instructions."
)

_OUTPUT_SCHEMA = (
    "Output format (JSON only): "
    '{"judgments":[{"rule_id":"<id>","violation_detected":true|false,'
    '"violation_type":"wrong_state"|"missing_state"|null,'
    '"evidence_line_ids":["L.."],"reason":"brief"}],'
    '"expectations":[{"rule_id":"<id>","expected_requirement":"..."}]}. '
    "For every requirement you judge, emit one judgment with a boolean "
    "violation_detected. Use violation_type wrong_state when the scene shows "
    "an explicit state that conflicts with the requirement, missing_state "
    "when the required state is absent, and null when you do not claim a "
    "type. evidence_line_ids must reference only labels that actually appear "
    "in the scene. Do not add text outside the JSON object."
)

_P4_OUTPUT_SCHEMA = (
    "Output format (JSON only): "
    '{"judgments":[{"rule_id":"<id>","violation_detected":true|false,'
    '"fulfilled":true|false,"evidence_line_ids":["L.."],"reason":"brief"}]}. '
    "Emit exactly one judgment for the requirement. fulfilled must be a "
    "boolean (true if the requirement is fulfilled, false if it is violated), "
    "and violation_detected must be the opposite of fulfilled. "
    "evidence_line_ids must reference only labels that actually appear in the "
    "scene. Do not add text outside the JSON object."
)

_P1_TASK = (
    "Inspect the scene below for consistency and completeness. Report every "
    "requirement stated in the scene that is violated."
)

_P2_TASK = (
    "Below is the scene and the full list of applicable requirements. Report "
    "every requirement that is violated."
)

_P3_TASK = (
    "Below is the scene and the full list of applicable requirements. First "
    "enumerate each requirement you intend to check in the expectations "
    "field, then verify each one against the scene and emit one judgment per "
    "enumerated requirement."
)

_P4_TASK = (
    "Below is the scene and one specific requirement. Determine whether that "
    "requirement is fulfilled. Emit exactly one judgment for the requirement, "
    "with a boolean fulfilled field (true if fulfilled, false if violated)."
)


def _setup_block(case):
    return "Scene setup:\n" + case["setup"]


def _script_block(case):
    return "Scene:\n" + case["script"]


def _catalog_block(case):
    lines = ["Applicable requirements:"]
    for rid in sorted(case["rules"]):
        lines.append("%s: %s" % (rid, case["rules"][rid]))
    return "\n".join(lines)


def build_messages(case, protocol):
    if protocol not in PROTOCOLS:
        raise ValueError("Unknown protocol: %r" % protocol)

    parts = [_setup_block(case)]
    if protocol in ("P2", "P3"):
        parts.append(_catalog_block(case))
    parts.append(_script_block(case))

    if protocol == "P1":
        task = _P1_TASK
    elif protocol == "P2":
        task = _P2_TASK
    elif protocol == "P3":
        task = _P3_TASK
    elif protocol == "P4":
        parts.append("Requirement to verify:\n%s: %s"
                     % (case["rule_id"], case["target_requirement"]))
        task = _P4_TASK
    else:  # pragma: no cover
        raise ValueError("Unknown protocol: %r" % protocol)

    schema = _P4_OUTPUT_SCHEMA if protocol == "P4" else _OUTPUT_SCHEMA
    user = "\n\n".join(parts + [task, schema])
    return [
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": user},
    ]


def check_leakage(case, protocol, messages):
    """Return a list of leakage violation strings (empty means clean)."""
    violations = []
    joined = "\n".join(m["content"] for m in messages).lower()

    for condition in CONDITIONS:
        if condition.lower() in joined:
            violations.append("condition label %r appears in prompt" % condition)

    oracle_ids = [case["expected_event"], *case["incompatible_events"],
                  *case["observed_events"]]
    for oid in oracle_ids:
        if str(oid) and str(oid).lower() in joined:
            violations.append("oracle event id %r leaks into prompt" % oid)

    if protocol != "P4":
        cue = "Requirement to verify:"
        if cue.lower() in joined:
            violations.append("target singled out in non-P4 prompt")

    return violations


def check_triplet_leakage(variants):
    """Cross-check a triplet: no prompt leaks a sibling variant's target text.

    Returns a list of violation strings. The three variants of one base case
    must never be co-present, and each rendered prompt must not contain the
    target-beat text of the other two conditions.
    """
    violations = []
    target_texts = {}
    for v in variants:
        target_beat = next(b for b in v["beats"] if b.get("is_target"))
        target_texts[v["condition"]] = target_beat["text"].strip()

    for v in variants:
        for protocol in PROTOCOLS:
            messages = build_messages(v, protocol)
            violations.extend(check_leakage(v, protocol, messages))
            joined = "\n".join(m["content"] for m in messages).lower()
            for condition, text in target_texts.items():
                if condition != v["condition"] and text and text.lower() in joined:
                    violations.append(
                        "%s/%s prompt leaks sibling %s target text"
                        % (v["base_case_id"], protocol, condition))
    return violations
