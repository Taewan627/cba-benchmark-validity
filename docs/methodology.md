# Methodology summary

This is a short orientation; the manuscript is the authoritative description.

## Design
- Each base case specifies a scene, one audited rule, one required event, incompatible events, and ordered beats.
- Three variants share setup and rules: CLEAN (required event occurs), COMMISSION (an incompatible event occurs, required event does not), OMISSION (neither occurs).
- A deterministic event-ledger oracle labels CLEAN as a nonviolation and both corrupt variants as violations. It does not use an LLM.
- Matching controls requirement identity, position, and surrounding text, not perceived severity or salience.

## Outcomes
- Gap G = mean over cases of (commission detected - omission detected).
- Study 1: G_ordinary averages P1 and P2 gaps per case; intervals are cluster bootstrap over base cases within rule family (10,000 replicates, seed 1732).
- Study 2b: model decisions are averaged within case; Delta_scope = G_scope - G_point; percentile cluster bootstrap within POINT and SCOPE; practical threshold +0.15.
- Conservative CLEAN FPR counts invalid CLEAN responses as false positives.

## Status of each analysis
| Analysis | Status |
|---|---|
| Study 1 exploratory and held-out scoring, frozen decision | Frozen (pre-specified criteria) |
| Study 1 omission-miss audit | Post-hoc, not independently adjudicated |
| Study 2 v1 scoring and quality gate | Frozen; benchmark failed the gate |
| Study 2 v1 CLEAN census, descriptive recovery | Post-hoc, descriptive only |
| Study 2b scoring, bootstrap interval, decision | Frozen before execution |
| Study 2b exact permutation analysis | Post-hoc sensitivity only |

## Internal labels in frozen manifests
Frozen manifests keep internal development labels unchanged. Mapping to paper terminology:

| Manifest label | Paper terminology |
|---|---|
| `INCONCLUSIVE` | INCONCLUSIVE under the frozen decision criteria |
| `KILL` (Study 2b `verdict`) | The pooled Delta_scope interval excludes the pre-specified +0.15 practical threshold (threshold exclusion) |
| `clean_fpr_exceeded` | Conservative CLEAN FPR quality gate failed |
| `delta_scope_ruled_out` | Pooled interaction as large as +0.15 excluded |
| `GO` | Positive-effect route, not triggered |

## Limits
Two evaluator models; synthetic compact scenes; Study 2b omission recall at ceiling; POINT/SCOPE confounded with family and content; audits author-coded and not independently adjudicated; no human-evaluator comparison.
