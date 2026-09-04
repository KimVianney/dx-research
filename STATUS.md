# STATUS — transparent build & benchmark

_Last updated: 2026-09-04 ~22:30Z (session session_019FtoBbsrGyBxSLTdgLe7tR)_

## Mode
Transparent (a). No blinding, no history rewrite, no injection/subversion, no
side-channel repo-visibility PATCH. De-tainting is done only by ordinary forward
commits + honest reporting of residual bias.

## Access
- Owner granted the Claude GitHub App write access. All three repos pushable via git.
- `dx-research` is still PRIVATE. The side-channel visibility PATCH was declined
  (owner can flip it in the GitHub UI). Findings are NOT mirrored into the public lab.

## Done
- claimline baseline (CI green); dx-research harness/manifest; score.py validated
  against hand-labeling in W0 (results/validation.md), plus `--manifest-pr` flag for
  re-run scoring.
- **W0 fingerprint + detection** (fuller disclosure): coderabbitai[bot], CHILL,
  Advanced plan, defaults. PR #2 mixed: recall 8/13, precision 1.0, 5 misses
  (SQLi/md5/res-leak/unbounded-quad/XSS), 2 bonus real finds. Full anatomy captured.
- **W1-A correctness** (fuller disclosure, PR #3): recall 10/10, precision 1.0,
  decoys clean.
- **Disclosure de-taint**: main softened (`5f45a08`) — plain README, SECURITY.md
  removed; originals preserved verbatim in `disclosure/`. See FINDINGS "Disclosure
  change".

## In flight (reduced-disclosure re-runs, A/B vs #2/#3)
- **PR #4** = W0 mixed re-run (reduced disclosure) — in review. Key comparison: does
  the hardcoded AWS key still rate Minor/Stability (dummy-key recognition) or shift to
  a security/secret finding (was README bias)?
- **PR #5** = W1-A correctness re-run (reduced disclosure) — in review.
- Score with `score.py --pr 4 --manifest-pr 2` and `--pr 5 --manifest-pr 3`.

## Contaminated (fuller-disclosure) PRs
- #1, #2, #3 — retained as the fuller-disclosure A/B arm, not discarded.

## Next
- Collect + hand-validate #4/#5; write the A/B comparison (esp. the AWS-key severity).
- Continue W1 families under the softened main: B=security, C=concurrency,
  D=performance, E=error-handling, F=api-contract, G=iac+ci, H=phi+domain.
- Close probe PRs unmerged; main stays clean. Pace against 10 reviews/hour.
- W11 (private control) deprioritized per owner (public repo is on paid Advanced tier).

## Environment quirks
- Commit-time secret guard blocks committing a literal AWS secret key; hardcoded-cred
  probe uses the access-key-id canary alone.
- Repo creation via API blocked; direct-curl API writes proxy-blocked (use git / MCP).
- Out of scope and untouched: the `ReveloopRCM` org of real healthcare repos.
