# CodeRabbit evaluation — consolidated summary

Transparent evaluation of CodeRabbit (AI code-review GitHub App) on
`KimVianney/claimline` (public) with a private analysis repo `dx-research`. This file
consolidates the evidence in `FINDINGS.md`, `results/*.json`, `results/profiles.md`,
`results/determinism.md`, and `evidence/**`. **All numbers are observed and
hand-validated; every recall figure is single-run and therefore provisional** — see the
determinism section for why that matters.

## 0. Mode & integrity

- **Transparent** evaluation: the lab was an honest project; no blinding, no deception of
  the tool, no prompt-injection/subversion testing, no git-history rewriting. The initial
  `SECURITY.md`/`README` disclosure was softened via an ordinary forward commit (no history
  rewrite); originals preserved verbatim in `dx-research/disclosure/`.
- **Caveat:** results describe CodeRabbit reviewing a repo it can plainly tell is a demo.
- **Safety:** canary/example credentials only; no live/exploitable endpoints committed
  (the routed-endpoint security family was blocked by the environment guard and abandoned);
  nothing contacts third parties; probe PRs closed unmerged; `main` clean + green.
- Subject config: bot `coderabbitai[bot]`, **Plan: Advanced** (paid), default **profile
  CHILL**, later **assertive** via `.coderabbit.yaml`.

## 1. Fingerprint / output anatomy

- Fires **unprompted within seconds**; ~50s on a 1-line PR, ~4-5 min on ~200 LOC.
- Posts one **issue comment edited in place** (in-progress -> summary) + a submitted
  **review** with inline comments. On a clean trivial PR: "No actionable comments" (no
  invented nits).
- Inline finding = `category | severity | effort` header (🔒/🎯/🩺/📐/🗄️ · Major/Minor ·
  Quick win/Heavy lift), a title, prose (security adds CWE + Reachability/Exploitability),
  optional `🧰 Tools` linter attribution, a `🔎 Supported by static analysis` block that
  **shows shell/rg scripts CodeRabbit actually ran** (agentic verification), and a
  `🤖 Prompt for AI Agents` block that itself opens with an **anti-prompt-injection preamble**.
- Summary adds Walkthrough table, Estimated review effort, Merge Risk, Suggested reviewers,
  a Pre-merge-checks table, and a quota line ("up to 10 included reviews/hour").

## 2. Cross-family detection matrix (CHILL default, single-run/provisional)

| family | recall | precision | notes |
|---|---|---|---|
| correctness (W1-A) | 10/10 | 100% | identical under fuller vs reduced disclosure |
| concurrency (W1-C) | 6/7 | 100% | missed only the `time.Tick` leak; understood Go 1.22 semantics |
| error-handling (W1-E) | 4/7 | 100% | caught mechanical ones; missed judgment-y ones |
| security (helpers, W1-B) | 3/9 | 100% | many missed in an uncalled module |
| performance (W1-D) | 0/8 | 100% | **CHILL suppresses perf** (see §5) |
| W0 mixed (13) | 7-9/13 | 100% | across 4 runs |

**Precision was 100% in every family** — zero hard false positives; decoys (provably
correct look-alikes) were never falsely flagged. **Recall varies enormously by defect
type**: mechanical/correctness/concurrency high; performance and low-context security low.
Detection tracks **defect type more than reachability** (concurrency helpers 6/7 vs security
helpers 3/9 in equally-uncalled modules), with reachability a secondary factor (see §5).

Bonus: across families CodeRabbit repeatedly found **real, unplanted bugs** (a `units`
correctness bug, a missing `requests` dependency verified by running scripts, a dedup-key
mismatch, etc.).

## 3. Determinism (W10) — the key caveat

Same diff, 3 identical reviews (PRs #4/#6/#7): **4 of 13 defects (31%) flipped** TP<->FN;
recall ranged **7/13–9/13 (54%–69%)** on identical input. Stable-detected: path-traversal,
md5, bare-except, Go race, CI-injection, migration. Stable-missed: resource-leak, unbounded
O(n^2), SSRF. Unstable: SQLi (dead fn), hardcoded key, XSS (unused cmp), a correctness bug.
**Implication: single-run per-defect recall is unreliable; report mean/range over N>=3.**

## 4. Disclosure A/B — inconclusive (confounded)

Fuller-disclosure PRs (#2/#3) vs reduced-disclosure re-runs (#4/#5): correctness identical
(10/10 both); on the mixed probe md5/SSRF/hardcoded-key differed across arms but **within
the run-to-run variance from §3**, so no clean disclosure effect can be attributed. The
owner's original question (was the AWS-key's Minor/Stability rating README-induced?) is
**not answerable** at n=1/arm given the variance.

## 5. Config profile (W4) — the biggest lever, and a two-cause resolution

`.coderabbit.yaml profile: assertive` vs default CHILL, identical probes:
- **Performance family: 0/8 (CHILL) -> 4/8 (assertive)**, comment volume 4->8, precision
  still 100%. Assertive caught recompute-O(n^2), quadratic membership, load-then-filter
  (push to SQL), regex-compile-in-loop.
- **Mixed probe under assertive recovered the unbounded-O(n^2) dedup** that CHILL stably
  missed — but **still missed the dead-code security defects** (SQLi in an uncalled fn,
  SSRF, resource-leak, XSS in an unrendered component).

**Two causes, cleanly separated:**
1. **Performance / soft-issue misses = profile conservatism** — fixed by `assertive`.
2. **Unreachable/dead-code security misses = reachability/context gating** — NOT fixed by
   `assertive`; would require the defect to be reachable (or a whole-file/context setting).

Practical takeaway for the owner: the **default CHILL profile is materially under-reporting
performance and soft issues**; switching to `assertive` roughly quadrupled perf recall with
no precision cost. It will not, by itself, surface issues in code the tool judges unreachable.

## 6. Linters & CI integration (W4 toggle / W8 preview)

- CodeRabbit is **not merely surfacing ruff**: on CHILL it missed md5/SQLi that ruff catches;
  under assertive it caught them.
- Disabling CodeRabbit's built-in ruff (`tools.ruff.enabled: false`) did **not** remove a
  lint finding, because CodeRabbit **also ingests GitHub Actions CI check annotations**
  (tool line `🪛 GitHub Actions: CI/api -> Ruff F401`) and re-surfaces them with a fix diff.
  Two independent deterministic channels (built-in linters + CI ingestion).
- CI-annotation ingestion depends on **CI having finished before the review runs** (on the
  fast W0 CHILL reviews, CI annotations were not yet available and weren't surfaced).

## 7. Operations

- **Auto-review pauses under sustained volume** (~11 PRs / ~5.5h): a new PR got no
  auto-review, but a manual `@coderabbitai review` produced a full review in ~12s. Drive
  reviews manually after a burst; space PRs out.
- Formal `reviews` API can be empty on no-comment runs; always read issue + inline comments.

## 8. Harness integrity

`score.py`'s automated matcher was **validated against hand-labeling** (W0) and repeatedly
corrected (proximity-only matching and over-generic keywords caused false TP/FP); every
wave's numbers here are the **hand-validated** ones, not the raw matcher output.

## 9. What was NOT done (scope / future work)

W2 (context scope), W3 (scale/truncation), W5 (triggers), W6 (interactive/agentic beyond the
manual-review probe), W7 (robustness/prompt-injection — deliberately excluded as out of
transparent scope), W9 (pre-merge checks depth), W11 (private control — deprioritized since
the public repo is already on the paid Advanced tier). The per-family recalls should be
repeated N>=3 for headline numbers (see §3). Remaining W1 families api-contract / iac-ci /
phi-domain were not run (auto-review throttle + a natural stopping point after the profile
result).
