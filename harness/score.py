#!/usr/bin/env python3
"""Score a tool's emitted comments against the ground-truth manifest.

For each manifest entry the matcher looks for a tool comment that (a) is anchored
to the same file within +/- ``--line-window`` lines, OR (b) mentions the file's
basename and contains any of the entry's ``detect_any`` substrings. Then:

  defect / canary matched   -> true positive
  defect / canary unmatched -> false negative
  decoy matched (flagged)   -> false positive
  any comment matching no entry -> 'unmatched' bucket (reviewed by hand)

IMPORTANT: this matcher must be validated against a hand-labeled fixture of real
comments before its numbers are trusted (see results/validation.md). Treat output
as provisional until that check passes.

Usage:
    python score.py --manifest ../probes/manifest.yaml \
        --evidence ../evidence/claimline/pr-2/<ts>.json --repo claimline --pr 2
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
from collections import defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _load_manifest(path: str) -> list[dict]:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(open(path).read()) or {}
    return data.get("probes", []) or []


def _comments(snap: dict) -> list[dict]:
    """Flatten all tool-authored comments with optional anchors."""
    out = []
    for it in snap.get("review_comments") or []:
        if isinstance(it, dict):
            out.append({
                "kind": "review_comment",
                "id": it.get("id"),
                "path": it.get("path"),
                "line": it.get("line") or it.get("original_line"),
                "body": it.get("body") or "",
                "user": (it.get("user") or {}).get("login", ""),
            })
    for it in snap.get("issue_comments") or []:
        if isinstance(it, dict):
            out.append({
                "kind": "issue_comment",
                "id": it.get("id"),
                "path": None,
                "line": None,
                "body": it.get("body") or "",
                "user": (it.get("user") or {}).get("login", ""),
            })
    return out


def _matches(entry: dict, c: dict, window: int, decoy: bool = False) -> bool:
    """A comment matches an entry only if it contains one of the entry's
    detect_any keywords AND is either anchored near the entry's line or names the
    entry's file. Keyword is always required (pure line-proximity is unreliable
    when several defects cluster in one file). Decoys match only when anchored.
    """
    body = c["body"].lower()
    needles = [n.lower() for n in entry.get("detect_any", [])]
    if not needles or not any(n in body for n in needles):
        return False
    anchored = (
        c["path"] == entry["file"]
        and c["line"] is not None
        and (entry.get("line") is None
             or abs(int(c["line"]) - int(entry["line"])) <= window)
    )
    if decoy:
        return anchored
    return anchored or os.path.basename(entry["file"]) in body


def score(manifest: list[dict], snap: dict, repo: str, pr: int, window: int) -> dict:
    entries = [e for e in manifest if e.get("repo") == repo and e.get("pr") == pr]
    comments = _comments(snap)
    bot_comments = [c for c in comments if "coderabbit" in c["user"].lower()]
    used_ids: set = set()

    per_cat = defaultdict(lambda: {"tp": 0, "fn": 0, "fp": 0})
    results = []
    for e in entries:
        cat = e.get("category", "uncategorized")
        kind = e.get("kind", "defect")
        if kind not in ("defect", "canary", "decoy"):
            # 'bonus' (real, unplanted) and 'invalid' (contaminated) are recorded
            # but never scored for recall/precision.
            results.append({"id": e["id"], "kind": kind, "category": cat,
                            "outcome": "not-scored", "matched_comment_id": None})
            continue
        hit = None
        for c in bot_comments:
            if _matches(e, c, window, decoy=(kind == "decoy")):
                hit = c
                break
        if kind == "decoy":
            if hit:
                per_cat[cat]["fp"] += 1
                used_ids.add(hit["id"])
                outcome = "FP (decoy flagged)"
            else:
                outcome = "OK (decoy not flagged)"
        else:  # defect / canary
            if hit:
                per_cat[cat]["tp"] += 1
                used_ids.add(hit["id"])
                outcome = "TP"
            else:
                per_cat[cat]["fn"] += 1
                outcome = "FN"
        results.append({"id": e["id"], "kind": kind, "category": cat,
                        "outcome": outcome, "matched_comment_id": hit["id"] if hit else None})

    unmatched = [{"id": c["id"], "user": c["user"], "path": c["path"],
                  "line": c["line"], "excerpt": c["body"][:160]}
                 for c in bot_comments if c["id"] not in used_ids]

    tp = sum(v["tp"] for v in per_cat.values())
    fn = sum(v["fn"] for v in per_cat.values())
    fp = sum(v["fp"] for v in per_cat.values())
    recall = tp / (tp + fn) if (tp + fn) else None
    precision = tp / (tp + fp) if (tp + fp) else None

    return {
        "repo": repo, "pr": pr,
        "totals": {"tp": tp, "fn": fn, "fp": fp,
                    "recall": recall, "precision": precision},
        "per_category": per_cat,
        "entries": results,
        "unmatched_bot_comments": unmatched,
        "bot_comment_count": len(bot_comments),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--line-window", type=int, default=5)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    manifest = _load_manifest(args.manifest)
    snap = json.loads(open(args.evidence).read())
    card = score(manifest, snap, args.repo, args.pr, args.line_window)
    text = json.dumps(card, indent=2, default=dict)
    if args.out:
        pathlib.Path(args.out).write_text(text)
    print(text)


if __name__ == "__main__":
    main()
