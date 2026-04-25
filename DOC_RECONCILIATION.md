# Doc Reconciliation — Phase 3

**Status:** EXECUTED 2026-04-25. Strategy B chosen (full process: move + merge + keep). 4 files moved, 8 files extracted into curated insights, ~150 files explicitly deprecated bulk, ~10 kept as read-only reference. Legacy clone (`/tmp/baseia-planning-legacy`) cleaned post-execution.

---

## Why this file exists as a skeleton

Phase 3 (per ULTRAPLAN.md) reconcilia docs de `romeuhr/baseia-planning` (legacy fragmented planning) contra o novo `CUSTOMER_JOURNEY.md`. Decisões per-arquivo (keep / merge / deprecate / move-to-new-repo) exigem human judgment — contexto histórico, intenção original, relevância pro novo design — que autonomous não tem.

O autonomous run criou este skeleton pra que quando Romeu retomar, o path de execução esteja documentado e não precise redescobrir o processo.

---

## Process (quando Romeu autorizar retomar)

### 1. Clone legacy read-only

```
git clone --depth 1 https://github.com/romeuhr/baseia-planning.git /tmp/baseia-planning-legacy
```

**NÃO** adicionar remote pushável. **NÃO** `cd` para dentro. Só leitura do path.

### 2. Distill via subagent

Invocar `context-distill` subagent (per rule `.claude/rules/background-agents.md`). Prompt:

> **Conversation Context:** BaseIA customer journey reset. Novo CUSTOMER_JOURNEY.md locked persona v0.2 (solo founder, amplia capacidade sem CLT), Canal B wedge regularizar CNPJ, triggers canônicos a-d.
>
> **Specific Request:** Listar **todo arquivo** em `/tmp/baseia-planning-legacy` que mencione customer journey, flow, scope, product definition, ou persona. Também listar arquivos em `/tmp/baseia-planning-legacy/projetos/baseia-api` com mesmos critérios. Para cada: file_path + one-line summary + conflitos explícitos com novo CUSTOMER_JOURNEY.md (ex: "menciona persona diferente", "propõe canal contador", "conflita com sub-flavor regularizar").
>
> **Referenced Files:** `/tmp/baseia-planning-legacy` (inteiro) + `projects/baseia/CUSTOMER_JOURNEY.md` (contexto de comparação).

Output esperado: lista de arquivos com classificação preliminar do subagent.

### 3. Classify per file (Romeu decide)

Pra cada arquivo retornado pelo subagent, Romeu escolhe:

| Ação | Quando usar |
|------|-------------|
| `keep` | Arquivo permanece em legado, não vem pro novo repo. Relevante mas out-of-scope agora. |
| `merge` | Conteúdo útil é extraído e mergeado em arquivo novo (ex: CUSTOMER_JOURNEY.md ou shape). Arquivo legado deprecia. |
| `deprecate` | Arquivo não é mais relevante. Marca como deprecated no legado. Sem cópia pro novo. |
| `move-to-new-repo` | Arquivo inteiro vem pro `projects/baseia`. Usar `cp` + `git add` (não cross-repo `git mv` — rule `.claude/rules/git-file-ops.md`). |

### 4. Execute moves aprovados

Pra cada `merge` ou `move-to-new-repo`:

```
cp /tmp/baseia-planning-legacy/<path> projects/baseia/<dest>
git -C projects/baseia add <dest>
git -C projects/baseia commit -m "phase3: merge/move <name> from baseia-planning"
```

Commits separados por arquivo pra auditabilidade.

### 5. Fill this file (EXECUTED — see § Execution Record below)

### 6. Cleanup

Rodar `rm -rf /tmp/baseia-planning-legacy` ao terminar (é scratch path).

---

## Execution Record — 2026-04-25

**Source repo:** `https://github.com/romeuhr/baseia-planning.git` (clonado em `/tmp/baseia-planning-legacy`, depth=1).

**Total files processed:** ~370 mds in legacy. ~207 in non-excluded dirs. ~40 genuinely material to journey reset; the rest deprecated bulk via patterns.

**Result counters:**
- **Moved (cp + git add):** 0 files (2 candidates já em new repo: shape `2026-04-24-customer-journey-reset-shape.md` e research `2026-04-24-discovery-channel-hypotheses.md` — verified via diff). Actual moves: 4 files in `legacy-imports/cashflow-conciliador/`.
- **Merged (insights extracted):** 9 files → single curated doc `_shape/2026-04-25-legacy-insights-extracted.md`.
- **Kept (read-only reference, not migrated):** ~10 files documented in table below.
- **Deprecated bulk:** ~150 files (Captura_Processos_AI/ ~85, produto/ v1+v2 ~12, prompts/sprints+fases+blueprint ~20, _memoria CONSOLIDACAO_*+jornada*+quiz* ~15, _plan/baseia-self-hosted-migration ~15, etc).

### Moved files

| Legacy path | New repo destination | Reason |
|-------------|---------------------|--------|
| `projetos/Cashflow_Conciliador/README.md` | `legacy-imports/cashflow-conciliador/README.md` | Feature spec source for Step 4-5 (auto-conciliação product surface) |
| `projetos/Cashflow_Conciliador/GUIA-IMPLEMENTACAO.md` | `legacy-imports/cashflow-conciliador/GUIA-IMPLEMENTACAO.md` | Implementation hints for Phase 5 SDD (subordinate to README) |
| `projetos/Cashflow_Conciliador/DEPLOY_PRODUCAO.md` | `legacy-imports/cashflow-conciliador/DEPLOY_PRODUCAO.md` | Deployment context (Phase 5 infra reference) |
| `projetos/Cashflow_Conciliador/EXECUTAR-AGORA.md` | `legacy-imports/cashflow-conciliador/EXECUTAR-AGORA.md` | Quick-start patterns (Phase 5 reference) |

NÃO migrados de Cashflow_Conciliador/: SQL, docker-compose, scripts/, n8n-workflow/, exemplos/, database/ (Phase 5 vai re-build infra com decisões novas).

### Merged into `_shape/2026-04-25-legacy-insights-extracted.md`

| Legacy path | Insight extracted (1-line) |
|-------------|---------------------------|
| `produto/baseia-v2/00-discovery/jornada-cliente-sonho.md` | Health check trimestral + WhatsApp referral patterns (Phase 2+ retention) |
| `produto/baseia-v2/00-discovery/jornada-v2-simplificada.md` | "Cada tela justifica existência" minimization principle |
| `produto/baseia-v2/SERVICE-BLUEPRINT-AS-IS-vs-SHOULD-BE.md` | Goldilocks framing (grátis vs pago tension) |
| `produto/baseia-v2/00-discovery/review-findings-31mar2026.md` | F1 (feasibility test antes de Phase 1) + F2 (timeline guard-rails) |
| `produto/baseia-v2/00-discovery/validacao-fases-31mar2026.md` | "Construir é barato — founder time é o custo real" |
| `produto/visao/managed-agents-pivot.md` | Managed Agents hypothesis log pra Phase 5 delivery runtime |
| `produto/UX-Copy-Funil-BaseIA.md` | Voice & Tone brand guardrails (consultor sênior, números não adjetivos, BR coloquial-profissional) |
| `validation/decisions.md` | Open questions A1 (Claude→artefato) + B2 (multi-tenant isolation) pra Phase 4 SDD |
| `projetos/Captura_Processos_AI/CRITICA_MKT_ESTRATEGICA.md` | Brand tese central: "PMEs querem menos risco, não IA" |

### Kept (read-only reference, not migrated)

| Legacy path | Why kept |
|-------------|----------|
| `_memoria/BRIEFING_ESTADO_ATUAL.md` | Estado real de produção (FastAPI, R$50/mês recurring) — referência sobre o que existe |
| `_memoria/MEMORIAS_PROJETOS.md` | Historical ledger 27jan-31mar — não migrate, mas preserve for archaeology |
| `produto/baseia-v2/01-brief/product-brief-BaseIA-V2.md` | Pivot intermediário 31 mar — referência histórica |
| `produto/PROTOCOLO-MUDANCAS.md` | Process rules — pode informar `.claude/rules/` se ainda úteis |
| `produto/baseia-v2/00-discovery/raio-x-n8n-31mar2026.md` | n8n audit — Phase 4 SDD pode citar |
| `planning-artifacts/architecture.md` | V2 stack decisions — Phase 4 SDD reference |
| `validation/experiments/A1, A2, B2/*.md` | Hypothesis test results — Phase 4 input |
| `validation/hardening/*.md` | n8n hardening + incident response — Phase 4 reference |
| `projetos/baseia_sdk/README.md` + `GUIA_RAPIDO.md` | Internal Romeu+Claude tooling — Phase 4 SDD reference se tooling continua |
| `_plan/baseia-self-hosted-migration/*.md` | Migration plan (já executada) — Phase 4 historical reference |

Kept files NÃO foram copiados pro repo novo. Romeu pode acessá-los via `git clone` legacy quando necessário.

### Deprecated bulk

Patterns deprecated (no per-file enumeration — todos seguem mesmos critérios de não-alinhamento com novo persona/wedge/produto):

| Pattern | Approx count | Reason for deprecation |
|---------|--------------|----------------------|
| `projetos/Captura_Processos_AI/**` | ~85 files | Toda a stack do produto v1 vídeo (CRITICA_*, ANALISE_*, ARQUITETURA_*, SALES_*, UX_*, REESCRITA_*, PRICING_*, IMPLEMENTATION_*, melhorias/, docs/, deploy/, workflows/, backups/) — produto deprecated |
| `produto/VISAO_PRODUTO.md`, `produto/MODELO_NEGOCIO.md`, `produto/PLANO-v2-BaseIA-Assinatura.md`, `produto/PRD-BaseIA-Jornada-Cliente-PME.md`, `produto/JORNADA-CLIENTE-v2.md`, `produto/MVP_REQUISITOS.md`, `produto/INVENTARIO-v1.md`, `produto/BASEIA_PRODUCT_DECISION_ENGINE.md`, `produto/CRITIQUE-Gap-Analysis-BaseIA.md`, `produto/CRITICA_UX_UI_FUNIL_MAR2026.md`, `produto/MARKETING_EMAIL.md`, `produto/Estrategia_Video_to_Automation_BaseIA.md`, `produto/ROADMAP_BASEIA_V2.md`, `produto/ROADMAP_PRODUCAO.md`, `produto/DUAS_VISOES_BASEIA.md`, `produto/Nomenclatura_BaseIA_Proposta.md`, `produto/PROMPT_VIDEO_LP.md`, `produto/PROMPT_WONDERSHARE_*.md`, `produto/VIDEO_LP_ROTEIRO_COMPLETO.md` | ~20 files | Produto v1/v2 (vídeo wedge) PRDs/visions/copy/prompts |
| `prompts/sprints/SPRINT_0..4_*.md` + `prompts/fases/PROMPT_FASE*.md` + `prompts/blueprint_*.md` + `prompts/service_blueprint_*.md` + `prompts/docs_necessarios_system.md` + `prompts/workflow_generator_system.md` + `prompts/jornada/PROMPT_JORNADA_IDEAL.md` | ~20 files | Execution prompts do funil-vídeo deprecated |
| `_memoria/ANALISE_JORNADA_E_BACKLOG_28FEV2026.md`, `ANALISE_QUIZ_JORNADA_09MAR2026.md`, `REVISAO_COMPLETA_09MAR2026.md`, `PLANO_5_FASES_PROXIMOS_PASSOS.md`, `CHECKPOINT_V1_01MAR2026.md`, `CONSOLIDACAO_*` (5 files), `SESSAO_11FEV_RESUMO.md`, `skills/SKILL_CAPTURA_SPRINT.md` | ~12 files | Session ledgers + jornada/quiz analyses do produto deprecated |
| `_memoria/AUDITORIA_*`, `RELATORIO_EXECUTIVO_AUDITORIA.md`, `APRENDIZADOS_PIPELINE_v103_FEV2026.md`, `CONFIGURACAO_N8N_OBRIGATORIA.md`, `DIAGNOSTICO_FILE_NOT_FOUND_v102.md`, `MELHORES_PRATICAS_N8N_ASSEMBLYAI.md`, `SETUP_R2_SOLUTION.md`, `SOLUCAO_FINAL_DOCUMENTADA.md`, `ROADMAP_PRODUCAO_MOD2.md`, `MOD2_LATEST_REPORT_INFO.md` | ~10 files | Tech notes + auditorias do pipeline vídeo (out of scope per dir exclusion mas listadas pra completude) |
| `_plan/baseia-self-hosted-migration/**` | ~15 files | Migration plan (n8n→FastAPI Python). Migration JÁ aconteceu (FastAPI live em prod). Reference if needed via legacy clone, mas não migrate. |

**Preservation method:** legacy repo `romeuhr/baseia-planning` permanece intacto (read-only ref). Ninguém deleta. Romeu pode `git clone` quando necessário pra archaeology.

**Nota intencional:** Quando legacy repo for transferido pra `baseia-ai/baseia-planning` (per pendentes pós-org em CLAUDE.md raiz), considerar criar tag `legacy-pre-2026-04-25-reset` no commit current pra marcar momento do reset.

---

## Out-of-scope confirmed (excluded from analysis)

Per § 2 prompt do subagent + Strategy B confirmação:
- `tecnico/` — n8n troubleshooting, infra técnica
- `infra/` — Cloudflare, Docker, scripts
- `workflows/` — n8n workflow JSON
- `orquestrador/` — pipeline operacional, não customer journey
- `_test-screenshots/`, `status/`, `_Docs_Claude/_screenshots/` — test artifacts
- `.git/` — git internals
- `validation/experiments/`, `validation/hardening/` — kept as read-only ref (não bulk-deprecate; podem informar Phase 4)

---

## Human-in-loop required (não delegate)

**Não delegue isso pra autonomous agent.** Razão: classificação depende de contexto histórico que só o Romeu tem. Ex:

- Um arquivo `old_onboarding_flow.md` pode estar obsoleto (deprecate) OU pode ter texture que merece merge no novo journey. Autonomous não tem como saber.
- Um arquivo de spec de produto pode descrever uma feature abandonada OU uma feature planejada pra futuro. Autonomous não distingue.

Por isso Phase 3 é explicitamente parked no autonomous run.

---

## Resume pointer

Quando Romeu voltar e autorizar esta phase:

1. Criar nova branch `claude/phase3-reconciliation` a partir de `claude/phase1-interview` (se essa ainda estiver ativa) ou de `main` pós-merge.
2. Executar steps 1-6 acima.
3. PR único no fim.
