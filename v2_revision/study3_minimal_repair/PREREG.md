# Study 3 pre-registration: same-item minimal repair of audited omission nondetections

Status: FROZEN before any Study-3 model call. Written 2026-11-13 (KST).
The SHA-256 of this file, the case file and the code are recorded in
`FREEZE.json`. Any deviation after freezing is logged in `DEVIATIONS.md`.

## 1. Question
The Study-1 post-hoc audit classified 25 of 27 held-out omission
nondetections as ambiguous renderings, in two patterns: (a) the triggering
event of a conditional obligation was absent (b08, b13, b16), and (b) the
scene never established the required state, so responses read the absence of
a contrary change as satisfaction (b17, b18, b22). That audit was author-coded.
Study 3 tests its central claim behaviourally: if the nondetections were
caused by these renderings, a minimal edit that removes only the identified
ambiguity should restore omission detection on the same items, without
raising false alarms on the matched CLEAN items.

## 2. Items
Six held-out base cases (all with audited ambiguous nondetections). b34 is
excluded (its only audited nondetection was a transport failure).
Each case has an ORIG triplet (the frozen v1 variants, unchanged) and a
REPAIR triplet. Oracle labels are unchanged: CLEAN = no violation;
COMMISSION and OMISSION = violation of the target rule r01.

Repairs (one pre-specified edit type per arm; see `src/build_cases.py`):
- TRIGGER arm. b08: L6 becomes "The botanist starts the noon watering." in all
  three variants (the trigger never occurred in any variant).
  b13 OMISSION L4 becomes "The nurse draws the dose."; b16 OMISSION L5 becomes
  "The driver opens the cargo doors." (the v1 omission edit deleted the
  trigger together with the required act). b13/b16 CLEAN and COMMISSION are
  unchanged and share their ORIG responses.
- STATE arm (b17, b18, b22): the sentence "A required state counts as
  maintained only if a line explicitly shows it." is appended to the setup of
  all three variants. Nothing else changes.
All 36 variants pass the frozen v1 leakage checks and the Study-1 10%
within-triplet word-count tolerance.

## 3. Evaluators and execution
Five evaluators via OpenRouter:
google/gemini-3.8-flash and anthropic/claude-sonnet-5 (the Study-1 evaluators),
plus openai/gpt-6.1-sol, deepseek/deepseek-v4.1-flash-1017, qwen/qwen3.8-27b.
Protocols P1-P4 rendered by the frozen v1 renderer. Three repetitions per
cell (rep 0-2). Temperature 0 and reasoning disabled where the provider
accepts them; otherwise provider defaults, recorded per call. max_tokens 6000,
JSON response format requested. One transport retry. Identical prompts
(b13/b16 CLEAN and COMMISSION) are called once per model/protocol/rep and
scored for both versions.
Budget ceiling: USD 9 (runner stop) under a USD 10 key limit.
Planned calls: 1,920.

## 4. Scoring
Frozen v1 parser and scorer, unchanged. Invalid output = nondetection
(intention-to-evaluate). Primary analyses use the strict frozen parser; a
lenient parse that only strips Markdown code fences is a pre-specified
sensitivity analysis.

## 5. Outcomes (per arm)
Primary protocols: P1-P3 (non-privileged). P4 is reported separately.
Unit of aggregation: case x model, averaging over protocols and reps.
- R_orig, R_rep: OMISSION target recall, ORIG and REPAIR.
- dR = R_rep - R_orig (paired within case x model).
- Specificity control (primary): CLEAN target-rule conservative FPR
  (flag on r01, or invalid output). Pre-specified reason: in b22 the
  background rule r02 (gauge cover) is never shown in any variant, so the
  STATE sentence may legitimately trigger r02 flags on CLEAN; these are
  reported as any-rule FPR (secondary) and do not bear on the target claim.
- COMMISSION target recall, ORIG and REPAIR.

## 6. Decision rules (per arm; all on primary protocols)
C0 reproduction: R_orig <= 0.85. If not met, the arm is NOT INFORMATIVE
   (the v1 misses did not reproduce under the current evaluators).
C1 repair effect: (a) dR >= +0.20; (b) dR > 0 for at least 4 of 5 models;
   (c) dR >= 0 for all 3 cases (no case reversal).
C2 specificity: REPAIR CLEAN target-rule FPR <= 0.10 and no more than 0.05
   above ORIG; REPAIR COMMISSION recall >= 0.90.
C3 ceiling restoration: R_rep >= 0.85.
Verdict: SUPPORTED if C0, C1a-c, C2 and C3 hold. PARTIAL if C0, C1a and C2
hold but C1b, C1c or C3 fails. CONFOUNDED if C1a holds but C2 fails (the
edit increased flagging generally). NOT SUPPORTED otherwise.
With 3 cases per arm, no population-level inference is claimed. A
case x model cluster bootstrap (10,000 replicates, seed 1733) and the exact
counts are reported descriptively.

## 7. Pre-specified interpretation
- Both arms SUPPORTED: the audited nondetections are reversible by minimal,
  defect-targeted edits on the same items; the Study-1 asymmetry is
  attributable to rendering ambiguity for these items.
- NOT SUPPORTED or PARTIAL: reported as such; the author-coded audit
  classification is weakened for that arm, and the corresponding
  nondetections are treated as possibly genuine auditor misses.
- NOT INFORMATIVE: reported; no claim about that arm.
Results are reported in full regardless of direction.
