# Security policy

## This is a testbed, not a production system

`claimline` exists to demonstrate a polyglot service and to **evaluate
code-review and static-analysis tooling**. Please read the following before
drawing conclusions from anything in this repository:

- **Intentional defects.** Some feature branches and pull requests deliberately
  introduce bugs, insecure patterns, or misconfigurations so that automated
  review tools can be measured against a documented, known baseline. Their
  presence on a branch or in a PR is by design.
- **`main` is clean.** The default branch is kept free of intentional defects
  and is expected to pass CI. Intentional-defect changes are opened as pull
  requests and are **not merged** into `main`.
- **Canary secrets only.** Any credential-looking string in this repository is a
  well-known, non-functional placeholder (for example AWS's documented
  `AKIAIOSFODNN7EXAMPLE`). Nothing here authenticates to any real system, and
  nothing contacts a third-party service.
- **No real data.** All member IDs, claims, and payer records are synthetic. Do
  not submit real protected health information (PHI) or real credentials to this
  project.

## Reporting

Because this is an evaluation testbed rather than a deployed service, there is no
vulnerability disclosure process. Findings surfaced by review tooling are the
point of the exercise, not incidents to report.
