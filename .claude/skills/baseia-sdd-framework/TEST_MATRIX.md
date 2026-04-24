# baseia-sdd-framework — Test Matrix

Procedimento obrigatório do `bmad-rbtv-skill-spec.md` — 6 passos. Rodar em **sessão nova** do Claude Code em `projects/baseia/`.

Resultado final vai na mensagem de commit do ajuste seguinte: `test-matrix: N/6 passou` (ou lista do que falhou).

---

## Passo 1 — Auto-trigger positivo (DEVE disparar)

Digite literalmente cada frase abaixo em turnos separados. Claude DEVE escolher `baseia-sdd-framework` **sem** você digitar `/`. Não aceite "posso usar o skill X?" — skill deve disparar autônomo.

- [ ] `run SDD on unit a3f2b1c4`
- [ ] `classify unit a3f2b1c4`
- [ ] `executar SDD na unit a3f2b1c4`
- [ ] `run /baseia-sdd-framework a3f2b1c4 classify`

Pass: 4/4 → description está forte.
Fail (< 4/4) → description fraca; revisar trigger phrases + verbo imperativo.

---

## Passo 2 — Auto-trigger negativo (NÃO DEVE disparar)

Mesma sessão, turnos separados. Skill NÃO DEVE disparar em nenhuma.

- [ ] `write SDD`
- [ ] `edit SDD.md`
- [ ] `review the SDD`
- [ ] `lock a unit`
- [ ] `run tests`
- [ ] `/baseia-sdd-framework` (sem args)

Pass: 0/6 disparos indevidos.
Fail (≥ 1 disparo) → description vaga; diferenciar mais do verbo "execute".

---

## Passo 3 — Invocação explícita

Digite `/baseia-sdd-framework`. Deve aparecer no autocomplete. Ao Tab/Enter, skill deve carregar e pedir args (`unit_hash` + `task_type`).

Pass: aparece no autocomplete E pede args ao invés de assumir.
Fail: não aparece → frontmatter YAML quebrado; não pede args → corpo ignora "Parse args" step 1.

---

## Passo 4 — Critério de pronto (smoke test)

Rodar skill com uma das 2 units já existentes no SDD.md como smoke test. Ex: `unit_hash` da phase 1 (prefixo `d6c59fb5`).

```
run SDD on unit d6c59fb5 classify
```

Skill DEVE:
1. Parsear args ✓
2. Rodar `python _tools/hash_units.py` (drift check global)
3. Parsear SDD.md e achar a unit phase 1
4. **DETECTAR IDEMPOTÊNCIA** — phase 1 já está em `AI_EXECUTION_MAP.md`. Skill deve ABORTAR conforme "Quando NÃO usar", não re-classificar
5. Reportar em chat: "unit já classificada — skip"

Pass: skill aborta com mensagem clara.
Fail: skill re-classifica (= idempotência quebrada) ou trava (= bug em step 2 ou 3).

---

## Passo 5 — Colisão com vizinhas

Phase 4 workflow ainda não tem skills (verificar com `ls .claude/skills/`). Este passo PASSA por vacuidade v1.

Quando houver skills vizinhas (ex: `baseia-sdd-lock-unit`, `baseia-sdd-drift-check`), re-rodar: testar phrases gatilho de cada vizinha, skill correto deve disparar, não este.

Pass v1: "N/A — sem vizinhas ainda".

---

## Passo 6 — Registro

Após rodar 1-5, anotar resultado na próxima mensagem de commit:

- Tudo passou: `test-matrix: 6/6 passou`
- Falha parcial: `test-matrix: N/6 passou — passo X falhou (motivo)`

Atualizar `.claude/memory/domain/sdd-framework.md` marcando o gate "Test matrix (0/6)" como resolvido.

---

## Nota sobre ambiente de teste

Passos 1-3 rodam **sem efeito colateral** (skill só dispara, não escreve arquivos se Passo 1 parar antes do Builder).

Passo 4 (smoke test) tenta rodar o skill. Se escapar da ABORT por idempotência, Builder será dispatched via Task tool — custo real. Interromper imediatamente (Esc) se trigger for bem-sucedido; skill corrigido já deve abortar antes de dispatching.
