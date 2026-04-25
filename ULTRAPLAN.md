# BaseIA Ultraplan — Phase 1 Close → Phase 5 Execution

> **⚠️ CURRENT STATE (2026-04-24) — READ FIRST:**
>
> This document is the **original interactive brief**. Parts of it are now **historical** — Decisions 1-3 + sub-wedge flavor are locked, Phase 1 steps 1-2 are locked, scaffolding artifacts exist.
>
> **Canonical current state:** [`_shape/AUTONOMOUS_RUN_REPORT.md`](_shape/AUTONOMOUS_RUN_REPORT.md) — Resume Contract at top reconstructs full state in one read.
>
> **If you are a remote autonomous agent** (e.g., `/ultraplan` cloud session): do NOT execute this file. Read [`REMOTE_AGENT_BRIEF.md`](REMOTE_AGENT_BRIEF.md) instead — it has the autonomous-safe scope.
>
> **If you are an interactive local Claude session** helping Romeu continue Phase 1 interview: read the Resume Contract first, then this file for historical context on the Phase 2-5 constraints you'll apply.

> **Original human instruction (preserved):** Open the `Romeu89/baseia` repo in Cursor. Start a fresh Claude session (Sonnet or Opus). Paste the ENTIRE contents of this file as your first message. The agent will take over from there.

---

## You are

A Claude instance (running in Cursor) resuming a BaseIA customer-journey reset from a prior Claude Code session. That session locked the foundation; you execute the rest.

**What the prior session delivered** (already in this repo — read it, don't rebuild it):
- Persona v0.1 captured with two open flags.
- Step 1 of the journey locked as a multi-trigger pattern (4 convergent triggers).
- 4 acquisition-channel hypotheses ranked via web research, with cultural flags.
- Two critical flags raised that change downstream work (persona framing + B2B2C complication).

**What the prior session left open for you to close**:
1. Decision on which channel locks step 2 of the journey.
2. Approval of the persona framing reframe.
3. Empreendedor subtype segmentation.
4. Steps 3+ of the journey interview (not started).
5. Phases 2 → 5 end-to-end.

Your mission: close items 1–3 with the user, finish the Phase 1 interview (item 4), then execute Phases 2–5 delivering locked artifacts.

---

## Repos

You are inside `Romeu89/baseia` — the primary repo you commit to.

Two legacy repos exist for reference only:

| Repo | URL | Role |
|------|-----|------|
| `baseia-planning` | https://github.com/romeuhr/baseia-planning | Fragmented prior planning. Phase 3 reads it for reconciliation. Do not commit. |
| `baseia-api` | https://github.com/romeuhr/baseia-api | Production FastAPI. Out of scope for design work. Do not commit. |

For Phase 3 reconciliation, clone `baseia-planning` read-only to a scratch path like `/tmp/baseia-planning-legacy` and use the `context-distill` subagent to inspect it without loading its files into your main context.

---

## Mandatory first reads (strict order)

**Before any output beyond a greeting**, read these in order. Summarize each back to the user in 2 sentences before moving to the next. This enforces continuity.

1. [`_shape/2026-04-24-customer-journey-reset-shape.md`](./_shape/2026-04-24-customer-journey-reset-shape.md) — append-only decision log. This is your source of truth for Phase 1 state.
2. [`research/2026-04-24-discovery-channel-hypotheses.md`](./research/2026-04-24-discovery-channel-hypotheses.md) — channel research with cultural flags on "substituir funcionário" framing.
3. [`CLAUDE.md`](./CLAUDE.md) and the 8 files under [`.claude/rules/`](./.claude/rules). Use the `context-distill` subagent if you do not want to load all 8 into your main context — ask it specifically for "the hard rules I must not violate while executing the ultraplan".

Do not read anything else until these three are summarized.

---

## Open decisions you must close with the user — in priority order

Ask **one at a time** per the chat-discipline rule. Log each answer to the shape file the same turn it is given.

### Decision 1 — Lock step 2 (channel)

From the shape, five options are on the table:

1. **Contador Indicação** (B2B2C partner program) — the research agent's first-test rec. Precedents: Omie, Conta Azul, Nibo.
2. **Wedge "Abra/Regularize CNPJ grátis"** (lead-magnet funnel) — Contabilizei's playbook.
3. **LinkedIn pt-BR founder content** — Kamino ICP. Precedents thin.
4. **Multi-canal paralelo** (e.g., contador + wedge at once).
5. **Não locar** — run another research round before deciding.

Do not answer for the user. Do not rank. Ask.

### Decision 2 — Persona v0.1 reframe

Research showed the "substituir funcionário" framing is evidence-hostile:
- Contador channel is mechanically hostile (contador loses billable hours if clients automate).
- BR study cited: 72% of BR companies in early AI adoption; replacement fear is explicit barrier.

Persona v0.1 currently reads: *"empreendedor dono de PME que busca substituir ou evitar contratação de funcionário operacional"*.

Proposed reframe: *"amplia capacidade sem contratar próximo CLT"*.

Ask the user to approve, reject, or counter-propose. Log to shape same turn.

### Decision 3 — Empreendedor subtype

"Empreendedor" is still too broad. Three subtypes with materially different journeys:

| Subtype | Decision authority | Typical setup |
|---|---|---|
| Solo founder | Decides + pays from own pocket | 1–2 pessoas, fundador é o operador |
| 2–3 sócios | Shared decision | 3–10 pessoas, um sócio é o operacional |
| CEO de 20+ | Decides, delegates, has controller | 20–50+ pessoas, controller executa |

Ask which is the primary target segment. Secondary segments can be mapped later.

---

## After decisions 1–3 — resume the Phase 1 interview for steps 3+

Same rhythm as the prior session:
- One question per turn.
- After each user answer, restate the journey-so-far as a numbered linear list.
- Lock when two turns pass with no edits.

Write the final locked journey to `CUSTOMER_JOURNEY.md` at repo root — numbered linear steps, no flowchart yet.

---

## Phase 2 — Flowchart Lock (with testing-as-planning)

For each locked step of `CUSTOMER_JOURNEY.md`, produce a row with EXACTLY these columns:

| Step | Customer action | Input | Output | System touchpoint | Communication trigger | Decision/branch buttons | **Validation pattern** |

The last column is **mandatory** — this is the testing-as-planning constraint from the shape. Every step must have a concrete check at design time. Acceptable validation patterns include:

- schema assertion (expected input/output shape)
- golden-output comparison
- human-in-the-loop checkpoint
- webhook callback (n8n-style)
- metric threshold (e.g., "conciliation accuracy > 98%")

**If you cannot define a check for a step, say so and route the question back to the user.** Do not invent a validation pattern.

Outputs:
- Full table appended to `CUSTOMER_JOURNEY.md`.
- Mermaid flowchart rendered in chat.

**Validate the Mermaid syntax** using an MCP Mermaid validator before pasting in chat. If no Mermaid MCP tool is available in your Cursor environment, at minimum verify the syntax by rendering it in a scratch file and pasting the rendered version.

---

## Phase 3 — Doc Reconciliation (minimum viable)

Per the shape, Phase 3 is **enxuta** — only what the new vision needs. Do not do a full audit of the legacy repos.

1. Clone `romeuhr/baseia-planning` read-only to a scratch path. Do not set a pushable remote.
2. Use the `context-distill` subagent to list every file in `baseia-planning/` AND `baseia-api/` that references customer journey, flow, scope, or product definition. Ask the subagent to return only: file path + one-line summary + obvious conflicts with the new `CUSTOMER_JOURNEY.md`.
3. For each file, classify: `keep` / `merge` / `deprecate` / `move-to-new-repo`.
4. Output to `DOC_RECONCILIATION.md` in this repo.
5. Wait for user approval per action. Execute approved moves by **copying** the file into this repo and `git add`-ing it — not with cross-repo `git mv`.

---

## Phase 4 — SDD with hashing + `validation_pattern`

Build `SDD.md` with this schema per unit:

```yaml
- phase_id: <string — Step number from Phase 2>
  customer_action: <from Phase 2 row>
  io_signature: <canonical input + output contract, stable string>
  decision_buttons: <sorted list of decision/branch button names>
  unit_hash: <sha256 hex of: phase_id + "|" + customer_action + "|" + io_signature + "|" + "|".join(sorted(decision_buttons))>
  responsibility: <one sentence>
  interface: <input/output contract detail>
  ai_role: <none | assist | execute | autonomous>
  validation_pattern: <from Phase 2 column — MANDATORY, never blank>
  escalation_rule: <when human takes over>
  dependencies: [<other unit_hashes this depends on>]
```

Write a helper script at `_tools/hash_units.py`:

- Single-file, Python 3.11+, **stdlib-only** (no external deps).
- Parses the Phase 2 table in `CUSTOMER_JOURNEY.md`.
- Recomputes `unit_hash` for each row using the formula above.
- Compares to `SDD.md`. Prints drift rows in the format `phase_id: <old_hash> → <new_hash>  REVIEW NEEDED`.
- Runnable: `python _tools/hash_units.py`. Exit code 0 if no drift, 1 if drift detected.

---

## Phase 5 — AI Execution Map

Only start after the user signs off Phase 4. For each `unit_hash`:

| Field | Content |
|---|---|
| `unit_hash` | (from SDD) |
| `classification` | `ai_executable_at_scale` \| `human_in_loop_required` \| `blocked_by_missing_infra` |
| `model_pattern` | (if AI-executable) e.g., "Haiku with tool use for RAG over invoice PDFs" |
| `human_decision` | (if human-in-loop) what the human decides |
| `missing_infra` | (if blocked) what's needed to unblock |
| `validation_pattern` | re-surfaced from SDD |

Rule: **AI-executable units only qualify if `validation_pattern` is defined in SDD.** If a unit has no validation pattern, it cannot be classified as AI-executable regardless of model capability.

Output to `AI_EXECUTION_MAP.md`. Cross-reference every row to `unit_hash`.

---

## Hard constraints (non-negotiable)

1. **One decision per turn in chat.** Never dump 7+ items at once.
2. **Critical partner, not sycophant.** Flag drift, challenge premises, name trade-offs. Prior agent made at least two claims that later proved wrong — expect to do the same and surface it immediately.
3. **Shape file updates SAME TURN.** Any reasoned decision → append to `_shape/2026-04-24-customer-journey-reset-shape.md` before the turn ends. Never defer to session end.
4. **Commit pattern:** one accumulator branch per phase (e.g., `claude/phase2-flowchart`). Per-turn commits on the branch. **PR at phase locks only** — not per-turn PRs.
5. **`git mv` / `git rm`** for any moves inside a git repo.
6. **`context-distill`** subagent for any multi-file exploration. Never read 2+ files in a single interactive turn.
7. **`web-research`** subagent for any web research. Preserve outputs as standalone notes under `research/`.
8. **Validate Mermaid** before rendering in chat.
9. **Do not skip phases.** If Phase N is blocked, raise it — do not fabricate content for Phase N+1.
10. **Chat vs. file separation.** Detailed output goes to files. Chat is for decisions, summaries, and questions.

---

## Definition of done for this workflow

- `CUSTOMER_JOURNEY.md` — locked, human-approved.
- `DOC_RECONCILIATION.md` — approved, approved moves executed.
- `SDD.md` — unit hashes computed, `validation_pattern` populated for every unit.
- `_tools/hash_units.py` — runnable, detects drift.
- `AI_EXECUTION_MAP.md` — cross-referenced to unit hashes.
- All committed via phase-lock PRs on `Romeu89/baseia`. Main clean, branches deleted.
- `_shape/2026-04-24-customer-journey-reset-shape.md` has the full decision trail appended across every turn of your execution.

---

## Your first message to the user

After reading the three mandatory files, open with something like:

> "Resumo dos três arquivos obrigatórios:
> 1. Shape: [2 frases]
> 2. Research: [2 frases]
> 3. CLAUDE + rules: [2 frases]
>
> Primeira decisão pra destravar a Phase 1: qual das 5 opções de canal loca o step 2?"

Then wait. Do not propose the Phase 2 flowchart or any downstream work until Decisions 1–3 are answered and the Phase 1 interview is locked.
