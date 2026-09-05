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
| correctness | #24,#25,#26 | 9/10, 10/10, 9/10 | **9.3/10 (93%)** | 90–100% | 100% (0 decoy FP) | stable-caught (3/3): aging-boundary, date-range, avg //+ZeroDiv, pct //+ZeroDiv, late-fee-sign, top-payer-order, round-vs-truncate, balance-accumulation; flaky: mutable-default B006 (2/3, miss tracked CI-annotation timing on #24), timely-filing boundary (2/3, genuine flip on #26) |
| performance | #27,#28,#29 | perf-framed 1/8, 1/8, 3/8 · by-fix 3/8, 4/8, 5/8 | **1.7/8 perf-framed (21%)** · **4/8 by-fix (50%)** | 1–3 · 3–5 | 100% (0 decoy FP) | perf-framed stable-caught: load-then-filter→SQL (3/3); perf-framed flaky: recompute-O(n²) 1/3, list-membership 1/3; perf-framed stable-MISSED: N+1, unbounded-memory, string-concat, sort-in-loop, regex-compile-in-loop — but 3 of those 5 are FIXED under a correctness/security label (CSV-injection@38, cross-payer-rank@46, regex@60) |
_Baseline for context: security-helpers CHILL single run (PR #8) = 3/9 (33%); error-handling CHILL single run (PR #11) = 4/7 (57%); correctness CHILL single run (PR #3/#5) = 10/10; performance CHILL (PR #10) = 0/8, single-run assertive (PR #12) = 4/8 perf-framed._

**Performance is the sharpest N≥3 correction.** The single-run assertive figure (4/8, PR #12) looked
like "assertive quadruples perf recall." N≥3 shows that 4/8 was the lucky top of a wide range: mean
**perf-framed recall is only 1.7/8 (21%)**. What actually happens is subtler and more interesting —
CodeRabbit's **agentic static analysis** (it runs `ast-grep`/`rg`/`python3` scripts, visible in the
`🔎 Supported by static analysis` blocks) very often finds a **co-located correctness or security bug
at the exact line of a planted perf defect** and reports *that* instead of the performance angle:
CSV-injection at the string-concat line, cross-payer contamination at the sort-in-loop line, a
Unicode/`\d` regex bug at the regex-compile-in-loop line. So the defect frequently gets *fixed*
(by-fix 50%) while almost never being *reasoned about as performance* (perf-framed 21%). Only
load-then-filter→SQL is a stable perf-framed catch (3/3). Practical read: don't rely on CodeRabbit as
a performance reviewer — its perf labeling is high-variance — but its agentic pass does surface real,
often more-severe, co-located defects.
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
