# PHI / domain family — does CodeRabbit catch healthcare PHI leaks? Does `presidio` fire?

Probe: `api/claimline/phi.py` (PR #30, assertive). Five planted PHI defects + one redacted-logging
decoy. Synthetic member data only; helper functions, no live endpoints. Hand-validated.

## Result: recall 2/5 (40%), precision 100%, and **`presidio` NEVER fired**

| id | line | defect | detected? | how CodeRabbit framed it |
|---|---|---|---|---|
| PHI-LOG | 28 | name+DOB+SSN logged at INFO | **MISS** | — (no CWE-532 / log-PHI finding) |
| PHI-ERROR-MSG | 40 | name/DOB/SSN in error string | **MISS** | — |
| PHI-URL-QUERY | 49 | SSN+DOB in URL query params | **HIT** | 🔒 Security & Privacy, Major, **CWE-598** "Keep SSNs out of eligibility URLs" |
| PHI-API-BOUNDARY | 60 | full member record to payer (min-necessary) | **HIT** | 🔒 Security & Privacy, Major, **CWE-359** "Send only fields required by the payer" |
| PHI-FIXTURE | 65 | hardcoded realistic PHI in source | **MISS** | — |
| PHI-DECOY-REDACTED | 86 | already SSN-masked | not flagged (correct) | precision preserved |

## The `presidio` answer (the owner's specific question)
**No.** Across PR #30's review — including the agentic `🔎 Supported by static analysis` /
`🧩 Analysis chain` blocks, which `cat` the file and `rg` for usages — the string `presidio`
appears **nowhere**. There is no 🧰 Tools / 🪛 tool-attribution line for any PII/PHI scanner. PHI is
detected purely by **CodeRabbit's own security reasoning**, and it is filed under **🔒 Security &
Privacy with generic CWE codes (598 Sensitive-data-in-URL, 359 Exposure-of-private-info)** — not as
a dedicated HIPAA/PHI/PII category, and not by presidio. (Consistent with presidio never appearing
in 110+ prior comments across the whole study.)

## What this means for a healthcare-RCM owner
CodeRabbit is **not a PHI/HIPAA linter**. It reliably catches **egress-shaped** PHI leaks — data
*leaving* the system where a channel is inherently loggable/observable (SSN in a URL; over-sharing
across a payer API boundary) — and it even ran reachability analysis on both (the `cr-reachability`
tag) and flagged them anyway despite the helpers being uncalled. But it **misses PHI at rest**: PHI
written to application logs (the canonical CWE-532 that a PHI scanner exists to catch), PHI baked
into error messages, and unredacted PHI hardcoded in source/fixtures. If PHI-in-logs is a
compliance concern, CodeRabbit alone will not cover it — a dedicated scanner (presidio, a log
filter, or a custom `.coderabbit.yaml` path-instruction) is still needed.

## Note on framing variance
The URL line (49) drew TWO stacked comments — a `urlencode` correctness nit AND the CWE-598 PHI
finding — the same co-located-multiple-findings behavior seen in the performance family. The PHI
recall counts only the security/PHI-framed findings.
