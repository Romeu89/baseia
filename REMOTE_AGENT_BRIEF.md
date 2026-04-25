# Remote Agent Brief — Autonomous Review + Prep Run

> **Paste-into-`/ultraplan` spec.** Self-contained. Preempts every known failure mode of the previous remote run.

---

## You are

A remote autonomous Claude Code session (e.g., `/ultraplan` cloud sandbox) operating on `Romeu89/baseia`, branch `claude/phase1-interview` (PR #1 open). There is NO interactive user — cannot ask questions. Your job is review, research, and preparation. You do NOT lock decisions, do NOT fabricate journey content, do NOT reconcile legacy docs.

## Mission

Add value to existing scaffolding so that when Romeu returns, his next interactive session is **maximally productive** — a 30-min sprint, not hours of rediscovery.

Three concrete outputs. Nothing else:

1. **REMOTE_REVIEW.md** — critical review of existing artifacts (gaps, contradictions, weak validations, misclassifications).
2. **`research/2026-04-25-remote-review-research.md`** — web research on open empirical questions (conversion benchmarks, solo-founder PME friction points, MEI→ME transition triggers in BR).
3. **PHASE1_INTERVIEW_SCRIPT.md** — 10-15 interview questions for Phase 1 steps 3+ so Romeu runs a sprint instead of a 10-turn dialogue.

---

## Sandbox preflight (mandatory, runs before Task A)

Runs FIRST, before the Mandatory pre-flight section below. Purpose: make the sandbox commit-and-push capable in seconds so the time budget goes to deliverables, not environment discovery. Failures here are the #1 cause of past wasted runs.

### 1. Run the bootstrap script

```bash
bash _tools/sandbox_bootstrap.sh
```

The script's final stdout line is the result.

- `BOOTSTRAP OK push_mode=<mode> gh=<mode> user=<email>` → continue.
- `BOOTSTRAP FAIL: <reason>` → HALT. Emit one line to the user: `Sandbox bootstrap failed: <reason>. Re-run the local sandbox-prep prompt before relaunching the remote agent.` Do NOT attempt the rest of the brief.

### 2. Verify identity is scoped to Romeu

The bootstrap script set repo-scoped `user.email` and `user.name`. Confirm:

```bash
git config user.email   # must print romeuhrechdan@gmail.com
git config user.name    # must print Romeu Hungria Rechdan
```

If either is wrong, re-apply manually before any commit:

```bash
git config user.email romeuhrechdan@gmail.com
git config user.name "Romeu Hungria Rechdan"
```

Sandbox snapshots discard `.git/config`, so this MUST be re-checked every run even when a prior run set it.

### 3. Detect `gh` availability and pick the PR path

Read the `gh=<mode>` field from the bootstrap script's `BOOTSTRAP OK` line.

| Mode | Action |
|------|--------|
| `authenticated` | Use `gh pr create` at the end as the brief specifies. |
| `installed-no-auth` | Skip `gh pr create`. Append a `## PR creation pending` section to REMOTE_REVIEW.md containing the literal command for the user to run locally: `gh pr create --base claude/phase1-interview --head claude/phase1-remote-review --title "Remote review + prep for Phase 1 interview (stacked PR)" --body-file _shape/REMOTE_PR_BODY.md`. Write `_shape/REMOTE_PR_BODY.md` with the body content from the Final PR message template. No halt. |
| `absent` | Same fallback as `installed-no-auth`. No halt. |

Missing `gh` is NEVER a halt condition.

### 4. Push cadence (hard)

Push after EVERY deliverable, not at the end of the run. This supersedes any commit-batching language elsewhere in this brief.

| State | Verdict |
|-------|---------|
| 0 unpushed commits | Normal. |
| 1 unpushed commit | Maximum tolerated state. |
| 2 unpushed commits | Misbehavior. Push immediately, even mid-task, before any further edit. |

A deliverable is any write to: REMOTE_REVIEW.md, the research file, PHASE1_INTERVIEW_SCRIPT.md, or `_shape/REMOTE_PR_BODY.md`. Each write → commit → push. If `push_mode=local-only`, commit anyway and continue — work survives on disk for manual recovery.

### 5. Hard time cap

| Wall-clock from bootstrap completion | Behavior |
|---------------------------------------|----------|
| 0–75 min | Normal work. |
| T+75 min | STOP starting new tasks. Commit and push whatever is in flight. Append a `## Time-cap reached` section to REMOTE_REVIEW.md listing what is done vs. what is parked, per task (A / B / C). |
| T+90 min | Hard stop. Final commit + push. Open the PR with whatever exists. Partial > nothing. |

Track elapsed time from the moment the bootstrap script printed `BOOTSTRAP OK`, not from sandbox boot.

---

## Mandatory pre-flight (before ANY other work)

Execute in order. Halt on first failure with reason logged to REMOTE_REVIEW.md.

### 1. Git identity (scoped, never global)

```bash
git config user.email romeuhrechdan@gmail.com
git config user.name "Romeu Hungria Rechdan"
```

### 2. Auth check

```bash
gh auth status
```

If fails: halt, write reason, no commits.

### 3. Python version check

```bash
python3 --version
```

Requires 3.11+. If older: halt, write reason, do the review parts that don't need the script.

### 4. Branch setup

```bash
git fetch origin
git checkout claude/phase1-interview
git pull
git checkout -b claude/phase1-remote-review
```

Your work lands on `claude/phase1-remote-review`, branched from `claude/phase1-interview`. Final PR is against `claude/phase1-interview` (stacked PR), NOT against `main`.

### 5. Sanity check existing artifacts

```bash
python3 _tools/hash_units.py --self-test
python3 _tools/hash_units.py
```

Both should exit 0. If not: that's a review finding — log in REMOTE_REVIEW.md, continue with other tasks.

---

## Commit + push protocol (every turn with content)

**Every commit command MUST include `-c commit.gpgsign=false`**, preempting the remote sandbox signing 400s that killed the previous run:

```bash
git -c commit.gpgsign=false commit -m "<message>"
git push
git ls-remote origin claude/phase1-remote-review  # verify SHA matches local HEAD
```

If push fails:
- Retry once after 30 seconds.
- If still fails: halt, write reason to REMOTE_REVIEW.md, do NOT continue accumulating local-only commits.

Commit cadence: per content-producing turn. Do NOT batch multiple turns into one commit — durability requires small frequent commits.

---

## Source of truth reading order

Read in this order. Stop as soon as you have context for the specific task you're doing.

1. [`_shape/AUTONOMOUS_RUN_REPORT.md`](_shape/AUTONOMOUS_RUN_REPORT.md) — **READ FIRST.** Resume Contract at top. All locked state + parked items.
2. [`_shape/2026-04-24-customer-journey-reset-shape.md`](_shape/2026-04-24-customer-journey-reset-shape.md) — append-only decision log. Historical why behind each lock.
3. [`CUSTOMER_JOURNEY.md`](CUSTOMER_JOURNEY.md) — Phase 2 table partial (steps 1-2 locked, 3+ TBD).
4. [`SDD.md`](SDD.md) — units 1-2 locked with validation_pattern.
5. [`AI_EXECUTION_MAP.md`](AI_EXECUTION_MAP.md) — classifications for units 1-2.
6. [`research/2026-04-24-discovery-channel-hypotheses.md`](research/2026-04-24-discovery-channel-hypotheses.md) — original research that seeded the locked Canal B decision.
7. `ULTRAPLAN.md` — **historical**. Original interactive brief. Treat as out-of-date context, not instructions.

---

## Scope — what to DO

### Task A — Review existing artifacts

For each of CUSTOMER_JOURNEY.md, SDD.md, AI_EXECUTION_MAP.md, `_tools/hash_units.py`:

- **Logical gaps:** missing edge cases, unstated assumptions, invariants that should be enforced but aren't.
- **Contradictions:** where does the artifact conflict with the shape entries or the research file?
- **Weak validations:** validation_patterns that are untestable, unrealistic, or vacuous. A validation_pattern that nobody would actually run is no validation.
- **Classification errors:** in AI_EXECUTION_MAP, is unit 1 really human_in_loop? Is unit 2 really ai_executable_at_scale? Challenge with counter-arguments.

Output: **REMOTE_REVIEW.md** with one section per artifact. Each finding formatted as:

```
### Finding N — <short title>
**Artifact:** <file:section>
**Type:** gap | contradiction | weakness | misclassification
**Detail:** <what's wrong>
**Evidence:** <reference to shape, research, or code>
**Proposed fix:** <what Romeu would change on return>
**Severity:** blocking | important | minor
```

### Task B — Web research

Use web-research subagent (`Task` tool with `subagent_type="web-research"` if available; otherwise `WebSearch`/`WebFetch`). Research these specific empirical questions:

1. **Landing page conversion benchmark for "regularizar CNPJ" or similar BR fintech wedges.** Specific number for the `validation_pattern` threshold X in SDD unit 2.
2. **Solo-founder PME friction points at MEI→ME transition.** What triggers the migration decision empirically in BR?
3. **Cultural sensitivity around "CLT-free" framing in BR SaaS.** Does "não contratar CLT" resonate or sound cold?
4. **Comparable wedge funnels in BR (Contabilizei playbook details).** Specific tactics used, not just "they scaled to 100k".

Output: **`research/2026-04-25-remote-review-research.md`**. Max 600 words. Format per finding:

```
## Finding N — <question>
**Source:** <URL + domain credibility>
**Data point:** <specific number or claim>
**Confidence:** high | medium | low
**Implication for SDD:** <which unit's validation_pattern this informs>
```

### Task C — Phase 1 interview script

Draft 10-15 questions Romeu answers in a 30-min sprint to unlock Phase 1 steps 3+.

Questions must:
- Be about the solo founder's actual experience, not hypothetical frameworks.
- Have multiple-choice scaffolds where possible (faster than free-text).
- Include "why this matters" context so Romeu can answer without re-reading ULTRAPLAN.
- Probe each candidate step 3+ (primeiro contato, onboarding, primeira win, retention, expansion).

Output: **PHASE1_INTERVIEW_SCRIPT.md**. Format per question:

```
### Q<N> — <topic>
**Purpose:** <what this unlocks in the journey>
**Context:** <1-2 sentences why this matters>
**Question:** <direct question>
**Answer scaffold:** <multiple choice OR free-text with example>
**Follow-up probes:** <if answer is X, ask Y>
```

---

## Halt conditions (explicit)

Halt immediately and log to REMOTE_REVIEW.md when any of:

1. Pre-flight step fails (git config, gh auth, python, branch setup).
2. `python3 _tools/hash_units.py --self-test` fails.
3. Push fails twice with auth error.
4. Any task requires a decision only Romeu can make. Convert to a REMOTE_REVIEW.md finding instead of halting the whole run.
5. Subagent invocation fails or returns empty three consecutive times.

Halt ≠ crash. Halt = "stop THIS task, commit progress, continue OTHER tasks if independent, log reason." The goal is always: leave ground covered for Romeu.

---

## NEVER (hard constraints)

- **NEVER** edit `_shape/2026-04-24-customer-journey-reset-shape.md` (append-only, user-controlled).
- **NEVER** edit CUSTOMER_JOURNEY.md steps 1-2 rows OR persona block (locked).
- **NEVER** edit SDD.md units phase_id="1" or "2" (locked, hash-stable).
- **NEVER** edit AI_EXECUTION_MAP.md rows for units 1-2.
- **NEVER** edit `_shape/AUTONOMOUS_RUN_REPORT.md` — that's the resume contract, user-controlled.
- **NEVER** edit `ULTRAPLAN.md`.
- **NEVER** clone `romeuhr/baseia-planning` (Phase 3 PARKED — user judgment required).
- **NEVER** lock a new decision or claim a new step is "locked" in any artifact. Propose, don't lock.
- **NEVER** merge PR #1 or any other PR.
- **NEVER** force-push.
- **NEVER** bypass hooks or validation EXCEPT the signing bypass specified in the commit protocol.
- **NEVER** modify global git config.
- **NEVER** edit rules in `.claude/rules/`.

Violation of any NEVER = halt + log.

---

## Deliverable checklist (verify before final commit)

- [ ] Pre-flight green: git identity scoped, gh auth ok, python 3.11+, branch checked out.
- [ ] `python3 _tools/hash_units.py --self-test` still exits 0.
- [ ] `python3 _tools/hash_units.py` still exits 0 (no drift introduced).
- [ ] `REMOTE_REVIEW.md` created with ≥5 findings across the 4 artifacts reviewed.
- [ ] `research/2026-04-25-remote-review-research.md` (or appropriate date) created with ≥4 findings.
- [ ] `PHASE1_INTERVIEW_SCRIPT.md` created with 10-15 questions covering steps 3+.
- [ ] All commits authored as `romeuhrechdan@gmail.com`.
- [ ] Every commit pushed to `origin/claude/phase1-remote-review` (verified via ls-remote).
- [ ] PR opened: base=`claude/phase1-interview`, head=`claude/phase1-remote-review`, NOT merged.
- [ ] PR body links REMOTE_REVIEW.md and enumerates the 3 outputs.
- [ ] No modifications to any file in the NEVER list.

If any item is unchecked: the run is incomplete. Do NOT claim success.

---

## Final PR message template

```
Title: Remote review + prep for Phase 1 interview (stacked PR)

Base: claude/phase1-interview
Head: claude/phase1-remote-review

## Summary
Autonomous review run. Outputs:
- REMOTE_REVIEW.md — critical review of scaffolding artifacts
- research/2026-04-25-remote-review-research.md — web research on open empirical questions
- PHASE1_INTERVIEW_SCRIPT.md — 10-15 questions for Romeu's Phase 1 sprint

## Scope discipline
- Nothing in NEVER list was modified.
- No decisions locked. No fabrication. No cross-repo operations.
- Intended merge order: review PR #1 first, then this stacked PR, then Romeu runs Phase 1 sprint.

## Verification
- python3 _tools/hash_units.py --self-test: PASS
- python3 _tools/hash_units.py: exit 0, no drift
- All commits authored as romeuhrechdan@gmail.com
- Branch pushed, SHA verified

🤖 Remote /ultraplan review run
```

---

## If you are stuck

If you cannot proceed for any reason not covered above:

1. Commit whatever partial work you have.
2. Append a section `## HALT — <reason>` to REMOTE_REVIEW.md explaining exactly what blocked you.
3. Push.
4. Open the PR anyway — partial progress > lost work.

Never sit idle. Never fabricate to fill space. Never retry a failing operation more than 3 times.
