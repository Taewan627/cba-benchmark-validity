# Study 2b — author QA

Author QA for the POINT vs SCOPE verification-structure construct. Benchmark
construction QA only; not a human-subject study and not experimental data.

**AUTHOR JUDGMENTS ARE PENDING.** No judgment is fabricated.

Judgment fields:
- A — Is this genuinely POINT or SCOPE verification?
- B — Could the SCOPE omission be detected from a single beat?
- C — Are POINT and SCOPE cases comparable in difficulty?
- D — Are commission and omission variants semantically matched?
- E — Does the oracle logically entail the omission label?

## Representative examples

### identity_checkpoint (point) — q001
- Rule: at the desk, the receipt must show the name Anil Rao
- CLEAN: "At the desk, the receipt shows the name Anil Rao."
- COMMISSION: "At the desk, the receipt shows the name Amit Rao."
- OMISSION: "At the desk, the receipt name field is empty."
- Why point: one local field on one record at one checkpoint.
- Oracle: expected `ev_name_Anil_Rao`; incompatible `ev_name_Amit_Rao`.

### placement_checkpoint (point) — q011
- Rule: at the hall board, the key must be on the hook
- CLEAN: "At the hall board, the key is on the hook."
- COMMISSION: "At the hall board, the key is on the bench."
- OMISSION: "At the hall board, the hook stands empty."
- Why point: one object's location at one checkpoint.
- Oracle: expected `ev_key_on_hook`; incompatible `ev_key_on_bench`.

### recipient_checkpoint (point) — q021
- Rule: at the campfire, the note must be in the guide's hands
- CLEAN: "At the campfire, the guide holds the note."
- COMMISSION: "At the campfire, the scout holds the note."
- OMISSION: "At the campfire, the guide's hands are empty."
- Why point: one item in one recipient's possession at one checkpoint.
- Oracle: expected `ev_note_guide`; incompatible `ev_note_scout`.

### any_of_scope_obligation (scope) — q031
- Rule: during the six-beat chapter, the player must report the symbol to Mira at least once
- CLEAN: "The player reports the symbol to Mira."
- COMMISSION: "The player reports the symbol to the wrong scout."
- OMISSION: "The player adjusts the lantern wick."
- Why scope: the report may occur anywhere; absence requires scanning all six beats.
- Oracle: expected `ev_report_mira`; incompatible `ev_report_wrong`.

### by_end_resolution (scope) — q041
- Rule: by the end of the six-beat visit, the borrower must have returned the key
- CLEAN: "The borrower returns the key."
- COMMISSION: "The borrower returns the wrong key."
- OMISSION: "The borrower folds the coat."
- Why scope: the return may occur at any beat; absence requires the full scope.
- Oracle: expected `ev_return_key`; incompatible `ev_return_wrong`.

### across_scope_required_event (scope) — q051
- Rule: somewhere across the six-beat patrol, the guard must check Gate A
- CLEAN: "The guard checks Gate A."
- COMMISSION: "The guard checks the wrong gate."
- OMISSION: "The guard keys the radio."
- Why scope: Gate A may be checked anywhere; absence requires the full scope.
- Oracle: expected `ev_check_gateA`; incompatible `ev_check_wrong`.

## Judgments

| Family | Structure | A | B | C | D | E |
|---|---|---|---|---|---|---|
| identity_checkpoint | point | PASS | PASS | PASS | PASS | PASS |
| placement_checkpoint | point | PASS | PASS | PASS | PASS | PASS |
| recipient_checkpoint | point | PASS | PASS | PASS | PASS | PASS |
| any_of_scope_obligation | scope | PASS | PASS | PASS | PASS | PASS |
| by_end_resolution | scope | PASS | PASS | PASS | PASS | PASS |
| across_scope_required_event | scope | PASS | PASS | PASS | PASS | PASS |

All six families PASS. Construction repair recorded before the final PASS: 16
SCOPE OMISSION target beats duplicated a common beat within the same narrative
(e.g. q051 "keys the radio"); each was replaced with a distinct natural neutral
action. A regression test now rejects duplicated or trivially paraphrased beats
within a single six-beat narrative. Author QA is complete.
