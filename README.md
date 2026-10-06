# Benchmark Validity and Commission–Omission Asymmetry in LLM-Based Narrative Auditing

This repository contains the reproducibility artifacts for a study of commission–omission asymmetry in LLM-based narrative auditing. Commission-Biased Auditing (CBA) asks whether an LLM auditor detects an explicit wrong event (COMMISSION) differently from a missing required event (OMISSION). Both variants are matched to the same underlying obligation, and an intact CLEAN variant serves as a negative control. A deterministic event-ledger oracle supplies the formal labels.

The main methodological finding is deliberately bounded. An initial apparent commission–omission asymmetry in Study 1 was substantially qualified by artifact-level validity audits. A later benchmark failed its negative-control quality gate (Study 2 v1). A fresh defect-informed benchmark (Study 2b) produced low CLEAN false-positive rates and near-ceiling omission detection under the tested explicit-rule setting.

The repository does not claim that LLMs are free of omission difficulty. It is a record of the frozen data, code, and analyses behind the reported numbers, not a general-purpose benchmark release.

## Archival Release

Version v1.0.0 is archived on Zenodo.

- DOI: 10.5281/zenodo.23192501 (refers to this artifact release, not to the paper)
- GitHub repository: https://github.com/Taewan627/cba-benchmark-validity
- GitHub release: https://github.com/Taewan627/cba-benchmark-validity/releases/tag/v1.0.0

## Paper

**Title:** Benchmark Validity and Commission–Omission Asymmetry in LLM-Based Narrative Auditing

**Authors:** Taewan Kim, Taehoon Kim

**Affiliation:** Graduate School of Virtual Convergence, Sogang University

**Status:** Prepared for submission to IEEE Access.

## Repository Structure

| Path | Contents |
|---|---|
| `data/` | Benchmark cases, rule families, freeze records, and manifests for Study 1, Study 2 v1, and Study 2b |
| `config/` | Recorded evaluator and study configurations (the API-key *variable name* appears as metadata; no credential is included) |
| `code/` | Prompt construction, parsing, deterministic scoring, and frozen analysis code |
| `results/` | Frozen scored rows and result manifests per study, plus the Study 2 v1 CLEAN false-positive census |
| `audits/` | Post-hoc audit records: Study 1 omission-miss audit, Study 2 v1 descriptive recovery, Study 2b permutation sensitivity |
| `figures/` | Figure scripts (hard-coded frozen values) and the final figure images used in the manuscript |
| `scripts/` | Additional offline checks: permutation sensitivity, Study 1 raw-output parse check, and checksum verification |
| `docs/` | Methodology, reproduction guide, and artifact manifest |
| `reproduce_reported_results.py` | One-command offline verification of the reported statistics |
| `README_REPRODUCE.md`, `SHA256SUMS.csv` | Original review-package reproduction notes and integrity hashes |

The layout follows the original review package so that relative paths and the checksums remain valid.

## Studies

### Study 1
Forty authored cases across five rule families were split into an exploratory set and a disjoint held-out set of 20 cases. Each case was evaluated in CLEAN, COMMISSION, and OMISSION variants under four protocols (P1–P4) by two evaluator models. The held-out decision under the frozen criteria was **INCONCLUSIVE**.

### Study 1 Post-hoc Validity Audit
After the held-out run, all 27 omission nondetections were reviewed against the stored prompt, response, parser outcome, rendered scene, and oracle. The audit is author-coded and post-hoc. Initial classification notes were prepared with AI assistance and reviewed and finalized by the authors; no independent second coding or external semantic adjudication was performed. It did not rescore any row; the frozen scores and decision are unchanged. See `audits/study1_omission_miss_audit.md`.

### Study 2 v1
A POINT versus SCOPE contrast on 60 cases failed its negative-control quality gate (conservative CLEAN FPR = 50/120). The CLEAN false-positive rows were audited post-hoc (`results/study2_v1/clean_fpr_audit.*`). The recall quantities are descriptive only and are not mechanism evidence (`audits/study2v1_descriptive_recovery.md`).

### Study 2b
A fresh, defect-informed benchmark of 60 base cases (30 POINT, 30 SCOPE) was evaluated with 360 evaluator calls under a single explicit rule. Design, prompts, parser/scorer, and analysis assets were frozen before execution. A secondary exact case-level permutation analysis is reported as sensitivity only (`audits/study2b_sensitivity_analysis.md`).

## Reproduction

### Offline reproduction (no API keys, standard library only)

Run from the repository root:

```text
python reproduce_reported_results.py
python scripts/verify_study2b_permutation.py
python scripts/verify_study1_raw_outputs.py
python scripts/verify_checksums.py
```

Expected final lines: `OFFLINE REPRODUCTION CHECK: PASS`, `PERMUTATION SENSITIVITY CHECK: PASS`, `RAW OUTPUT PARSE CHECK: PASS`, `CHECKSUM VERIFICATION: PASS`. Python 3.10 or later is recommended.

### Optional re-execution (external model APIs)

The original evaluator calls used a paid third-party model gateway and require your own API credentials. They are **not** needed to verify the reported numbers, and re-running them may give different outputs because model behavior can change over time. The collection code and configuration are included for transparency only; do not commit credentials.

## Key Reported Results

**Study 1 held-out ordinary summaries**

| Evaluator | G_ordinary | 95% CI | CLEAN FPR |
|---|---:|---|---:|
| Gemini | +0.175 | [0.050, 0.300] | 0.150 |
| Claude | +0.100 | [0.025, 0.175] | 0.125 |

**Study 1 post-hoc omission audit:** 27 nondetections: 25 ambiguous renderings, 2 parser/evaluation artifacts, 0 unambiguous genuine auditor misses.

**Study 2 v1 (descriptive; failed quality gate):** commission recall 0.975, omission recall 0.958, gap +0.017, CLEAN FPR 41.7%.

**Study 2b:** 60 fresh base cases, 360 evaluator calls, pooled CLEAN FPR 0.83%, POINT omission recall 1.000, SCOPE omission recall 1.000, Δ_scope = +0.017, 95% bootstrap CI [−0.033, 0.067].

**Exact permutation sensitivity (Study 2b):** one-sided p = 0.500, two-sided p = 1.000, attainable range [−0.050, +0.050].

## Interpretation

This repository does not establish that LLMs are universally robust to omissions. It supports the narrower conclusion that benchmark validity can materially affect the interpretation of apparent commission–omission asymmetry, and that under the tested explicit-rule setting a pooled POINT–SCOPE interaction as large as +0.15 is not supported. Omission recall in Study 2b is at ceiling, which limits sensitivity to smaller or harder-to-elicit effects.

## Reproducibility Notes

- **Frozen records:** benchmark cases, freeze records, configurations, scored rows, and result manifests are the records produced before or at the time of each study and are not modified here. Some frozen manifests contain internal development labels (for example a `verdict` field); `docs/methodology.md` gives the mapping to the terms used in the paper.
- **Post-hoc analyses:** the Study 1 omission-miss audit, the Study 2 v1 CLEAN census and descriptive recovery, and the Study 2b permutation analysis were conducted after the corresponding results were known. They are author-coded or sensitivity analyses and are not independently adjudicated.
- **Deterministic/offline components:** parsing, scoring, bootstrap (seed 1732, 10,000 replicates), and permutation analyses are deterministic given the stored rows.
- **Model/API dependence:** the original responses came from two hosted models called through a gateway at temperature 0. Study 1 returned model text is published in sanitized form (`results/study1_heldout/raw_model_outputs_public.jsonl`: case, protocol, condition, model, returned text, parse status). Provider transport envelopes, request identifiers, billing data, and timestamps are not published; raw responses for Study 2 v1 and Study 2b are not published, and the stored scored rows suffice for the reported statistics.

## Citation

Kim, T., and Kim, T. "Benchmark Validity and Commission–Omission Asymmetry in LLM-Based Narrative Auditing." Manuscript prepared for submission to IEEE Access, 2026.

See also `CITATION.cff`.

## License

No repository-level license file is currently included.

## Contact

Corresponding author: Taehoon Kim, taehoonkim@sogang.ac.kr
