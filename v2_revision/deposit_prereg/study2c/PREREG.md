# Study 2c pre-registration: crossed POINT/SCOPE interaction without cue artifacts

Status: FROZEN before any Study-2c model call. Written 2026-11-19 (KST).
SHA-256 of this file, the case file, builder, validator, runner, and analysis code are in `FREEZE.json`.
Deviations after freezing are logged in `DEVIATIONS.md`.

## 1. Why
Study 2b excluded a POINT-SCOPE interaction of +0.15 under the frozen bootstrap, but (i) omission recall sat at 1.000
(ceiling), (ii) the SCOPE COMMISSION cases contained the cue word "wrong", (iii) POINT OMISSION cases contained an
explicit absence statement, (iv) POINT and SCOPE were different obligations, not the same obligation in both forms,
(v) one rule per case, (vi) two evaluators. Study 2c removes (ii)-(vi) and tests whether (i) can be avoided.

## 2. Design
- 24 obligations (8 recipient, 8 location, 8 identity), each rendered as POINT and SCOPE with the same target slot.
- Rule r01 is conjunctive: "must DO(A), and must not DO(B)". Two further background rules r02, r03 are satisfied in every variant.
- Four variants per structure: CLEAN (A, no B), COMMISSION (B in the target slot, no A), OMISSION (neutral action, neither A nor B),
  ADD (A in the target slot plus B in a later slot: contrary evidence without absence).
- 192 cases (24 x 2 x 4). Six beats each. No evaluative wording, no explicit absence statements (checked by `validate.py`).
- Protocol P2 only (rule-aware), frozen v1 renderer, strict frozen parser, frozen scorer (ADD scored as a violation case).
- Evaluators: google/gemini-3.8-flash, anthropic/claude-sonnet-5, openai/gpt-6.1-sol, deepseek/deepseek-v4.1-flash-1017, qwen/qwen3.8-27b.
- 2 repetitions each (seed 1731+rep); Study 3 request body (disable-reasoning flag sent where accepted). 1,920 calls planned; budget cap USD 7.

## 3. Estimands
G_structure = COMMISSION recall - OMISSION recall (target-rule detection). Delta = G_SCOPE - G_POINT.
Secondary: Delta computed with ADD in place of COMMISSION; ADD vs COMMISSION recall gap (cue decomposition).

## 4. Decision rules (fixed)
- Pooled over evaluators and repetitions; percentile cluster bootstrap by obligation (paired POINT/SCOPE), 10,000 reps, seed 1734.
- Data-quality gates: invalid-output rate <= 0.05; pooled CLEAN target-rule FPR <= 0.10. If violated, the study is reported as a validity failure, not as evidence about Delta.
- Ceiling rule: pooled OMISSION recall > 0.95 -> result labelled CEILING_UNINFORMATIVE for Delta.
- Otherwise: upper 95% bound < +0.15 -> EXCLUDES_+0.15; lower bound > +0.15 -> REACHES_+0.15; else INCONCLUSIVE.
- Per-evaluator results are reported as descriptive; no multiplicity-adjusted claims.
- Lenient-parser re-score reported as sensitivity only.

## 5. Interpretation limits (stated in advance)
Synthetic six-beat scenes; five evaluators; one parser. A null result excludes only effects of the stated size under this
construction. No claim is made about real narratives or human auditors. Failure of the ceiling or label gates is reported as such.
