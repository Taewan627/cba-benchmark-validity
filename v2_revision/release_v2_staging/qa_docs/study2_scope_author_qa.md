# Study 2 (scope) — author QA (RESOLVED)

Author QA for the POINT vs SCOPE verification-structure construct. Benchmark
construction QA, not a human-subject study and not experimental data.

Judgment fields:
- A — Is this genuinely POINT or SCOPE verification?
- B — Could the SCOPE omission be detected from a single beat?
- C — Are POINT and SCOPE cases comparable in difficulty?
- D — Are commission and omission variants semantically matched?
- E — Does the oracle logically entail the omission label?

## Author rationale (scope)

> The omission cannot be inferred from any single narrative beat. Because the
> required event may validly occur anywhere within the bounded six-beat scope,
> the auditor must inspect the complete scope before establishing its absence.
> In contrast, an explicit incompatible event provides a local positive witness
> for the commission violation.

## Author decisions

| Family | Structure | A | B | C | D | E |
|---|---|---|---|---|---|---|
| identity_checkpoint | point | PASS | PASS | PASS | PASS | PASS |
| placement_checkpoint | point | PASS | PASS | PASS | PASS | PASS |
| recipient_checkpoint | point | PASS | PASS | PASS | PASS | PASS |
| any_of_scope_obligation | scope | PASS | PASS | PASS | PASS | PASS |
| by_end_resolution | scope | PASS | PASS | PASS | PASS | PASS |
| across_scope_required_event | scope | PASS | PASS | PASS | PASS | PASS |

## Construction repairs recorded before these decisions

- POINT omission lexical cues: 20 `without …` omissions (placement + recipient)
  were rewritten to local checkpoint states ("the board hook stays empty …",
  "at the campfire, the guide has no note"), so the sentence states the local
  state rather than the omission action.
- Naturalness: three recipient cases had the approach beat after the delivery
  beat; the approach beats were replaced with post-arrival actions.

No scientific construct, rule, family, target position, or threshold changed.

## Representative examples

**SCOPE (any_of_scope_obligation)** — "before the chapter ends, the player must
report the symbol to Mira at least once." CLEAN: report occurs at one beat.
COMMISSION: report to the wrong scout. OMISSION: all six beats proceed with no
report.

**POINT (identity_checkpoint)** — "at the checkpoint, the receipt must show the
name Anil Rao." CLEAN: Anil Rao present. COMMISSION: Amit Rao present.
OMISSION: the receipt is completed with the name field absent.
