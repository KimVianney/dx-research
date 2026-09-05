# W4 — review profile: CHILL vs ASSERTIVE (performance family)

Identical performance probe (`api/claimline/analytics.py`, 8 perf defects + 3 decoys),
reviewed twice: PR #10 under default **CHILL**, PR #12 under **assertive**
(`.coderabbit.yaml: reviews.profile: assertive` on main). Both hand-validated.

| | CHILL (PR #10) | ASSERTIVE (PR #12) |
|---|---|---|
| inline comments | 4 | 8 |
| perf defects caught (on perf grounds) | **0 / 8** | **4 / 8** |
| — recompute-in-loop O(n^2) (`:29`) | missed | **caught** ("compute once", O(n), performance) |
| — list-membership O(n*m) (`:53`) | missed | **caught** ("avoid quadratic membership") |
| — load-then-filter-in-Python (`:68`) | missed | **caught** ("filter by status in SQL", memory/scale) |
| — regex-compile-in-loop (`:61`) | missed | **caught** ("compile once", + ASCII fix) |
| — N+1 (`:15`) | missed | missed |
| — unbounded read (`:22`) | missed | partial (flagged "close file", not memory) |
| — string-concat (`:38`) | missed-as-perf | flagged as csv correctness, not perf |
| — sort-in-loop (`:47`) | missed-as-perf | flagged as correctness (rank-within-group), not perf |
| decoy false-positives | 0 | 0 |

**Finding:** the default **CHILL profile suppresses performance findings**; switching to
**assertive** took the performance family from 0/8 to 4/8 (and roughly doubled total
comment volume, 4->8) with **no loss of precision** (still 0 decoy FPs). So the earlier
"perf 0/8" and, by extension, several low single-run recalls are **profile-dependent**,
not a capability ceiling. This is the highest-leverage config lever observed.
Caveat: single run per profile; W10 variance still applies, but a 0->4 shift on a family
that was a stable 0 across earlier observation is well outside the noise.

## Mixed probe (W0, 13 defects): CHILL runs #4/#6/#7 vs ASSERTIVE #13

| defect | CHILL (#4/#6/#7) | ASSERTIVE (#13) |
|---|---|---|
| CI-INJECT | TP/TP/TP | TP |
| CORR-CALC | TP/FN/TP | TP |
| CRYPTO-MD5 | TP/TP/TP | TP |
| ERR-BARE | TP/TP/TP | TP |
| CANARY-SECRET | FN/TP/FN | **TP** |
| CONC-RACE | TP/TP/TP | TP |
| SQL-MIGRATE | TP/TP/TP | TP |
| **PERF-QUAD** (unbounded O(n^2)) | **FN/FN/FN (stable miss)** | **TP (recovered)** |
| SEC-PATH | TP/TP/TP | **FN** (flip; likely W10 variance) |
| SEC-INJ (SQLi, dead fn) | FN/TP/FN | FN |
| SEC-SSRF | FN/FN/FN | FN |
| RES-LEAK | FN/FN/FN | FN |
| SEC-XSS (unused cmp) | FN/FN/FN | FN |
| **recall** | 7-9/13 | **8/13** |

**Resolution of the two hypotheses:**
- **Performance misses = profile conservatism.** Assertive recovered the unbounded O(n^2)
  dedup that CHILL stably missed (and, in the perf family, 0/8 -> 4/8). Turning up the
  profile fixes these.
- **Unreachable-security misses = reachability/context gating, NOT profile.** SQLi (in an
  uncalled fn), SSRF, resource-leak, and XSS (in an unrendered component) stayed missed even
  under assertive. Profile does not compensate for code the tool judges unreachable.
- Overall mixed recall barely moved (8/13) because assertive traded a gain (PERF-QUAD) for a
  variance-driven loss (SEC-PATH). Precision remained 100% (no decoy FPs).
