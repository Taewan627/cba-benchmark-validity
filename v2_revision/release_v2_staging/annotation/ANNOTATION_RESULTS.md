# Two-coder annotation results (Coder 1 external Fiverr; Coder 2 informal acquaintance), 2026-11-21

Scripts: analyze_annotation.py, analyze_coder2.py, analyze_two_coders.py; labels coder1_labels.json, coder2_labels.json (reproduce with reproduce_annotation.py). Pre-registered analysis (ANNOTATION_PREREG.md); both coders completed all 96 scenes.

## Quality control
Coder 1 attention 9/10; Coder 2 attention 10/10 (both meet the 9/10 criterion).

## Coder agreement
All 175 rule judgments: agreement 0.783, Cohen's kappa 0.641, Krippendorff's alpha 0.642.
Target-rule judgments only (90): agreement 0.789, kappa = alpha = 0.665.
Crosstab (165 non-attention judgments, C1 x C2): SAT-SAT 74, VIOL-VIOL 27, CT-CT 27, C1 SAT/C2 CT 8, C1 CT/C2 SAT 15, C1 VIOL/C2 CT 10, C1 CT/C2 VIOL 2, SAT/VIOL 2. Almost all disagreement involves CANNOT TELL; only 2 of 165 are SAT vs VIOL reversals. Coder 2 uses CANNOT TELL less often on target rules (16 vs 21 of 90).
Agreement with the oracle on target rules: C1 59/90, C2 69/90.

## Study 1 omission nondetections (27 rows): derived category (C1, C2)
- genuine miss, genuine miss: 6 rows (b08 1, b16 5)
- ambiguous, ambiguous: 9 rows (b13 4, b17 5)
- C1 genuine miss, C2 ambiguous: 10 rows (b18 3 valid, b22 7)
- parser artifact (mechanical): 2 rows (b18 1, b34 1)
Author audit: 25 ambiguous, 2 artifact. So neither coder reproduces "all 25 ambiguous": C1 gives 9 ambiguous / 16 genuine; C2 gives 19 ambiguous / 6 genuine. Both coders label the CLEAN counterpart of b08, b17, b18, b22 not SATISFIED (b17/b18/b22: C1 VIOLATED, C2 CANNOT TELL; b08 both CANNOT TELL); the CLEAN counterparts of b13, b16 (and b34) are SATISFIED for both. Rows from cases where both coders find the CLEAN counterpart not SATISFIED: 16 valid rows.

## Study 1 CLEAN false positives (17 rows), derived category (C1, C2)
false alarm both 2; label defect both 6; label defect (C1) / ambiguous (C2) 6; ambiguous (C1) / false alarm (C2) 3. Judged "not a false alarm" by both coders: 12 of 17.

## Study 2 v1 flagged CLEAN rows (50; 8 mechanical parser artifacts; 42 others)
Coder 1: defect 13, ambiguous 22, false alarm 7. Coder 2: defect 9, ambiguous 21, false alarm 12.
Author audit vs C1: agreement 0.69, kappa 0.49. Author vs C2: agreement 0.43, kappa 0.15. C1 vs C2 derived category: agreement 0.50, kappa 0.20.
Judged "not a false alarm" by both coders: 24 of 42. Author coding (1 false alarm of 42) is stricter toward the benchmark than either coder.

## Reading
1. Coders agree substantially on the underlying rule judgments (kappa 0.64), with disagreement mostly about whether a scene leaves the rule open (CANNOT TELL).
2. The author audit's categorical labels are only partly reproduced (Study 2 v1 kappa 0.49 with C1, 0.15 with C2); the claim "all 25 valid Study 1 omission misses are ambiguous renderings" is not supported as stated. What both coders support: 9 rows ambiguous, 6 genuine, and 10 rows (persistence cases b18, b22) where the coders split on genuine vs ambiguous but both find the CLEAN counterpart not clearly satisfied.
3. Benchmark-validity point (CLEAN variants not clean) is supported for a substantial share: Study 1 CLEAN FPs 12/17 and Study 2 v1 24/42 judged non-false-alarm by both coders.

## Adjudication of the two split scenes (D4, third annotator, 2026-11-22)
Frozen protocol, sheet, key, and decision rule: ADJUDICATION_PROTOCOL.md, FREEZE_ADJ.json (reproduce with reproduce_adjudication.py).
Attention 2/2. b18 OMISSION and b22 OMISSION (target r01): CANNOT TELL, so the 10 split rows are ambiguous.
Adjudicated split of the 25 valid rows: 19 ambiguous, 6 genuine (b08 1, b16 5), 0 unresolved; still not the author audit's 25 of 25.
Descriptive: b18 and b22 CLEAN SATISFIED (both coders: not SATISFIED); b13 OMISSION CANNOT TELL (agrees with both coders); b16 OMISSION CANNOT TELL (both coders VIOLATED).

## Pre-registered statistics 2 (second form) and 4 (reproduce_annotation.py)
Study 1 author coding with the trigger cases (b08, b13, b16) recoded as defects, 25 valid rows: agreement 5/25, kappa -0.02 (Coder 1); 15/25, kappa 0.26 (Coder 2).
Annotator-oracle agreement on target rules by study and condition (Coder 1, Coder 2, n): S1 CLEAN 8, 8, 13; S1 COMMISSION 7, 9, 10; S1 OMISSION 8, 5, 10; S2b CLEAN 5, 5, 5; S2b COMMISSION 2, 4, 5; S2b OMISSION 5, 5, 5; S2 v1 CLEAN 24, 33, 42.
