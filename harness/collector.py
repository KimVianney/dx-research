#!/usr/bin/env python3
"""Read-only PR evidence snapshotter.

Dumps a pull request's reviews, inline review comments, issue comments, check
runs, combined commit status, timeline, and labels into a single timestamped
JSON snapshot under ``evidence/<repo>/pr-<n>/<iso8601>.json``. It never mutates
the PR.

It shells out to ``curl`` so it inherits the environment's HTTPS proxy and CA
bundle. Authentication uses ``$GH_TOKEN`` (falls back to ``$GITHUB_TOKEN``).

Usage:
    python collector.py --owner KimVianney --repo claimline --pr 1
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys

API = "https://api.github.com"


def _token() -> str:
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        sys.exit("no GH_TOKEN / GITHUB_TOKEN in environment")
    return tok


def _get(path: str) -> object:
    """GET an API path (may be relative to API root) and return parsed JSON."""
    url = path if path.startswith("http") else f"{API}{path}"
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}per_page=100"
    out = subprocess.run(
        [
            "curl", "-sS", "-H", f"Authorization: Bearer {_token()}",
            "-H", "Accept: application/vnd.github+json", url,
        ],
        capture_output=True, text=True, check=True,
    ).stdout
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"_raw": out}


def snapshot(owner: str, repo: str, pr: int) -> dict:
    base = f"/repos/{owner}/{repo}"
    pull = _get(f"{base}/pulls/{pr}")
    head_sha = ""
    if isinstance(pull, dict):
        head_sha = (pull.get("head") or {}).get("sha", "")

    snap = {
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "owner": owner,
        "repo": repo,
        "pr": pr,
        "head_sha": head_sha,
        "pull": pull,
        "reviews": _get(f"{base}/pulls/{pr}/reviews"),
        "review_comments": _get(f"{base}/pulls/{pr}/comments"),
        "issue_comments": _get(f"{base}/issues/{pr}/comments"),
        "timeline": _get(f"{base}/issues/{pr}/timeline"),
        "labels": _get(f"{base}/issues/{pr}/labels"),
    }
    if head_sha:
        snap["check_runs"] = _get(f"{base}/commits/{head_sha}/check-runs")
        snap["combined_status"] = _get(f"{base}/commits/{head_sha}/status")
    return snap


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--out-root", default=str(pathlib.Path(__file__).resolve().parent.parent / "evidence"))
    args = ap.parse_args()

    snap = snapshot(args.owner, args.repo, args.pr)
    ts = snap["captured_at"].replace(":", "").replace("-", "")
    out_dir = pathlib.Path(args.out_root) / args.repo / f"pr-{args.pr}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{ts}.json"
    out_file.write_text(json.dumps(snap, indent=2, sort_keys=True))

    n_reviews = len(snap["reviews"]) if isinstance(snap["reviews"], list) else 0
    n_rc = len(snap["review_comments"]) if isinstance(snap["review_comments"], list) else 0
    n_ic = len(snap["issue_comments"]) if isinstance(snap["issue_comments"], list) else 0
    print(f"wrote {out_file}")
    print(f"  reviews={n_reviews} review_comments={n_rc} issue_comments={n_ic} head={snap['head_sha'][:7]}")


if __name__ == "__main__":
    main()
