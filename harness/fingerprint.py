#!/usr/bin/env python3
"""Structural fingerprint of a review comment / summary body.

Extracts a signature that is stable across PRs: markdown headings, emoji
vocabulary, severity words, whether GitHub ``suggestion`` blocks are used,
tool-attribution lines (e.g. ``🧰 ruff``, ``🪛 GitHub Actions``), and whether a
"Prompt for AI Agents" block is present. Useful for characterizing the tool's
output anatomy independent of correctness.

Usage:
    python fingerprint.py < body.md
    python fingerprint.py --evidence ../evidence/claimline/pr-1/<ts>.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys

HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿←-⇿⬀-⯿]"
)
SEVERITY_WORDS = [
    "critical", "high", "medium", "low", "minor", "major", "warning",
    "nitpick", "nit", "caution", "note", "potential issue", "suggestion",
    "refactor",
]
TOOL_LINE_RE = re.compile(r"^[\s>]*[\U0001F000-\U0001FAFF☀-➿].*\b([A-Za-z][\w.-]+)\b\s*$", re.MULTILINE)


def fingerprint(body: str) -> dict:
    lower = body.lower()
    headings = HEADING_RE.findall(body)
    emojis = sorted(set(EMOJI_RE.findall(body)))
    severities = sorted({w for w in SEVERITY_WORDS if w in lower})
    return {
        "length": len(body),
        "headings": headings,
        "emoji": emojis,
        "severity_words": severities,
        "has_suggestion_block": "```suggestion" in body,
        "has_diff_block": "```diff" in body,
        "has_prompt_for_ai_agents": "prompt for ai agents" in lower,
        "has_committable_suggestion": "committable suggestion" in lower,
        "mentions_walkthrough": "walkthrough" in lower,
        "mentions_sequence_diagram": "sequencediagram" in lower.replace(" ", "")
        or "sequence diagram" in lower,
        "tool_attribution_hits": sorted(set(TOOL_LINE_RE.findall(body)))[:20],
    }


def _bodies_from_evidence(path: str) -> list[str]:
    snap = json.loads(open(path).read())
    bodies: list[str] = []
    for key in ("issue_comments", "review_comments", "reviews"):
        items = snap.get(key)
        if isinstance(items, list):
            for it in items:
                if isinstance(it, dict) and it.get("body"):
                    bodies.append(it["body"])
    return bodies


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence", help="path to a collector snapshot JSON")
    args = ap.parse_args()

    if args.evidence:
        bodies = _bodies_from_evidence(args.evidence)
        print(json.dumps([fingerprint(b) for b in bodies], indent=2))
    else:
        body = sys.stdin.read()
        print(json.dumps(fingerprint(body), indent=2))


if __name__ == "__main__":
    main()
