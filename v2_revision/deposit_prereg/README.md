# Pre-registrations for the post-submission studies (Access-2026-51134 resubmission)

Contents: the pre-registration, freeze record (SHA-256 of the frozen assets), and deviation log for
Study 3 (same-item minimal repair; frozen 2026-11-12, before the review decision), the Study 2b reruns and Study 2c (frozen after the reviews), and the independent annotation.

Timing statement. These files were frozen locally and hashed before any model call or annotation; the freeze
records are author-controlled. This public deposit postdates the runs, so it establishes the deposit date and the
file contents (verifiable with SHA256SUMS.txt and the hashes inside each FREEZE.json), not the freeze time itself.
Deviations after freezing are listed in each DEVIATIONS.md.

Integrity check of pre-registration files against their freeze records:

| Study | File | Frozen at (UTC, per record) | Hash vs record |
|---|---|---|---|
| study3_minimal_repair | PREREG.md | 2026-11-12T16:02:11Z | MATCH |
| study2b_reruns | PREREG.md | 2026-11-18T16:55:53Z | MATCH |
| study2c | PREREG.md | 2026-11-18T16:55:53Z | MATCH |
| annotation | ANNOTATION_PREREG.md | 2026-11-18T15:16:34Z | MATCH |
| annotation | ADJUDICATION_PROTOCOL.md | 2026-11-22T03:36:01Z | MATCH |

Excluded on purpose: API keys, payment receipts, private item keys, annotator files and labels, and raw model outputs
(the outputs, labels, and analysis code are released with the code repository at v2.0.0).
