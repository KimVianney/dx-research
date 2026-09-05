# N>=3 repeats under the ASSERTIVE profile (mean + range per family)

Converts the provisional single-run recalls into mean/range. Each run is the identical
family probe re-opened as a fresh PR under `.coderabbit.yaml profile: assertive`, manually
triggered (auto-review throttled). All hand-validated by CWE/title. Precision = decoy
false-positives.

| family | runs (PRs) | recall per run | mean | range | precision | stable-caught / stable-missed |
|---|---|---|---|---|---|---|
| security-helpers | #15,#16,#17 | 4/9, 6/9, 4/9 | **4.7/9 (52%)** | 44–67% | 100% (0 decoy FP) | stable-caught: path-traversal, sensitive-logging; stable-missed: SQLi (uncalled fn), SSRF-proper (always reframed as response-size/DoS); flaky: timeout, md5, insecure-random, IDOR, XSS |

_Baseline for context: security-helpers CHILL single run (PR #8) = 3/9 (33%)._
_(concurrency, error-handling, correctness, performance rows appended as their batches complete.)_
