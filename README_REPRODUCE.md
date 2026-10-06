# Reproducing the reported results offline

This review package contains the stored scored rows, frozen result manifests,
benchmark definitions, configurations, prompt construction, deterministic
scoring code, and analysis code needed to verify the manuscript's numerical
tables without calling an evaluator API.

## Package structure

- `data/`: confirmatory, Study-2 v1, and Study-2b case and freeze manifests.
- `config/`: recorded evaluation and analysis configurations. The named API-key
  environment variable is configuration metadata; no credential is included.
- `code/`: prompt construction, parsing, deterministic scoring, and frozen
  analysis implementations.
- `results/`: scored rows, result manifests, and the Study-2 v1 diagnostic
  census. Raw API responses are intentionally omitted because the scored rows
  and frozen manifests suffice for the reported statistics.
- `SHA256SUMS.csv`: package integrity manifest.

## Runtime

Python 3.10 or later is recommended. The supplied verification script uses only
the Python standard library. The original project used PyYAML and pytest for
configuration handling and tests, but neither is required by this package's
offline verification command.

## One-command numerical verification

From this `supplement/` directory, run:

```text
python reproduce_reported_results.py
```

The script deterministically reconstructs the Study-1 protocol and ordinary
summaries from stored scored rows using 10,000 family-stratified bootstrap
replicates and seed 1732. It verifies the Study-2 v1 CLEAN census and reads the
frozen Study-2 v1 and Study-2b manifests for the reported primary quantities.
Expected final line:

```text
OFFLINE REPRODUCTION CHECK: PASS
```

## Integrity verification

Recompute SHA-256 hashes with the platform's standard hash tool and compare
them with `SHA256SUMS.csv`. The CSV contains paths relative to this directory.

## Frozen-study boundaries

- Study 1 held-out: 20 base cases, P1--P4, two evaluators, 480 planned rows;
  frozen decision INCONCLUSIVE.
- Study 2 v1: 60 base cases, P2, two evaluators, 360 planned calls; frozen
  decision INCONCLUSIVE because conservative CLEAN FPR was 50/120.
- Study 2b: 60 fresh base cases, P2, two evaluators, 360/360 completed calls;
  the frozen pooled practical-effect decision is retained exactly.

No command in this README runs an experiment. The original collection steps
required paid evaluator APIs and are outside this reproduction package. Do not
rerun them to verify the published tables.
