# FINDINGS

Append-only, plain-prose observations, one section per wave. Observations only —
interpretation is left to the report author. Every claim cites `pr#` and, where
possible, a `comment-id`. Where a number rests on a single observation, that is
stated explicitly.

> **Standing caveat (transparency mode).** The labs openly disclose in
> `SECURITY.md` that they are testbeds carrying intentional defects. All findings
> below therefore describe the tool reviewing a repo it can tell is a testbed.
> This is not a covert measurement and must not be compared against one.

---

## W0 — baseline / fingerprint

Environment: `KimVianney/claimline` (public), **no `.coderabbit.yaml`** present, so
this captures true defaults. Bot identity across all events: **`coderabbitai[bot]`**.
Run configuration reported by the bot itself: **Configuration used: defaults ·
Review profile: CHILL · Plan: Advanced**. (The "Advanced" plan means this is a paid
tier, not free — relevant when interpreting W11.)

### PR #1 — trivial 1-line docs change (`chore/readme-dev-note`)

- **Fires unprompted: yes.** PR opened ~18:53:5x UTC; bot posted an in-progress
  placeholder at **18:53:50Z** (within seconds) and the finished review at
  **18:54:41Z** — end-to-end ~**50s** for a one-line change.
- **Mechanism:** it posts a single **issue comment** and *edits it in place* from
  "review in progress" to the final summary. The formal PR **`reviews` API stayed
  empty (0)**, and there were **0 inline review comments**. So detection scoring must
  read issue-comments + inline review-comments, not the `reviews` endpoint (the
  collector does this).
- **Result on a trivial change:** *"No actionable comments were generated in the
  recent review. 🎉"* — i.e. it does **not** manufacture nits on a clean 1-liner.
- **Anatomy of the in-progress comment:** HTML-comment markers
  (`summarize by coderabbit.ai`), a `> [!NOTE]` block, collapsible **Run
  configuration** (with a **Run ID**, e.g. `c673af3a-…`), a **Commits** range
  (`base..head` SHAs), a **Files selected for processing** list, and a rotating
  ASCII-art cow banner.
- **Anatomy of the finished summary** (structural fingerprint): headings
  **Walkthrough** and **Changes**; a **Review Change Stack** image/link to
  `app.coderabbit.ai/change-stack/...`; a **Finishing Touches** section; emoji
  vocabulary `⚙ ⚪ ✅ ✨ 🎉 📒 📝 📥 🚥 🧪`; **no** `suggestion` blocks, **no**
  "Prompt for AI Agents" block, **no** tool-attribution lines (all expected, since
  there were no actionable findings). Length ~4.8 KB.
- Evidence: `evidence/claimline/pr-1/*.json` (append-only snapshots).

### PR #2 — ~200 LOC, 12 planted defects + 2 decoys (`feat/claim-batch-import`)

Opened ~19:08:44Z; review in progress at snapshot time. Manifest: 14 entries with
`pr: 2` in `probes/manifest.yaml`. Local linters (our own CI) catch **4 of the 12**
defects deterministically before CodeRabbit even runs — ruff `S324` (md5),
`S608` (SQL f-string), `S110` (except/pass), `S105` (would-be hardcoded secret) —
useful separation of static-analysis vs. LLM findings. Results recorded after the
review completes.

_Note on the secret probe:_ the environment's own commit-time secret guard blocked
committing a literal `AWS_SECRET_ACCESS_KEY`. The planted `W0-CANARY-SECRET` therefore
keeps only the hardcoded **AWS access key id** (`AKIAIOSFODNN7EXAMPLE`, a documented
non-functional canary) with the secret read from env — still a valid hardcoded-credential
finding for the reviewer.
