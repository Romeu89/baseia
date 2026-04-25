# System Design Document — BaseIA

**Status:** Partial lock. Units pros steps 1 e 2 preenchidos. Steps 3+ parked aguardando Phase 1 interview completion.
**Source (Phase 2 table):** [`CUSTOMER_JOURNEY.md`](CUSTOMER_JOURNEY.md)
**Drift checker:** [`_tools/hash_units.py`](_tools/hash_units.py)
**Hash formula:** `sha256(phase_id + "|" + customer_action + "|" + io_signature + "|" + "|".join(sorted(decision_buttons)))`

---

## Schema (reference)

Cada unit tem todos os campos abaixo. `validation_pattern` é MANDATORY (nunca blank) per ULTRAPLAN Phase 4 constraint.

```
- phase_id: <string — Step number from Phase 2>
  customer_action: <from Phase 2 row>
  io_signature: <canonical "IN: ... | OUT: ...">
  decision_buttons: <sorted list of button identifiers>
  unit_hash: <sha256 hex>
  responsibility: <one sentence — what this unit is accountable for>
  interface: <input/output contract detail>
  ai_role: <none | assist | execute | autonomous>
  validation_pattern: <how we test this step; from Phase 2 validation_pattern column>
  escalation_rule: <when human takes over>
  dependencies: [<phase_id or unit_hash of prerequisite units>]
```

---

## Units (locked)

- phase_id: "1"
  customer_action: "Solo founder experiencia 1+ dos 4 gatilhos (a/b/c/d)"
  io_signature: "IN: Evento real no mundo (perda de FTE financeiro / erro de conciliação / teto MEI / FOMO competitivo) | OUT: Estado interno mudado: \"preciso resolver sem contratar CLT\""
  decision_buttons: ["which_trigger"]
  unit_hash: "d6c59fb5c0e02d4d2ad0aa5f06e5f04b7b3aaefa991fe800661c58ec92770f5b"
  responsibility: "Detectar intenção emergente de resolver back-office sem contratar CLT, originada em um dos 4 gatilhos canônicos."
  interface: "Input = evento externo (não observável pelo sistema BaseIA). Output = trigger self-report capturado no primeiro touchpoint downstream (step 2 submission)."
  ai_role: "none"
  validation_pattern: "Behavioral self-report em onboarding questionnaire. Metric threshold: >60% self-select um dos 4 triggers canônicos. Se 'other' ≥40%, persona missing triggers — human revisa."
  escalation_rule: "Self-report 'other' ≥40% sustentado 2 semanas → human (Romeu) revisa persona definition antes de continuar."
  dependencies: []

- phase_id: "2"
  customer_action: "Solo founder encontra wedge \"Regularizar CNPJ grátis\" e clica pro landing"
  io_signature: "IN: Search intent OR referral link OR anúncio paid OR founder content | OUT: User na wedge landing page com intent explícita de regularizar CNPJ"
  decision_buttons: ["learn_more", "start_regularization", "talk_to_human"]
  unit_hash: "af58f450d1761704b37b2fafb05fd42776ccb81ed600a739b72b66336d50a8bc"
  responsibility: "Capturar intenção explícita de regularizar CNPJ via landing page do wedge, com self-report do trigger e variant da headline."
  interface: "Input = sessão de user com intent discovery-stage. Output = record no DB com {email, CNPJ, trigger_self_report, headline_variant, timestamp}, evento webhook downstream."
  ai_role: "assist"
  validation_pattern: "(1) Metric threshold: landing→submit conversion ≥X% (X a calibrar; define Phase 5 go/no-go). (2) Webhook callback (n8n-style) no submit captura trigger+variant. (3) Golden-output A/B das 3 headlines, tie-breaker = retention D7."
  escalation_rule: "Conversion sustentada <X% por 2 semanas → halt paid acquisition; rotate creative; Romeu aprova nova variant."
  dependencies: ["1"]

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
