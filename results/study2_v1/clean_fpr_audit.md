# Study-2 CLEAN false-positive audit

## Summary
- CLEAN rows: 120
- False positives: 50 (41.7%)
- FP status: {'B': 41, 'C': 8, 'A': 1}
- Benchmark quality: {'LIKELY DEFECT': 25, 'CLEAR CLEAN': 8, 'AMBIGUOUS': 17}

## Model comparison
- Gemini: 34 FPs / 60 CLEAN = 56.7%
- Claude: 16 FPs / 60 CLEAN = 26.7%

## Structure comparison
- point: 24 / scope: 26

## Family comparison
- across_scope_required_event: 5
- any_of_scope_obligation: 11
- by_end_resolution: 10
- identity_checkpoint: 5
- placement_checkpoint: 15
- recipient_checkpoint: 4

## Root-cause categories
- : 19
- RC3: 16
- RC11: 8
- RC4: 6
- RC2: 1

## Cross-model
- shared FP cases: 13 -> ['c02', 'c04', 'c08', 'c10', 'c14', 'p10', 'p12', 'p13', 'p14', 'p16', 'p17', 'p18', 'p22']
- Gemini-only: 21 -> ['c01', 'c03', 'c07', 'c11', 'c12', 'c13', 'c15', 'c16', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c27', 'c29', 'p02', 'p15', 'p19', 'p20', 'p21']
- Claude-only: 3 -> ['p03', 'p08', 'p30']

## Benchmark quality
- {'LIKELY DEFECT': 25, 'CLEAR CLEAN': 8, 'AMBIGUOUS': 17}

## Representative cases (author review)

- c01 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the player checks the chapter door at l3, b
- c02 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the bench did not stay clear throughout the
- c02 | claude-sonnet-5 | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the act of clearing the bench at l2 implies
- c03 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the scout closes the pack during the patrol
- c04 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the gardener moves the rake by setting it a
- c04 | claude-sonnet-5 | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the rake is explicitly set aside, meaning i
- c07 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the scene never establishes that the lamp r
- c08 | gemini-3.8-flash | scope | RC11 | CLEAR CLEAN | parser invalid (finish=length)
- c08 | claude-sonnet-5 | scope | RC4 | LIKELY DEFECT | target event placed after scope terminal: the briefing closes at l5 before the officer marks the map
- c10 | gemini-3.8-flash | scope | RC4 | LIKELY DEFECT | target event placed after scope terminal: the guard finishes the round at l5 before calling the stat
- c10 | claude-sonnet-5 | scope | RC4 | LIKELY DEFECT | target event placed after scope terminal: the round ends at l5, but the call to the station occurs a
- c11 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the scene mentions checking the lamp at l1,
- c12 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the porter only parks the cart at l2, so th
- c13 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the flag is checked at l1 but is never esta
- c14 | gemini-3.8-flash | scope | RC11 | CLEAR CLEAN | parser invalid (finish=length)
- c14 | claude-sonnet-5 | scope | RC4 | LIKELY DEFECT | target event placed after scope terminal: the cart is returned at l3 but then wheeled again at l5, i
- c15 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the keeper clears the board at l1, showing 
- c16 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the bag was not tagged from the beginning o
- c18 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the scene never establishes that the lanter
- c19 | gemini-3.8-flash | scope | RC4 | LIKELY DEFECT | target event placed after scope terminal: the guest reaches the end of the stay at l5 before handing
- c20 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the scene reaches the end of the shift with
- c21 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the scene does not establish that the lamp 
- c22 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the keeper coils the rope at l2, showing th
- c23 | gemini-3.8-flash | scope |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the courier closes the satchel at l1, indic
- c27 | gemini-3.8-flash | scope | RC11 | CLEAR CLEAN | parser invalid (finish=length)
- c29 | gemini-3.8-flash | scope | RC4 | LIKELY DEFECT | target event placed after scope terminal: the porter finishes the delivery at l5 before scanning the
- p02 | gemini-3.8-flash | point | RC11 | CLEAR CLEAN | parser invalid (finish=length)
- p03 | claude-sonnet-5 | point | RC11 | CLEAR CLEAN | parser invalid (finish=stop)
- p08 | claude-sonnet-5 | point |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: the check-in time is written (l1) but not e
- p10 | gemini-3.8-flash | point | RC11 | CLEAR CLEAN | parser invalid (finish=length)
- p10 | claude-sonnet-5 | point | RC2 | AMBIGUOUS | rule over-strictness: the recipe note contains both the step number and the word 'salt', not salt al
- p12 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the book is placed on the shelf, but it is not s
- p12 | claude-sonnet-5 | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the scene states the book is placed on 'the shel
- p13 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the vase is set on the table, but there is no in
- p13 | claude-sonnet-5 | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the helper sets the vase on 'the table' without 
- p14 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the coat is hung on the rack in l1, but it is no
- p14 | claude-sonnet-5 | point | RC11 | CLEAR CLEAN | parser invalid (finish=stop)
- p15 | gemini-3.8-flash | point | RC11 | CLEAR CLEAN | parser invalid (finish=length)
- p16 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the bowl is placed in the sink, but it is not sp
- p16 | claude-sonnet-5 | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the bowl is placed in a sink, but the scene neve
- p17 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the worker sets the crate on the dock, but fails
- p17 | claude-sonnet-5 | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the crate is set 'on the dock' (l3) but the scen
- p18 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the flower is set in the pot, but it is not set 
- p18 | claude-sonnet-5 | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the flower is set in the pot (l5), but no line s
- p19 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the towel is hung on the rail, but the scene doe
- p20 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the torch is set in the sconce, but it is not es
- p21 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the note is handed to the guide, but the scene d
- p22 | gemini-3.8-flash | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the buyer gives the coin to the vendor, but the 
- p22 | claude-sonnet-5 | point |  | LIKELY DEFECT | background rule 'throughout' contradicted by CLEAN text: although the basket was lifted earlier (l1)
- p30 | claude-sonnet-5 | point | RC3 | AMBIGUOUS | rule location qualifier not repeated in CLEAN beat: the whistle is handed to the lookout after the d
