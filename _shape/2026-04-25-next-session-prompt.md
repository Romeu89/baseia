# Prompt — Next Session (paste no Claude local)

Cole **tudo abaixo da linha `===== START =====`** como primeira mensagem da nova sessão Claude (Cursor ou terminal). Repo: `Romeu89/baseia` checked out localmente.

===== START =====

# Você é

Claude session local da Romeu (Romeu89/baseia). Sessão remota anterior parou em `bef788a` (branch `claude/phase1-remote-review`, unsigned, sem push). Tua missão: (A) reconciliar git, (B) destravar 5 findings com Romeu, (C) rodar interview Phase 1 steps 3+ em modo TDD-style, (D) fechar Phases 2-5 do ULTRAPLAN.

## Mandatory primeira leitura (ordem estrita, summarize cada uma em 2 frases antes da próxima)

1. `_shape/2026-04-25-readiness-validation.md` — relatório go/no-go atual. Source of truth pra estado.
2. `_shape/AUTONOMOUS_RUN_REPORT.md` — Resume Contract anterior (estagnado, mas tem invariants + parked items).
3. `CLAUDE.md` + `.claude/rules/` (se ainda não na memória) — non-negotiables.

## Parte A — Reconciliar git e PR (não pular steps)

```bash
git fetch
git checkout claude/phase1-remote-review
git pull
git log -1 --format='%h %ae %s'   # esperado: bef788a noreply@anthropic.com readiness:...
git config user.email              # esperado: romeuhrechdan@gmail.com (scoped)
```

Se `user.email` ≠ romeuhrechdan@gmail.com:

```bash
git config user.email romeuhrechdan@gmail.com
git config user.name "Romeu Hungria Rechdan"
```

Reauthor + sign do commit (sandbox remote não pôde signar):

```bash
git commit --amend --reset-author --no-edit
git log -1 --format='%h %ae %G?'   # esperado: <novo SHA> romeuhrechdan@gmail.com G (good signature)
```

Push + reconciliar PR:

```bash
git remote -v                                          # confirma origin = git@github.com:Romeu89/baseia.git
git push --force-with-lease origin claude/phase1-remote-review
gh pr list --state all                                 # vê PR #1 + qualquer stacked
```

Romeu decide com base em `gh pr list`:
- Se PR #1 ainda aberto contra `main` com base `claude/phase1-interview` outdated → opção (a) rebase + force-push, (b) close + new PR contra main, (c) keep stacked.
- Se PR #1 já merged → cria novo PR `claude/phase1-remote-review` → `main`.

Re-roda tooling pra confirmar:

```bash
python _tools/hash_units.py --self-test    # 22 PASS
python _tools/hash_units.py                # 2 units, no drift
```

**Halt se qualquer falhar.** Reporta antes de prosseguir.

## Parte B — Destravar 5 findings (one-decision-per-turn)

Per `_shape/2026-04-25-readiness-validation.md` seção 4. Aborda nesta ordem:

| Ordem | Finding | Pergunta pra Romeu | Owner deliverable |
|---|---|---|---|
| 1 | #1 (blocking) | X threshold em unit 2: qual número + duração de calibração? `research/2026-04-25-remote-review-research.md` tem candidatos. | Edita `SDD.md` unit 2 + `CUSTOMER_JOURNEY.md` row 2; re-roda hash_units; atualiza SDD com novo hash. |
| 2 | #7 (important) | Hash inclui `validation_pattern`? Sim → estende `_tools/hash_units.py` + schema. Não → aceitar gap explícito. | Schema decision. |
| 3 | #3 (important) | 5ª comm tone pra `trigger=other`? Generic nurture? Manual review queue? | Adiciona row em `CUSTOMER_JOURNEY.md` Comm tone table + escalation_rule em SDD unit 1. |
| 4 | #10 (important) | Visitor com intent "abrir CNPJ" no wedge: redirect off-funnel ou waitlist? | Adiciona `is_existing_cnpj` decision button em `CUSTOMER_JOURNEY.md` row 2. |
| 5 | #2 (important) | Unit 1 schema: collapse em unit 2 ou split com pre-landing measurement? | Restruct units 1-2 em SDD + journey table. |

Pra **cada** decisão: append no `_shape/2026-04-24-customer-journey-reset-shape.md` same-turn (rule context-preservation). Sem deferir.

Findings minor (#4, #5, #6, #8, #9) — Romeu autoriza batch fix em PR separado depois.

## Parte C — Phase 1 interview steps 3+ (TDD-style)

**Filosofia:** mesmo padrão dos mods n8n da Romeu — cada step nasce com check inline. Não vai pra próximo step sem ter respondido as 4 perguntas:

1. **Input:** o que entra nesse step? (schema + source)
2. **Output:** o que sai mensurável? (schema + sink)
3. **System touchpoint:** qual pedaço do produto?
4. **Validation pattern:** como sei que rodou? Escolher de: schema assertion / golden output / human checkpoint / webhook callback (n8n-style) / metric threshold / behavioral self-report.

Sem validation pattern = step não é locked, não vira unit no SDD.

**Roteiro:** `PHASE1_INTERVIEW_SCRIPT.md` tem 15 Qs prontas (Q1-Q15 cobrem steps 3-8). Per Q:

1. Pergunta a Q. Romeu responde (MCQ ou free-text).
2. Restate **journey-so-far** como linear list numerada.
3. **Append no shape same-turn** (decisão + why).
4. Atualiza row no `CUSTOMER_JOURNEY.md` Phase 2 table (8 colunas, validation pattern obrigatório).
5. Roda `python _tools/hash_units.py` — drift expected (row nova). Captura novo hash.
6. Adiciona unit no `SDD.md` com schema completo (incluindo io_signature + validation_pattern + escalation_rule + dependencies).
7. Adiciona row no `AI_EXECUTION_MAP.md` (classification + model_pattern OU human_decision OU missing_infra).
8. Re-roda hash_units — exit 0 esperado.
9. Commit. Mensagem: `phase1: lock step <N> — <action> with <validation_pattern>`.

**Lock criteria:** 2 turns passam sem edit no step → considera locked.

**Critical partner mandate:** se a resposta da Romeu introduz contradição com decisão anterior do shape, flag explicitly antes de aceitar. Não acomodar.

## Parte D — Phase 2 Mermaid

Quando steps 3-8 todos locked:

1. Gera Mermaid flowchart de `CUSTOMER_JOURNEY.md` inteiro (todos os steps + decision branches).
2. Valida sintaxe local: cria scratch `.md` com bloco mermaid, abre no preview do Cursor.
3. Substitui seção `## Mermaid flowchart` (atualmente PARKED) com bloco renderizado.
4. Commit: `phase2: lock Mermaid flowchart for steps 1-N`.

## Parte E — Phase 3 reconciliation

Per `DOC_RECONCILIATION.md` process. **Não autônomo** — per-arquivo Romeu decide.

```bash
git clone --depth 1 https://github.com/romeuhr/baseia-planning.git /tmp/baseia-planning-legacy
```

Invoca `context-distill` subagent (rule background-agents.md) com prompt do `DOC_RECONCILIATION.md` § 2. Romeu classifica per-arquivo em chat. Executa moves aprovados via `cp` + `git add` (não cross-repo `git mv`).

Preenche tabela final em `DOC_RECONCILIATION.md` § 5. Commit: `phase3: reconcile <N> files from baseia-planning`.

## Parte F — Phase 4 + 5 re-lock

1. Re-roda `python _tools/hash_units.py` — exit 0; todas units 1..N hashed sem drift.
2. Confirma `SDD.md` tem todas units com `validation_pattern` ≠ blank.
3. Confirma `AI_EXECUTION_MAP.md` tem todas rows com `classification` válido (e que `ai_executable_at_scale` só aparece quando `missing_infra` está vazio — Finding 4 do REMOTE_REVIEW).
4. Append no shape: entrada `2026-MM-DD — ULTRAPLAN ciclo 1 completo` com pointer pra estado final.
5. Open PR final: `phase4+5: lock SDD + AI execution map for full journey (steps 1-N)`.

## Hard constraints (re-stated)

| Rule | Onde |
|---|---|
| One decision per turn | `.claude/rules/chat-discipline.md` |
| Shape append-only same-turn | `.claude/rules/context-preservation.md` |
| Critical partner, não sycophant | `.claude/rules/reasoning.md` |
| `validation_pattern` MANDATORY per step | `ULTRAPLAN.md` Phase 4 constraint |
| Background agents pra multi-file research | `.claude/rules/background-agents.md` |
| `git mv` / `git rm` pra moves | `.claude/rules/git-file-ops.md` |
| Pre-commit: fetch → check remote → commit → push | `.claude/rules/git-file-ops.md` |
| Não bypass signing sem autorização Romeu | system rule |

## Tua primeira mensagem pra Romeu

Após ler os 3 arquivos mandatory:

> "Resumo dos três arquivos:
> 1. Readiness validation: [2 frases]
> 2. AUTONOMOUS_RUN_REPORT: [2 frases]
> 3. CLAUDE.md + rules: [2 frases]
>
> Pronto pra Parte A (reconciliar git). Confirma `pwd`, `git status`, e me diz se quer que eu rode os commands ou só dite e tu executas?"

Espera. Não toca em nada do plano antes de Romeu confirmar.

===== END =====
