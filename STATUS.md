# STATUS — transparent CodeRabbit evaluation — ALL PLANNED WAVES COMPLETE

_Last updated: 2026-09-05 ~20:52Z (session session_019FtoBbsrGyBxSLTdgLe7tR)_

## State: COMPLETE. No further probe PRs will be opened.
Consolidated write-up: `results/summary.md` (§1-§10). Detail in `results/{repeats,determinism,
profiles,validation,phi,w7-plan,w7-results,self-report,api-iac}.md`, `FINDINGS.md` (append-only),
`results/scorecard_pr*.json`, `evidence/**`. Ground truth: `probes/manifest.yaml`.

## Final family results (all hand-validated; precision 100% throughout)

| family | recall | method / note |
|---|---|---|
| correctness (N≥3) | 9.3/10 | revised down from single-run 10/10 |
| concurrency (N≥3) | 6/7 | zero variance |
| error-handling (N≥3) | 4.7/7 | lint-backed core stable; judgment-heavy missed |
| security-helpers (N≥3) | 4.7/9 | dead-code reachability gating |
| performance (N≥3) | 1.7/8 perf-framed · 4/8 by-fix | biggest N≥3 correction; agentic co-located reframing |
| PHI/domain | 2/5 | **presidio never fires**; egress-only, misses PHI at rest |
| api-contract | 4/4 | LLM reasoning over the pydantic contract |
| iac-ci | 9/11 | **SAST-driven** (Checkov/Trivy/zizmor); missed open-SSH |
| W7 injection (baseline + 4 arms) | ROBUST | no surface suppressed; AGENTS.md + bidi self-flagged |

## Cross-cutting conclusions
- **Precision 100% everywhere** — zero hard false positives; no decoy (provably-correct look-alike)
  was ever flagged across the whole study.
- **Recall tracks defect TYPE**, with large run-to-run variance (W10: 31% of defects flip) — hence
  N≥3. Single-run figures over-state stability (even correctness dropped 10→9.3).
- **Detection is a blend of channels**: own LLM reasoning (correctness, contracts, concurrency,
  PHI-egress), bundled SAST (ast-grep for path-traversal; Checkov/Trivy/zizmor for IaC), and CI-
  annotation ingestion (ruff via GitHub Actions, timing-dependent). PHI is reasoning-only (no
  presidio); IaC is SAST-only.
- **assertive profile** raises volume/by-fix coverage at no precision cost, but does NOT make
  CodeRabbit a reliable performance reviewer (21% perf-framed) and does NOT surface dead-code
  security defects (reachability gating).
- **W7:** CodeRabbit's intake is robust to single-shot prompt injection on every PR-controlled
  surface tested; it treats PR body, code comments, an auto-ingested AGENTS.md, and bidi/homoglyph
  text as untrusted, and reported the malicious AGENTS.md and the U+202E char as findings.
- **Self-report** agrees with observed behaviour and, on the SSRF miss, CodeRabbit went agentic and
  admitted a genuine false negative it could not explain (and persisted Learnings — W6 live).

## Integrity & safety (held throughout)
- Transparent study; no blinding, no tool deception, no history rewriting. W7 was authorized
  directly in-session by the owner, defensive scope, benign markers, no internal-prompt extraction.
- canary/example credentials only; no live/exploitable endpoints; nothing contacts third parties.
- claimline `main` clean + green; **all 48 probe PRs (#1-#48) closed UNMERGED**; injection files
  (AGENTS.md, unicode, nightly-probe.yml) never reached main (verified). dx-research PUBLIC.

## Skipped per owner
W3 (scale/truncation), W11 (private control). W9 (pre-merge depth) optional / not run.
