# Adjudication protocol: third annotator for the two split Study 1 scenes

Status: FROZEN before the sheet is sent (hashes in FREEZE_ADJ.json). Deviation D4 from ANNOTATION_PREREG.md, which planned no adjudication.

## Why
Coder 1 and Coder 2 agreed on 15 of the 25 valid Study 1 omission nondetections. The other 10 rows come from two
scenes, the OMISSION variants of b18 and b22 (target rule r01), which Coder 1 judged VIOLATED and Coder 2 CANNOT TELL.
Reviewer 1 asked how disagreements were resolved. This step resolves only these two scenes.

## Adjudicator
One person who is not an author, not Coder 1 or Coder 2, has no role in the study, and has not seen the earlier sheets
or results. The adjudicator is not told about the earlier coders, the hypothesis, the evaluators, the conditions, the
oracle labels, the source study, or which items are of interest. Compensation, recruitment, and self-reported tool use
are recorded and reported as for the earlier coders.

## Materials
8 scenes in shuffled order (seed 20261122), each with the original setup, lines, rules and rule order:
- contested: b18 OMISSION, b22 OMISSION
- context: b18 CLEAN, b22 CLEAN
- anchors: b13 OMISSION (both coders CANNOT TELL), b16 OMISSION (both coders VIOLATED)
- attention: two items of the original packet with clear answers
Labels (SATISFIED / VIOLATED / CANNOT TELL), confidence, reason, definitions, examples and task rules are those of the
original guide; only the item count (8) and time estimate (15 to 20 minutes) differ.

## Decision rule (fixed now)
For each contested scene, the adjudicated target-rule (r01) label is the adjudicator's label if it is one of the two
coders' labels (VIOLATED or CANNOT TELL), and is mapped by the pre-registered rule: VIOLATED -> genuine miss,
CANNOT TELL -> ambiguous. Every valid nondetection row of that scene takes the adjudicated category. If the adjudicator
answers SATISFIED, the scene is reported as unresolved (third label) and its rows stay split.
The adjudication counts only if both attention items are answered correctly on r01; otherwise it is reported as
failed and not used. Context and anchor items are reported descriptively and do not enter the decision.

## Reporting (whatever the result)
Sec. IV-A and Table 7 report the adjudicated split (agreed 15 rows plus adjudicated rows), the adjudicator's labels and
reasons for the two scenes, the anchor and context labels, and this deviation; the abstract reports the adjudicated
counts with the words "after third-annotator adjudication of the two split scenes". The unadjudicated two-coder
result stays in the paper.
