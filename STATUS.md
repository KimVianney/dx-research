# STATUS — transparent build & benchmark

_Last updated: 2026-09-04 ~19:11Z (session session_019FtoBbsrGyBxSLTdgLe7tR)_

## Mode
Transparent variant (labs openly disclose they are testbeds; no deception of the
tool; no injection/subversion testing). Deliberately-vulnerable diffs live only in
un-merged PRs; `main` stays clean and green.

## Access
- RESOLVED: owner granted the Claude GitHub App write access. `claimline`,
  `claimline-edge`, `dx-research` all attached and pushable.
- Note: `git push` works now; earlier read-only 403s are gone.

## Done
- **claimline baseline** on `main`, CI green (run #1 success). Bundle also sent to owner.
- **dx-research scaffold** pushed: harness (collector/fingerprint/score), manifest schema,
  README/FINDINGS/STATUS.
- **W0 PR#1** (trivial docs): CodeRabbit fired unprompted in ~50s, "no actionable
  comments", single edited issue comment, empty reviews API. Fingerprint recorded.
- **W0 PR#2** (`feat/claim-batch-import`, PR #2): 12 defects + 2 decoys planted &
  manifested; PR open; **review in progress** at time of writing. Local ruff catches
  4/12 deterministically.

## In flight
- Waiting on PR #2 review to complete (subscribed; fallback check scheduled 19:17Z).
  Next: collect -> score -> hand-validate matches -> write W0 PR#2 findings + first
  recall/precision read -> push.

## Next
- Validate score.py against the real PR#2 comments (hand-label them) before trusting numbers.
- W1 detection matrix (8 family PRs). Then W2-W4, W10; W11 in claimline-edge.
- Probe PRs will be **closed without merging** to keep `main` clean.

## Environment quirks observed
- Commit-time secret guard blocks committing a literal AWS secret key; used the
  access-key-id canary alone for the hardcoded-credential probe.
- `claimline` git-over-HTTPS push works; direct-curl API writes are proxy-blocked
  (writes must go via MCP tools or git). Repo creation via API is blocked (owner must
  create repos manually).
- Out of scope and untouched: the `ReveloopRCM` org of real healthcare repos.
