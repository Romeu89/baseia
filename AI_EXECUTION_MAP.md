# AI Execution Map — BaseIA

**Status:** Partial. Rows for units 2 e 3 (locked via SDD). Step 1 collapsed em finding #2 (não é unit, é hypothesis context). Steps 4+ aguardando Phase 1 interview completion.
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
| `05a2ae6e...30819745` (phase 2) | `ai_executable_at_scale` | Haiku 4.5 gera variants de headline por trigger (a/b/c/d). Sonnet 4.6 opcional pra refinamento. A/B orchestration via feature-flag infra (ex: PostHog, GrowthBook, ou home-grown). Conversion tracking via webhook n8n-style. Gate `is_existing_cnpj` = static branch (não AI). | Romeu aprova primeira batch de variants antes de dispatch; daí AI roda sozinha. Decisão de aceitar/rejeitar opt-in waitlist é static UX. | Feature-flag/experiment infra; analytics webhook; landing page CMS com slot de headline dinâmica; opt-in waitlist DB. | Metric threshold (conversion ≥8% @ 500sess) + behavioral gate `is_existing_cnpj` + webhook submit + webhook waitlist_optin + golden-output A/B D7. |
| `c5e3a6b4...fa8723cc` (phase 3) | `ai_executable_at_scale` | Haiku 4.5 (low-latency) bot triagem em n8n: classifica reply do user em FAQ category vs out-of-scope; resposta auto pra FAQ, escalation pra Romeu/contador em out-of-scope. Sonnet 4.6 opcional em edge case com confidence ambígua. Email send via Resend (static template selection por `trigger_self_report`). | Romeu/contador respondem replies escalados (out-of-scope OU bot confidence baixo). Romeu aprova FAQ scripts iniciais + revisões periódicas. | n8n bot infra com confidence-score + scope-check; inbox unificada bot+humano (single thread per user); FAQ KB editável; reply webhook. | Metric threshold (reply rate ≥10% @ 500submits) + webhook email_send + webhook reply_received + human_checkpoint bot_escalation_to_romeu. |

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

**Princípio derivado (não estava explícito no ULTRAPLAN):** a classificação é sobre **a capacidade do sistema de rodar o unit em escala sem supervisão constante**, não sobre o "grau de IA" envolvido. Unit pode ter AI heavy mas ser human_in_loop se o humano tem que aprovar cada execução.
