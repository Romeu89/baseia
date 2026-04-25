# System Design Document — BaseIA

**Status:** Partial lock. Unit pro step 2 preenchido. Step 1 collapsed em finding #2 (validation circularity — trigger capture migra pra onboarding unit parked). Steps 3+ parked aguardando Phase 1 interview completion.
**Source (Phase 2 table):** [`CUSTOMER_JOURNEY.md`](CUSTOMER_JOURNEY.md)
**Drift checker:** [`_tools/hash_units.py`](_tools/hash_units.py)
**Hash formula (bumped 2026-04-25 finding #7):** `sha256(phase_id + "|" + customer_action + "|" + io_signature + "|" + "|".join(sorted(decision_buttons)) + "|" + validation_signature)` where `validation_signature` is the canonical structured form from journey table col 9 (semicolon-joined `pattern_type:args` segments, sorted alphabetically).

---

## Schema (reference)

Cada unit tem todos os campos abaixo. `validation_pattern` é MANDATORY (nunca blank) per ULTRAPLAN Phase 4 constraint.

```
- phase_id: <string — Step number from Phase 2>
  customer_action: <from Phase 2 row>
  io_signature: <canonical "IN: ... | OUT: ...">
  decision_buttons: <sorted list of button identifiers>
  validation_signature: <canonical structured form, semicolon-joined pattern_type:args, sorted; from Phase 2 col 9>
  unit_hash: <sha256 hex; includes validation_signature per finding #7 bump>
  responsibility: <one sentence — what this unit is accountable for>
  interface: <input/output contract detail>
  ai_role: <none | assist | execute | autonomous>
  validation_pattern: <prose human-readable; from Phase 2 col 8 — NOT hashed, prose-only>
  escalation_rule: <when human takes over>
  dependencies: [<phase_id or unit_hash of prerequisite units>]
```

---

## Units (locked)

> **Step 1 collapsed (finding #2, 2026-04-25):** trigger event não é touchpoint observável (mental state pre-discovery). Validation circularity rejeitada. Trigger capture (`which_trigger` MCQ + discovery prompt for 'other' do finding #3) migra pra onboarding unit — currently parked, será locked durante Phase 1 interview (Phase C do session prompt). Comm matrix por trigger (a/b/c/d/other) permanece em CUSTOMER_JOURNEY.md como contexto de hypothesis pra headlines.

- phase_id: "2"
  customer_action: "Solo founder encontra wedge \"Regularizar CNPJ grátis\" e clica pro landing"
  io_signature: "IN: Search intent OR referral link OR anúncio paid OR founder content | OUT: User na wedge landing page com intent explícita de regularizar CNPJ"
  decision_buttons: ["back_office_optin", "is_existing_cnpj", "learn_more", "start_regularization", "talk_to_human", "waitlist_optin"]
  validation_signature: "behavioral_self_report:cnpj_state_gate;golden_output:headline_ab_retention_d7;metric_threshold:landing_to_submit_conversion>=0.08@500sess;webhook_callback:back_office_optin_capture;webhook_callback:submit_event_capture;webhook_callback:waitlist_optin_event"
  unit_hash: "7fd213d80d2f777ced1fd41a71b8c0bfaef773fa2b4a042d014d126f74fbcbde"
  responsibility: "Capturar intenção explícita de regularizar CNPJ via landing page do wedge, com gate de ICP (CNPJ existente sim/não), self-report do trigger e variant da headline."
  interface: "Input = sessão de user com intent discovery-stage. Output (path-yes) = record no DB com {email, CNPJ, trigger_self_report, headline_variant, timestamp}, evento webhook downstream. Output (path-no) = educational page + opt-in opcional → record {email, intent='open_cnpj', cohort='waitlist'} pra nurture longo."
  ai_role: "assist"
  validation_pattern: "(1) Metric threshold: landing→submit conversion ≥8% calibrado em janela de 500 sessões (anchor: B2B SaaS self-serve high-intent band 4-10%, Unbounce + daydream 2025 — mid-band conservador; researcher confidence medium, no BR-fintech-wedge benchmark). Revisit triggers: >15% (raise X — set too low) ou <4% (kill creative/wedge — below floor). (2) Behavioral gate `is_existing_cnpj` antes de CTA: yes → flow regularizar; no → redirect educational (link externo Sebrae/parceiro) + opt-in waitlist (não default). (3) Webhook callback (n8n-style) no submit captura trigger+variant. (4) Webhook separado captura waitlist_optin (cohort off-ICP). (5) Golden-output A/B das 3 headlines, tie-breaker = retention D7."
  escalation_rule: "(1) Conversion <8% após 500 sessões completas → halt paid acquisition; rotate creative; Romeu aprova nova variant. (2) Se `is_existing_cnpj`=no representar ≥30% das sessões sustentado, sinaliza canal misalign (atraindo pre-revenue não-ICP) — Romeu revisa headlines/keywords."
  dependencies: []

- phase_id: "3"
  customer_action: "Solo founder recebe email auto-responder com next steps da regularização (D0); pode clicar status link ou responder pra tiered handler"
  io_signature: "IN: Submission record da unit 2 — {email, CNPJ, trigger_self_report, headline_variant, timestamp} | OUT: Auto-responder email enviado D0 + tiered reply handler ativo (bot triagem + escalation Romeu/contador)"
  decision_buttons: ["click_status_link", "reply_email"]
  validation_signature: "human_checkpoint:bot_escalation_to_romeu;metric_threshold:auto_responder_reply_rate>=0.10@500submits;webhook_callback:email_send_event;webhook_callback:reply_received_event"
  unit_hash: "c5e3a6b48d96132dad01dc966a76bbf277828dc5212f4c7d85fc34e2fa8723cc"
  responsibility: "Estabelecer primeiro contato pós-submit via email transactional + provisionar canal de reply tiered (bot+humano) pra dúvidas, sem founder load."
  interface: "Input = unit 2 submission record. Output (immediate D0) = email enviado via Resend com template trigger-specific. Output (post-D0, eventual) = reply do user roteado pra bot triagem (n8n+Anthropic); confidence/scope check; escalation pra Romeu/contador inbox quando bot insuficiente."
  ai_role: "assist"
  validation_pattern: "(1) Metric threshold: auto-responder reply rate ≥10% medido sobre janela de 500 submits (= 500 emails enviados D0). Threshold preliminary; revisitar após 1ª medição real (sem benchmark BR-fintech específico, US B2B SaaS auto-responder reply ~5-15% wild). (2) Webhook callback (n8n-style) no email_send (D0) captura template+trigger. (3) Webhook callback no reply_received captura conteúdo + roteamento pro bot. (4) Human checkpoint: bot escala pra Romeu/contador quando confidence baixo ou scope out-of-FAQ."
  escalation_rule: "(1) Reply rate <10% em 500 submits → halt envio + revisar copy do auto-responder; Romeu aprova nova variant. (2) Bot escalation rate >50% sustentado → FAQ coverage gap; Romeu/contador expandem scripts do bot. (3) Confidence baixo no bot triagem → escalation imediata (single user)."
  dependencies: ["2"]

- phase_id: "4"
  customer_action: "Solo founder (back_office_optin=true) loga 1ª vez no BaseIA back-office: vê Receita Federal data pre-populada, sistema auto-roda 1ª conciliação como demo de valor, pede approval pra default future auto-runs"
  io_signature: "IN: User com back_office_optin=true da unit 2 + regularização completed evento (Receita Federal data disponível) | OUT: Onboarded user com 1ª conciliação AI auto-rodada exibida + approval status pra future runs (default_auto_runs: yes/no)"
  decision_buttons: ["approve_auto_runs", "dispute_first_run", "keep_manual_runs"]
  validation_signature: "golden_output:first_conciliacao_ai_vs_rulebased_accuracy>=0.95;human_checkpoint:dispute_first_run_review;metric_threshold:first_login_completion_rate>=0.70@500optins;webhook_callback:first_login_event;webhook_callback:first_run_completed_event"
  unit_hash: "e27d0a7da94bee131bf74d6a82c5419c46162b508d2c3db318e1443bfa347290"
  responsibility: "Onboardar user opt-in via wedge cross-sell em BaseIA back-office: provisioning automático com Receita Federal seed, AI executa 1ª conciliação como demo de valor (com golden-output validation pre-display), captura preferência de approval pra future runs."
  interface: "Input = user record com back_office_optin=true + regularization_completed event payload (CNPJ, razão social, CNAE, endereço da Receita Federal). Output = app account ativo + 1ª conciliação AI output (validated vs rule-based) exibida + user choice persistida em DB (approve_auto_runs | keep_manual_runs | dispute_first_run)."
  ai_role: "execute"
  validation_pattern: "(1) Golden-output: 1ª conciliação AI output comparada a baseline rule-based deterministic; accuracy ≥95% antes de display ao user (D0 trust-protection — falsa primeira conciliação mata a relação). (2) Metric threshold: first-login completion rate ≥70% medido em 500 opt-ins (preliminary, calibrar pós-launch — sem benchmark BR specific). (3) Webhook callback: first_login_event captura entrada; first_run_completed_event captura output + user choice. (4) Human checkpoint: dispute_first_run flow envia AI output pra Romeu/contador review queue (humano resolve disputa)."
  escalation_rule: "(1) Golden-output accuracy <95% no batch → halt auto-run pra futuros opt-ins; route todos pra Romeu/contador manual ate fix; rebuild AI conciliador com mais training data. (2) First-login completion rate <70% em 500 opt-ins → revisar onboarding UX + email subject line de provisioning. (3) Dispute rate >10% por user (lifetime) → user → review queue + 1:1 contact (likely persona mismatch). (4) Sustained dispute trend cross-users → halt execute, downgrade ai_role pra assist (require user click pra rodar)."
  dependencies: ["2", "3"]

---

## TBD units (parked)

Steps 3+ do Phase 2 table estão marcados TBD aguardando Phase 1 interview interativo. Quando interview completar:

1. Adicionar rows correspondentes no Phase 2 table de CUSTOMER_JOURNEY.md.
2. Rodar `python _tools/hash_units.py` — deve listar units faltantes no SDD.
3. Adicionar blocks YAML aqui, um por step, seguindo o schema.
4. Rodar drift check de novo — deve exit 0.

**Unidades pendentes (placeholders):**

*(Steps 5+ a levantar no interview.)*

---

## AI role vocabulary

Per ULTRAPLAN Phase 5 constraint:

| Role | Significado |
|------|-------------|
| `none` | Humano 100%, nenhum componente AI envolvido. |
| `assist` | AI auxilia humano (copilot-style, rascunhos, sugestões). Humano decide. |
| `execute` | AI executa a unit end-to-end **com validation_pattern rodando**. Humano revisa via validation output. |
| `autonomous` | AI executa sem intervenção humana direta. **Só qualificável se validation_pattern é mensurável 100% automaticamente.** |

**Rule (ULTRAPLAN Phase 5):** unit sem `validation_pattern` não pode ser `execute` nem `autonomous`. No máximo `assist`.
