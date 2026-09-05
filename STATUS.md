# STATUS — transparent CodeRabbit evaluation (pipeline RUNNING)

_Last updated: 2026-09-05 ~11:35Z (session session_019FtoBbsrGyBxSLTdgLe7tR)_

## State: core study complete + refinement pipeline actively running.
Consolidated write-up in results/summary.md. Evidence in evidence/**, per-PR scorecards in
results/scorecard_pr*.json, FINDINGS.md (append-only), profiles.md, determinism.md, validation.md,
repeats.md (N≥3), w7-plan.md, self-report.md.

## Waves done (single-run core)
- W0 fingerprint + mixed detection (PRs #1,#2, reduced re-run #4).
- W1 families: A correctness 10/10 (#3/#5), B security-helpers 3/9 (#8), C concurrency 6/7 (#9),
  D performance 0/8->4/8 assertive (#10/#12), E error-handling 4/7 (#11).
- W10 determinism: 3 identical runs (#4/#6/#7) -> 31% of defects flip; recall 54-69%.
- Disclosure A/B (#2/#3 vs #4/#5): confounded by variance.
- W4 config: profile assertive perf 0/8->4/8 (#12), mixed under assertive (#13), two-cause
  resolution (profile vs reachability); linter toggle + CI ingestion (#14).

## N>=3 repeats under assertive (results/repeats.md) — IN PROGRESS
- security-helpers (#15/#16/#17): mean 4.7/9 (52%), range 44-67%. DONE.
- concurrency (#18/#19/#20): mean 6/7 (86%), range 0. DONE.
- error-handling (#21/#22/#23): mean 4.7/7 (67%), range 57-71%. DONE.
- correctness (#24/#25/#26): batch open, collection scheduled. IN PROGRESS.
- performance: next batch (cherry-pick 071d87c, --manifest-pr 10).

## Key results
- Precision 100% across all families (0 hard FPs; decoys never falsely flagged).
- Recall tracks defect TYPE; wide run-to-run variance (report N>=3).
- Mechanical/lint-backed defects = stable-caught floor; judgment-heavy = stable-missed; assertive
  mostly adds flaky recovery, not new depth.
- Default CHILL under-reports performance/soft issues; assertive is the biggest lever.
- Dead-code security defects gated by reachability, not fixed by profile.
- Auto-review pauses under sustained burst; manual @coderabbitai review still works. (This
  session's P1 batches auto-reviewed without pausing.)

## Authorization / scope updates (were stale — now corrected)
- **W7 (prompt-injection robustness): AUTHORIZED** by the owner directly in-session (2026-09-05,
  AskUserQuestion). Defensive scope only; plan in results/w7-plan.md (canary corrected to
  path-traversal + bare-except + Go race, baseline N=3, pre-registered decision rule). No
  internal-prompt extraction. QUEUED after the P1 repeats + PHI.
- **dx-research is PUBLIC** (verified via API: private=false). Owner flipped it in the UI; the
  side-channel PATCH was never used.

## Repo hygiene
- claimline main clean + green; .coderabbit.yaml = assertive (ruff re-enabled).
- All probe PRs closed unmerged (#1-#23 closed; #24-#26 open under review, will close unmerged).

## Remaining pipeline (task order)
1. Finish P1 N>=3: correctness (open), performance (next).
2. P2 PHI/domain family (presidio) — owner's actual domain (healthcare RCM); also the only way to
   learn whether `presidio` ever fires (not seen in 110+ comments).
3. W7 (corrected plan).
4. P3 self-report probe (results/self-report.md) + autofix/docstrings/unit-test checkboxes.
5. P4 api-contract + iac-ci families.
Skipped per owner: W3 scale/truncation, W11 private control. W9 pre-merge depth optional.
