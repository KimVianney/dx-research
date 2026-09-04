# score.py validation against hand-labeled comments (W0 PR #2)

The brief requires validating `score.py` before trusting its numbers. W0 PR #2 (10
inline CodeRabbit comments) was the first fixture. Every comment was read by hand and
mapped to a manifest entry; the automated scorer was then corrected until it agreed.

## Bugs found in the first `score.py` and fixed

1. **Proximity-only matching.** Rule (a) returned a match for any comment anchored
   within the line window *regardless of keywords*. This falsely credited `W0-RES-LEAK`
   (line 40) to the path-traversal comment (line 41) and inflated recall. Fix: a
   keyword (`detect_any`) hit is now always required; anchoring or file-name mention is
   necessary but not sufficient.
2. **`kind` not fully handled.** `kind: invalid` and `kind: bonus` fell through to the
   defect branch and were scored as defects. Fix: only `defect`/`canary` count toward
   recall, only `decoy` toward precision; `bonus`/`invalid` are recorded `not-scored`.
3. **Generic keywords cross-matched.** `W0-DECOY-EXCEPT` (line 78) was falsely marked a
   false-positive because its needle `catch`/`except` matched the real bare-except
   comment 16 lines away via the file-name rule. Fix: decoys match only when a comment
   is anchored near the decoy's own line; and two over-broad needle lists were tightened
   (`PERF-QUAD` dropped `set`/`dictionary`).

## Reconciliation

| | Recall | Precision | FP |
|---|---|---|---|
| score.py (before fix) | 0.81 | 0.93 | 1 (spurious) |
| **hand-validated** | **8/13 = 0.615** | **1.0** | **0** |
| score.py (after fix) | 8/13 = 0.615 | 1.0 | 0 |

Automated == hand-validated after the fix. `score.py` is trusted for subsequent waves
at `--line-window 5`, but **each wave's comments are still spot-checked by hand**, since
the matcher depends on the quality of `detect_any` lists.
