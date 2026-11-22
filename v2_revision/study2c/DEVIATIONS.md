# Deviations

None at freeze time.

## D1 (2026-11-19, after calls, before analysis)
The frozen parser raised RecursionError on one or more pathologically nested model outputs. `analyze.py` was edited only to catch
this and count the output as invalid (the frozen parser's own treatment of malformed output). No other analysis code changed.
The post-edit hash of analyze.py differs from FREEZE.json for this reason.

## Errata (2026-11-19, after Fable audit audit_fable_study2c_2026-11-19.md; no relabel, no rerun)
- E1: D1 above says the guard was added "before analysis"; precisely, it was added after the first analysis attempt crashed, before any analysis output was used. Removing the guard reproduces the frozen analyze.py hash.
- E2: POINT OMISSION scripts omit the `At the <checkpoint>,` prefix (it is attached only to A/B beats), so POINT OMISSION is not fully label-coherent for the trigger; the only two valid nondetections (Gemini, case o11P OMISSION) show this. Disclosed in the manuscript.
- E3: PREREG/builder say B is "in a later slot" in ADD; B precedes A in 16 of 24 obligations. Labels unaffected (ADD is a violation either way).
- E4: The "external timestamp" is an author-controlled claude.ai document, not a third-party timestamp; before submission deposit PREREG/FREEZE on OSF/Zenodo. 
- E5: One Gemini row has finish_reason=error but was stored ok=True (runner checked only top-level error); counted invalid by the parser.
- E6: Request facts: reasoning-disable flag rejected for Gemini/GPT (768 HTTP 400 then resent without it); temperature 0 not sent for Claude/GPT; seeds 1731/1732 (2c), 1732/1733 (rerun original body).
