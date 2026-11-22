# Study 2b reruns pre-registration: repeatability and evaluator breadth on the frozen Study 2b cases

Status: FROZEN before any rerun call. Written 2026-11-19 (KST). Hashes in `FREEZE.json`; deviations in `DEVIATIONS.md`.

## 1. Why
Study 2b had one run per evaluator and two evaluators (Gemini, Claude) with an unverified seed. Reviewers asked for repeated
runs and more models. Cases are the frozen `public_release/data/study2b_scope_cases.jsonl` (180 variants), unchanged.

## 2. Design
- P2 only; frozen renderer, parser, scorer.
- Part A (repeatability): the two original evaluators, 2 additional repetitions each, with the ORIGINAL request body
  (temperature 0, max_tokens 6000, JSON object, seed 1731+rep, no reasoning parameter). 720 calls.
- Part B (breadth): three further evaluators (openai/gpt-6.1-sol, deepseek/deepseek-v4.1-flash-1017, qwen/qwen3.8-27b),
  1 repetition, Study 3 request body (disable-reasoning flag sent where accepted). 540 calls. Budget cap USD 4.

## 3. Analysis (fixed)
Same estimands and gates as Study 2b (G_scope - G_point; threshold +0.15). Percentile cluster bootstrap by base case, resampled
independently within structure (cases are not crossed), 10,000 reps, seed 1734. Ceiling rule: pooled OMISSION recall > 0.95 ->
CEILING_UNINFORMATIVE. Gates: invalid <= 0.05, CLEAN target-rule FPR <= 0.10. Reported: pooled, per evaluator, and the two
original evaluators' Part A rows separately (run-to-run variation). Lenient parser as sensitivity only.
The reruns are replications of an existing design, not a new test; they cannot remove the construction artifacts of Study 2b,
which Study 2c addresses.
