# api-contract & iac-ci families (PRs #47, #48, assertive)

Hand-validated. The interesting result is the **tool attribution** contrast with PHI.

## api-contract (PR #47) — recall 4/4 (100%), precision 100%

| defect | line | caught | how |
|---|---|---|---|
| APIC-SHAPE (dict missing `currency`, paid_cents as str) | 34 | ✅ | "Return a valid ClaimResponse object" (Data Integrity, Major) |
| APIC-ENUM (`status="settled"` not in Literal) | 42 | ✅ | ran a **web query** confirming Pydantic 2.6 raises ValidationError, then flagged it |
| APIC-STATUS-CODE (returns 200, contract says 201) | 51 | ✅ | "Return the documented create response" (also caught the omitted fields) |
| APIC-NULL (returns None though `-> ClaimResponse`) | 59 | ✅ | "Make the missing-claim result explicit; return `ClaimResponse | None`" |
| decoy APIC-DECOY-OK | 68 | not flagged (correct) | — |

CodeRabbit is strong on **response-contract drift** reasoned from the pydantic model + docstring —
no external schema tool needed; it even web-verified the Literal/ValidationError behavior.

## iac-ci (PR #48) — recall 9/11, precision 100%; **SAST-driven**

| defect | file:line | caught | tool |
|---|---|---|---|
| S3 public-read ACL | reporting.tf:5 | ✅ | Checkov/Trivy |
| S3 public-access-block all-false | reporting.tf:10 | ⚠️ folded into the public-bucket finding (same vuln), not a separate thread |
| SSH 0.0.0.0/0 → port 22 | reporting.tf:24 | ❌ **MISS** | — |
| hardcoded DB password | reporting.tf:34 | ✅ | Checkov/Trivy ("remove and rotate") |
| RDS storage_encrypted=false | reporting.tf:35 | ✅ | Checkov/Trivy |
| RDS publicly_accessible=true | reporting.tf:36 | ✅ | Checkov/Trivy (CWE-668) |
| Docker python:latest unpinned | Dockerfile.batch:1 | ✅ | Checkov/Trivy |
| Docker ADD+run remote script | Dockerfile.batch:3/4 | ✅ | Checkov (Critical) |
| Docker USER root | Dockerfile.batch:10 | ✅ | Checkov/Trivy (CWE-250) |
| GH Actions permissions: write-all | nightly-probe.yml:5 | ✅ | zizmor (CWE-250) |
| GH Actions checkout@main unpinned | nightly-probe.yml:11 | ✅ | zizmor |
| decoy audit bucket (private+KMS+blocked) | reporting.tf:48 | not flagged (correct) | — |

**Recall 9/11 (82%)** counting S3-noblock and SSH-open as misses; **10/11** if S3-noblock is
credited (its public-access risk WAS reported via the bucket finding). The one clear, surprising
miss is **SSH open to 0.0.0.0/0** — a textbook Checkov rule (CKV_AWS_24) that did not surface.
Precision 100% (audit-bucket decoy untouched). **3 bonus real findings**: missing
`skip_final_snapshot` recoverability, pip `--no-cache-dir`, and a workflow schedule/placeholder nit.

### Tool attribution — the headline for these families
Unlike PHI (pure LLM reasoning, no tool line), **IaC detection is almost entirely SAST-driven**:
every terraform/Dockerfile finding carries `🧰 Tools · 🪛 Checkov`/`Trivy` and GH-Actions findings
carry `🪛 zizmor`, tagged `_Source: Linters/SAST tools_`. So for IaC, CodeRabbit is largely a
well-integrated front-end over checkov/trivy/zizmor — which explains both the high recall on
tool-covered rules and the miss on a rule that didn't fire. api-contract, by contrast, is LLM
reasoning over the pydantic contract (no schema SAST), and it was perfect on this probe.
