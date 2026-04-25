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
