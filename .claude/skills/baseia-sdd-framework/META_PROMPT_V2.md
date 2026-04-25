# SDD Orchestration — Design Prompt v2

Reusable prompt for designing SDD-adjacent orchestration skills. Rewrites the original SDD++ Framework brief into a tighter, project-anchored form.

## Mission (one line)

Design a production-grade orchestration skill that executes ONE locked unit of a spec through a parallel Builder/Critic/Tester subagent loop, bounded by hash-based drift detection and a mandatory ground-truth field.

## Inputs (caller must supply)

| Field | Required | Example |
|-------|----------|---------|
| `target_project` | yes | `projects/baseia/` |
| `spec_file` | yes | `SDD.md` (file defining the unit schema) |
| `unit_hash_fn` | yes | `sha256(phase_id\|customer_action\|io_signature\|sorted(decision_buttons))` |
| `ground_truth_field` | yes | `validation_pattern` — the per-unit field Tester validates against |
| `execution_log_target` | yes | `_tools/sdd-runs/` (where trace JSON lands) |
| `classification_target` | conditional (if task_type=classify) | `AI_EXECUTION_MAP.md` |
| `task_types` | yes | `[classify, implement]` (extensible) |
| `max_iterations` | no, default 3 | integer ≥ 1 |
| `escalation_source` | yes | field name in the unit that routes on overflow (e.g., `escalation_rule`) |

## Mandatory deliverables

1. `SKILL.md` compliant with the target project's skill-spec rule (frontmatter + SPEC block + body)
2. JSON schemas for Builder, Tester, Critic handoffs — inline in SKILL.md
3. Arbitration table covering all Tester × Critic outcomes
4. Explicit "Quando NÃO usar" section
5. Cost disclosure ("~15× tokens vs single-agent")
6. Trace JSON schema for execution log
7. Mapping from this skill's output to every task_type's persistence target

## Mandatory behaviors

- **Proposer–Verifier**: Tester validates against `ground_truth_field` using executable check when possible; Critic ranks only proposals that already passed Tester
- **Parallel Builder+Tester dispatch**; Critic serialized after Tester
- **Independent subagent contexts** — no shared scratchpad; orchestrator re-synthesizes
- **JSON control fields + free-text `notes`** — never pure-JSON, never pure-NL
- **Critic REJECT requires `defects[]` with each defect citing a fragment of `ground_truth_field`** — bare rejections coerce to APPROVE with warning log
- **iteration == max_iterations → escalation** via unit's `escalation_source`; never silent fail

## Mandatory constraints

- Cost gate: skill body must state the 15× multiplier and direct invoker to use external complexity threshold
- Scope: skill processes ONE unit per invocation; batching is a wrapper concern
- Drift-first: hash verification BEFORE loop; abort on mismatch
- Idempotency: repeat invocation on same unit_hash with unchanged spec must produce stable outputs (or explicit "non-deterministic, reason: ...")

## Research budget (for designing the skill)

- Web research: max 2 parallel subagents, each under 400 words
- Codebase grounding: max 1 Explore subagent call covering up to 4 files
- No direct Read tool chains of 2+ context files — violates project background-agents rule

## Success criteria

1. Passes all 6 tests in target project's skill-spec rule
2. Executes one real unit end-to-end — trace JSON written, persistence target updated
3. Produces test-matrix line in commit message: `test-matrix: N/6 passou`

## Anti-patterns (reject on review)

| Anti-pattern | Fix |
|--------------|-----|
| Reinvent hashing when project has formula | Use `unit_hash_fn` from inputs |
| Assume test-framework ground truth when project uses NL patterns | Tester executes `ground_truth_field` semantics, not pytest |
| Append classify output to implement target (or vice versa) | Enforce persistence-target mapping per task_type |
| Unbounded loop | Hard cap at `max_iterations`; throw on overflow |
| Restate referenced docs in skill body | Reference by path; follow atomic-files rule |
| Critic approves without defect citation | Coerce to APPROVE with explicit warning; log for audit |
| Skill name doesn't start with project prefix in multi-project repo | Use `<project>-sdd-framework` or similar |

## Meta-improvement (self-applying)

After first real execution:

1. Count coerced-approvals across runs — if > 5% of REJECTs coerced, tighten Critic prompt to require fragment
2. Measure iteration distribution — if > 80% terminate at iteration 0, drop `max_iterations` to 2 (trio wasted)
3. Capture token usage per run into trace — flag runs > 2× the 15× baseline for review

## What this prompt explicitly REMOVES from v1

- Generic "behavioral rules" section (redundant with constraints)
- Undifferentiated "Agent Architecture (MANDATORY)" — now collapsed into mandatory behaviors + schemas
- "FINAL STEP: generate an improved version of this prompt" — circular; v2 IS that improved version. Future improvement is the "Meta-improvement" section above (empirical, not prompt-recursive)
- Loose "Begin" at the end — v2 has explicit inputs and deliverables, so the caller knows what to hand over
