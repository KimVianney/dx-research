# N>=3 repeats under the ASSERTIVE profile (mean + range per family)

Converts the provisional single-run recalls into mean/range. Each run is the identical
family probe re-opened as a fresh PR under `.coderabbit.yaml profile: assertive`, manually
triggered (auto-review throttled). All hand-validated by CWE/title. Precision = decoy
false-positives.

| family | runs (PRs) | recall per run | mean | range | precision | stable-caught / stable-missed |
|---|---|---|---|---|---|---|
| security-helpers | #15,#16,#17 | 4/9, 6/9, 4/9 | **4.7/9 (52%)** | 44–67% | 100% (0 decoy FP) | stable-caught: path-traversal, sensitive-logging; stable-missed: SQLi (uncalled fn), SSRF-proper (always reframed as response-size/DoS); flaky: timeout, md5, insecure-random, IDOR, XSS |

| concurrency | #18,#19,#20 | 6/7, 6/7, 6/7 | **6/7 (86%)** | 86% (no variance) | 100% (0 decoy FP) | stable-caught: wg.Add-in-goroutine, map race, counter race, goroutine leak, append race, missing-unlock; stable-missed: time.Tick ticker leak |
| error-handling | #21,#22,#23 | 5/7, 4/7, 5/7 | **4.7/7 (67%)** | 57–71% | 100% (0 decoy FP) | stable-caught: swallow-returns-True, missing-`raise from`, broad-except-bad-state, fd-leak-no-`with`; stable-missed: unchecked financial-reversal return; flaky: broad-except→None (1/3), generic-Exception-not-domain-type (1/3) |
_Baseline for context: security-helpers CHILL single run (PR #8) = 3/9 (33%); error-handling CHILL single run (PR #11) = 4/7 (57%)._
_(correctness, performance rows appended as their batches complete.)_

**Read so far:** the four *mechanical* error-handling defects (S110 try/except/pass, B904 missing
`from`, the partial-charge bad-state, the un-`with`'d file handle) are the stable-caught 4/7 that
already showed under CHILL — assertive did not raise the floor for them. Assertive's gain is
*flaky* recovery of the two judgment-lighter-but-non-lint ones (err→None, generic-Exception), each
seen in exactly one of three runs. The one genuinely judgment-heavy defect — a financial reversal
whose return value is never checked — was **stable-missed 0/3** under assertive, same as CHILL. So
for this family the profile lever mostly adds variance around the lint-backed core, not new depth.
CI-annotation ingestion (`🪛 GitHub Actions ... Ruff S110/B904`, "Source: Pipeline failures")
appeared on #22/#23 but not #21 — timing-dependent, matching the earlier W6/W8 finding.
