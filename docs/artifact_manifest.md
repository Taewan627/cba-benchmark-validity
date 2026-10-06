# Artifact manifest

SHA-256 hashes are given for every published file except this manifest. Frozen result/config files are also bound by `SHA256SUMS.csv` and checked by `scripts/verify_checksums.py`.

| Path | Purpose | Study | Status | Needed for reproduction | SHA-256 |
|---|---|---|---|---|---|
| `.gitattributes` | Repository metadata | All | n/a | No | `ced447a891638bf2cc804146c15fd5b0d6f511be94c9d2369e4be0e6d8abf09e` |
| `.gitignore` | Repository metadata | All | n/a | No | `b8832b2f3b12a0235c25e0d5dcfb1ab63017c3294015809ecddc668054d78d66` |
| `CITATION.cff` | Repository metadata | All | n/a | No | `deae2f1af690502ec3e17fb1dcce7c919991edd19c66344b954d0d20deed11af` |
| `README.md` | Repository metadata | All | n/a | No | `448740983e014b28d48ae08c3c6d7cbb023e0a81151d169d561b11c769bbfdad` |
| `README_REPRODUCE.md` | Original review-package reproduction notes | All | n/a | No | `ba9818348fb8b7347ca02f753cd8cffaa9fe8e8ca64f8d8d29515537db226809` |
| `SHA256SUMS.csv` | Integrity hashes of the review package | All | n/a | Yes | `771b20d80ecf4b50ac84742ce3ffc76be437b84cdaf255425632155d4bc9ed50` |
| `audits/study1_omission_miss_audit.md` | Study 1 omission-miss audit (post-hoc, not independently adjudicated) | Study 1 | Post-hoc | No (documentation) | `a1dd95986594e09e11fc642652847726349f73f20f2efc5d228dfd7fc3dbc322` |
| `audits/study2b_sensitivity_analysis.md` | Study 2b permutation sensitivity write-up | Study 2b | Post-hoc | No (documentation) | `b4bd4198ec1a64a0abf2449821890788365aeb1f002a0ae322b9c4eb2dbbdc07` |
| `audits/study2v1_descriptive_recovery.md` | Study 2 v1 descriptive recovery | Study 2 v1 | Post-hoc | No (documentation) | `2af91e6bacaccb11280e4a33589d10b6331f1ed3bdf195bb05a7e3fa8d4e4e95` |
| `code/__pycache__/analysis.cpython-311.pyc` | Prompt construction, parser, deterministic scoring, analysis | All | Frozen | Yes | `166a008418abc583de8569356eb7b5eab8110b5fc810f7a5e9fce1d7c8d7676b` |
| `code/__pycache__/parser.cpython-311.pyc` | Prompt construction, parser, deterministic scoring, analysis | All | Frozen | Yes | `3e33884adc39c9c4bc7dd379da31e17acf400643623942122d7ef8c02c733c7c` |
| `code/analysis.py` | Prompt construction, parser, deterministic scoring, analysis | All | Frozen | Yes | `b4627605efee6433b8221911bd810a620ce031f50772c68e25fb64e1334c2b92` |
| `code/deterministic_scoring.py` | Prompt construction, parser, deterministic scoring, analysis | All | Frozen | Yes | `3a3f9e9a6faf69213f8cb47fe743af186333b93168407e523452323fda6c7664` |
| `code/parser.py` | Prompt construction, parser, deterministic scoring, analysis | All | Frozen | Yes | `331e596090ca32ff9361e4e35a4123bda9dc53423e2a0352e35a0fb631e61e72` |
| `code/protocol_construction.py` | Prompt construction, parser, deterministic scoring, analysis | All | Frozen | Yes | `f14dafe8d4b8a49cdd8e0da65322f2f8c91432967402d3b32ed05e8a3917eaa7` |
| `code/study2_scope.py` | Prompt construction, parser, deterministic scoring, analysis | Study 2 v1 | Frozen | Yes | `a7c818511a7fddfe0db8b611073b67b8ac6f9a44f5f1ea275abed1aeb1878276` |
| `code/study2b_scope.py` | Prompt construction, parser, deterministic scoring, analysis | Study 2b | Frozen | Yes | `e12a603723b65c7f6234df128affba0eff06398670025a734203d801335a005d` |
| `config/evaluators.yaml` | Recorded evaluator/study configuration | All | Frozen | Reference | `e4cfc1737a5a59082f9fc6e4dd976ec0d5ef24bfe1086fafd89175ed24f27587` |
| `config/pilot.yaml` | Recorded evaluator/study configuration | All | Frozen | Reference | `848637564f0bbbbd6f57fc41695ccc504ae283631e50674f19ee39b1e594911f` |
| `config/study2_scope.yaml` | Recorded evaluator/study configuration | Study 2 v1 | Frozen | Reference | `90bbd4f74b042e49359ec1e6603fc11b82c453e44a7d91f8263b0c23e4c041bb` |
| `config/study2b_scope.yaml` | Recorded evaluator/study configuration | Study 2b | Frozen | Reference | `182c6aefa497d3187b084762a2d345b402204d177aff53451f47abbedd1d3ce6` |
| `data/confirmatory_cases.jsonl` | Benchmark cases, rule families, freeze records and manifests | Study 1 | Frozen | Yes | `bfc28c7c0cf628f0112ec430143e49f1fbe5bbcaa5eb4c34ab33da851e49a8e1` |
| `data/confirmatory_freeze.json` | Benchmark cases, rule families, freeze records and manifests | Study 1 | Frozen | Yes | `bffcad55a47e5c7c56af77d42c11a1a71e66482ff3574bbbd0f0434f67becc54` |
| `data/confirmatory_manifest.json` | Benchmark cases, rule families, freeze records and manifests | Study 1 | Frozen | Yes | `4bc0ab167d13b5dfa1eafb946d577b1be6f8b9cf3feb8d4e3f9062077f70f52e` |
| `data/rule_families.yaml` | Benchmark cases, rule families, freeze records and manifests | All | Frozen | Yes | `eb2ed1f3e9a6e4da21c41e7dbf11d60c9518b9a6142a1455c829ef823306e70c` |
| `data/study2_scope_cases.jsonl` | Benchmark cases, rule families, freeze records and manifests | Study 2 v1 | Frozen | Yes | `5cc8bdee6dd4a8b98bacfb85ab6b84822e77a0e871249abe0d1cc9d474a012b1` |
| `data/study2_scope_freeze.json` | Benchmark cases, rule families, freeze records and manifests | Study 2 v1 | Frozen | Yes | `6e1ffc4e1795743f6d0aac5b92fca6b460a3fe0b4be529cc081d287df1efcd06` |
| `data/study2_scope_manifest.json` | Benchmark cases, rule families, freeze records and manifests | Study 2 v1 | Frozen | Yes | `2c87bb9584704e804918ab071140ead41ff7fbca254d5111bcba88c0e712de23` |
| `data/study2_scope_rule_families.yaml` | Benchmark cases, rule families, freeze records and manifests | Study 2 v1 | Frozen | Yes | `b542f9d30cf32dfeadde28d2beb1be4e49bf6bb3b1ffea83d7ee4e847952eff0` |
| `data/study2b_scope_cases.jsonl` | Benchmark cases, rule families, freeze records and manifests | Study 2b | Frozen | Yes | `0f2f087c19cd327383cbac0c1c04504f6576e4562350865c20798207a86b0cad` |
| `data/study2b_scope_freeze.json` | Benchmark cases, rule families, freeze records and manifests | Study 2b | Frozen | Yes | `e964bb6bf9fe42df00d6f9e37bff20873816a1cbf2b68635cf20dab07735c49c` |
| `data/study2b_scope_manifest.json` | Benchmark cases, rule families, freeze records and manifests | Study 2b | Frozen | Yes | `d736cfc17982ca74561d8c9abc6c07fe3ba4bbb756adaac28b245530581265f2` |
| `data/study2b_scope_rule_families.yaml` | Benchmark cases, rule families, freeze records and manifests | Study 2b | Frozen | Yes | `b9c0ed41a66a2dd9363ce994f3430142226ee2d9099bb49ef5466bddb72bea71` |
| `docs/methodology.md` | Documentation | All | n/a | No | `968924c4242cfb5edf0671e5e8f403a7400422c47517daf23dfbd7e2c19d5b77` |
| `docs/reproduction.md` | Documentation | All | n/a | No | `8bb8a62e0b1b63ea13a8165ba082610824240353d2a6c48d3d5aeb20d6f7b314` |
| `figures/fig1_study_pipeline_new.png` | Final manuscript figure images | All | Derived | No | `273f93c33260ad999639f983935e6f02644c2f8f8b4bfbd1b052284d30aac815` |
| `figures/fig2_matched_design_new.png` | Final manuscript figure images | All | Derived | No | `101148c4b469f204ff841e0bc416c7d333b96a7c13069d5f3a886214124a1dd8` |
| `figures/fig3_study1_protocols_new.png` | Final manuscript figure images | Study 1 | Derived | No | `ec8e8704f285f17e141d3da66f2a52412a663167a3f86fa545f4ed44139101c0` |
| `figures/fig4_clean_quality_new.png` | Final manuscript figure images | All | Derived | No | `258cb82c0c5fa9e915df696abc63fa3640efcbe3be0d2b027463e5445bbe7680` |
| `figures/fig5_study2b_point_scope_new.png` | Final manuscript figure images | Study 2b | Derived | No | `98cf88a541023680e04f0be457d514b43fe82552caaa51ae413e9edef0926d7c` |
| `figures/source/fig1_study_sequence.py` | Figure scripts (hard-coded frozen values) | All | Derived | No | `601c4dbb50bda37772d5eb33e1edadf52898d044ee19164d98830d99e868434d` |
| `figures/source/fig2_matched_design.py` | Figure scripts (hard-coded frozen values) | All | Derived | No | `9363d4087e9ae846d9ff6bd574f162e720bef18f95c6db8eea8400f62b9b6855` |
| `figures/source/fig3_study1_results.py` | Figure scripts (hard-coded frozen values) | Study 1 | Derived | No | `b3e3b667a456052351e71caa5f8567edc5ff3d3049eacfeb2bbd0b11971b2c45` |
| `figures/source/fig4_clean_fpr.py` | Figure scripts (hard-coded frozen values) | All | Derived | No | `fe18a5e96bcce4dc8a54d35be9feda27073c4b7f42cf6218060cb2d483d2974f` |
| `figures/source/fig5_study2b_results.py` | Figure scripts (hard-coded frozen values) | Study 2b | Derived | No | `8f31102ee4fcd379714b240b80a68da1b8d46572f43ebad39a054d0026399347` |
| `reproduce_reported_results.py` | One-command offline verification | All | n/a | Yes | `56f5276cc7409ad8457420484c9c28ab84dbbe4b0043228ca44c3d4b1d80c703` |
| `requirements.txt` | Repository metadata | All | n/a | No | `d90826a2e03c26fed6c7645bd1d9a97c024c53383239b4a1c689aaf72d1b40c4` |
| `results/study1_heldout/raw_model_outputs_public.jsonl` | Sanitized Study 1 returned model text (no envelopes, ids, costs, timestamps); parse-checkable | Study 1 | Frozen record (sanitized extract) | Verification | `d30821f89784441d4e7fb55679f55c392b87e05d2206b52d93b9726d22c54b1a` |
| `results/study1_heldout/result_manifest.json` | Study 1 held-out scored rows and manifest | Study 1 | Frozen | Yes | `e7f734e0ea8cd423350375fb2006de0d30e98a3744f2bddbfd968514d0878c3d` |
| `results/study1_heldout/scores.jsonl` | Study 1 held-out scored rows and manifest | Study 1 | Frozen | Yes | `a9d4ae3c3f0cd7618d0b68aeb0780c88481aa4aad4a054281a3f76827ce82bdc` |
| `results/study2_v1/clean_fpr_audit.csv` | Study 2 v1 CLEAN false-positive census (author-coded) | Study 2 v1 | Post-hoc | Yes | `059a90cfc33083377a2559e0a5f168ca96a0e972151fa2bd98b5d0099a0e6341` |
| `results/study2_v1/clean_fpr_audit.md` | Study 2 v1 CLEAN false-positive census (author-coded) | Study 2 v1 | Post-hoc | Yes | `138e386021913a35950a5906c54802d72c0cede6503a366e476db0e035e83b33` |
| `results/study2_v1/result_manifest.json` | Study 2 v1 scored rows and manifest | Study 2 v1 | Frozen | Yes | `fcd958204687cb5a91f2f24c30ef6ef8b467717695b19f1a9195afe81c51fcac` |
| `results/study2_v1/scores.jsonl` | Study 2 v1 scored rows and manifest | Study 2 v1 | Frozen | Yes | `93a3ee7df5cf126cf97384acf9c20e7be35fb09ab6c17828c17496527307bc65` |
| `results/study2b/result_manifest.json` | Study 2b scored rows and manifest | Study 2b | Frozen | Yes | `71a6bc1fafc62f9ee38e65355289048ac3a5de3c5f264b716545fb444dd2af27` |
| `results/study2b/scores.jsonl` | Study 2b scored rows and manifest | Study 2b | Frozen | Yes | `d152acb60e495a868789011218f2a68f4ccec7503d71572e5c837a06558defa4` |
| `scripts/verify_checksums.py` | Checksum verification (added for release) | All | n/a | Yes | `e466bafbea92c8769a6b37632c01282e59075e1ee176ce5a4ce5498f15ba5bf9` |
| `scripts/verify_study1_raw_outputs.py` | Re-parses published Study 1 raw text and checks frozen validity flags (added for release) | Study 1 | n/a | Yes | `11749f9149208eb32589f7d76af32e291dabdd4ea87fa10ac54f947cb9777a74` |
| `scripts/verify_study2b_permutation.py` | Offline permutation sensitivity check (added for release) | Study 2b | Post-hoc | Yes | `7abb7403ad521f7f352fcf032d68d32d461f3dbeea0ed9206350a92457ca3ba4` |
