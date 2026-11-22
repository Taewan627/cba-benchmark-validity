# Study 2 v1 commission/omission descriptive recovery

## Mandatory interpretation boundary

**POST-HOC DESCRIPTIVE ONLY**  
**BENCHMARK QUALITY FAILURE**  
**NOT VALID MECHANISM EVIDENCE**

Study 2 v1 failed its negative-control quality gate: conservative CLEAN
false-positive rate was **50/120 = 41.7%**. The statistics below show what the
frozen invalid benchmark produced. They do not rehabilitate Study 2 v1, test a
scope mechanism, or support a substantive POINT/SCOPE conclusion.

No experiment or API call was run. Counts were recovered exactly from
`results/study2_v1/scores.jsonl` and checked
against its frozen `result_manifest.json`.

## Scoring convention

- Recall is `detected / all frozen corrupt rows`; parser-invalid rows remain
  nondetections under the frozen intention-to-evaluate scoring.
- `G = commission recall - omission recall`.
- Conservative CLEAN FPR counts both substantive CLEAN flags and invalid CLEAN
  outputs.
- POINT and SCOPE each contain 30 base cases evaluated by two fixed models,
  giving 60 rows per condition and structure.

## Pooled descriptive results

| Quantity | Count | Rate |
|---|---:|---:|
| Commission recall | 117/120 | 0.9750 |
| Omission recall | 115/120 | 0.9583 |
| Gap `G` | — | +0.0167 |
| Conservative CLEAN FPR | 50/120 | 0.4167 |
| Parser-invalid/malformed rows, all conditions | 15/360 | 0.0417 |

These near-ceiling corrupt-condition recalls do not offset the failed CLEAN
control. The pooled gap is descriptive only.

## POINT/SCOPE descriptive breakdown

| Structure | Commission recall | Omission recall | `G` | Conservative CLEAN FPR | Invalid rows, all conditions |
|---|---:|---:|---:|---:|---:|
| POINT | 60/60 = 1.0000 | 59/60 = 0.9833 | +0.0167 | 24/60 = 0.4000 | 6/180 = 0.0333 |
| SCOPE | 57/60 = 0.9500 | 56/60 = 0.9333 | +0.0167 | 26/60 = 0.4333 | 9/180 = 0.0500 |

The descriptive interaction is `G_scope - G_point = 0.0000`, matching the
frozen manifest. It is **not interpretable as evidence for or against the
proposed scope account** because both structures fail the CLEAN quality gate.

## Evaluator-specific descriptive breakdown

| Evaluator | Commission recall | Omission recall | `G` | Conservative CLEAN FPR | Invalid rows |
|---|---:|---:|---:|---:|---:|
| Claude | 59/60 = 0.9833 | 59/60 = 0.9833 | 0.0000 | 16/60 = 0.2667 | 3/180 = 0.0167 |
| Gemini | 58/60 = 0.9667 | 56/60 = 0.9333 | +0.0333 | 34/60 = 0.5667 | 12/180 = 0.0667 |

### Evaluator by structure

| Evaluator | Structure | Commission recall | Omission recall | `G` | Conservative CLEAN FPR | Invalid rows |
|---|---|---:|---:|---:|---:|---:|
| Claude | POINT | 30/30 = 1.0000 | 30/30 = 1.0000 | 0.0000 | 11/30 = 0.3667 | 2/90 = 0.0222 |
| Claude | SCOPE | 29/30 = 0.9667 | 29/30 = 0.9667 | 0.0000 | 5/30 = 0.1667 | 1/90 = 0.0111 |
| Gemini | POINT | 30/30 = 1.0000 | 29/30 = 0.9667 | +0.0333 | 13/30 = 0.4333 | 4/90 = 0.0444 |
| Gemini | SCOPE | 28/30 = 0.9333 | 27/30 = 0.9000 | +0.0333 | 21/30 = 0.7000 | 8/90 = 0.0889 |

## Invalid/malformed row census

There are 15 parser-invalid rows:

| Dimension | Invalid count |
|---|---:|
| CLEAN | 8 |
| COMMISSION | 2 |
| OMISSION | 5 |
| POINT | 6 |
| SCOPE | 9 |
| Claude | 3 |
| Gemini | 12 |

The eight invalid CLEAN rows are included in the conservative CLEAN FPR. The
seven invalid corrupt rows are retained as nondetections. Raw responses were
not required to recover these frozen descriptive counts, although they would
be required to diagnose the specific parser failures.

## Why these results remain non-mechanistic

1. The 41.7% conservative CLEAN FPR shows that nominally correct scenes did
   not function as valid negative controls.
2. The existing post-hoc CLEAN audit identifies benchmark defects, ambiguity,
   parser/schema artifacts, and evaluator-attributed behavior among the 50
   flagged rows; it is author-coded and not independently adjudicated.
3. Once the negative control fails, a high corrupt-condition detection rate or
   a small commission/omission gap cannot be cleanly attributed to the intended
   auditing construct.
4. The POINT/SCOPE equality of descriptive gaps is therefore not a valid null
   mechanism result.

No confidence interval or inferential test was newly calculated for Study 2
v1. The frozen decision remains **INCONCLUSIVE because benchmark quality
failed**.
