# AI Execution Map — BaseIA

**Status:** Phase 1 LOCKED. Rows for units 2, 3, 4, 5, 6 (todos lockados via SDD). Step 1 collapsed em finding #2 (não é unit, é hypothesis context). Phase 1 termina em Step 6 per Q11 — Steps 7+ deferred pra Phase 2 com PMF data.
**Source:** [`SDD.md`](SDD.md) — cross-referenced por unit_hash.
**Rule (ULTRAPLAN):** unit sem `validation_pattern` não pode ser classificado como `ai_executable_at_scale`. No máximo `human_in_loop_required`.

---

## Classification vocabulary

| Classification | Significado |
|----------------|-------------|
| `ai_executable_at_scale` | Unit tem validation_pattern mensurável automaticamente; AI pode executar com auditoria via validation output. Ex: headline gen + A/B + webhook. |
| `human_in_loop_required` | Unit precisa judgment humano por natureza (trigger, relationship, qualitative). AI pode assistir mas não substituir. |
| `blocked_by_missing_infra` | Unit seria AI-executable mas falta infra (ex: sem database, sem webhook, sem credential). Desbloquear via missing_infra. |

---

## Units mapped

| unit_hash | classification | model_pattern | human_decision | missing_infra | validation_pattern (from SDD) |
|-----------|----------------|---------------|----------------|---------------|-------------------------------|
| `7fd213d8...74fbcbde` (phase 2) | `ai_executable_at_scale` | Haiku 4.5 gera variants de headline por trigger (a/b/c/d). Sonnet 4.6 opcional pra refinamento. A/B orchestration via feature-flag infra. Conversion tracking via webhook n8n-style. Gates `is_existing_cnpj` + checkbox `back_office_optin` = static branches (não AI). | Romeu aprova primeira batch de variants antes de dispatch; daí AI roda sozinha. Decisão de aceitar/rejeitar opt-ins (waitlist + back_office) é static UX. | Feature-flag/experiment infra; analytics webhook; landing page CMS com slot de headline dinâmica; opt-in waitlist DB; back_office_optin capture + cohort routing pra unit 4. | Metric threshold (conversion ≥8% @ 500sess) + behavioral gate `is_existing_cnpj` + 3× webhook (submit + waitlist + back_office_optin) + golden-output A/B D7. |
| `c5e3a6b4...fa8723cc` (phase 3) | `ai_executable_at_scale` | Haiku 4.5 (low-latency) bot triagem em n8n: classifica reply do user em FAQ category vs out-of-scope; resposta auto pra FAQ, escalation pra Romeu/contador em out-of-scope. Sonnet 4.6 opcional em edge case com confidence ambígua. Email send via Resend (static template selection por `trigger_self_report`). | Romeu/contador respondem replies escalados (out-of-scope OU bot confidence baixo). Romeu aprova FAQ scripts iniciais + revisões periódicas. | n8n bot infra com confidence-score + scope-check; inbox unificada bot+humano (single thread per user); FAQ KB editável; reply webhook. | Metric threshold (reply rate ≥10% @ 500submits) + webhook email_send + webhook reply_received + human_checkpoint bot_escalation_to_romeu. |
| `e27d0a7d...3bfa347290` (phase 4) | `blocked_by_missing_infra` | Sonnet 4.6 (ou Haiku 4.5 se accuracy permitir) pra conciliação AI; comparado contra rule-based deterministic conciliador (Python/Pandas) como golden-output baseline. n8n orchestration: trigger=regularization_completed+optin → seed Receita data → run AI conciliacao → run rule-based → diff → if accuracy ≥95% display, else queue pra human review. Anthropic credentials já em uso. | Romeu/contador resolvem `dispute_first_run` (review queue). Aprovam expansão de training data quando golden-output accuracy cai. | (1) Rule-based conciliação engine (baseline pra golden-output diff). (2) Receita Federal seed pipeline (regularization completion → CNPJ data fetch). (3) Conciliação training corpus pro AI model. (4) App back-office BaseIA (web/mobile UI com login + dispute flow). (5) Approval state DB (default_auto_runs flag por user). **NENHUM destes existe hoje** — BaseIA hoje é só FastAPI prod sem app cliente. Phase 5 unblock = build esses 5 itens. | Golden-output (AI vs rule-based ≥95%) + metric_threshold (first-login ≥70%) + 2× webhook (first_login + first_run_completed) + human_checkpoint (dispute_first_run review). |
| `52068a9d...213d69f313` (phase 5) | `blocked_by_missing_infra` | Sonnet 4.6 pra error-detection pass (segunda call sobre conciliação output validated). Haiku 4.5 (reused do unit 2) gera trigger-tone copy pro win-screen. Confidence-score interno do model usado como gate ≥95% pro error claim. Golden-output diff secundário: AI's error claim vs rule-based detection — só publica se ambos flagam. Win-screen UI exibe error_highlight OR clean_report layout. | Romeu/contador review primeiros 3 wins por client (D0 trust insurance) antes de display. Aprovam ajuste de confidence threshold + sensitivity de error detection cross-client. | (1) AI error-detection corpus (golden examples de erros legítimos pra training/eval). (2) Win-screen UI (web/mobile component). (3) Per-client confidence threshold storage (raise se user error-dismiss-rate >20%). (4) Review queue UX pros first 3 wins (mesma queue do dispute_first_run da unit 4). (5) Trigger-tone copy templates pre-approved por Romeu (3+ variants por trigger). **NENHUM existe hoje** — depende de unit 4 infra + extras específicos. Phase 5 unblock = build estes + os 5 da unit 4. | Confidence gate (≥95%) + golden-output (AI error vs rule-based) + human_checkpoint (first 3/client) + behavioral_self_report (confirm/dismiss) + metric (win-event-rate ≥70%) + 2× webhook (win + error_dismissed). |
| `153839bc...4645967105` (phase 6) | `blocked_by_missing_infra` | Sonnet 4.6 reusado do unit 5 (error-detection model) com sensitivity threshold mais permissive pra unusual transaction detection (recurring cycle context, push notification target). n8n cron mensal dispara recurring conciliação (reuse unit 4 AI conciliador). Push copy gerada por Haiku 4.5 (reused do unit 2). Paywall display + payment processing = static UX + Stripe Brasil API (não AI). Subscription state machine (active/churned) trackada em DB. | Romeu approva pricing + N threshold (3 conciliações pre-paywall) + push sensitivity ajustes. Romeu/contador handle churn survey responses pra retraining + product fixes. | (1) Payment gateway integration (Stripe Brasil ou alternativa BR). (2) Subscription state DB (active/churned/trialing) + billing cycle. (3) Push notification infra (Web Push API + mobile push se iOS/Android app existir). (4) Unusual-txn detection model (reuse unit 5 com diff sensitivity OR train específico pra recurring context). (5) Per-user paywall state tracker (gate quando N=3 successful atingido). (6) Churn survey UX (post-decline_paywall flow). **NENHUM existe hoje** — soma de unit 4 + unit 5 + extras específicos de retention/billing. Phase 5 unblock total: ~15 itens infra. | Metric thresholds (paywall conv ≥15% + push tap ≥15%) + 3× webhook (paywall + unusual_push + dismissed) + behavioral_self_report (churn reason). |

---

## TBD rows (parked)

Quando Phase 1 interview completar e units 3+ forem lockadas no SDD:

1. Adicionar row aqui por unit_hash.
2. Classificar: `ai_executable_at_scale` / `human_in_loop_required` / `blocked_by_missing_infra`.
3. Se ai_executable, documentar model_pattern (modelo + tool use pattern).
4. Se human_in_loop, documentar human_decision (o que exatamente o humano decide).
5. Se blocked, documentar missing_infra + unblock path.
6. **Sempre** re-surfacear validation_pattern do SDD — se não tem, unit é no máximo human_in_loop.

---

## Notes

**Step 1 collapsed (finding #2, 2026-04-25):** trigger event não é touchpoint observável. Removido do lockset. Trigger capture (`which_trigger` MCQ + discovery prompt) migra pra onboarding unit (parked, Phase 1 interview vai locar).

**Step 2 qualifica como ai_executable_at_scale:** validation é mensurável automaticamente (conversion rate + webhook events + behavioral gate). AI gera conteúdo (headlines) e participa da decisão (A/B selection). Humano entra no escalation path (se conversion cai OU off-ICP rate alta, halt).

**Step 3 qualifica como ai_executable_at_scale:** auto-responder send é determinístico (template selection por trigger); bot triagem AI roda em escala com escalation a humano em out-of-scope/low-confidence. Validation é metric_threshold (reply rate) + webhook events + human_checkpoint bot_escalation. Human entra no path de escalation (substância das replies escaladas, FAQ script reviews).

**Step 4 é `blocked_by_missing_infra`:** AI execution end-to-end é viável (Sonnet/Haiku faz conciliação, golden-output via rule-based diff é mensurável), MAS infra base não existe. Hoje BaseIA é só FastAPI sem app cliente — Step 4 requer (1) rule-based conciliação engine, (2) Receita Federal seed pipeline, (3) training corpus, (4) app back-office com login/dispute UX, (5) approval state DB. Phase 5 desbloqueio: build esses 5 itens. Sem isso, classification não pode subir pra ai_executable_at_scale, mesmo com validation_pattern presente. Princípio: missing_infra > validation_pattern na hierarquia de classificação.

**Step 5 também `blocked_by_missing_infra`:** depende dos 5 itens da unit 4 + 5 extras específicos (error-detection corpus, win-screen UI, per-client confidence threshold storage, review queue UX, trigger-tone copy templates). Layered validation (confidence gate + golden-output diff + human review primeiros 3 + behavioral self-report + metric_threshold + 2 webhooks) requer todos pra rodar sem supervisão. Princípio aplicado igual unit 4: missing_infra trava classificação.

**Step 6 também `blocked_by_missing_infra`:** retention/recurring loop depende de payment gateway + subscription DB + push notification infra + unusual-txn detection (reuse Step 5 com diff sensitivity) + paywall state tracker + churn survey UX. Soma cumulativa unit 4 + unit 5 + unit 6 = ~15 itens infra a build pra Phase 5 desbloqueio. Phase 1 está LOCKED em design (5 units lockadas + Step 1 collapsed); Phase 5 transforma design em implementação executable.

**Princípio derivado (não estava explícito no ULTRAPLAN):** a classificação é sobre **a capacidade do sistema de rodar o unit em escala sem supervisão constante**, não sobre o "grau de IA" envolvido. Unit pode ter AI heavy mas ser human_in_loop se o humano tem que aprovar cada execução.
