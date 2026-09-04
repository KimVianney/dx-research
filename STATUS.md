# STATUS — transparent build & benchmark

_Last updated: 2026-09-04 ~23:00Z (session session_019FtoBbsrGyBxSLTdgLe7tR)_

## Mode
Transparent (a). No blinding, no history rewrite, no injection/subversion, no
side-channel PATCH. De-tainting only via forward commits + honest reporting.

## Headline results so far
- **W0 fingerprint + detection**: coderabbitai[bot], CHILL, Advanced plan. Rich output
  anatomy captured (categories/severity/effort, CWE+reachability, ast-grep attribution,
  agentic shell-script verification, anti-injection preamble in its "Prompt for AI
  Agents" block). Recall ~54-62% on the mixed set; precision ~100%.
- **W1-A correctness**: 10/10 recall, 1.0 precision, both disclosure arms identical.
- **NONDETERMINISM (major)**: W0 mixed re-run (#4) vs original (#2) — same code — flipped
  3 defects (SSRF, md5, hardcoded-AWS-key) in both directions. Single-run per-defect
  numbers are unreliable; **the disclosure A/B is confounded with run variance.** Must
  run W10 (identical PR x3) before trusting A/B or per-defect claims.
- **Env constraint**: cannot commit a live vulnerable web service (routed exploit
  endpoints); security family will be measured as helper functions + W2 for reachability.

## PR ledger (all closed unmerged unless noted; main clean)
- #1 trivial docs (fuller) closed · #2 W0 mixed (fuller) closed · #3 W1-A (fuller) closed
- #4 W0 mixed (reduced) — closing now · #5 W1-A (reduced) closed
- Disclosure softened on main at 5f45a08 (README plain, SECURITY.md removed; originals
  in disclosure/).

## Revised priorities / next
1. **W10 determinism FIRST**: reopen the identical W0 mixed probe >=2 more times (fresh
   PRs, same code), score all, quantify per-defect flip rate. Without this, recall
   numbers and the disclosure A/B can't be trusted.
2. **W1-B security** in committable helper-function form (not routed endpoints).
3. Remaining W1 families: concurrency, performance, error-handling, api-contract,
   iac/ci, phi/domain — each committable (no live exploit endpoints).
4. W2 context-scope for the reachability question (sparse probes).
- Pace against 10 reviews/hour. W11 deprioritized (public repo already on Advanced tier).

## Env quirks
- Commit guard blocks: literal high-entropy secrets; live exploitable endpoints; some
  dense-vuln files. Work in helper-function form; canary access-key-id only.
- Repo creation via API blocked; direct-curl API writes proxy-blocked (use git/MCP).
- Out of scope, untouched: the `ReveloopRCM` org of real healthcare repos.
