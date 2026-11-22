# No-cost re-analyses (HANDOFF §7.2) — results, 2026-11-19

No model calls, no cost. All inputs are stored outputs. Scripts in this folder (`common.py`, `s1_fpr.py`, `s1_gate.py`,
`s1_family.py`, `rescore_all.py`, `s2b_intervals.py`, `extra.py`, `reasoning_check.py`, `doi_check.py`); JSON outputs next to them.
Raw responses were read from the private provider archives (`outputs/*/raw_attempts.jsonl` of the original repository; not published)
(read-only). `public_release/` and everything outside `v2_revision/` untouched.

**Integrity check:** re-parsing every stored response with the frozen parser reproduces the published `valid` / `detected`
flags for all 480 + 360 + 360 rows (0 mismatches), and the Study 2b bootstrap reproduces [−0.0333, +0.0667] exactly (seed 1732).

## 1. F1 — target-only vs any-rule CLEAN FPR (conservative, invalid = FP)

| Study | any-rule (published) | target-rule only | off-target-only flags |
|---|---|---|---|
| Study 1 held-out (160 CLEAN rows) | 17/160 = 10.6% | **2/160 = 1.3%** (both Claude, b04, P1 and P4) | 15 (b22 ×6, b37 ×6, b26 ×3, all on background rule r02) |
| Study 2 v1 (120 CLEAN rows) | 50/120 = 41.7% | **31/120 = 25.8%** (valid-only target: 23/120 = 19.2%) | 19 (= the 19 "background throughout" rows of Table 5) |
| Study 2b (120 CLEAN rows) | 1/120 = 0.83% | 1/120 = 0.83% | 0 (single rule, no change) |

Gate consequences (gate: conservative CLEAN FPR ≤ 0.10):
- **Study 1: the gate's FPR condition passes under target-only scoring** (cell FPRs 0.00–0.05). **The verdict stays INCONCLUSIVE, but for a different reason than the paper says.** The paper says the verdict "does not depend on [the P3 intervals] because the FPR conditions fail first". Under target-only scoring the FPR conditions pass, and the verdict is INCONCLUSIVE because (i) G_ordinary is 0.100 (Claude) and 0.175 (Gemini), both < 0.20 so GO fails; (ii) the P3 intervals are too wide for the KILL equivalence margin ±0.10. Re-ran frozen `decide()` with target-only FPR: INCONCLUSIVE.
- **Study 2 v1: gate still fails** (25.8% and 19.2% both > 10%), but the headline falls from 41.7% to 25.8%. The paper must report both; the "41.7%" is mostly an any-rule artifact (19 of 50 are off-target-only flags on the "throughout" background rule).
- Study 2 v1 target-only by family: placement_checkpoint 15/20 (all target; the worst family), any_of_scope 4/20, by_end_resolution 3/20, identity 4/20, recipient 3/20, across_scope 2/20. So the defect is concentrated in placement_checkpoint (POINT) and the background-rule artifact in the SCOPE families.

## 2. F2 — Study 1 cell intervals (frozen decision inputs; `decide()` uses the wider of Newcombe / bootstrap)
| Cell | gap | Newcombe | cluster bootstrap |
|---|---|---|---|
| Claude P1 | .050 | [−.116, .236] | [.000, .150] |
| Claude P2 | .150 | [−.038, .360] | [.050, .200] |
| Claude P3 | .200 | [−.001, .416] | [.100, .300] |
| Claude P4 | .150 | [−.038, .360] | [.050, .200] |
| Gemini P1 | .100 | [−.077, .301] | [.000, .200] |
| Gemini P2 | .250 | [.038, .469] | [.100, .400] |
| Gemini P3 | .100 | [−.118, .318] | [−.050, .250] |
| Gemini P4 | .300 | [.077, .519] | [.150, .450] |
Bootstrap: percentile, 10,000 replicates, seed 1732, resampling base cases within rule family (config/pilot.yaml).
G_ordinary bootstrap CI: Claude [.025, .175], Gemini [.050, .300].

## 3. A1-d — Study 1 per-family (held-out, 4 cases/family, 2 models × 4 protocols = 32 cells per condition)
| Family | comm recall | omission recall | gap | omission misses |
|---|---|---|---|---|
| preservation (b17,b18,b22,b43) | 32/32 | 16/32 = .500 | **.500** | 16 (b17 5, b18 4, b22 7) |
| temporal_ordering (b13,b16,b41,b42) | 32/32 | 23/32 = .719 | **.281** | 9 (b13 4, b16 5) |
| placement | 32/32 | 31/32 | .031 | 1 (b08) |
| commitment | 32/32 | 31/32 | .031 | 1 (b34, SSL transport failure) |
| identification | 31/32 | 32/32 | −.031 | 0 (1 comm miss = parser invalid) |
Of 27 omission misses, **25 are in preservation (16) + temporal_ordering (9)**, all in just 5 of 20 cases. The other three families pooled: comm 95/96, omission 94/96, gap ≈ +0.01. The asymmetry sits entirely in two families — the two the reviewers flagged (ordering = construction defect candidates; preservation = state-inertia reading). Unaudited CLEAN FPs by family (any-rule): commitment 6, preservation 6, identification 3, placement 2, ordering 0.

## 4. B5 — Study 2b interaction Δ_scope = G_scope − G_point (observed +0.0167; zero-event-robust intervals)
Cells (model-responses): comm POINT 58/60, omission POINT 60/60, comm SCOPE 59/60, omission SCOPE 60/60.
| Interval | 95% interval | excludes +0.15? |
|---|---|---|
| Frozen percentile cluster bootstrap | [−0.033, +0.067] | yes (but cannot see unobserved omission misses) |
| Jeffreys-Bayes (Beta(.5,.5) per cell; P(Δ ≥ .15) = 0.001) | [−0.054, +0.091] | yes |
| MOVER-Wilson score interval, n = 60 responses/cell | [−0.080, +0.118] | yes |
| MOVER-Wilson, conservative n_eff = 30 (one unit per case) | [−0.154, +0.192] | **NO** |
Honest summary: the exclusion of +0.15 survives zero-event-aware intervals when the 60 model-responses per cell are treated as independent, but **not** under the most conservative treatment (one independent unit per case). The abstract/conclusion must say "pooled, and not robust to the most conservative interval". I did not run a hierarchical case-effects model (R1 mentions it as an option); a true effective n lies between 30 and 60.

### Design sensitivity (simulation, 2,000 reps, 1,000 bootstrap reps each; comm recall .967 both structures, POINT omission recall 1.0, SCOPE omission recall = 1 − δ; 30 cases × 2 models per structure; independent responses, so optimistic)
| true Δ (= δ) | P(frozen exclusion rule fires: bootstrap upper < .15) | P(GO-type detection: Δ̂ ≥ .15 and CI excludes 0) |
|---|---|---|
| 0 | .977 | .000 |
| .05 | .561 | .019 |
| .10 | .170 | .204 |
| .15 | .034 | .552 |
| .20 | .004 | .833 |
| .25 | 0 | .955 |
| .30 | 0 | .991 |
The design had ~55% power to detect a true +0.15 and reaches 80% power only near Δ ≈ +0.20. So "ruling out +0.15" is a statement the design could support only if the true effect was ≲ 0.10; it is a modest-sensitivity result, and R3's "can barely fail" is partly right: the exclusion rule fires with probability .977 under no effect, but also .17 at a true +0.10.

## 5. E2 — lenient parser re-score (fence-stripping + first balanced JSON object; otherwise identical frozen parser)
Only 5 responses change validity (all Claude): Study 1 b18/OMISSION/P3 (stays a nondetection; target not flagged), Study 2 v1 c11/OMISSION/P2 (becomes a detection), p03 & p14 CLEAN (become valid, target not flagged: any-rule FP count 16→14 for Claude), **Study 2b q001/COMMISSION Claude (becomes a correct detection)**.
- Study 1: no change to any gate quantity.
- Study 2 v1: any-rule CLEAN FP 50→48 (41.7%→40.0%); target-only 31→29; gate still fails.
- **Study 2b: Δ_scope = 0.000** (G_point −0.017, G_scope −0.017); bootstrap [−0.050, +0.050]. Remaining commission nondetections: q026 (Claude, substantive) and q043 (Gemini, invalid even under lenient parsing — finish_reason "error", no usable text). Comm recall: Claude 59/60 (was 58/60).
- Gemini Study 2 v1 invalid: 12 (all stay invalid; truncation at max_tokens 6000, finish_reason "length"). Gemini produced long reasoning despite the recorded "none" setting (see §7).

## 6. D1 — DOI verification (CrossRef/DataCite content negotiation, 2026-11-19)
All 16 DOIs resolve; title/authors/year/pages match the reviewer's list (details: `doi_check.json`):
Northcutt 2021, Gema 2025 (pp. 5069–5096), Vendrow 2025, Bean 2025, Bowman & Dahl 2021 (4843–4855), Zou 2023 (14268–14286), Ahuja 2025, Kim & Schuster 2023 (3835–3855), Dwyer 1999 (411–420), Newcombe 1998 (17(22):2635–2650), Field & Welsh 2007 (69(3):369–390), Lakens 2017 (8(4):355–362), Miller 2024, Gururangan 2018 (pp. 107–112), Pavlick & Kwiatkowski 2019 (TACL 7:677–694), Ribeiro 2020 (4902–4912). Karakaş & Şimşek 2026 also resolves (skipped by decision; weak relevance).
Caveats: Northcutt, Vendrow, Bean, Ahuja, Miller DOIs are arXiv DOIs; the NeurIPS/COLM venue is not verifiable from the DOI itself — cite as "arXiv:... (NeurIPS D&B 2021)" only after checking the proceedings page. Lakens' CrossRef title is the short "Equivalence Tests"; full title is "Equivalence Tests: A Practical Primer for t Tests, Correlations, and Meta-Analyses". Newcombe's DOI contains `<` `>`; escape in BibTeX.

## 7. Facts for E3 / F3 / F4 found while reading the original repo (not on your list, but they change the paper)
- **Gateway**: OpenRouter; returned model strings equal the requested ones (`google/gemini-3.8-flash`, `anthropic/claude-sonnet-5`); upstream provider recorded per call (Gemini: Google 90+%, Google AI Studio a few; Claude: "Claude Platform on AWS").
- **Run dates (UTC)**: Study 1 confirmatory 2026-09-18 23:40 → 09-19 00:22; Study 2 v1 09-19 02:55 → 03:48; Study 2b 09-19 05:50 → 06:12; "corrected" exploratory Stage-1 run 09-18 19:11 → 19:55.
- **Settings recorded**: temperature 0, seed 1731 (`seed_supported: False`), `response_format: json_object`, `reasoning_setting: none`; max_tokens 6000 in confirmatory/Study 2 v1/Study 2b, but **2400 in the exploratory run**.
- **F3 (exploratory run)**: the "corrected" run used max_tokens 2400; 17 of 480 responses hit `finish_reason: length`; 18/480 (3.75%) parser-invalid; its INCONCLUSIVE came from `invalid_output_fraction_exceeded` (a per-cell 5% cap). The confirmatory rerun raised max_tokens to 6000 (0 truncations, 3 invalid of 480). This matches the HANDOFF's "18/480"; the "222/480" figure refers to an earlier run I have not examined.
- **CORRECTION 2026-11-19 (Fable audit, verified in `src/executor.py::_request_body`): no reasoning parameter was ever sent in Studies 1-2b; `reasoning_setting: none` was only a log label, so provider defaults applied. The sentence below that blames the gateway for ignoring a request is wrong; manuscript pass 4 fixes it.**
- **⚠ "Reasoning disabled" is not supported by the logs.** With `reasoning_setting: none`, Gemini returned reasoning text in 177–229 of 180–240 responses per run (mean 414–1,555 reasoning tokens; max 5,761), and Claude in 5–69 of 180–240 (mean 2–93 tokens). The manuscript's "reasoning disabled" statement for Study 2b (and any similar claim) should be changed to "reasoning requested off; the gateway still returned reasoning tokens for N responses". This is exactly R1 Major-4(c)'s concern. Study 2 v1's 12 truncations are Gemini responses whose reasoning consumed the 6,000-token budget.
- F4 (external timestamp, +0.15 timing) is NOT answered here: needs git/commit history of the original repo; `docs/study2b_scope_gate.md` fixes 0.15 and FPR ≤ 0.10, I did not yet check its file timestamp against the Study 2 v1 run date.

## 8. Things that need your attention
1. Study 1 text "FPR conditions fail first" is inaccurate under target-only scoring (see §1); the verdict is unchanged. Both versions should be reported in the paper.
2. The Study 2b exclusion of +0.15 is not robust to the most conservative interval (upper 0.192) and the design's power at +0.15 is ~55%; the reframing as a ceiling regime (B3) is warranted, and the abstract must not read as strong evidence.
3. "Reasoning disabled" claim needs correction (see §7).
4. Under the lenient parser the Study 2b interaction is exactly 0.000 and two of the three commission nondetections are not parser-recoverable (q026 substantive; q043 Gemini error response) — so "one parser-invalid and one substantive" replaces the manuscript's "two parser-invalid + one substantive". Confirm before editing the text: q001's Claude response was fence-wrapped JSON (recoverable); q043 had `finish_reason: error`.
