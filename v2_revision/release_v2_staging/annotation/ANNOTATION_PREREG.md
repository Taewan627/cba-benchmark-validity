# Independent annotation: pre-registered protocol and analysis

Status: FROZEN before any file is sent to an annotator. Written 2026-11-19 (KST).
Answers reviewer requests R1-1(a–f), R2-1, R3-4, R4, R5-3 (IEEE Access decision of 2026-11-18).

## 1. Annotators
One or two external annotators recruited through Fiverr (online freelance platform), paid at or above
their posted hourly rate, fluent English readers, with no involvement in item construction. They receive
only `Annotation_Guide.docx` and `annotation_sheet.xlsx`. They are not told the study hypothesis, the
evaluators, the conditions, the oracle labels, or which study an item comes from, and are instructed not to
use AI, translation or search tools. They label synthetic text and are not research participants.

## 2. Items (96 scenes, 175 rule judgments; shuffled with seed 20261119; rule order shuffled per scene)
| Pool | Scenes | Purpose |
|---|---|---|
| Study 1, the seven base cases with audited omission nondetections (b08, b13, b16, b17, b18, b22, b34), all three variants | 21 | DQ1 audit validation; also covers the correct commission detections and CLEAN passes of the same cases (R1-1c) |
| Study 1 CLEAN variants with conservative false positives not covered above (b04, b26, b37) | 3 | the 17 Study-1 CLEAN false positives (R1-1c) |
| Study 1 random error-free held-out cases, all three variants (3 cases, seed 20261119) | 9 | symmetric control: ambiguity rate on items with only correct responses (R1-1c) |
| Study 2 v1 CLEAN variants with at least one flagged response | 37 | DQ2 audit validation (all 50 flagged rows) |
| Study 2 v1 CLEAN variants with no flagged response (random 5) | 5 | symmetric control |
| Study 2b: q026 triplet + 2 random POINT and 2 random SCOPE cases, all variants | 15 | external check of Study-2b items (R1-1f, R3-1) |
| Attention checks with unambiguous answers | 6 | quality control |
The mapping from item ids to sources is in `KEY_PRIVATE_do_not_send.json` (never sent to annotators).

## 3. Labels
Per rule: SATISFIED / VIOLATED / CANNOT TELL; confidence high / medium / low; one-line reason citing lines.

## 4. Quality control
An annotator who labels fewer than 9 of the 10 attention rule judgments (6 scenes) as keyed is excluded and replaced;
the exclusion is reported. Missing cells are reported, not imputed.

## 5. Derived categories (mechanical; no author judgment)
Target-rule label of the annotator on the variant that produced the response:
- Study-1 omission nondetection rows (27; 2 are parser/transport artifacts, classified mechanically):
  VIOLATED → genuine auditor miss; CANNOT TELL → ambiguous rendering; SATISFIED → label defect.
- Study-1 CLEAN false-positive rows (17) and Study-2 v1 flagged CLEAN rows (50), using all rules of the scene:
  parser-invalid rows → parser artifact (mechanical); otherwise all rules SATISFIED → evaluator false alarm;
  any rule VIOLATED → label defect (CLEAN item not clean); else any CANNOT TELL → ambiguous rendering.
- Correct-response items (control pools and correct responses on audited cases): rate of CANNOT TELL and of
  annotator–oracle disagreement, compared with the error pools (symmetry check, R1-1c).
- Study 2b items: annotator–oracle agreement per variant; q026 reported individually.

## 6. Reported statistics
1. Counts of derived categories per annotator for each row set (Study-1 omission misses, Study-1 CLEAN FPs,
   Study-2 v1 CLEAN flags), with exact row identifiers.
2. Agreement between annotator-derived and author audit categories (Cohen's kappa; three categories
   genuine miss / ambiguous / defect, or evaluator false alarm / ambiguous / defect for CLEAN rows).
   For Study 1 the author's 25 "ambiguous" rows include the trigger cases now treated as construction defects;
   agreement is reported both for the original author coding and with trigger cases recoded as defects.
3. If two annotators: Cohen's kappa and Krippendorff's alpha (nominal) over all 175 rule judgments and over
   target-rule judgments only; disagreements are reported, not adjudicated by the authors.
4. Annotator–oracle agreement on target rules by study and condition (includes the symmetric controls).
5. Per-family breakdown of Study-1 omission nondetections and gaps (R1-1d), computed from frozen scores.

## 7. Interpretation rules (fixed now)
- If the annotator(s) label a Study-1 omission-miss item VIOLATED, that row is reported as a genuine auditor
  miss in the revised paper, replacing the author classification.
- If the annotator(s) label CLEAN items flagged by evaluators as SATISFIED on all rules, those flags are
  reported as evaluator false alarms.
- With two annotators who disagree, both labels are reported and the row is reported as "annotators disagree".
- All results are reported whatever their direction.
