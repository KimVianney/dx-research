# STATUS — transparent CodeRabbit evaluation (winding down)

_Last updated: 2026-09-05 ~01:35Z (session session_019FtoBbsrGyBxSLTdgLe7tR)_

## State: core study complete; pipeline stopped.
Consolidated write-up in results/summary.md. All evidence in evidence/**, per-PR
scorecards in results/scorecard_pr*.json, FINDINGS.md (append-only), profiles.md,
determinism.md, validation.md.

## Waves done
- W0 fingerprint + mixed detection (PRs #1,#2 and reduced re-run #4).
- W1 families: A correctness 10/10 (#3/#5), B security-helpers 3/9 (#8),
  C concurrency 6/7 (#9), D performance 0/8 (#10), E error-handling 4/7 (#11).
- W10 determinism: 3 identical runs (#4/#6/#7) -> 31% of defects flip; recall 54-69%.
- Disclosure A/B (#2/#3 fuller vs #4/#5 reduced): confounded by variance.
- W4 config: profile assertive perf 0/8->4/8 (#12), mixed under assertive (#13),
  two-cause resolution (profile vs reachability); linter toggle + CI ingestion (#14).

## Key results
- Precision 100% across all families (0 hard FPs; decoys never falsely flagged).
- Recall tracks defect TYPE; wide run-to-run variance (report N>=3).
- Default CHILL under-reports performance/soft issues; assertive is the biggest lever.
- Dead-code security defects gated by reachability, not fixed by profile.
- Auto-review pauses under burst; manual @coderabbitai review still works.

## Repo hygiene
- claimline main clean + green; .coderabbit.yaml = assertive (ruff re-enabled).
- All 14 probe PRs closed unmerged. dx-research PRIVATE (owner can flip in UI).

## Not done (future work)
W2 context-scope, W3 scale/truncation, W5 triggers, W6 interactive/agentic (beyond manual
review), W7 robustness/prompt-injection (out of transparent scope), W9 pre-merge depth,
W11 private control; remaining W1 families (api-contract/iac-ci/phi-domain); N>=3 repeats
for headline recall. Owner action optional: make dx-research public if the parent session
needs read access (declined the side-channel PATCH per transparent constraints).
