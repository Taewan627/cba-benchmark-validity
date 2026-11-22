"""Study 3: build ORIGINAL and REPAIRED triplets for the six Study-1 base cases
whose held-out omission nondetections were audited as ambiguous renderings.

Reads the frozen v1 cases (public_release/data/confirmatory_cases.jsonl, never
modified) and writes data/study3_cases.jsonl. Each repair is ONE pre-specified
edit matched to the defect type recorded in the Study-1 audit:

  TRIGGER arm (b08, b13, b16): the audit found responses treating the
    obligation as untriggered because the triggering event was absent.
    Repair = make the triggering event occur, leaving the required act absent
    in OMISSION.
  STATE arm (b17, b18, b22): the audit found responses treating the absence
    of a contrary change as satisfaction (inertia reading) while the scene
    never establishes the required state. Repair = one disambiguating sentence
    appended to the setup of all three variants.

b34 is excluded: its only audited nondetection was a transport failure (no
substantive response).
"""
import copy, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # CBA_IEEE_Submission_Final
V1 = ROOT / "public_release" / "data" / "confirmatory_cases.jsonl"
OUT = Path(__file__).resolve().parents[1] / "data" / "study3_cases.jsonl"

TRIGGER = ("b08", "b13", "b16")
STATE = ("b17", "b18", "b22")
STATE_SENTENCE = ("A required state counts as maintained only if a line "
                  "explicitly shows it.")

# (case, condition) -> (line_id, new_text, new_event_id) ; condition "*" = all
TRIGGER_EDITS = {
    ("b08", "*"): ("L6", "The botanist starts the noon watering.", "ev_noon_watering"),
    ("b13", "OMISSION"): ("L4", "The nurse draws the dose.", "ev_draw_without_label"),
    ("b16", "OMISSION"): ("L5", "The driver opens the cargo doors.", "ev_doors_without_brake"),
}


def render_script(beats):
    return "\n".join("%s: %s" % (b["line_id"], b["text"]) for b in beats)


def word_count(case):
    return len(case["setup"].split()) + sum(len(b["text"].split()) for b in case["beats"])


def repair(case):
    c = copy.deepcopy(case)
    bid, cond = c["base_case_id"], c["condition"]
    edits = []
    if bid in TRIGGER:
        for key in ((bid, "*"), (bid, cond)):
            if key in TRIGGER_EDITS:
                line, text, ev = TRIGGER_EDITS[key]
                for b in c["beats"]:
                    if b["line_id"] == line:
                        edits.append({"line_id": line, "old": b["text"], "new": text})
                        old_ev = b["event_id"]
                        b["text"], b["event_id"] = text, ev
                        c["observed_events"] = [ev if e == old_ev else e for e in c["observed_events"]]
        c["script"] = render_script(c["beats"])
    elif bid in STATE:
        c["setup"] = c["setup"] + " " + STATE_SENTENCE
        edits.append({"setup_append": STATE_SENTENCE})
    else:
        raise ValueError(bid)
    c["repair_edits"] = edits
    return c


def main():
    v1 = [json.loads(l) for l in V1.open(encoding="utf-8")]
    keep = [r for r in v1 if r["base_case_id"] in TRIGGER + STATE]
    assert len(keep) == 18, len(keep)
    out = []
    for r in keep:
        arm = "TRIGGER" if r["base_case_id"] in TRIGGER else "STATE"
        o = copy.deepcopy(r); o.update(version="ORIG", arm=arm, repair_edits=[])
        p = repair(r); p.update(version="REPAIR", arm=arm)
        p["identical_to_orig"] = (p["setup"] == o["setup"] and p["script"] == o["script"])
        # oracle label unchanged by design: CLEAN false, corrupt true
        assert p["oracle_label"] == o["oracle_label"]
        out.append(o); out.append(p)
    # within-triplet word-count tolerance (10%), as in Study 1
    for ver in ("ORIG", "REPAIR"):
        for bid in TRIGGER + STATE:
            wc = [word_count(c) for c in out if c["base_case_id"] == bid and c["version"] == ver]
            spread = (max(wc) - min(wc)) / max(wc)
            print("%s %-6s wc=%s spread=%.3f %s" % (bid, ver, wc, spread, "OK" if spread <= 0.10 else "FAIL"))
            assert spread <= 0.10
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("x", encoding="utf-8") as f:
        for c in out:
            f.write(json.dumps(c, ensure_ascii=False, sort_keys=True) + "\n")
    print("wrote", OUT, len(out), "variants;",
          sum(c["identical_to_orig"] for c in out if c["version"] == "REPAIR"), "repaired variants identical to ORIG")


if __name__ == "__main__":
    main()
