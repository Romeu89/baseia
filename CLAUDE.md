# BaseIA — Agent Orientation

You are a Claude instance operating inside the `Romeu89/baseia` repo — the clean workspace for BaseIA product design.

## If the user pasted `ULTRAPLAN.md` as their first message

Follow it. It is the canonical brief for the active multi-phase workflow (Phase 1 close → Phase 2 flowchart → Phase 3 doc reconciliation → Phase 4 SDD with hashing → Phase 5 AI execution map).

## If the user is asking for something else

Ask before acting. Do not invent tasks. Read [`ULTRAPLAN.md`](ULTRAPLAN.md) anyway — it gives you the state of the design work, which is likely relevant context.

## Non-negotiables (regardless of task)

Full text in `.claude/rules/`. Short enumeration:

| Rule | Short rule |
|------|-----------|
| [`reasoning.md`](.claude/rules/reasoning.md) | Critical partner, not sycophant. Fix at root cause. |
| [`chat-discipline.md`](.claude/rules/chat-discipline.md) | One decision per turn. Max 5–7 items per batch. Chat for decisions; files for detail. |
| [`context-preservation.md`](.claude/rules/context-preservation.md) | Append decisions to `_shape/…` same turn as made. Never defer. |
| [`atomic-files.md`](.claude/rules/atomic-files.md) | Self-contained files. No content repetition. Lean and objective. |
| [`background-agents.md`](.claude/rules/background-agents.md) | Never read 2+ files in a single interactive turn. Use `context-distill` subagent. Web research → `web-research` subagent. |
| [`git-file-ops.md`](.claude/rules/git-file-ops.md) | `git mv` / `git rm` for any moves inside a git repo. Pre-commit workflow (fetch → check remote → commit → push). |
| [`memory-system.md`](.claude/rules/memory-system.md) | Structured knowledge at `.claude/memory/` (create on demand). |
| [`n8n-patterns.md`](.claude/rules/n8n-patterns.md) | Reference only — applies if Phase 4/5 touches n8n workflows. |

## Source of truth

[`_shape/2026-04-24-customer-journey-reset-shape.md`](./_shape/2026-04-24-customer-journey-reset-shape.md) is the **append-only** decision log from the Phase 1 reset session. Do not rewrite; append. Every reasoned decision lands there the same turn it is made.

## Legacy repos (read-only reference)

| Repo | Role |
|------|------|
| `romeuhr/baseia-planning` | Fragmented prior planning. Phase 3 references it read-only. Do not commit. |
| `romeuhr/baseia-api` | Production FastAPI. Out of scope for design work. |

## Commit pattern

One accumulator branch per phase (`claude/phaseN-<purpose>`). Per-turn commits on the branch. **PR only at phase locks.** Not per-turn PRs.

## Definition of done (for the ultraplan)

See [`ULTRAPLAN.md`](ULTRAPLAN.md) § "Definition of done".
