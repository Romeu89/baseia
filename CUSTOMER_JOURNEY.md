# Customer Journey — BaseIA

**Status:** Phase 1 partial lock + Phase 2 partial (steps 1-2). Steps 3+ pendentes de interview interativo.
**Source of truth para decisões:** [`_shape/2026-04-24-customer-journey-reset-shape.md`](_shape/2026-04-24-customer-journey-reset-shape.md) (append-only)
**Last updated:** 2026-04-24 autonomous run

---

## Persona v0.2 (LOCKED)

> **Solo founder** de PME, 1-2 pessoas, decide e paga do bolso. Baixa literacia em IA, sem tempo. Busca **ampliar capacidade sem contratar próximo CLT** — começando por atividades recorrentes de back-office financeiro (prestação de contas, conciliação). Típico: bateu teto MEI/ME e precisa regularizar CNPJ pra escalar.

**Autoridade de decisão:** Solo — 1 pessoa (ele próprio).
**Setup operacional:** 1-2 pessoas (ele + contador externo ou esposa/parente como apoio).
**Preço-sensibilidade:** Alta (paga do bolso).
**Capacidade técnica:** Baixa pra operar ferramenta complexa.

**Segmentos secundários deferidos:** 2-3 sócios e CEO 20+ ficam fora da Phase 2 primária. Mapear depois de PMF do primário.

---

## Canal de descoberta (step 2 — LOCKED)

**Canal:** B — Wedge "Regularizar CNPJ grátis"
**Sub-flavor:** Regularizar (operador MEI/ME existente batendo teto), não abrir (pre-revenue).
**Por que regularizar:** ICP matching com produto BaseIA (back-office recorrente). Pre-revenue não tem back-office pra automatizar.
**Motor (paid / SEO / founder content):** Deferido. Decisão de go-to-market, não de jornada.

---

## Trigger context (hypothesis, NOT a journey unit)

> **Collapsed em finding #2, 2026-04-25:** Trigger event não é touchpoint mensurável (mental state pre-discovery). Foi removido do SDD como unit. O que segue abaixo é **contexto hypothesis** pra informar headlines, comms e segmentação — não é step formal da journey. Trigger capture real (`which_trigger` MCQ + discovery prompt for 'other') vive em onboarding unit (parked, Phase 1 interview vai locar).

Solo founder sofre um dos 4 gatilhos. Não é evento único — é padrão convergente.

| # | Trigger | Comm tone pra segmentar no step 2 |
|---|---------|-----------------------------------|
| a | Perdeu alguém do financeiro e não quer repor | Operacional — urgência, alívio imediato, "escala sem CLT" |
| b | Fechou o mês com erro de conciliação / prejuízo não detectado | Controle — trust, zero-erro, reputação, "faz o back-office sozinho" |
| c | Bateu teto de faturamento mas CLT impede contratar | Operacional — mesmo tom de (a) |
| d | Viu concorrente/colega usando IA e ficou com FOMO | Educativa — desmistificar IA, mostrar case |
| other | Trigger fora dos 4 canônicos | Discovery — follow-up "o que te trouxe aqui?" (open-text). Resposta tenta reclassificar automaticamente em a/b/c/d via keyword match; se sem match, entra queue de revisão semanal pra Romeu ampliar taxonomia. Sem CTA de produto até reclassificar (evita comm errada). |

Triggers a+c convergem; b e d têm comms distintas. `other` é discovery loop — não comm tactic estável; serve pra capturar trigger novo OU reclassificar.

---

## Phase 2 — Flowchart table

**Todas as 9 colunas são mandatory per ULTRAPLAN constraint (col 9 adicionada 2026-04-25 finding #7). Coluna 8 (validation pattern) é prosa human-readable; coluna 9 (validation signature) é canonical hashable form.**

> **Step 1 collapsed (finding #2, 2026-04-25):** Trigger event não é touchpoint observável (mental state pre-discovery). Trigger capture (`which_trigger` MCQ + discovery prompt for 'other') migra pra onboarding unit — parked, Phase 1 interview vai locar como step >2 com phase_id próprio. Trigger context fica documentado na seção acima. Numeração de steps preservada (phase_id 2 é primeiro unit lockado).

| Step | Customer action | Input | Output | System touchpoint | Communication trigger | Decision/branch buttons | Validation pattern | Validation signature |
|------|-----------------|-------|--------|-------------------|-----------------------|-------------------------|--------------------|----------------------|
| 2 | Solo founder encontra wedge "Regularizar CNPJ grátis" e clica pro landing | Search intent OR referral link OR anúncio paid OR founder content | User na wedge landing page com intent explícita de regularizar CNPJ | Wedge landing page (web) com gate `is_existing_cnpj` (yes/no); branch yes → flow regularizar; branch no → educational redirect + waitlist opt-in | Headline variants por trigger: a/c → "Regularize seu CNPJ sem contratar contador fixo"; b → "Regularize seu CNPJ sem travar no mês"; d → "Como outros founders estão regularizando com IA"; gate "Você já tem CNPJ?" precede CTA de produto | `is_existing_cnpj` (gate yes/no antes de tudo) / `start_regularization` (primary CTA path-yes) / `talk_to_human` (secondary escape) / `learn_more` (educational) / `waitlist_optin` (path-no opt-in) | **Metric threshold + webhook callback + behavioral gate.** (1) Conversion landing → email/CNPJ submit ≥8% em 500 sessões (anchor: B2B SaaS self-serve high-intent 4-10%, Unbounce/daydream 2025); revisit >15%/<4%; **(2) Gate `is_existing_cnpj`** filtra ICP — visitor "no" (pre-revenue, intent abrir CNPJ) vai pra educational page com link externo (Sebrae/parceiro contábil) + opt-in waitlist (não default); (3) Webhook n8n no submit captura trigger+variant; (4) Webhook separado no waitlist_optin captura cohort off-ICP pra nurture longo (12-18m); (5) A/B golden-output 3 headlines, retention @ D7 tie-breaker. | `behavioral_self_report:cnpj_state_gate`; `golden_output:headline_ab_retention_d7`; `metric_threshold:landing_to_submit_conversion>=0.08@500sess`; `webhook_callback:submit_event_capture`; `webhook_callback:waitlist_optin_event` |
| 3 | TBD — Primeiro contato | TBD | TBD | TBD | TBD | TBD | TBD — **Phase 1 interview incomplete.** Romeu completa interativamente. | TBD |
| 4 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 5+ | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

---

## Validation pattern vocabulary (reference)

Patterns permitidos pela coluna "Validation pattern" (ULTRAPLAN constraint):

1. **Schema assertion** — expected input/output shape (tipos, campos obrigatórios).
2. **Golden-output comparison** — resultado real vs. resultado esperado pré-canonizado.
3. **Human-in-the-loop checkpoint** — aprovação humana embedada no fluxo (não podefalhar silenciosamente).
4. **Webhook callback (n8n-style)** — evento assíncrono confirma estado downstream. Inspired by Romeu's n8n pipeline discipline.
5. **Metric threshold** — KPI numérico com go/no-go explícito (ex: conversão ≥X%, accuracy ≥98%).
6. **Behavioral self-report** — user identifica próprio state/intent via questionnaire ou UI select.

Cada step ≥1 pattern. Múltiplos permitidos. Sem pattern = step não entra no SDD (Phase 4) nem na AI execution map (Phase 5).

---

## Mermaid flowchart

**PARKED — Phase 1 steps 3+ incompletos.**

Render do flowchart visual espera Phase 1 interview completar. Rationale: Mermaid com só 2 steps não ajuda nada — desperdício de esforço antes de ter jornada completa.

**Ao retomar:** gerar Mermaid do Phase 2 table completo, validar sintaxe em scratch file local (sem MCP Mermaid no env), inserir aqui.

---

## Human-in-loop queue (Romeu's return)

1. **Revisar steps 1-2** acima. Confirmar customer action, decision buttons, validation pattern. Corrigir se necessário (mudanças devem ser appended ao shape same-turn per rule).
2. **Completar Phase 1 interview** pros steps 3+ (primeiro contato, onboarding, primeira wins, retention, expansion, etc — estrutura exata depende do interview interativo).
3. **Renderizar Mermaid** após Phase 1 full lock.
