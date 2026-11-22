# Study 3 results (1,920/1,920 calls, USD 4.62, invalid 1.39%)

Analysis: frozen `src/analyze.py`, primary protocols P1-P3, units = case x model.
Strict and lenient (fence-stripping) parsing give the same verdicts.

## Pre-registered verdicts
| Arm | R_orig | R_rep | dR [boot95] | models dR>0 | cases dR>=0 | CLEAN target FPR orig->rep | COMMISSION recall orig->rep | Verdict |
|---|---|---|---|---|---|---|---|---|
| TRIGGER (b08,b13,b16) | 0.637 | 0.985 | +0.348 [0.148, 0.563] | 4/5 | 3/3 | 0.015 -> 0.000 | 0.970 -> 1.000 | **SUPPORTED** |
| STATE (b17,b18,b22) | 0.393 | 0.970 | +0.578 [0.385, 0.763] | 5/5 | 3/3 | 0.030 -> 0.326 | 0.993 -> 0.970 | **CONFOUNDED** (C2 failed) |

P4 (privileged target cue), reported separately: TRIGGER omission 0.533 -> 1.000,
CLEAN target FPR 0.022 -> 0.022; STATE omission 0.000 -> 0.800, CLEAN target FPR 0.000 -> 0.400.

Per model (P1-P3), omission recall ORIG -> REPAIR; CLEAN target FPR under REPAIR:
| Model | TRIGGER | STATE | STATE CLEAN FPR (rep) |
|---|---|---|---|
| gemini-3.8-flash | 0.15 -> 1.00 | 0.56 -> 0.96 | 1.00 |
| claude-sonnet-5 | 1.00 -> 1.00 | 0.48 -> 1.00 | 0.33 |
| gpt-6.1-sol | 0.26 -> 1.00 | 0.89 -> 1.00 | 0.30 |
| deepseek-v4.1-flash | 0.93 -> 1.00 | 0.04 -> 1.00 | 0.00 |
| qwen3.8-27b | 0.85 -> 0.93 | 0.00 -> 0.89 | 0.00 |

## Exploratory (post-hoc, labelled as such) diagnosis of the STATE confound
CLEAN target flags under REPAIR: b17 25, b22 9, b18 8 (of 45 each).
Responses state that the required state is confirmed at only one beat, e.g.
"Gate is confirmed shut only once at L2; no further confirmation that it stayed
closed through the rest of the inspection (L3-L6)." (claude-sonnet-5, b17, P1).
The v1 CLEAN preservation scenes confirm the state at a single beat. Their
CLEAN label therefore requires an inertia reading (the state persists unless
changed), while the OMISSION label requires rejecting that same reading.
No single reading makes all three labels of these triplets correct:
under inertia, OMISSION is not a violation; under explicit evidence, CLEAN is.
Evaluators also differ in their default reading (gemini flags CLEAN 1.00 under
the explicit-evidence sentence; deepseek and qwen 0.00).
