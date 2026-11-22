# Annotation deviations

## D1 (2026-11-20) Coder 2 simplified sheet
Coder 2 (informal acquaintance, not Fiverr) receives a 30-scene subset (21 Study-1 audited-case scenes, 3 Study-1 CLEAN-FP scenes, 6 attention checks), same scene text and judgment labels; confidence and reason columns removed; scene order reshuffled (seed 20261121). Reason: cost and burden; affects only the Coder-1/Coder-2 agreement analysis (judgments only), which will be reported as an informal second coding on a subset.

## D2 (2026-11-21) Coder 2 completed the full original sheet
The simplified 30-scene sheet (D1) was not used. Coder 2 (informal acquaintance) completed the original 96-scene sheet (same item ids, with confidence and reason columns), so the pre-registered analysis (kappa and Krippendorff's alpha over all 175 rule judgments and the target-rule subset) applies unchanged. Coder 2's file name contains a personal name; names are not recorded in the paper or release.

## D3 (2026-11-21) Coder 2 recruitment, sheet provenance, and recorded caveats
- Coder 2 was recruited informally (an acquaintance of the authors) after Coder 1's results had been analyzed on 2026-11-20, outside the route in ANNOTATION_PREREG.md section 1. The analysis plan (kappa/alpha, mechanical mapping) was unchanged.
- The file returned by Coder 2 is a copy of the Coder-1-returned workbook layout rather than the frozen blank sheet: Item S067 carries the same accidental scene-text deletion in both returned files, while the frozen blank sheet is intact. No residue of Coder 1's answers was found in Coder 2's file, but the exact file sent to Coder 2 was not archived or hashed. Seven small rule-text slips in Coder 2's file are recorded; none changes a numeric result.
- Coder 2's independence statement: the coder is unfamiliar with the research area (authors' report); whether the coder was told anything about the hypothesis is not documented beyond that.
- Post-hoc observation (not pre-registered): Coder 1 labeled similar evidential situations differently in preservation cases (b17 CANNOT TELL; b18, b22 VIOLATED).

D3 update (2026-11-21, authors' recollection): the file sent to Coder 2 was most likely Coder 1's returned workbook with the answer cells cleared. This is not archived; a check of Coder 2's returned file found no residue of Coder 1's answers (cells, reasons, comments, hidden sheets: single sheet only). Coder 1's results were not shown to Coder 2 as answers.

## D4. Third-annotator adjudication of the two split scenes (decided 2026-11-22, after both coders' results were known)
ANNOTATION_PREREG.md planned no adjudication. Reviewer 1 asked how disagreements were resolved; the 10 split rows come
from two scenes (b18 and b22 OMISSION, target r01: Coder 1 VIOLATED, Coder 2 CANNOT TELL). A third annotator judges these
two scenes, mixed with their CLEAN counterparts, two agreed anchors (b13, b16 OMISSION), and two attention items, under
the original guide text. Protocol, guide, sheet, and key were frozen before sending (FREEZE_ADJ.json, 2026-11-22T03:36:01Z,
author-controlled). The decision rule and the reporting commitment (report whatever the result; keep the two-coder result)
are in ADJUDICATION_PROTOCOL.md. Because the step was decided after the results were known, it is reported as post hoc.

D4 result (applied 2026-11-22 under the frozen rule; ADJUDICATION_RESULT.txt). The returned sheet was opened and re-saved
by the authors in a spreadsheet application before analysis (sheet renamed, drop-down lists dropped); item IDs, scene
texts, and rule texts were checked identical to the frozen sent sheet. Attention 2/2 correct. Target rule r01:
b18 OMISSION CANNOT TELL, b22 OMISSION CANNOT TELL -> all 10 rows ambiguous. Adjudicated split of the 25 valid rows:
19 ambiguous, 6 genuine, 0 unresolved. Descriptive only (not in the decision): b18 CLEAN SATISFIED, b22 CLEAN SATISFIED,
b13 OMISSION CANNOT TELL (both coders CANNOT TELL), b16 OMISSION CANNOT TELL (both coders VIOLATED).
Adjudicator: recruited through a personal contact of the authors, no prior involvement; compensation a coffee gift
voucher; about 15 minutes; no AI, translation, or search tools and no discussion of the items (self-report).
analyze_adjudication.py was edited after the freeze only to accept a renamed sheet and to verify the returned item, scene,
and rule texts against the sent sheet; it is not in FREEZE_ADJ.json, and the rule it applies is the frozen protocol text.
The as-received attachment was not retained separately; only the authors' re-saved copy exists. Its item IDs, scene texts,
and rule texts were verified identical to the frozen sent sheet; only the judgment, confidence, and reason cells were filled.
