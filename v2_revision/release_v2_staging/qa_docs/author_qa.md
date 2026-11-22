# Author QA — MEDIUM severity-risk cases (RESOLVED)

Scope: the seven `severity_risk = MEDIUM` cases (b12, b15, b20, b25, b31, b34,
b39). These are benchmark-author quality-assurance decisions provided by the
author, recorded exactly as given. They are not human-subject data and not
experimental outcome data.

## Final decisions

- **b12 — REPLACE** (A=FAIL, B=QUESTIONABLE, C=FAIL, D=QUESTIONABLE) → retired, replaced by b41.
- **b15 — REPLACE** (A=FAIL, B=QUESTIONABLE, C=FAIL, D=QUESTIONABLE) → retired, replaced by b42.
- **b20 — REPLACE** (A=FAIL, B=QUESTIONABLE, C=QUESTIONABLE, D=PASS) → retired, replaced by b43.
- **b25 — REPLACE** (A=PASS, B=FAIL, C=QUESTIONABLE, D=PASS) → retired, replaced by b44.
- **b31 — REPLACE** (A=PASS, B=FAIL, C=QUESTIONABLE, D=PASS) → retired, replaced by b45.
- **b34 — KEEP** (A=PASS, B=QUESTIONABLE, C=QUESTIONABLE, D=PASS). Rationale: both COMMISSION and OMISSION fail the same intended-recipient delivery obligation (the room-212 guest does not receive the message); wrong-room delivery may add a secondary consequence, but the benchmark evaluates fulfillment of the designated-recipient obligation.
- **b39 — KEEP** (A=PASS, B=QUESTIONABLE, C=PASS, D=PASS). Rationale: both variants fail the same handoff obligation because reviewer Chen does not receive the findings; the Chen/Chan substitution is a near-miss identification error while the primary obligation and downstream non-delivery remain shared.

## Retired cases

| Original ID | Rule family | Failed dimension(s) | Replacement ID |
|---|---|---|---|
| b12 | temporal_ordering | A=FAIL, C=FAIL | b41 |
| b15 | temporal_ordering | A=FAIL, C=FAIL | b42 |
| b20 | preservation | A=FAIL | b43 |
| b25 | identification | B=FAIL | b44 |
| b31 | identification | B=FAIL | b45 |

Retired IDs (b12, b15, b20, b25, b31) are never reused.

## Kept cases

- b34 (commitment): KEEP with written rationale (above).
- b39 (commitment): KEEP with written rationale (above).

---

## b12 — temporal_ordering — REPLACE

- Target rule: the grounds must be tamped before the shot is pulled
- CLEAN: The barista tamps the grounds, then pulls the shot.
- COMMISSION: The barista pulls the shot, then tamps the grounds.
- OMISSION: The barista wipes the steam wand and the drip tray.
- Known concern: reversed ordering "pulls the shot, then tamps" is physically awkward.

| Check | Judgment |
|---|---|
| A — same underlying rule | FAIL |
| B — comparable narrative importance | QUESTIONABLE |
| C — no detectability confound | FAIL |
| D — naturalness | QUESTIONABLE |

## b15 — temporal_ordering — REPLACE

- Target rule: the reagent must be added before the flask is heated
- CLEAN: The chemist adds the reagent, then heats the flask.
- COMMISSION: The chemist heats the flask, then adds the reagent.
- OMISSION: The chemist adjusts the clamp height and the stir speed.
- Known concern: "heats the flask, then adds the reagent" is an unsafe, salient sequence.

| Check | Judgment |
|---|---|
| A — same underlying rule | FAIL |
| B — comparable narrative importance | QUESTIONABLE |
| C — no detectability confound | FAIL |
| D — naturalness | QUESTIONABLE |

## b20 — preservation — REPLACE

- Target rule: the sample must remain frozen for the whole transport
- CLEAN: The technician keeps the sample in the chilled carrier.
- COMMISSION: The technician lifts the sample out of the chilled carrier.
- OMISSION: The technician checks the cart wheel and the brake.
- Known concern: the "throughout" state is the hardest to render as a single obligation.

| Check | Judgment |
|---|---|
| A — same underlying rule | FAIL |
| B — comparable narrative importance | QUESTIONABLE |
| C — no detectability confound | QUESTIONABLE |
| D — naturalness | PASS |

## b25 — identification — REPLACE

- Target rule: the receipt must record holder name Dana Voss and no other name
- CLEAN: The clerk types the name Dana Voss on the receipt.
- COMMISSION: The clerk types the name Mara Voss on the receipt.
- OMISSION: The clerk adjusts the paper roll and the ribbon.
- Known concern: wrong name vs blank name may differ strongly in importance.

| Check | Judgment |
|---|---|
| A — same underlying rule | PASS |
| B — comparable narrative importance | FAIL |
| C — no detectability confound | QUESTIONABLE |
| D — naturalness | PASS |

## b31 — identification — REPLACE

- Target rule: the prescription must record patient name Lin Mei and no other name
- CLEAN: The pharmacist records patient name Lin Mei on the prescription.
- COMMISSION: The pharmacist records patient name Lin Wei on the prescription.
- OMISSION: The pharmacist checks the refill line and the date.
- Known concern: wrong name vs blank name may differ strongly in importance.

| Check | Judgment |
|---|---|
| A — same underlying rule | PASS |
| B — comparable narrative importance | FAIL |
| C — no detectability confound | QUESTIONABLE |
| D — naturalness | PASS |

## b34 — commitment — KEEP

- Target rule: the message must be delivered to the guest in room 212
- CLEAN: The clerk delivers the message to the guest in room 212.
- COMMISSION: The clerk delivers the message to the guest in room 122.
- OMISSION: The clerk refills the pen tray and the notepad.
- Known concern: 122 vs 212 is a digit transposition.

| Check | Judgment |
|---|---|
| A — same underlying rule | PASS |
| B — comparable narrative importance | QUESTIONABLE |
| C — no detectability confound | QUESTIONABLE |
| D — naturalness | PASS |

## b39 — commitment — KEEP

- Target rule: the findings must be forwarded to reviewer Chen
- CLEAN: The analyst forwards the findings to reviewer Chen.
- COMMISSION: The analyst forwards the findings to reviewer Chan.
- OMISSION: The analyst clears the clipboard and the scratch pad.
- Known concern: Chen vs Chan is a near-miss name confusion.

| Check | Judgment |
|---|---|
| A — same underlying rule | PASS |
| B — comparable narrative importance | QUESTIONABLE |
| C — no detectability confound | PASS |
| D — naturalness | PASS |

---

## Replacement QA (offline, structural)

The five replacements follow the author's matching rule (OMISSION keeps the
higher-level task with the required subevent/state/fact absent). Offline
structural QA: A (same underlying rule) = PASS for all; B/C/D = PASS (no
obvious severity or detectability confound; neutral VN/game settings). No
replacement has FAIL on any dimension.
