# dx-research

Analysis, harness, ground truth, and evidence for a **transparent** evaluation of
an AI code-review tool (CodeRabbit) against the `claimline` / `claimline-edge`
testbeds.

## Transparency mode

This evaluation is run openly, on repositories the account owner controls:

- The labs (`claimline`, `claimline-edge`) disclose up front, in their
  `SECURITY.md`, that they are testbeds that intentionally carry planted defects
  in un-merged PRs. There is **no** attempt to hide what is being measured from
  the review tool, and **no** adversarial prompt-injection / subversion testing.
- **Consequence for interpretation:** results reflect the tool reviewing a repo
  it can plainly tell is a testbed. That is an honest measurement, but it is not
  the same as a covert measurement, and comparisons to any "blind" numbers should
  not be made. This caveat is repeated in `FINDINGS.md`.

## Layout

| Path | Purpose |
|------|---------|
| `probes/manifest.yaml` | Ground truth: one entry per planted item (defect / decoy / canary). |
| `harness/collector.py` | Read-only snapshotter: dumps a PR's reviews, comments, checks, etc. to `evidence/`. |
| `harness/fingerprint.py` | Structural signature of a review comment (headings, emoji, tool lines, ...). |
| `harness/score.py` | Match emitted comments against the manifest → TP/FN/FP scorecard. |
| `evidence/<repo>/pr-<n>/<iso8601>.json` | Verbatim raw snapshots, append-only. |
| `results/` | Generated scorecards and markdown tables. |
| `FINDINGS.md` | Append-only, plain-prose observations per wave, with pr#/comment-id citations. |
| `STATUS.md` | Overwritten each wave: what's done, blocked, next. |

## Terminology

- **defect** — a real planted bug. Missed by the tool ⇒ false negative.
- **decoy** — code that looks wrong but is provably correct. Flagged ⇒ false positive.
- **canary** — an identical defect repeated across PRs / diff positions, for
  truncation and positional-bias measurement.
