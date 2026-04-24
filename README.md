# BaseIA

Clean workspace for BaseIA product design. Created 2026-04-24 to replace the fragmented state of the legacy planning repo.

BaseIA is an AI product targeting Brazilian SMB owners ("empreendedor dono de PME") who want to automate recurring financial back-office work — conciliação, prestação de contas, fechamento, controle de contas a pagar/receber — instead of hiring or retaining operational staff.

## Layout

| Path | Purpose |
|---|---|
| [`ULTRAPLAN.md`](ULTRAPLAN.md) | The handoff prompt. **This is what you paste into a fresh Claude session in Cursor** to resume the multi-phase design workflow. |
| [`CLAUDE.md`](CLAUDE.md) | Default orientation for any Claude instance opening this repo. |
| [`_shape/`](./_shape) | Append-only decision log from the reset session. Source of truth for what was already decided. |
| [`research/`](./research) | Research artifacts that back design decisions (with citations). |
| [`.claude/rules/`](./.claude/rules) | Behavioral rules for any Claude instance working here. |
| [`_tools/`](./_tools) | Helper scripts (e.g., `hash_units.py` will land here in Phase 4). |

## Getting started (human, not agent)

1. Open this repo in Cursor.
2. Start a fresh Claude session (Sonnet or Opus).
3. Paste the full contents of [`ULTRAPLAN.md`](ULTRAPLAN.md) as the first message.
4. Follow the agent's lead. It will ask you one question at a time.

## Legacy repos

These exist as historical context. **Do not commit to them.** Phase 3 of the ultraplan will reference them read-only for doc reconciliation.

| Repo | Purpose | GitHub |
|------|---------|--------|
| `baseia-planning` | Fragmented prior planning + docs | [romeuhr/baseia-planning](https://github.com/romeuhr/baseia-planning) |
| `baseia-api` | Production FastAPI (out of scope for design work) | [romeuhr/baseia-api](https://github.com/romeuhr/baseia-api) |
