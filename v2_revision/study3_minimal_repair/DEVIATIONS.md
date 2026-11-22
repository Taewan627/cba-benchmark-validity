# Deviations from PREREG.md

None so far.

## Note 1 (2026-11-13 01:05 KST, after 10 smoke calls; not a deviation)
google/gemini-3.8-flash and openai/gpt-6.1-sol return HTTP 400 "Reasoning is
mandatory for this endpoint and cannot be disabled." when reasoning is disabled.
As pre-specified (PREREG section 3), these calls use the provider default and
`reasoning_off_sent=false` is recorded per call. Consequence for interpretation:
Study-1 Gemini calls were recorded with reasoning disabled, so the Gemini ORIG
reproduction check (C0) compares a reasoning-default run against a
reasoning-off Study-1 run. claude-sonnet-5, deepseek-v4.1-flash-1017 and
qwen3.8-27b accept reasoning disabled.

## Erratum (2026-11-22)
Note 1 says the Study 1 Gemini calls were recorded with reasoning disabled. That is incorrect: no reasoning parameter was sent in Studies 1-2b (provider defaults), as stated in the revised manuscript (Run Configuration). The C0 comparison for Gemini is therefore default versus default; the verdicts are unchanged.
