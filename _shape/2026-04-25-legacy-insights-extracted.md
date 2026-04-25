# Legacy Insights — Curated 2026-04-25

These insights são extraídos de docs legacy do produto v1/v2 (wedge "diagnóstico via vídeo + automações geradas por IA"), deprecated em favor do novo wedge: regularizar CNPJ + back-office conciliação para PME. Os princípios e guard-rails abaixo sobrevivem à mudança de produto porque tratam de meta-estratégia (founder time, validação, voz de marca, hipóteses abertas), não de mecânica do produto antigo. Detalhes específicos do funil-vídeo, telas, copy de paywall e personas (Carlos da distribuidora) foram descartados.

## Retention & Referral Patterns (Phase 2+)
*Source: produto/baseia-v2/00-discovery/jornada-cliente-sonho.md (Fases 7-9)*

Health check trimestral como gatilho de re-engajamento + upsell (re-diagnóstico detecta novos processos). Referral via WhatsApp deep-link com benefício mensal pro indicador (1 mês grátis), executado quando cliente já tem ≥60 dias e resultado tangível medido. Marco de resultado ("X horas economizadas") como nudge celebratório, não cobrança.

## Tela Justifies Existence
*Source: produto/baseia-v2/00-discovery/jornada-v2-simplificada.md*

Princípio: cada tela DEVE justificar sua existência — se cliente não precisa dela pra avançar, ela não existe. Minimização de etapas é critério de design, não estética; consolidar fases em loadings inline quando possível.

## Goldilocks: Grátis vs Pago
*Source: produto/baseia-v2/SERVICE-BLUEPRINT-AS-IS-vs-SHOULD-BE.md (seção 1)*

Tensão central: grátis demais não converte (cliente tem tudo), grátis de menos quebra confiança (cliente foge). "Just right" = cliente vê valor CLARO e SENTE limitação que cria desejo pelo próximo nível. Analogia Spotify: o free funciona, mas a limitação (ads, sem offline) é palpável. Mistura grátis+paywall na MESMA tela vira armadilha — cliente sente que metade foi escondida, não que ganhou algo.

## Feasibility Test antes de Phase 1 Lock
*Source: produto/baseia-v2/00-discovery/review-findings-31mar2026.md (F1, F2)*

**F1 — Salto de fé não testado é red flag de Phase 1:** qualquer tese de produto que dependa de capacidade técnica não-prototipada (ex: "Opus gera output production-grade") DEVE rodar feasibility test antes de commit de roadmap. Pegar 1 caso real, medir intervenção humana necessária. Se "significativa" → arquitetura precisa human-in-the-loop, e Phase 1 muda.

**F2 — Timelines de migração otimistas:** estimativas curtas para migrar/refatorar sistemas vivos (5-8 dias) tipicamente ignoram edge cases, integration testing contra deps externas, regression E2E e cutover risk. Regra: auditar inputs/outputs/side-effects ANTES de estimar; estimar de verdade só depois. Aplica ao Phase 1 atual se tocar pipeline existente.

## Construir é Barato — Founder Time é o Custo Real
*Source: produto/baseia-v2/00-discovery/validacao-fases-31mar2026.md*

Lean Startup clássico (smoke tests, fake LPs) era resposta à era em que construir custava equipe + meses. Com IA como co-developer, o gargalo é tempo do founder, não código. Implicação: validar com produto real construído, não landing fake. Validação muda de pergunta — de "alguém quer isso?" para "conseguimos entregar com qualidade e economia?". MVP pode (e deve) entregar mais valor que smoke test.

## Managed Agents Hypothesis (open)
*Source: produto/visao/managed-agents-pivot.md*

Hipótese ativa 24-abr (mesma sessão do reset): substituir runtime in-house (`automation_compiler.py` + `automation_registry.py` + `automation_sandbox.py`, em desenvolvimento) por Managed Agents da Anthropic quando Phase 5 SDD tocar delivery runtime. Ainda não decidido — `automation_compiler.py` segue em dev. Útil ter no radar quando Phase 5 SDD escolher arquitetura de execução.

## Voice & Tone — Brand Guardrails
*Source: produto/UX-Copy-Funil-BaseIA.md ("Guia de Voz e Tom")*

- Persona: consultor sênior de operações que já atendeu centenas de empresas. Autoridade sem arrogância.
- **Números, não adjetivos.** Nunca vende — mostra.
- Português BR coloquial-profissional (você, não tu).
- Zero jargão tech: nunca "workflow", "pipeline", "IA generativa", "n8n", "RPA", "deploy", "stack".
- Substituir "automação" → "organizar com tecnologia"; "blueprint" → "plano de ação".
- Ancoragem SEMPRE em R$ e horas — nunca em features.
- Cada CTA responde "o que acontece quando eu clico?".
- Frases curtas. Máximo ~20 palavras na copy principal.

## Open Questions — Phase 4 SDD Delivery Runtime
*Source: validation/decisions.md (A1, B2)*

**A1 — Claude gera artefato de automação válido:** primeiro round (n8n JSON) passou sintaticamente, semântica 70% correta. Aplicabilidade ao novo wedge depende do artefato de delivery escolhido (n8n? código Python? config Managed Agent?). Re-testar quando Phase 4 escolher runtime.

**B2 — Multi-tenant isolation de credenciais:** runtime compartilhado expõe credenciais de clientes; aceitável até ~10 clientes com hardening, mas precisa migração pra secrets store dedicado antes de escala. Question aberto pra Phase 4 SDD: qual store, qual modelo de tenancy.

## Brand Tese Central
*Source: projetos/Captura_Processos_AI/CRITICA_MKT_ESTRATEGICA.md*

PMEs não querem IA — querem menos risco, menos dependência de pessoas, mais previsibilidade. Vender IA é vender o veículo errado; vender redução-de-risco-operacional é o frame correto.

## NOT extracted

- Telas, formulários, copy específica do funil-vídeo (entrada.html, processando.html, saida.html, blueprint.html, diagnostico.html).
- Persona "Carlos da distribuidora" e jornadas detalhadas Fases 1-6.
- Pricing R$50 one-shot, R$197/R$497 automação, planos Starter/Professional/Enterprise.
- ARS Score / Service Blueprint / Quick Win / "9 seções do plano de ação" — todos artefatos do produto deprecated.
- Calibração Sonnet (grátis) vs Opus (pago) específica do funil-vídeo.
- Tese central N4 ("BaseIA opera tudo / hospeda automações em infra própria") de validation/decisions.md.
- "3 erros de comunicação" do SERVICE-BLUEPRINT — específicos ao paywall do produto vídeo.
- Reescritas de headline/subheadline do CRITICA_MKT_ESTRATEGICA — copy do produto antigo.
- Pacotes R$500-15k do MODELO_NEGOCIO antigo, mencionados como "descontinuar" no managed-agents-pivot.
- Hipóteses C1-C3, D1-D3, E1-E3 do decisions.md (integrações Google/WhatsApp, delivery operacional, economia técnica) — todas ancoradas no wedge antigo.
