# Readiness Validation — ULTRAPLAN Phase 1→5

**Date:** 2026-04-25
**Scope:** Validar se o workflow inteiro (Phase 1→5) da `ULTRAPLAN.md` está apto a retomar.
**Branch verificada:** `claude/phase1-remote-review` @ `0816cac`
**Decision log (append-only):** [`2026-04-24-customer-journey-reset-shape.md`](2026-04-24-customer-journey-reset-shape.md) — entrada `2026-04-25 — Readiness validation snapshot` referencia este arquivo.

---

## 1. Tooling — GREEN

| Check | Result |
|---|---|
| `python3 --version` | `Python 3.11.15` (≥3.11 OK) |
| `python3 _tools/hash_units.py --self-test` | `SELF-TEST OK — all checks passed` (22 PASS, 0 FAIL) |
| `python3 _tools/hash_units.py` | `OK — 2 units hashed, no drift vs SDD.md` |

Tooling pronto. Sem regressão vs run anterior (REMOTE_REVIEW pre-flight reportou os mesmos 22/22 + drift 0).

---

## 2. Git reality vs Resume Contract — RED (3 deltas)

`AUTONOMOUS_RUN_REPORT.md` Resume Contract está estagnado em 2026-04-24. Estado atual:

| Dimensão | Resume Contract claim | Actual (2026-04-25) | Delta |
|---|---|---|---|
| Active branch | `claude/phase1-interview` (remote tracked) | `claude/phase1-remote-review` (sem upstream) | **MISMATCH** — branch divergiu, remote-review stack ativo |
| HEAD SHA | `a1a3e5a` | `0816cac` | **MISMATCH** — 7 commits novos não-logados |
| Remote `origin` | "pushed to origin" | `git remote -v` vazio | **MISMATCH** — sem remote configurado |
| PR | https://github.com/Romeu89/baseia/pull/1 aberto | `gh` não instalado neste sandbox; não verificável | **UNVERIFIABLE** |
| `gh auth` | "PASS (authenticated as romeuhr)" — REMOTE_REVIEW preflight | `gh: command not found` | **MISMATCH** — sandbox atual não tem `gh` |

### Commits posteriores ao último entry do autonomous run log

| SHA | Mensagem |
|---|---|
| `e70a98c` | phase1: log PR URL in run report |
| `9ce50a0` | remote-agent: add REMOTE_AGENT_BRIEF.md + state-pointer header on ULTRAPLAN |
| `756d3ae` | skill: draft baseia-sdd-framework v1 orchestration primitive |
| `ec6a133` | chore: harden sandbox preflight + time cap for remote agent runs |
| `e4e0598` | skill: correct baseia-sdd-framework v1 after artifact grounding + test matrix |
| `9ac6736` | remote-review: add REMOTE_REVIEW.md with 10 findings across 4 artifacts |
| `1e9bcb9` | research: add 4 findings on conversion benchmarks, MEI->ME triggers, CLT framing, Contabilizei playbook |
| `0816cac` | interview: add 15-question Phase 1 sprint script for steps 3+ (HEAD) |

Nenhum desses commits aparece na seção `## Autonomous run log` do Resume Contract.

---

## 3. Artifact integrity — GREEN local; RED cross-doc

### Presence + lock state

| Artifact | Estado | OK? |
|---|---|---|
| `CUSTOMER_JOURNEY.md` | Persona v0.2 LOCKED; steps 1-2 LOCKED na Phase 2 table; steps 3-5+ marcados `TBD`; Mermaid section diz PARKED | OK |
| `SDD.md` | Schema presente; units phase_id `1` e `2` com todos os campos; units 3-4 como TBD placeholders | OK |
| `AI_EXECUTION_MAP.md` | Rows 1-2 com classification + validation_pattern re-surfaced; vocabulary completo | OK |
| `_tools/hash_units.py` | Self-test + drift = 0 (Step 1) | OK |
| `DOC_RECONCILIATION.md` | Skeleton + processo documentado; body explicit PARKED | OK |
| `_shape/2026-04-24-customer-journey-reset-shape.md` | Append-only intacto (verificável via `git log --follow`) | OK |

### Cross-doc inconsistências (re-surfaced, ainda abertas)

| # | Inconsistência | Onde | Source |
|---|---|---|---|
| a | `>40%` vs `>=40%` | `CUSTOMER_JOURNEY.md:52` vs `SDD.md:40` | REMOTE_REVIEW Finding 9 |
| b | `ai_executable_at_scale` com 3 itens em `missing_infra` | `AI_EXECUTION_MAP.md:24` | REMOTE_REVIEW Finding 4 |
| c | Hash não inclui `validation_pattern` | `_tools/hash_units.py:67` + `SDD.md:6` | REMOTE_REVIEW Finding 7 |
| d | Shape `## Phase Status` (linhas 257-268) estagnado em estado pré-autonomous; não diz que Phase 2/4/5 scaffold já saiu | `_shape/2026-04-24-customer-journey-reset-shape.md:257` | Drift visível neste audit; append-only impede rewrite |

---

## 4. REMOTE_REVIEW findings triage

10 findings de `REMOTE_REVIEW.md`, classificados por phase bloqueada e owner de remediação:

| # | Title (truncado) | Severity | Blocks which phase? | Owner |
|---|---|---|---|---|
| 1 | X threshold em unit 2 untestable | **blocking** | Phase 4 (legitimidade SDD) + Phase 5 (`ai_executable_at_scale` invalidado) | Romeu (ou agente com benchmark research validado) |
| 2 | Unit 1 validation circularity | important | Phase 4 (rigor) | Romeu (decisão schema: collapse vs split) |
| 3 | `other` sem routing | important | Phase 1 (segmentação assumida incompleta) | Romeu (define 5ª comm tone) |
| 4 | Unit 2 misclassification | important | Phase 5 (overstates readiness) | Autonomous pode reclassificar com OK do Romeu |
| 5 | Silent row-drop em hash_units.py | minor | — | Autonomous |
| 6 | canonical_buttons fallback frágil | minor | — | Autonomous |
| 7 | validation_pattern não hashed | important | Phase 4 (drift checker subverte propósito) | Romeu (decisão schema) |
| 8 | Sorted hash perde semantics | minor | — | Romeu (extensão schema) |
| 9 | `>40%` vs `>=40%` | minor | — | Autonomous (escolher um) |
| 10 | Sem funnel pra abrir CNPJ | important | Phase 1 (gap de jornada) | Romeu (decisão produto) |

**Resumo:** 1 blocking + 5 important + 4 minor. 5 itens precisam de Romeu; 4 podem ir autônomos com OK; 1 (Finding 4) é híbrido.

---

## 5. Per-phase verdict — go/no-go

| Phase | State atual | Pode resumir? | Bloqueador |
|---|---|---|---|
| **Phase 1 — interview steps 3+** | Steps 1-2 locked; `PHASE1_INTERVIEW_SCRIPT.md` tem 15 Qs prontas | **GO** com Romeu (sprint ~30min) | Findings 3, 10 surgem durante interview mas não bloqueiam o início |
| **Phase 2 — Mermaid render** | PARKED (só faria sentido com jornada completa) | **NO-GO** até Phase 1 fechar | Phase 1 steps 3+ |
| **Phase 3 — doc reconciliation** | PARKED skeleton | **NO-GO** autônomo | Requer (a) rede pra `git clone https://github.com/romeuhr/baseia-planning.git`, (b) `context-distill` subagent, (c) Romeu per-arquivo |
| **Phase 4 — SDD lock** | Units 1-2 lockadas mas Findings 1+7 abertos | **NO-GO** sem decisão Romeu | Finding 1 (X) bloqueia legitimidade; Finding 7 (hash) bloqueia rigor |
| **Phase 5 — AI execution map** | Rows 1-2 escritas mas Finding 4 misclassifica unit 2 | **NO-GO** sem decisão Romeu | Mesmos gates de Phase 4 + Finding 4 |

### Caveat estrutural (não-phase-específico)

A discrepância **branch / remote / PR** (§2) precisa ser reconciliada **antes** de qualquer commit downstream ser publicado, senão o trabalho atual fica encalhado em branch sem upstream e o PR #1 (se existir) referencia um SHA já antigo.

---

## 6. Recommended unblock sequence

Em ordem de dependência (não pular):

1. **Romeu reconcilia branch/remote/PR.** Confirma onde o trabalho atual será publicado: continua em `claude/phase1-remote-review` (stack sobre `claude/phase1-interview`), ou rebase/merge antes de seguir.
2. **Romeu decide os 5 findings que dependem dele:** 1 (X threshold), 2 (unit 1 schema), 3 (`other` routing), 7 (hash schema), 10 (abrir CNPJ).
3. **Autonomous aplica findings minor com OK:** 4 (re-classify se concordado), 5 (warn-on-drop), 6 (fail-loud fallback), 9 (`≥40%` consistente).
4. **Phase 1 sprint** via `PHASE1_INTERVIEW_SCRIPT.md` — 15 Qs com Romeu, lock steps 3+.
5. **Phase 2 Mermaid render** após Phase 1 lockar.
6. **Phase 3 reconciliation** com Romeu (clone legacy + per-arquivo).
7. **Phase 4 + 5 re-lock** com novas units (3+) + ajustes do (2).

Steps 1-2 são gates duros — não-paralelizáveis com 4-7.

---

## 7. Overall verdict

**Tooling:** GO. **Phase 1 interview:** GO (com Romeu). **Phases 2-5:** NO-GO sem ação humana primeiro (reconciliação git + 5 decisões pendentes). 

Não há bloqueio técnico irrecuperável — todos os blockers são decisões humanas ou ajustes determinísticos pequenos. O caminho está claro; falta input do Romeu.
