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
  decision_buttons: ["is_existing_cnpj", "learn_more", "start_regularization", "talk_to_human", "waitlist_optin"]
  validation_signature: "behavioral_self_report:cnpj_state_gate;golden_output:headline_ab_retention_d7;metric_threshold:landing_to_submit_conversion>=0.08@500sess;webhook_callback:submit_event_capture;webhook_callback:waitlist_optin_event"
  unit_hash: "05a2ae6e84eba81c3dff8109aa3fbf88349b07f6cb6dfc2a821f356730819745"
  responsibility: "Capturar intenção explícita de regularizar CNPJ via landing page do wedge, com gate de ICP (CNPJ existente sim/não), self-report do trigger e variant da headline."
  interface: "Input = sessão de user com intent discovery-stage. Output (path-yes) = record no DB com {email, CNPJ, trigger_self_report, headline_variant, timestamp}, evento webhook downstream. Output (path-no) = educational page + opt-in opcional → record {email, intent='open_cnpj', cohort='waitlist'} pra nurture longo."
  ai_role: "assist"
  validation_pattern: "(1) Metric threshold: landing→submit conversion ≥8% calibrado em janela de 500 sessões (anchor: B2B SaaS self-serve high-intent band 4-10%, Unbounce + daydream 2025 — mid-band conservador; researcher confidence medium, no BR-fintech-wedge benchmark). Revisit triggers: >15% (raise X — set too low) ou <4% (kill creative/wedge — below floor). (2) Behavioral gate `is_existing_cnpj` antes de CTA: yes → flow regularizar; no → redirect educational (link externo Sebrae/parceiro) + opt-in waitlist (não default). (3) Webhook callback (n8n-style) no submit captura trigger+variant. (4) Webhook separado captura waitlist_optin (cohort off-ICP). (5) Golden-output A/B das 3 headlines, tie-breaker = retention D7."
  escalation_rule: "(1) Conversion <8% após 500 sessões completas → halt paid acquisition; rotate creative; Romeu aprova nova variant. (2) Se `is_existing_cnpj`=no representar ≥30% das sessões sustentado, sinaliza canal misalign (atraindo pre-revenue não-ICP) — Romeu revisa headlines/keywords."
  dependencies: []

---

## TBD units (parked)

Steps 3+ do Phase 2 table estão marcados TBD aguardando Phase 1 interview interativo. Quando interview completar:

1. Adicionar rows correspondentes no Phase 2 table de CUSTOMER_JOURNEY.md.
2. Rodar `python _tools/hash_units.py` — deve listar units faltantes no SDD.
3. Adicionar blocks YAML aqui, um por step, seguindo o schema.
4. Rodar drift check de novo — deve exit 0.

**Unidades pendentes (placeholders):**

- phase_id: "3"
  customer_action: TBD — Phase 1 interview incomplete
  unit_hash: TBD
  validation_pattern: TBD

- phase_id: "4"
  customer_action: TBD
  unit_hash: TBD
  validation_pattern: TBD

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
