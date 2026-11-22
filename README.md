# cba-benchmark-validity — v2.0.0 (revision materials for IEEE Access Access-2026-51134)

Paper (revised): *Benchmark Validity Before Auditor Attribution: Repair and Label-Coherence Checks for Omission Detection in LLM-Based Narrative Auditing*.

The repository name predates the revision: the matched-triplet framework called CBA in v1.0.0 is called Matched-Triplet Auditing (MTA) in the revised paper; the code and data are the same.

## Layout
- `public_release/` — the v1.0.0 release, byte-identical (Zenodo DOI 10.5281/zenodo.23192501). Moved into this folder so that the v2 code, which loads the frozen v1 renderer, parser, and scorer from `public_release/code/`, runs without modification.
- `v2_revision/` — materials added in the revision:
  - `study3_minimal_repair/`, `study2b_reruns/`, `study2c/` — pre-registration, freeze record (SHA-256), deviation log, cases, raw model outputs, analysis code and results.
  - `common_runner/` — the shared runner and analyzer for the reruns and Study 2c (running new calls needs your own API key; none is included).
  - `release_v2_staging/` — sanitized raw responses of Study 2 v1 and Study 2b (`results_raw/`), the independent-annotation materials (`annotation/`), author QA checklists (`qa_docs/`), and the reproduction scripts below.
  - `deposit_prereg/` — the pre-registration deposit, archived on Zenodo with this release (all versions of the record: https://doi.org/10.5281/zenodo.23192500).
  - `analysis_free/` — offline interval, gate, family, and DOI checks; `manuscript/main.tex` — the revised manuscript source.

## Reproduce (offline, Python 3.10+, standard library only)
Run from the repository root:

```
python public_release/reproduce_reported_results.py
python public_release/scripts/verify_study1_raw_outputs.py
python v2_revision/release_v2_staging/reproduce_study2_from_scores.py public_release
python v2_revision/release_v2_staging/reproduce_followups.py
python v2_revision/study3_minimal_repair/src/analyze.py
python v2_revision/release_v2_staging/reproduce_annotation.py public_release
python v2_revision/release_v2_staging/annotation/reproduce_adjudication.py
```

Each prints its results and a PASS/FAIL line where a frozen value is compared. `study3_minimal_repair/src/analyze.py` rewrites `results/summary.json`; the values are identical, but on Windows the rewritten file can differ in line endings, so its SHA-256 check in `SHA256SUMS.txt` should be done on a fresh copy. The offline helpers in `v2_revision/analysis_free/` (`s1_family.py`, `s1_fpr.py`, `s1_gate.py`, `s2b_intervals.py`) also run from the repository root; `doi_check.py` needs network access. `release_v2_staging/extract_study2_raw_outputs.py` documents how the sanitized Study 2 responses were produced from the private provider archives (not published); its input hashes equal those in the frozen result manifests.

## Notes
- Freezing was local; hash records are author-controlled. The public deposit establishes the deposit date and contents, not the freeze time.
- `public_release/results/study2_v1/clean_fpr_audit.csv`: the `clean_text` column lists CLEAN beats in a different order from the frozen scripts in 42 of 50 rows; the frozen scripts (`public_release/data/study2_scope_cases.jsonl`) are the reference, and the audit notes cite their line numbers. Scores are unaffected.
- `public_release/README_REPRODUCE.md` (v1) states that Study 2b completed 360/360 calls; one of them returned a provider error with no text (scored invalid), as reported in the revised manuscript.
- Integrity: `SHA256SUMS.txt` lists every file in this release.
