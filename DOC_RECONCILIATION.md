# Doc Reconciliation — Phase 3

**Status:** PARKED — requires user-in-loop per-file decisions. Autonomous run did NOT execute cross-repo clone ou classification.

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

### 5. Fill this file

Substituir esta seção "Process" por uma tabela executada:

| File (legacy path) | Action | Destination (if move/merge) | Reason |
|--------------------|--------|----------------------------|--------|

Com linha por arquivo processado.

### 6. Cleanup

Rodar `rm -rf /tmp/baseia-planning-legacy` ao terminar (é scratch path).

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
