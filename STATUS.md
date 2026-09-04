# STATUS — transparent build & benchmark

_Last updated: 2026-09-04 (session session_019FtoBbsrGyBxSLTdgLe7tR)_

## Mode

Running the **transparent** variant agreed with the owner:
- Labs are honestly labeled as an intentional testbed (disclosure up front in
  `claimline/SECURITY.md`), no vocabulary-scrubbing or deception of the review tool.
- No prompt-injection / bidi-homoglyph subversion attacks (original Wave 7 dropped).
- Deliberately-vulnerable diffs live only in **PRs that are not merged**; `main`
  stays clean and green.
- Caveat to record in findings: because the repo openly discloses it is a testbed,
  numbers reflect CodeRabbit reviewing a repo it *can* tell is a testbed.

## Done

- **claimline baseline built and verified green locally** (committed on `main`,
  commit `10c8612` in the local clone / bundle):
  - `api/` Python 3.12 FastAPI + adjudication engine — ruff clean, 13 pytest pass.
  - `worker/` Go settlement worker — gofmt clean, go vet clean, go test pass.
  - `web/` TS/React console — tsc clean, eslint clean, 4 vitest pass.
  - `migrations/`, `openapi/`, `infra/` (Dockerfile + Terraform), `.github/workflows/ci.yml`.
  - `README.md` + `SECURITY.md` with the transparency disclosure.

## BLOCKED (owner action required)

1. **All GitHub writes to `claimline` are 403 (read-only integration).**
   - git push → `403 Claude doesn't have GitHub access ... for your organization`
   - MCP `create_or_update_file`/`push_files` → `403 Resource not accessible by integration`
   - direct curl writes → proxy-blocked
   - Reads succeed (get_me, list_branches), so the App is installed but **read-only**.
   - Likely cause: the App installation returned to read-only / pending approval when
     repo access was reconfigured to add the new repos.
   - **Fix:** grant the Claude GitHub App **write (contents), workflows, and
     pull-requests** permissions and include `claimline`, `claimline-edge`, and
     `dx-research`. Then a **fresh session** is probably needed so the git-proxy
     re-binds. Baseline is preserved as `claimline-baseline.bundle` (sent to owner)
     and committed in this container.

2. **`dx-research` and `claimline-edge` not visible to the session.**
   - Owner created them, but they do not appear in the session's repo listing and
     `add_repo` returns "no access" — the App installation hasn't been granted access
     to them either. Same fix as (1).

## Next (once write access is restored)

1. Push claimline baseline `main`; confirm CI green.
2. Push this `dx-research` scaffold (harness + manifest) once its repo is attached.
3. W0 fingerprint PR (trivial 1-line, then ~200-LOC mixed-defect PR), capture
   CodeRabbit anatomy/latency/login/check-run.
4. W1 detection matrix (8 family PRs), score recall/precision.
5. Continue W2–W4, W10; W11 in claimline-edge. Pace later waves via send_later.

## Notes

- Account also has access to a `ReveloopRCM` org of real healthcare repos — strictly
  out of scope; untouched.
- Harness/manifest are being built locally under `/home/user/dx-research` pending the
  repo becoming pushable.
