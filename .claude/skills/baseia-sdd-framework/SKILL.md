---
name: baseia-sdd-framework
description: Orchestrate Builder/Critic/Tester subagents over a locked SDD unit to classify or implement. Use when user says "run SDD on <unit>" or "executar SDD na <hash>".
---

<!--
SPEC (pré-implementação — não lida pelo Claude, é pra auditoria humana):

Propósito: Executar uma unit locked do SDD.md através de ciclo Builder/Critic/Tester com drift detection (via unit_hash) e ground truth (via unit.validation_pattern). Append a AI_EXECUTION_MAP.md para task_type=classify; stub output para task_type=implement em v1.

Usuário-alvo: Romeu, durante Phase 5 (classify) ou Phase 6+ (implement) do ULTRAPLAN.

Inputs esperados:
- unit_hash (obrigatório) — sha256 full hash ou prefix >= 8 chars matching exatamente 1 unit em SDD.md
- task_type (obrigatório) — "classify" | "implement"

Outputs esperados:
- Sempre: _tools/sdd-runs/<ISO-timestamp>-<hash8>.json com trace completo
- task_type=classify: append 1 linha a AI_EXECUTION_MAP.md
- task_type=implement (v1): stub apenas — NÃO aplica diff automaticamente

Dependências:
- SDD.md (leitura de unit)
- AI_EXECUTION_MAP.md (append em classify)
- _tools/hash_units.py (verificação; se CLI não suportar --verify, skill parseia SDD.md como fallback)
- Task tool (subagents Builder/Tester/Critic — general-purpose subagent_type)

Trigger matrix:
- DEVE disparar com:
  - "run SDD on unit a3f2b1c4"
  - "classify unit a3f2b1c4"
  - "executar SDD na unit a3f2b1c4"
  - "run /baseia-sdd-framework a3f2b1c4 classify"
- NÃO DEVE disparar com:
  - "write SDD" (isso é Phase 4, não execução)
  - "edit SDD.md"
  - "review the SDD"
  - "lock a unit"
  - "run tests" (genérico demais)
  - "/baseia-sdd-framework" sem args (skill deve pedir args, não assumir)
- Skills vizinhas: nenhuma ainda — Phase 4 workflow não está skill-ificado. Quando existirem skills para Phase 4 (criar unit, drift-check), re-testar trigger matrix.

Critério de pronto:
1. unit_hash passa verificação de existência em SDD.md E sha256(phase_id|customer_action|io_signature|sorted(decision_buttons)) bate com unit.unit_hash
2. Builder e Tester dispatched em paralelo via Task tool; Critic dispatched sequencialmente após Tester
3. iteration <= 3 sempre; overflow invoca unit.escalation_rule
4. Critic REJECT inválido se defects[] vazio OU se qualquer defect omite validation_fragment; nestes casos coerce para APPROVE + log warning
5. task_type=classify: 1 linha nova em AI_EXECUTION_MAP.md com colunas unit_hash | classification | model_pattern | human_decision | missing_infra | validation_pattern
6. Sempre: trace JSON escrito em _tools/sdd-runs/ com campos unit_hash, task_type, iterations[], final_state, needs_human
-->

# baseia-sdd-framework

Orchestration primitive: executa UMA unit locked do SDD.md em ciclo Builder/Critic/Tester.

## Quando usar

Executar uma unit individual do SDD.md durante Phase 5 (classify) ou Phase 6+ (implement). Uma unit por invocação.

## Quando NÃO usar

- Edição ou criação do SDD.md — isso é Phase 4
- Batch de múltiplas units — use wrapper externo que chama este skill em loop
- Unit já classificada como `blocked_by_missing_infra` — resolver infra primeiro
- Mudança trivial que não justifica custo 15× do trio (research Anthropic 2025-06)
- Invocação sem `unit_hash` e `task_type` — skill DEVE pedir args, nunca assumir

## O que fazer

### 1. Parse args
Ler `unit_hash` (obrigatório, >=8 chars) e `task_type` (obrigatório, `classify | implement`). Qualquer ausente → perguntar ao usuário no chat e PARAR.

### 2. Verify hash
Invocar `python _tools/hash_units.py --verify <unit_hash>`. Se CLI não expor `--verify`: parsear SDD.md diretamente, recomputar sha256(phase_id|customer_action|io_signature|sorted(decision_buttons)), comparar com unit.unit_hash. Drift ou unit inexistente → ABORT, reportar.

### 3. Load unit
Ler a unit inteira de SDD.md. Campos esperados (todos obrigatórios por contrato Phase 4): `phase_id`, `customer_action`, `io_signature`, `decision_buttons`, `unit_hash`, `responsibility`, `interface`, `ai_role`, `validation_pattern`, `escalation_rule`, `dependencies`. Campo ausente → ABORT.

### 4. Pre-flight (task_type=implement apenas)
Ler linha da unit em AI_EXECUTION_MAP.md. Se `classification != "ai_executable_at_scale"`: ABORT; pedir ao usuário rodar `classify` primeiro.

### 5. Loop Builder/Tester/Critic

Inicializar: `iteration=0`, `state="pending"`, `history=[]`.

Enquanto `iteration < 3 AND state == "pending"`:

**5a. Dispatch Builder + Tester em paralelo** (single Task tool block, duas chamadas):

Builder input: unit (full JSON) + task_type + history (se iteration > 0).
Builder output schema:
```json
{
  "proposal": {},
  "reasoning": "string",
  "confidence": 0.0,
  "notes": "string"
}
```

Tester input: unit.validation_pattern + Builder proposal (passar via second round se precisar — em iteration 0 Tester pode executar validation_pattern contra unit schema como pré-check).
Tester output schema:
```json
{
  "verdict": "PASS",
  "evidence": [{"check": "string", "result": "string"}],
  "notes": "string"
}
```

**5b. Dispatch Critic** sequencial (após Tester retornar):

Critic input: Builder.proposal + Tester.verdict + unit (full).
Critic output schema:
```json
{
  "decision": "APPROVE",
  "defects": [{"field": "string", "issue": "string", "validation_fragment": "string"}],
  "confidence": 0.0,
  "notes": "string"
}
```

**5c. Arbitrate**:

| Tester | Critic | Ação |
|--------|--------|------|
| FAIL | (qualquer) | `history.push(Tester.evidence)`; `iteration++`; continuar |
| PASS | APPROVE | `state = "done"` |
| PASS | REJECT com defects[] não vazio E todo defect tem validation_fragment populado | `history.push(Critic.defects)`; `iteration++`; continuar |
| PASS | REJECT sem defects OU defect sem validation_fragment | **COERCE APPROVE** + log warning "Critic rubber-stamp detected"; `state = "done"` |

### 6. Overflow
`iteration == 3 AND state == "pending"` → invocar `unit.escalation_rule`; marcar `needs_human=true` no trace; reportar ao usuário.

### 7. Emit output

**Sempre** — trace em `_tools/sdd-runs/<ISO8601>-<hash[:8]>.json`:
```json
{
  "unit_hash": "...",
  "task_type": "classify",
  "started_at": "ISO8601",
  "finished_at": "ISO8601",
  "iterations": [
    {"n": 0, "builder": {}, "tester": {}, "critic": {}, "arbitration": "..."}
  ],
  "final_state": "done",
  "needs_human": false,
  "coerced_approvals": 0
}
```

**task_type=classify** — append a AI_EXECUTION_MAP.md:
```
| <unit_hash> | <classification> | <model_pattern> | <human_decision> | <missing_infra> | <validation_pattern> |
```
`classification` ∈ `ai_executable_at_scale | human_in_loop_required | blocked_by_missing_infra`.

**task_type=implement (v1 stub)** — NÃO aplicar diff. Builder.proposal fica no trace apenas. Reportar ao usuário que v1 não aplica; upgrade path para v2.

### 8. Chat summary
Uma linha: `<hash[:8]> → <final_state> em <N> iter. Trace: _tools/sdd-runs/<file>`

## Output esperado

| Artefato | Path | Condição |
|----------|------|----------|
| Trace JSON | `_tools/sdd-runs/<ts>-<hash8>.json` | sempre |
| AI_EXECUTION_MAP.md row | raiz do repo | `task_type=classify` |
| Diff stub | trace JSON apenas | `task_type=implement` v1 |

## Orçamento de custo

Trio consome ~15× tokens vs single-agent (Anthropic multi-agent research, 2025-06). NÃO usar para trivialidade. Invocador DEVE gate por complexidade da unit — julgamento externo.

## Reusable Skill Definition

Contrato I/O estável entre versões:
- **Entrada**: `unit_hash` (hash completo ou prefix ≥ 8) + `task_type` ∈ `{classify, implement}`
- **Saída**: trace JSON em `_tools/sdd-runs/` + (condicional) append a AI_EXECUTION_MAP.md
- **Invariantes**: max 3 iterações; Critic REJECT exige defect testável; drift no hash aborta antes do loop

Workflows superiores (batch classifier, retry-on-needs-human, etc.) DEVEM chamar este skill externamente — não estender o corpo.
