# Study 2b exact case-level permutation sensitivity

## Status

**OFFLINE SENSITIVITY ANALYSIS ONLY.** This is not confirmatory, does not
replace the frozen percentile cluster bootstrap, and does not change the
frozen Study 2b result:

- `Delta_scope = +0.0167`
- frozen cluster-bootstrap 95% CI `[-0.0333, 0.0667]`
- pre-specified practical threshold `+0.15`

No benchmark, score, analysis decision, or API output was changed. The analysis
uses the 360 stored scored rows in
`results/study2b/scores.jsonl`.

## Estimand and case-level reduction

For base case `i`, retain the two fixed evaluator outcomes as a pair and define

```text
d_i = mean over evaluators (commission_detected - omission_detected).
```

The structure gap is the mean `d_i` over its 30 cases, and the interaction is

```text
Delta_scope = mean(d_i | SCOPE) - mean(d_i | POINT).
```

This is the same case-level pairing/averaging logic as the frozen analysis.
Evaluator calls are not treated as independent cases.

All 120 Study 2b omission rows are detected. The only nonzero case-level
differences are:

| Case | Structure | Frozen row-level cause | `d_i` |
|---|---|---|---:|
| q001 | POINT | Claude commission output invalid/nondetected; other evaluator detected | -0.5 |
| q026 | POINT | Claude valid commission nondetection; other evaluator detected | -0.5 |
| q043 | SCOPE | Gemini commission output invalid/nondetected; other evaluator detected | -0.5 |

The other 57 cases have `d_i = 0`. Therefore:

- POINT: two `-0.5` cases and 28 zero cases, mean `-1/30 = -0.0333`;
- SCOPE: one `-0.5` case and 29 zero cases, mean `-0.5/30 = -0.0167`;
- interaction: `-0.0167 - (-0.0333) = +0.0167`.

## Exact permutation method

The sensitivity null is:

> **H0 (case-label exchangeability):** conditional on the 60 observed
> case-level paired outcomes `d_i`, their distribution is invariant to which
> 30 cases are labeled POINT and which 30 are labeled SCOPE. Equivalently,
> structure has no effect on the distribution of `d_i` under this hypothetical
> exchangeability model.

The exact permutation retains each case and its paired two-evaluator average
intact, and retains group sizes of 30 POINT and 30 SCOPE. It enumerates the
`choose(60,30) = 118,264,581,564,861,424` equally weighted label allocations
analytically. Because the 57 zero cases are interchangeable, the distribution
depends only on `k`, the number of the three `-0.5` cases assigned to SCOPE.

| `k` in SCOPE | Permuted `Delta_scope` | Exact probability |
|---:|---:|---:|
| 0 | +0.0500 | 0.118644 |
| 1 | +0.0167 (observed) | 0.381356 |
| 2 | -0.0167 | 0.381356 |
| 3 | -0.0500 | 0.118644 |

Under this exchangeability null:

- one-sided `P(Delta_perm >= Delta_observed) = 0.5000`;
- two-sided `P(|Delta_perm| >= |Delta_observed|) = 1.0000`; and
- the full attainable permutation range is `[-0.0500, +0.0500]`.

Thus there is no exact-permutation evidence for a positive POINT-SCOPE
interaction. Conditional on the observed case-level outcomes, no admissible
30/30 reassignment can produce an interaction as large as `+0.15`; the maximum
is `+0.05`.

## Relationship to the +0.15 practical threshold

The permutation test directly tests the zero-effect/exchangeability null, not
the nonzero composite null `Delta_scope >= +0.15`. The fact that `+0.15` is
outside the entire conditional permutation support is a sensitivity result,
not a new confidence interval and not a formal equivalence test.

Within its stated assumptions, the exact analysis produces **no evidence
compatible with an observed case-label interaction as large as +0.15**. This
agrees with, but does not replace, the frozen bootstrap conclusion whose upper
bound is `+0.0667`.

The cases were authored into distinct POINT and SCOPE families rather than
randomly assigned between structures. Exchangeability is therefore a
hypothetical robustness assumption, not a design-based causal guarantee. The
permutation result must remain sensitivity-only.

## Why no call-level exact/binomial test is reported

A binomial analysis treating 120 evaluator calls per condition as independent
would violate the requested case-level dependence structure: two fixed models
are paired within each case, and commission and omission are matched within
case. Collapsing to “any evaluator missed” would instead change the estimand.
For those reasons, no call-level binomial bound is presented as if it were an
exact analysis of the frozen interaction.

## Ceiling limitation

POINT omission recall is `1.000`, and SCOPE omission recall is `1.000`.
Consequently:

- every nonzero `d_i` is driven by a commission nondetection, including two
  parser-invalid commission outputs;
- the analysis has no observed omission-error variation from which to estimate
  a subtle structure-dependent omission effect; and
- small or harder-to-elicit omission effects remain weakly identified despite
  the result being inconsistent with a practically large `+0.15` interaction
  under the tested operationalization.

The appropriate conclusion is unchanged: Study 2b does not support a pooled
interaction as large as `+0.15` in this setting, but it does not establish the
universal absence of scope effects or smaller omission-related differences.
