# Reproduction guide

All commands run from the repository root, offline, using only the Python standard library.

```text
python reproduce_reported_results.py          # Study 1 protocol/ordinary summaries, Study 2 v1 census, manifest checks
python scripts/verify_study2b_permutation.py  # Study 2b exact permutation: p = 0.500 / 1.000, range [-0.050, +0.050]
python scripts/verify_study1_raw_outputs.py   # Study 1 published raw text re-parses to the frozen validity flags
python scripts/verify_checksums.py            # SHA-256 integrity of frozen files (SHA256SUMS.csv)
```

Figures: `python figures/source/fig1_study_sequence.py` (etc.) regenerates the figure images in the current working directory from hard-coded frozen values. Requires matplotlib and numpy.

Study 1 returned model text is published in sanitized form (`results/study1_heldout/raw_model_outputs_public.jsonl`); `python scripts/verify_study1_raw_outputs.py` re-parses it with the frozen parser and reproduces the frozen validity flags.

Not published: provider transport envelopes, request identifiers, billing data, and timestamps for Study 1, and raw responses for Study 2 v1 and Study 2b. The original evaluator calls require paid API access and are not part of the offline reproduction. The Study 1 audit was originally verified against a private raw-attempt archive; its SHA-256 is recorded in the audit text.
