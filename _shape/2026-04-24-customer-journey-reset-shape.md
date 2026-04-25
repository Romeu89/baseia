# Customer Journey Reset — Shape

**Session start:** 2026-04-24
**Driver:** Reset BaseIA project definition to a single locked customer-journey view, then rebuild forward (flowchart → doc reconciliation → SDD with hashing → AI execution map).
**Shape file role:** Append-only log of reasoned decisions. One decision per entry. Do not rewrite history.

---

## Decisions and Discoveries

### 2026-04-24 — Canonical docs folder = `_docs-claude/` (lowercase, hyphen)

**Decision:** All reset-phase outputs land in `projects/BaseIA_Projetos/_docs-claude/`. The existing `_Docs_Claude/` (capitalized, underscore) stays in place untouched until Phase 3 reconciliation decides its fate.

**Why:**
- `bmad-rbtv-baseia-docs-sync.md` rule and the session brief both reference `_docs-claude/`. Matching the rule avoids rewriting it.
- Creating the new folder fresh gives Phase 3 a clean audit target instead of mutating `_Docs_Claude/` mid-reset.
- Case-sensitive filesystems will treat them as distinct — no accidental overwrite risk.

**Cost:** Phase 3 must reconcile two near-identically-named folders. Accepted.

### 2026-04-24 — Persona v0.1 (hypothesis, not locked)

**Target customer (stated by Romeu, turn 1):**
- Role: empreendedor — dono/fundador de pequena ou média empresa
- Knowledge: baixa literacia em IA, sem tempo
- Explicit goal: substituir ou evitar contratação de funcionário operacional
- Domain where offer fits: back-office recorrente — financeiro, prestação de contas, conciliação

**Romeu's own caveat:** "considerando hipóteses" — persona é direcional, não travada.

**Two flags raised to revisit (NOT resolved):**

1. **"Substituir funcionário" é framing de venda, não de procura.** Dono de PME raramente chega dizendo "quero demitir X". Mais comum: perdeu alguém, sobrecarga, não consegue contratar. Isso afeta o trigger de comunicação no passo 1 da jornada (Phase 2).
2. **"Empreendedor" é amplo demais pra uma jornada única.** Fundador solo (decide + paga do bolso) ≠ sócio de 2-3 (decisão compartilhada) ≠ CEO de 20+ pessoas (decide, delega, tem controller). Jornadas materialmente diferentes. Não precisa decidir agora; precisa antes do lock da Phase 2.

### 2026-04-24 — Triggers múltiplos aceitos como step 1 da jornada

**Decision:** Os 4 gatilhos hipotéticos (a-d) foram todos validados pelo Romeu ("tds corretos"). Step 1 da jornada NÃO é um evento único — é um padrão convergente de múltiplos triggers.

- (a) Perdeu alguém do financeiro e não quer repor
- (b) Fechou o mês com erro de conciliação / prejuízo não detectado
- (c) Bateu teto de faturamento mas CLT impede contratar
- (d) Viu concorrente/colega usando IA e ficou com FOMO

**Implicação pra Phase 2:** Os 4 triggers convergem pro mesmo step 2 (contato inicial), mas pedem **comms diferentes**:
- a + c → comm operacional (urgência, alívio imediato)
- b → comm de controle (trust, zero-erro, reputação)
- d → comm educativa (desmistificar IA, mostrar case)

A + c e b + d não se contradizem; são segmentação de comms dentro do mesmo passo.

**Why:** Forçar trigger único geraria persona falsa. Aceitar multi-trigger mantém realismo e já entrega insumo direto pro mapa de comms da Phase 2.

### 2026-04-24 — Reordenação de fases: Git prep agora, handoff via "ultraplan"

**Decision:** A ordem original (Phase 1 → 5 todas aqui) muda. Nova sequência:

1. **Preparar GitHub e território** (agora, bloqueante)
2. **Retomar interview + lock do conceito** (Phase 1 enxuta + parte da Phase 2)
3. **Adaptar o que já foi feito à nova visão** (Phase 3 enxuta, sem reconciliação completa ainda)
4. **Entregar prompt pro Cursor Claude rodar o "ultraplan"** — SDD com hashing aprimorado + AI execution map saem lá, não aqui

**Why:** Romeu vai executar o "ultraplan" em outra instância Claude (Cursor). Se o git estiver confuso, o ultraplan quebra. Melhor estabilizar o território antes, aqui, onde temos contexto.

**Aberto:** O que exatamente "preparar GitHub corretamente" significa — ver pergunta em aberto no turn atual.

### 2026-04-24 — Testing-as-planning como constraint de primeira classe

**Decision:** Cada unidade do SDD (Phase 4) nasce com um **padrão de validação definido no momento do design**, não depois. Replica a disciplina que Romeu teve quando usava n8n como ferramenta de check ao longo do pipeline.

**Impacto por fase:**

| Fase | Constraint adicionada |
|------|----------------------|
| Phase 2 (flowchart) | Cada linha da tabela ganha coluna "como testamos que esse passo funcionou" |
| Phase 4 (SDD) | Schema de cada unit inclui `validation_pattern` (ex: assertion, golden output, human-check, n8n-style webhook) |
| Phase 5 (AI map) | Para cada unidade AI-executable, a validation_pattern é condição pra classificar como "execute" vs "assist" |

**Why:** Sem padrão de check embarcado no design, AI execution em escala vira roleta. O n8n provou que checkpoints inline funcionam; queremos preservar esse hábito mesmo sem n8n como ferramenta.

### 2026-04-24 — Phase 0.5 (git prep) concluída — Option (i) + WIP branch pattern

**Decision:** Executado Option (i) — consolidar os 2 repos atuais. Concretamente:
- PR #1 mergeado (squash) em `romeuhr/baseia-planning/main` → commit `735b626`.
- Branch `claude/customer-journey-reset` deletada local + remoto.
- Nova branch `claude/shape-phase1-wip` criada e pushed — backup remoto do shape acumulando turns.
- `baseia-api` intocado (estava limpo).
- `_Docs_Claude/` (capitalizado) intocado — reconciliação é Phase 3.

**Padrão de commit adotado pra resto da sessão:**
- Shape é editado a cada turn relevante (context-preservation same-turn).
- Commits na WIP branch acontecem a cada turn com edit significativo (hygiene local).
- **NÃO abrir PR novo a cada turn.** Um único PR por phase lock. Isso evita ruído no repo — que era exatamente a reclamação original do Romeu ("esses andam muito confuso").

**Why:** Balanceia (a) hábito de commit frequente pra não perder trabalho, (b) histórico limpo no main (só merges de phase completas), (c) handoff pro Cursor Claude no final — ele pode ler o shape + docs locados e começar o ultraplan sem precisar arqueologar PRs intermediários.

**Pendente flagado:** git user.email global do Romeu tá como `romeuhungriarechdan@mac.lan` — commits não linkam ao perfil GitHub. Não mutei porque rule `NEVER update git config`. Decisão dele.

### 2026-04-24 — Canal de descoberta (step 2) = unknown ativo

**Discovery (não decisão):** Romeu respondeu "não sei ainda" pra como o empreendedor descobre a BaseIA. Canal de aquisição é um unknown ativo, não uma escolha feita.

**Blast radius — o que fica bloqueado enquanto não resolver:**
- Superfície de first-touch (landing page / WhatsApp / DM / formulário) indefinida.
- Tom de comms inicial (cold educativo vs. warm qualificador) indefinido.
- CAC e volume esperado — impossível estimar.
- Plataforma onde concentrar presença (LinkedIn vs. Google vs. comunidade) indefinida.

**Opções propostas ao Romeu no turn 3 (aguardando escolha):**
- (A) Skip step 2 e seguir pro step 3 (primeiro contato), assumindo "ele chegou" sem definir como. Aceita o buraco.
- (B) Pausar Phase 1 pra hipotetizar canal via background agent (research leve, não Phase 3 completa).
- (C) Placeholder "indicação" como default — canal dominante em SaaS B2B SMB early-stage. Segue jornada e re-valida depois. Unknown vira item obrigatório no AI execution map.

**Recomendação do agente:** (C). Motivo: assumption de menor custo, compatível com realidade inicial de qualquer SaaS B2B SMB, e steps 3+ da jornada são majoritariamente canal-independentes.

### 2026-04-24 — Option B escolhido — research agent dispatched

**Decision:** Romeu escolheu (B). Background web-research agent dispatched pra levantar 3-5 hipóteses ranqueadas de canal de aquisição pra SaaS B2B SMB financeiro no Brasil early-stage (0-500 clientes).

**Why:** Aceitamos o custo de 1 turn pausado em troca de hipóteses ancoradas em precedentes reais, não chute. Melhor research leve agora do que locar a jornada com canal fantasia que vira débito técnico de produto/marketing.

**Escopo do agent:** APENAS hipóteses de canal + leading indicators + flag cultural pt-BR. NÃO reconcilia docs do repo, NÃO toca em Phase 3. Research é externa (precedents da indústria tipo Conta Azul, Contabilizei, Omie, Nibo), não interna (estado atual da BaseIA).

**Output esperado:** máx 400 palavras, ranked list com evidência, 1 leading indicator mensurável por canal, recomendação de "primeiro canal a testar".

### 2026-04-24 — Research agent retornou — 4 canais ranqueados + 2 flags críticos NOVOS

**Finding:** Agent retornou. Output completo em `_docs-claude/research/2026-04-24-discovery-channel-hypotheses.md`.

**Síntese do ranking (forte → fraco):**

1. **Contador Indicação** (B2B2C partner program) — STRONGEST. Precedentes repetidos: Omie 21k parceiros, Conta Azul + Nibo 10k+ cada. First-test rec do agent.
2. **Wedge "Abra/Regularize CNPJ grátis"** — playbook dos primeiros 100k da Contabilizei.
3. **LinkedIn pt-BR founder content** (ICP controller/sócio de serviços, tipo Kamino). Precedentes thin pra early-stage — hypothesis only.
4. **Sebrae + comunidades WhatsApp/Telegram** (institutional trust). Precedentes thin — hypothesis only.
- **Anti-rec:** Google Ads puro em "automatizar financeiro". Não queimar budget antes de 1 ou 2 funcionarem.

**FLAG CRÍTICO NOVO #1 — Framing "substituir funcionário" é evidência-hostil, não só hunch.**

A flag levantada no turn 2 (que "substituir" era framing de venda, não de procura) agora tem evidência dura:
- Canal #1 (contador) é **mecanicamente hostil** ao framing: contador perde billable hours se cliente automatiza demais. Framing obrigatório no canal: "amplia capacidade sem contratar próximo CLT" + "libera contador de retrabalho operacional" — nunca "dispensa seu financeiro".
- Canal #3 (LinkedIn) também hostil quando leitor é o próprio controller (você fala com quem seria substituído).
- Estudo independente: medo de substituição é barreira citada em estudo BR [9]. 72% das empresas BR em adoção inicial de IA.
- **Implicação obrigatória:** reframar persona v0.1 de "substituir ou evitar contratação" pra "amplia capacidade sem contratar próximo CLT". A segunda é true-subset da primeira mas culturalmente neutra. Refletir no `CUSTOMER_JOURNEY.md` quando ele for escrito.

**FLAG CRÍTICO NOVO #2 — Canal #1 (contador) cria dinâmica B2B2C. Steps 3+ NÃO são canal-independentes.**

Eu tinha afirmado no turn 3 que "steps 3+ da jornada são majoritariamente canal-independentes". Research contradiz parcialmente:
- Se canal = contador, o **first contact não é o dono da PME — é o contador**. A jornada tem duas personas: contador (canal + gatekeeper) e PME owner (end-user). Jornada B2B2C.
- Se canal = wedge CNPJ, Sebrae, ou LinkedIn, o first contact é o dono direto. Jornada B2B2C desaparece.
- **Implicação:** a escolha de canal determina se a Phase 2 flowchart tem 1 persona ou 2. Não dá pra adiar essa decisão como eu havia proposto.

**Decisão pendente (turn 5):** Locar step 2 em qual canal — opções abaixo pro Romeu escolher.

### 2026-04-24 — Decisão 1 LOCKED — Canal B (Wedge "Abra/Regularize CNPJ grátis")

**Decision:** Step 2 da jornada = wedge de abrir/regularizar CNPJ. Romeu respondeu "b" no turn 6 (primeiro turn da sessão local pós-handoff).

**Opções consideradas (consolidadas do research + briefing ULTRAPLAN):**
- A — Contador Indicação (B2B2C, strongest research evidence)
- B — **Wedge CNPJ (escolhido)**
- C — Multi-canal paralelo A+B
- D — Não locar, mais research

**Opções #3/#4 do research (LinkedIn founder content, Sebrae/comunidades) foram conscientemente omitidas** porque research marcou "hypothesis only, precedentes thin" — não maduro pra lock. Ficam como fallback, não como opção de lock.

**Why:**
- Evita dinâmica B2B2C (1 persona vs 2) — simplifica Phase 2 flowchart materialmente.
- Elimina gatekeeper com incentivo parcialmente adversarial (contador perde billable hours se cliente automatiza).
- Precedente existente: Contabilizei construiu os primeiros 100k clientes com esse playbook.

**Trade-offs aceitos:**
- Build upfront maior — wedge exige landing + automação de abertura/regularização + nurture funcionando antes de gerar lead útil. Não é canal "ligar pro contador amanhã".
- Precedente é de uma empresa que queimou muito budget de paid pra provar. Custo de aquisição real ainda desconhecido.
- Canal exige decisão de motor: paid ads (Google/Meta "abrir CNPJ") vs. SEO orgânico vs. founder content. Research não comprometeu — fica pendente.

**Sub-decisão aberta dentro de B (não travando turn atual):** o wedge captura **"abrir CNPJ"** (pre-revenue, empreendedor ainda sem operação — ICP não-matching com "back-office recorrente") ou **"regularizar CNPJ"** (operador existente batendo teto MEI/ME — ICP matching com trigger (c) da persona)? As duas formas estão no nome do canal e têm ICPs materialmente diferentes. Resolver antes de Phase 2 lock.

**Impacto em Decisão 2 (próxima):**
- Persona reframe ("substituir" → "amplia capacidade sem contratar") NÃO é mais forçado pelo canal (era forçado em A por hostilidade contábil). Continua sendo smart move por razão independente — evidência BR de que 72% das empresas em adoção inicial de IA citam medo de substituição como barreira. Reframe ainda recomendado, mas agora é julgamento cultural e não obrigação estrutural.

**Impacto em Decisão 3 (subtipo):**
- Wedge CNPJ tende a filtrar solo founders + sócios pequenos (2-3) — quem abre/regulariza CNPJ é quase sempre o dono operacional. CEO-de-20+ não abre CNPJ pessoalmente, um sócio operacional ou contador faz. Subtype "CEO 20+" fica improvável como primário via canal B. Não decide a Decisão 3 sozinho, mas enviesa.

### 2026-04-24 — Decisão 2 LOCKED — Persona reframe aprovado

**Decision:** Persona v0.1 reescrita: "empreendedor dono de PME que **amplia capacidade sem contratar próximo CLT**, começando por atividades recorrentes de back-office financeiro (prestação de contas, conciliação)."

**Romeu's choice:** "Aceitar reframe" (opção recomendada pelo agente).

**Why:**
- Research BR citado: 72% das empresas em adoção inicial de IA citam medo de substituição como barreira ativa. Framing "substituir" é evidência-hostil mesmo em Canal B (direto ao dono).
- Wedge "regularizar CNPJ" captura muito pre-hire (solo founders ou empresas que operam no limite de MEI/ME sem CLT formal). "Substituir funcionário" é literalmente incoerente — não tem funcionário a substituir.
- "Amplia capacidade sem contratar próximo CLT" é true-subset culturalmente neutro: não perde audiência que também busca "evitar contratação", e ganha audiência que rejeitaria "substituir".

**Trade-off aceito:** framing perde punch comercial direto ("não contrato mais ninguém" é mais concreto que "amplia capacidade"). Recuperado via comms: triggers a/c (operacional, teto) usam tom "escala sem CLT"; triggers b/d (controle, FOMO) usam tom "faz o back-office sozinho".

### 2026-04-24 — Decisão 3 LOCKED — Subtipo primário = Solo founder

**Decision:** Target primário é **solo founder** — decide e paga do bolso, 1-2 pessoas, ele é o operacional.

**Romeu's choice:** "Solo founder".

**Why:**
- Fit duplo: Canal B (regularizar CNPJ) pega solo founders que bateram teto MEI/ME, e persona reframeada (amplia capacidade sem CLT) descreve exatamente o solo founder que não quer contratar primeiro funcionário.
- Decisão implica: (a) autoridade de decisão = 1 pessoa (ele próprio), (b) setup = 1-2 pessoas (ele + contador ou esposa/parente), (c) preço-sensibilidade alta (paga do bolso), (d) capacidade técnica baixa pra operar ferramenta complexa.

**Segmentos secundários deferidos (não descartados):** 2-3 sócios e CEO 20+ ficam fora da Phase 2 primária. Mapear depois quando segmento primário tiver product-market fit.

**Implicação pro SDD (Phase 4):** units de first-touch e onboarding devem assumir "usuário final = decisor = pagador = operador". Sem persona-split no flowchart.

### 2026-04-24 — Sub-flavor do wedge LOCKED — Regularizar CNPJ

**Decision:** Wedge de Canal B é **"Regularizar CNPJ grátis"** — operador existente batendo teto MEI/ME, não "Abrir CNPJ" (pre-revenue).

**Romeu's choice:** "Regularizar CNPJ (Recommended)".

**Why:**
- ICP matching com produto: BaseIA é back-office recorrente (financeiro, prestação de contas, conciliação). Pre-revenue (abrir CNPJ pela primeira vez) não tem back-office pra automatizar ainda — ICP não bate.
- Alinhamento com triggers travados: "bateu teto de faturamento mas CLT impede contratar" (trigger c) é literalmente o mesmo arquétipo de "regularizar CNPJ" (MEI limite ~R$81k, ME ~R$360k — quem bate teto precisa migrar de regime).
- Concentração de esforço: wedge único simplifica funnel (landing + automação de regularização + nurture). "Ambos" foi rejeitado — dobra complexidade antes de provar que 1 funciona.

**Trade-off aceito:** perde volume de lead que "abrir CNPJ" geraria. Aceitável porque lead abrir-CNPJ tem ICP distinto (pre-revenue) e nurture seria longo (meses até ter back-office).

---

## Journey-So-Far (Phase 1, rebuilt each turn)

**Persona v0.1** (hipótese, turn 1 — aguardando próxima confirmação):

> Empreendedor dono de PME (subtipo solo/sócios/CEO-20+ ainda não segmentado), baixa literacia em IA, sem tempo, que busca substituir ou evitar contratação de funcionário operacional — começando por atividades recorrentes de back-office financeiro (prestação de contas, conciliação).

**Turn:** 7 (pre-flight do autonomous run fechado — pronto pra autonomous deterministic work)
**Edits pedidos por Romeu nesta iteração:** Decisões 2, 3, sub-wedge lockadas. Autonomous run autorizado com escopo determinístico.

**Persona v0.1 → v0.2 (LOCKED):**
> Solo founder de PME, 1-2 pessoas, decide e paga do bolso, baixa literacia em IA, sem tempo, que **amplia capacidade sem contratar próximo CLT** — começando por atividades recorrentes de back-office financeiro (prestação de contas, conciliação). Típico: bateu teto MEI/ME e precisa regularizar CNPJ pra escalar.

**Draft de jornada (Phase 1, steps 1-2 lockados, steps 3+ pendentes):**

| # | Passo | Estado |
|---|-------|--------|
| 1 | Solo founder sofre um dos 4 gatilhos (a-d) | **LOCKED** — multi-trigger com comms diferenciadas |
| 2 | Discovery via wedge "Regularizar CNPJ grátis" | **LOCKED** — operador existente batendo teto MEI/ME |
| 3 | Primeiro contato | **PARKED** — requer interview user-dependent |
| 4+ | — | **PARKED** — requer interview user-dependent |

**Ambiguidades abertas (deferred, não bloqueiam autonomous):**
- Motor do canal (paid vs SEO orgânico vs founder content): decisão de go-to-market, não de jornada. Fora do escopo Phase 1-5.
- Segmentos secundários (2-3 sócios, CEO 20+): mapear depois de PMF do primário.

**Postura:** Não forçar decisão onde não há. Unknowns são discoveries legítimas e viram research items no AI execution map.

---

## Phase Status

| Phase | State |
|-------|-------|
| 0 — Repo discovery | Done |
| 0.5 — Git prep (Option i) | Done — PR #1 merged, WIP branch `claude/shape-phase1-wip` ativa |
| 1 — Customer journey interview | Active (turn 5) — step 1 locked, step 2 research done, canal pendente de lock |
| 2 — Flowchart lock (com coluna de validação) | Blocked on Phase 1 |
| 3 — Doc reconciliation (enxuta, só o necessário pra visão) | Blocked on Phase 2 |
| 4 — SDD com hashing + validation_pattern por unit | **Movido pra Cursor Claude via prompt de "ultraplan"** |
| 5 — AI execution map | **Movido pra Cursor Claude via prompt de "ultraplan"** |
| 6 — Entrega: prompt pro ultraplan + handoff limpo | Novo — target final desta sessão |

---

### 2026-04-25 — Readiness validation snapshot

**Decision:** Antes de retomar Phase 1 steps 3+ ou autorizar qualquer mudança em SDD/AI_EXECUTION_MAP, ler [`2026-04-25-readiness-validation.md`](2026-04-25-readiness-validation.md) (relatório completo).

**Why:** Resume Contract de 2026-04-24 (`AUTONOMOUS_RUN_REPORT.md`) está estagnado:
- Branch real (`claude/phase1-remote-review` @ `0816cac`) ≠ branch declarada (`claude/phase1-interview` @ `a1a3e5a`).
- `git remote -v` vazio neste sandbox; PR #1 não verificável daqui.
- 7 commits pós-`a1a3e5a` (REMOTE_REVIEW, research, skill SDD framework, PHASE1_INTERVIEW_SCRIPT, sandbox preflight) sem entry no autonomous run log.
- REMOTE_REVIEW Finding 1 (X threshold) bloqueia legitimidade Phase 4/5.

**Verdict consolidado:** Tooling GREEN (22/22 self-test, 0 drift). Phase 1 interview GO com Romeu (script de 15 Qs pronto). Phases 2-5 NO-GO até reconciliação git + 5 decisões pendentes do Romeu.

**Append-only respeitado:** sem rewrite das entries anteriores; Phase Status table (linhas 257-268) fica com snapshot 2026-04-24 — relatório novo é a fonte de verdade atual.

### 2026-04-25 — Part A complete — git reconciled vs merged PR #1

**Decision:** Pulou re-signing (manter `N`); rebased `claude/phase1-remote-review` onto `origin/main` + force-with-lease push; PR #2 retargeted base de `claude/phase1-interview` (deletado/merged) pra `main`.

**State pós-Part A:**
- HEAD = `d15c1f4` (era `6c50082`); 6 commits replayed clean sem conflito
- `git config user.email` = `romeuhrechdan@gmail.com` (já estava — reauthor desnecessário)
- PR #2 OPEN, base=main, head=claude/phase1-remote-review
- `python3 _tools/hash_units.py --self-test`: 22 PASS, exit 0
- `python3 _tools/hash_units.py`: 2 units, 0 drift, exit 0

**Why skip signing:** Romeu autorizou (3 perguntas via AskUserQuestion). Trade-off aceito: commits ficam unsigned no GitHub (badge ausente) em troca de zero rebase destrutivo extra.

### 2026-04-25 — Finding #1 LOCKED — X threshold = 8% / window = 500 sessões

**Decision:** Unit 2 conversion threshold = **≥8%** medido em janela de **500 sessões** (volume-anchored, não time-anchored). Revisit triggers: **>15%** (X set too low — raise) ou **<4%** (below floor — kill creative/wedge).

**Why:**
- Anchor: B2B SaaS self-serve high-intent benchmark band 4-10% (Unbounce + daydream 2025). 8% = mid-band conservador.
- Volume-anchor (500 sessões) substitui "2 semanas" original do SDD.md:53 — robusto a low-traffic; pareado com 8% = ~40 conversions mínimas pra significância.
- Researcher confidence medium — sem BR-fintech-wedge benchmark; todos candidatos são US/global B2B SaaS proxies.
- Form-length tailwind: BaseIA wedge tem 2-3 fields vs 6+ "lift de 120%" (Unbounce) — favorável.

**Trade-offs aceitos:**
- Threshold US-anchored sem BR-specific data — risco de calibration off na realidade pt-BR (mitigado por revisit triggers).
- Time-based escalation antigo (2 semanas) substituído por volume — mais robusto mas deixa cenários de tráfego muito baixo sem deadline temporal explícito.

**Edits aplicados (same-turn):**
- `SDD.md` unit 2 — `validation_pattern` + `escalation_rule` reescritos com 8% / 500 sessões / revisit triggers + source citation.
- `CUSTOMER_JOURNEY.md` Phase 2 row 2 — coluna validation pattern atualizada com mesmos números + anchors.

**Discovery não-obvia (alimenta finding #7):** unit 2 hash NÃO mudou pós-edit. `_tools/hash_units.py:67` formula é `sha256(phase_id + customer_action + io_signature + sorted(decision_buttons))` — `validation_pattern` e `escalation_rule` ficam fora. Ou seja, mudei a regra de validação core do step e o drift checker não nota. **Isso é exatamente o gap que finding #7 chama** ("hash inclui `validation_pattern`?") — vai ser próxima decisão na queue.

**Split unit 2 em (a) capture + (b) first-payment (research finding #4):** adiado pra finding #2 da queue (unit 1/2 split discussion). Não resolvido aqui.

### 2026-04-25 — Finding #7 LOCKED — schema bump: hash inclui validation_signature

**Decision:** Hash formula extended to include canonical structured `validation_signature` (option C — canonical structure, escolhido por Romeu via AskUserQuestion).

**Schema change:**
- Phase 2 table grows from 8 → 9 colunas — coluna 9 "Validation signature".
- SDD unit schema ganha campo `validation_signature` (mandatory, paralelo ao `validation_pattern` prosa).
- Hash formula: `sha256(phase_id + "|" + customer_action + "|" + io_signature + "|" + sorted_buttons_joined + "|" + validation_signature)`.
- Delimiter dentro de `validation_signature` é `;` (não `|` — pipes quebram parser de tabela markdown).

**Canonical signature format:**
- Pipe-segments substituídos por semicolon-segments: `pattern_type:args[;pattern_type:args...]`
- Sorted alphabetically pra estabilidade.
- Pattern types do vocab CUSTOMER_JOURNEY.md (6): `schema_assertion`, `golden_output`, `human_checkpoint`, `webhook_callback`, `metric_threshold`, `behavioral_self_report`.
- Args convention: `metric_threshold:<metric_id><op><value>@<window>` (op ∈ `>=,<=,>,<,==`); outros pattern types levam single args ID.

**Why C (não A nem B):**
- (A) skip aceita drift checker meio cego — viola rigor de Phase 4.
- (B) hash full prose: rephrases viram drift fake → agente vai evitar editar prosa → doc rot.
- (C) hash structured: rephrases livres, mudança de tipo/número trava hash. Verdadeiro testing-as-planning lock.

**Implementação (same-turn):**
- `_tools/hash_units.py`: nova fn `canonical_validation_signature()` (split em `;`, strip backticks, sort, join). `compute_hash` ganha 5º arg. `parse_journey_table` aceita 9 cols. Self-test fixtures atualizados (30 PASS, era 22).
- `CUSTOMER_JOURNEY.md`: header tabela 9 cols, units 1+2 com signatures, units 3+ com `TBD`. Texto "8 colunas" virou "9 colunas".
- `SDD.md`: hash formula doc atualizada, schema example com `validation_signature`, units 1+2 com novo campo + novo `unit_hash`.
- Hashes recomputadas: unit 1 `d6c59fb5...` → `004ec912...`; unit 2 `af58f450...` → `4f382dbc...`.

**Trade-offs aceitos:**
- ULTRAPLAN constraint "8 colunas mandatory" agora "9 colunas" — bump deliberado, documentado.
- Human escreve signature canonical à mão. Risco de inconsistência entre signature e prose `validation_pattern`. Mitigação futura: lint que parser prose pra validar consistência (parked, não bloqueia).
- Backtick wrap nas signatures cells é cosmético (markdown display) — parser strip-a.

**Drift check pós-implementação:** 2 units, 0 drift, exit 0. Self-test 30/30 PASS.

### 2026-04-25 — Finding #3 LOCKED — comm tone pra trigger='other' = Discovery prompt

**Decision:** 5ª comm tone do `which_trigger` = **Discovery prompt** (option C, escolhido por Romeu). Follow-up open-text "o que te trouxe aqui?" → keyword match em a/b/c/d ou review queue.

**Why C (não A nem B):**
- A (generic nurture): perde signal — não learn nada com 'other'.
- B (manual review queue): honest mas vira gargalo humano em escala.
- C (discovery prompt): converte 'other' em learning loop. Captura trigger novo OU reclassifica retroativamente. Custa UI extra e introduz friction de 1 step.

**Edits aplicados:**
- `CUSTOMER_JOURNEY.md` Step 1 trigger matrix — adiciona 5ª linha `other` com discovery loop spec; nota explicativa "discovery loop, não comm tactic estável".
- `CUSTOMER_JOURNEY.md` Phase 2 row 1 — validation pattern prosa expandida com branch 'other'; validation signature ganha `behavioral_self_report:discovery_other_freetext`.
- `SDD.md` unit 1 — `validation_pattern` (prose), `validation_signature`, `responsibility`, `interface`, `ai_role`, `escalation_rule` atualizados.
- `unit_hash` recomputado: `004ec912...` → `50f7c32f...` (signature mudou).

**Discovery flagged: ai_role unit 1 mudou de `none` → `assist`.** Keyword reclassifier do discovery loop é componente AI (regex/embedding match). Por definição do vocab, `assist` = "AI auxilia humano (copilot-style, rascunhos, sugestões). Humano decide." Reclassifier propõe trigger; sem match → human revisa via review queue. Bate com `assist`.

**Trade-offs aceitos:**
- Friction extra no funnel pra cohort 'other' — aceitável porque cohort 'other' já é signal de problema, não de revenue path.
- Keyword reclassifier requer setup (lista de keywords por trigger). Build cost real pra Phase 5 — vai virar item no AI execution map.
- Comm 'other' fica congelada até reclassificação. Se reclassificador é lento, user fica em limbo. Mitigação: escalation timeout (e.g., 48h) → manual review automático. **Parked como sub-item — não bloqueia finding #3 lock.**

**Drift check:** 2 units, 0 drift, exit 0.

### 2026-04-25 — Finding #10 LOCKED — gate `is_existing_cnpj` + waitlist opt-in pra path "abrir CNPJ"

**Decision:** Visitor com intent "abrir CNPJ" no wedge → option C (hybrid educational + opt-in waitlist). Visitor primeiro responde gate `is_existing_cnpj` (yes/no). Path-yes proceeds wedge regularizar; path-no vai pra educational page com (1) link externo Sebrae/parceiro contábil pra abrir agora, (2) opt-in waitlist OPCIONAL (não default).

**Why C:**
- A (redirect off-funnel) honest mas perde lead pra sempre.
- B (waitlist default) economia ruim: pre-revenue founders pivotam/fecham em ~50% dos casos no nurture window de 6-18m.
- C força auto-qualificação via opt-in — só quem realmente planeja regularizar futuramente faz opt-in.

**Edits aplicados:**
- `CUSTOMER_JOURNEY.md` Phase 2 row 2 — system touchpoint expandido (gate + branches), comm trigger expandido (gate question), decision_buttons crescido de 3 → 5 (`is_existing_cnpj`, `learn_more`, `start_regularization`, `talk_to_human`, `waitlist_optin`), validation pattern prosa expandida com 5 sub-itens, validation signature expandida com 2 segmentos novos (`behavioral_self_report:cnpj_state_gate`, `webhook_callback:waitlist_optin_event`).
- `SDD.md` unit 2 — `decision_buttons`, `validation_signature`, `responsibility`, `interface`, `validation_pattern`, `escalation_rule` atualizados.
- `unit_hash` recomputado: `4f382dbc...` → `05a2ae6e...` (signature + buttons mudaram).

**Trade-offs aceitos:**
- Wedge agora tem step extra (gate antes de CTA) — adiciona friction. Mitigação: pergunta única binária, 2 segundos pro user.
- Educational page + waitlist UI = build cost real. Vai virar item Phase 5 AI execution map (provavelmente low-AI: page é static + form opt-in).
- Threshold "30% off-ICP rate sinaliza canal misalign" é unanchored (judgment call). Pode precisar revisita após 500 sessões reais.

**Discovery (não-obvia):** unit 2 agora tem 2 outputs distintos por path (yes/no). Tecnicamente isso é split de unit em sub-units, mas mantemos como unit única com `interface` documentando ambos paths. Se complexidade crescer, finding #2 (próximo na queue, unit 1/2 split) pode acabar splitando unit 2 também — flagged.

**Drift check:** 2 units, 0 drift, exit 0.
