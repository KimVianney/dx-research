# W10 — run-to-run determinism (identical diff, 3 reviews)

Same code (W0 mixed probe, `56ac899`) reviewed on three separate PRs against the
same softened `main`, all reduced-disclosure: **PR #4, #6, #7**. Numbers are
**hand-validated** by mapping each inline comment (by CWE / bold title) to a manifest
defect; the automated `score.py` over-counted #6 (11/13) because the SSRF entry's
`detect_any` included the bare word "url", which cross-matched an unrelated comment.
Hand-validated #6 is 9/13. (SSRF `detect_any` since tightened.)

## Per-defect outcome across the 3 identical runs

| defect | #4 | #6 | #7 | stable? |
|---|:--:|:--:|:--:|---|
| W0-CORR-CALC | TP | FN | TP | UNSTABLE |
| W0-SEC-INJ (SQLi, dead fn) | FN | TP | FN | UNSTABLE |
| W0-SEC-PATH | TP | TP | TP | stable-TP |
| W0-SEC-SSRF | FN | FN | FN | stable-FN* |
| W0-CRYPTO-MD5 | TP | TP | TP | stable-TP |
| W0-RES-LEAK | FN | FN | FN | stable-FN |
| W0-ERR-BARE | TP | TP | TP | stable-TP |
| W0-PERF-QUAD (unbounded O(n^2)) | FN | FN | FN | stable-FN |
| W0-CANARY-SECRET (AWS key) | FN | TP | FN | UNSTABLE |
| W0-CONC-RACE | TP | TP | TP | stable-TP |
| W0-SEC-XSS (unused cmp) | FN | TP | FN | UNSTABLE |
| W0-CI-INJECT | TP | TP | TP | stable-TP |
| W0-SQL-MIGRATE | TP | TP | TP | stable-TP |
| **recall** | **7/13** | **9/13** | **7/13** | 54%–69% |

\* SSRF was a clear TP on the *fuller-disclosure* run (#2) but FN on all three reduced
runs — suggestive, but inside the variance envelope, so not a clean disclosure effect.

## Observations

- **4 of 13 defects (31%) are nondeterministic** across identical input; single-run
  recall swings from 54% to 69%. A single review is therefore not a reliable estimate
  of recall for a given defect.
- **What's stable-detected:** clearly reachable, local, "textbook" issues — path
  traversal, md5, bare-except, Go data race, CI expression-injection, unsafe migration.
- **What's stable-missed:** resource leak (unclosed file), unbounded O(n^2), and SSRF
  (in reduced runs).
- **What flips:** SQL-injection in a dead function, the hardcoded AWS key, XSS in an
  unrendered component, and the copay/coinsurance correctness bug. The three security
  flippers are all "borderline reachability" items — consistent with the W0
  reachability-gating hypothesis, but here the gate behaves nondeterministically.
- **Precision:** no hard false positives in any run. One borderline nit recurs on the
  bounded-quad decoy in #4 and #7 ("enforce the <=8 bound", Minor/Perf) but not #6 — so
  even the soft-precision behaviour varies.
- **md5** was FN on the fuller run (#2) yet TP on all three reduced runs; **SSRF** the
  reverse. Because per-defect detection varies this much run-to-run, the fuller-vs-
  reduced **disclosure A/B cannot be attributed** — the differences are within the
  observed noise. A disclosure effect, if any, would need many more repeats per arm to
  detect above this variance.

## Consequence for the study

Report recall as a range or mean-of-N (N>=3), never a single number. The disclosure
question (W4-adjacent) and any per-defect claim require repeated runs. This is the
single most important methodological result so far.
