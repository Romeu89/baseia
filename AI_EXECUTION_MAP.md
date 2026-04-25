# AI Execution Map — BaseIA

**Status:** Partial. Rows for units 1 e 2 (locked via SDD). Steps 3+ aguardando Phase 1 interview completion.
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
| `d6c59fb5...92770f5b` (phase 1) | `human_in_loop_required` | — | User auto-identifica trigger via questionnaire pós-signup. Sem AI de classificação — self-report direto. | — | Behavioral self-report; threshold >60% self-select um dos 4 triggers canônicos. |
| `af58f450...36d50a8bc` (phase 2) | `ai_executable_at_scale` | Haiku 4.5 gera variants de headline por trigger (a/b/c/d). Sonnet 4.6 opcional pra refinamento. A/B orchestration via feature-flag infra (ex: PostHog, GrowthBook, ou home-grown). Conversion tracking via webhook n8n-style. | Romeu aprova primeira batch de variants antes de dispatch; daí AI roda sozinha. | Feature-flag/experiment infra; analytics webhook; landing page CMS com slot de headline dinâmica. | Metric threshold (conversion ≥X%) + webhook callback + A/B golden-output D7 retention. |

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

**Step 1 é human_in_loop mesmo tendo validation_pattern:** validation existe (self-report questionnaire) mas o evento original (trigger real-world) não é observável pelo sistema. AI não substitui o humano dizendo "isso foi o que me trouxe aqui". AI só roda o questionnaire.

**Step 2 qualifica como ai_executable_at_scale:** validation é mensurável automaticamente (conversion rate + webhook events). AI gera conteúdo (headlines) e participa da decisão (A/B selection). Humano entra no escalation path (se conversion cai, halt).

**Princípio derivado (não estava explícito no ULTRAPLAN):** a classificação é sobre **a capacidade do sistema de rodar o unit em escala sem supervisão constante**, não sobre o "grau de IA" envolvido. Unit pode ter AI heavy mas ser human_in_loop se o humano tem que aprovar cada execução.
