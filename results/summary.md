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
| PHI/domain (assertive) | 2/5 | 100% | **`presidio` never fires**; PHI = generic CWE-598/359 egress only; misses PHI in logs/errors/fixtures (see `results/phi.md`) |
| W0 mixed (13) | 7-9/13 | 100% | across 4 runs |

_Note: the recall figures above are the original single-run/CHILL values; the **N≥3 assertive
means** (which revise several of them, esp. performance and correctness) are in `results/repeats.md`._

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
- **Performance family: 0/8 (CHILL) -> single-run 4/8 (assertive, PR #12).** ⚠️ **N≥3 REVISES
  THIS DOWN** (see `results/repeats.md`, PRs #27/#28/#29): mean **perf-*framed* recall is only
  1.7/8 (21%)**, range 1–3/8 — the single-run 4/8 was the lucky top of a wide range, not a stable
  quadrupling. What IS robust: the defects' inefficiencies still get *fixed* ~50% of the time
  (**by-fix mean 4/8**), but usually under a **correctness/security label**, not a performance one —
  CodeRabbit's agentic static analysis finds a co-located bug at the perf defect's exact line
  (CSV-injection, cross-payer contamination, Unicode-regex) and reports that instead. Only
  load-then-filter→SQL is a stable perf-framed catch (3/3). Precision still 100%.
- **Mixed probe under assertive recovered the unbounded-O(n^2) dedup** that CHILL stably
  missed — but **still missed the dead-code security defects** (SQLi in an uncalled fn,
  SSRF, resource-leak, XSS in an unrendered component).

**Two causes, cleanly separated:**
1. **Performance / soft-issue misses = profile conservatism** — fixed by `assertive`.
2. **Unreachable/dead-code security misses = reachability/context gating** — NOT fixed by
   `assertive`; would require the defect to be reachable (or a whole-file/context setting).

Practical takeaway for the owner: the **default CHILL profile is materially under-reporting
performance and soft issues**, and `assertive` raises comment volume and by-fix coverage with no
precision cost — but (per the N≥3 correction above) **do not treat CodeRabbit as a reliable
performance reviewer**: whether it *labels/reasons* an issue as performance is high-variance
(21% perf-framed over N≥3). Its agentic pass is better understood as a general co-located-bug
finder that frequently surfaces the more-severe correctness/security issue sitting on the same
line. Neither profile will, by itself, surface issues in code the tool judges unreachable.

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

## 9. Partially answered (with evidence) vs not done

**Partially answered already (reclassified from "not done"):**
- **W2 (context scope beyond the diff):** demonstrated. CodeRabbit reasons across files and
  beyond the changed lines — the dead-code security gating (SQLi in an uncalled fn, XSS in an
  unrendered component), the migration comment cross-referencing `imports.py` idempotency, and
  the `🔎 Supported by static analysis` blocks that run `sed`/`rg` over other files
  (e.g. reading `pyproject.toml` to confirm the missing `requests` dep). Evidence: PR #2/#4/#6
  comments and the `W0-BONUS-DEP` finding. Not done: the controlled diff-only-vs-whole-file and
  third-config-file single-variable probes.
- **W5 (triggers/limits):** partially answered. Observed the "up to 10 included reviews/hour"
  quota line with a live remaining counter (PR #1), the **auto-review pause after ~11 PRs**
  (PR #11), and that a manual `@coderabbitai review` still returns a full review in ~12s
  (PR #11/#12/#13/#14). Not done: draft-vs-ready, `auto_review.labels`, `ignore_title_keywords`,
  `@coderabbitai ignore`, non-default base, force-push/reopen, `auto_pause_after_reviewed_commits`.

**In progress (this session, resumed):** N>=3 repeats under assertive per family
(results/repeats.md); PHI/domain family (presidio); W6 learnings-persistence + autofix/docstrings/
unit-test checkboxes; api-contract + iac-ci families.

**W7 (robustness / prompt-injection):** legitimate authorized-security-testing in principle
(owner's tool, owner's repos, contained in `claimline`, defensive merge-gating question).
Excluded pending the **owner's direct confirmation in-session** — I told the owner this item
must come from them directly, and the current go-ahead arrived via the parent-session/automated
relay, not the owner's own message. Will run defensively-scoped (comment/PR-body/CLAUDE.md
instruction-injection + homoglyph/bidi smuggling, N>=2/arm vs a measured baseline, reported as a
limitation) once the owner confirms directly. Noteworthy prior: CodeRabbit already ships an
anti-injection preamble in its "Prompt for AI Agents" block, so the test is whether that
hardening extends to its own intake.

**Skipped (low value per owner):** W3 (scale/truncation), W11 (private control — public repo is
already on the paid Advanced tier). W9 (pre-merge depth) remains optional.
