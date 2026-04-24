# SDD Framework Skill — Design State

Status: v1 DESIGN IN PROGRESS — started 2026-04-24.

## Locked decisions (user-confirmed)

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Scope: baseia-specific skill, not BMAD-wide | Couples to ULTRAPLAN artifacts; generic version later if it proves reusable |
| 2 | Relation to Phase 4: complements, does not replace | Phase 4 produces `SDD.md` + `hash_units/`; skill is the EXECUTION layer over those |
| 3 | Orchestration: real Task-tool subagents | Auditable, higher cost accepted for traceable handoffs |
| 4 | Research basis: SDD state-of-the-art + multi-agent orchestration | Both done 2026-04-24; web blocked, output based on training |

## Research-derived choices (2026-04-24)

| Choice | Source | Why |
|--------|--------|-----|
| Proposer–Verifier pattern (Tester runs real checks; Critic ranks passing candidates) | SWE-bench winners (Agentless, SWE-agent, Factory Droids) | Terminates on objective signal, not agent consensus |
| Max N=3 iterations per unit | Anthropic multi-agent post + GAN/Self-Refine literature | Prevents infinite approve-reject; forces escalation |
| JSON control fields + free-text `notes` | Multi-agent research consensus | Pure-JSON degrades review quality; pure-NL loses machine parse |
| Independent subagent context windows | Anthropic multi-agent system design | Prevents cross-contamination; orchestrator re-synthesizes |
| Per-section SHA256 in frontmatter (initial hashing strategy) | Spec-kit / Kiro survey | Simplest; swap to test-based ground truth later if SDD.md ships executable tests |
| Critic MUST cite a concrete testable defect to REJECT | Mitigation for "reward hacking on approval" failure mode | Without this Critic drifts to rubber-stamp |

## Pending before skill can ship (priority order)

1. **(BLOCKER)** Phase 1 interview not closed. Skill cannot land in `main` until Phase 1 locks. Branch decision still open — see "Gates" below.
2. Read SDD.md / AI_EXECUTION_MAP.md / ULTRAPLAN Phase 4+5 to ground skill in actual artifact schemas — IN PROGRESS (Explore agent 2026-04-24).
3. Resolve `hash_units/` directory anomaly — commit `a1a3e5a` claims scaffolding created but dir does not exist on disk. Either commit was partial or dir is git-ignored. Must verify before skill depends on it.
4. Draft SKILL.md v1 with:
   - Frontmatter per `bmad-rbtv-skill-spec.md` (6 description rules)
   - SPEC audit block (purpose, target user, I/O, deps, trigger matrix, criterio de pronto)
   - Body with Proposer-Verifier protocol, JSON handoff schema, N=3 cap, Critic defect-citation requirement
5. Run 6-step test matrix from `bmad-rbtv-skill-spec.md`. Cannot skip — required for commit.
6. Decide hashing granularity FINAL: per-section vs per-acceptance-criterion vs commit-hash-of-spec-file. V1 = per-section; revisit after first real execution.
7. Define Tester subagent ground-truth source. Options: (a) executable tests in SDD.md (requires Phase 4 to produce them), (b) acceptance-criteria checklist from SDD unit (human-auditable but not machine-executable), (c) hybrid. V1 = (b) with upgrade path to (a).
8. Define how skill appends to AI_EXECUTION_MAP.md — schema must match existing file's format (unknown until task 2 completes).

## Gates

| Gate | Status | Unblocks |
|------|--------|----------|
| Phase 1 interview closed | OPEN (on branch `claude/phase1-interview`) | Merge skill to `main` |
| Phase 2 flowchart locked | OPEN | Phase 4 start |
| Phase 4 `hash_units/` populated | OPEN (dir missing) | First real skill invocation |

## Branch decision still pending (chat)

Option A: stop all skill work, complete Phase 1 interview first, resume skill afterward.
Option B: sibling branch `claude/skill-sdd-framework` off `main`, v1 draft lives there, merge only after Phase 1 locks.

Recommendation: B — parallelism preserves momentum; merge gate still respected.

## Risk register

| Risk | Mitigation |
|------|-----------|
| Skill drifts from Phase 4 artifact schema while Phase 4 is still being shaped | Keep skill in v1 state, no production use until SDD.md has one real hash_unit and skill executes it end-to-end as validation |
| Cost blowout (15× token multiplier per Anthropic) | Gate skill behind "complexity > threshold" — not every edit. Add explicit "when NOT to use" section |
| Two competing SDD sources of truth (ULTRAPLAN Phase 4 doc + skill body) | Skill body references ULTRAPLAN Phase 4 for lifecycle semantics; never restates. Follows `atomic-files.md` |
| Critic rubber-stamping | Enforce "cite testable defect" gate; audit via AI_EXECUTION_MAP.md REJECT entries having defect[] populated |

## Anomalies to investigate

- `hash_units/` directory missing despite commit `a1a3e5a` titled "phase2+4+5 scaffolding: SDD, AI_EXECUTION_MAP, DOC_RECONCILIATION, hash_units". Commit message likely referred to `_tools/hash_units.py` (script), not a dir. Verify with `git log --all -- _tools/hash_units.py` and `git log --all -- hash_units/`.

## Post-Explore revisions (2026-04-24, after reading SDD/AI_EXECUTION_MAP/ULTRAPLAN Phase 4-5)

### Grounded hashing strategy — REPLACES "per-section SHA256"

SDD.md already defines: `sha256(phase_id + "|" + customer_action + "|" + io_signature + "|" + "|".join(sorted(decision_buttons)))`.
This hashes the **behavioral contract** (not spec text). Two units with identical IO behavior hash the same; cosmetic edits don't trigger drift. Superior to my initial proposal — use as-is. Tester ground truth = `validation_pattern` field (mandatory per unit).

### Skill purpose narrowed (and parameterized)

V1 is an **orchestration primitive** with `task_type` parameter:
- `classify` (Phase 5 — default) → appends row to AI_EXECUTION_MAP.md
- `implement` (Phase 6+ — schema defined, execution stub only in v1)
- Extensible via future `task_type` values

Rationale: user prompt was written as executor; project reality is Phase 5 classifier. Parameterization preserves both without forcing phase-jump.

### Resolved pending items

| Was | Status | Resolution |
|-----|--------|-----------|
| #7 Tester ground-truth source | RESOLVED | `unit.validation_pattern` — mandatory per SDD.md contract |
| Hashing granularity | RESOLVED | Use existing SDD.md formula (behavioral hash). Do not add per-section hashing |
| Skill appends where? | RESOLVED | AI_EXECUTION_MAP.md for classify; `_tools/sdd-runs/<ts>-<hash>.json` for full trace (both task_types) |

### Newly discovered pending items

| # | Item |
|---|------|
| 9 | `_tools/hash_units.py` must expose `--verify <unit_hash>` CLI that the skill invokes. Verify script has this; if not, either extend script or skill parses SDD.md directly as fallback |
| 10 | `model_pattern` column in AI_EXECUTION_MAP.md — vocabulary not in Explore output; need to enumerate before skill can fill this field on classify |
| 11 | Decide: does classify skill INVENT classification or READ user's upstream decision? V1 assumption: Builder PROPOSES classification, Critic REVIEWS, Tester validates against validation_pattern presence + quality. User makes FINAL call via chat before append |

### Meta-prompt v2 (user asked for improved prompt at end of original)

Will be written to `.claude/skills/baseia-sdd-framework/META_PROMPT_V2.md` alongside SKILL.md. Not a skill itself — reference artifact only.
