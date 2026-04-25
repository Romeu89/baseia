# 📘 Guia de Implementação - CashFlow Conciliador

## (C) GUIA COMPLETO DE DEPLOY E CONFIGURAÇÃO

---

## 1. VARIÁVEIS DE AMBIENTE

Configure as seguintes variáveis no n8n (Settings > Variables ou via `.env`):

```bash
# ========================================
# BANCO DE DADOS
# ========================================
DATABASE_URL=postgresql://user:password@host:5432/cashflow
# Ou use variáveis separadas:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cashflow
DB_USER=cashflow_user
DB_PASSWORD=sua_senha_segura

# ========================================
# MODO DE OPERAÇÃO
# ========================================
DEMO_MODE=true                    # true = usar dados mock, false = produção
DEMO_CLIENT_ID=11111111-1111-1111-1111-111111111111
DEMO_BANK_ACCOUNT_ID=22222222-2222-2222-2222-222222222222

# ========================================
# CLIENTE PADRÃO (quando não informado via header)
# ========================================
DEFAULT_CLIENT_ID=               # UUID do cliente padrão

# ========================================
# CLASSIFICAÇÃO IA (opcional)
# ========================================
ENABLE_AI_CLASSIFICATION=false   # true para ativar OpenAI
OPENAI_API_KEY=sk-...           # Sua API key da OpenAI

# ========================================
# DETECÇÃO DE ANOMALIAS
# ========================================
ANOMALY_HIGH_EXPENSE=10000      # Alertar despesas acima deste valor

# ========================================
# NOTIFICAÇÕES
# ========================================
SEND_NOTIFICATIONS=false        # true para enviar emails
NOTIFICATION_EMAIL=financeiro@empresa.com

# ========================================
# SMTP (para envio de emails)
# ========================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=app_password      # Use app password do Gmail
```

---

## 2. CONFIGURAÇÃO DO BANCO DE DADOS

### Opção A: Supabase (Recomendado para começar)

1. Crie conta em https://supabase.com
2. Crie um novo projeto
3. Vá em **Settings > Database** e copie a Connection String
4. Execute o schema:
   - Vá em **SQL Editor**
   - Cole todo o conteúdo de `database/schema.sql`
   - Clique em **Run**

### Opção B: Postgres Local/Docker

```bash
# Docker
docker run -d \
  --name cashflow-db \
  -e POSTGRES_USER=cashflow \
  -e POSTGRES_PASSWORD=cashflow123 \
  -e POSTGRES_DB=cashflow \
  -p 5432:5432 \
  postgres:15

# Executar schema
psql -h localhost -U cashflow -d cashflow -f database/schema.sql
```

---

## 3. IMPORTAR WORKFLOW NO N8N

### Passo a Passo:

1. Abra seu n8n (self-hosted ou cloud)
2. Vá em **Workflows** > **Import from File**
3. Selecione `n8n-workflow/cashflow-conciliador.json`
4. O workflow será importado com todos os nodes

### Configurar Credenciais:

1. **Postgres:**
   - Settings > Credentials > Add Credential > Postgres
   - Nome: `Postgres CashFlow`
   - Preencha host, database, user, password
   - Copie o ID da credencial e substitua `POSTGRES_CREDENTIAL_ID` no workflow

2. **OpenAI (opcional):**
   - Settings > Credentials > Add Credential > OpenAI
   - Nome: `OpenAI API`
   - Cole sua API Key
   - Substitua `OPENAI_CREDENTIAL_ID` no workflow

3. **SMTP (para emails):**
   - Settings > Credentials > Add Credential > SMTP
   - Configure seu servidor SMTP
   - Substitua `SMTP_CREDENTIAL_ID` no workflow

---

## 4. MODO DEMO (Testar sem dados reais)

1. Configure `DEMO_MODE=true` nas variáveis
2. Execute o workflow manualmente (botão Execute)
3. O sistema irá:
   - Gerar 15-25 transações fictícias dos últimos 7 dias
   - Classificar automaticamente usando regras
   - Gerar relatório
4. Verifique no banco: `SELECT * FROM transactions LIMIT 10;`

---

## 5. MODO PRODUÇÃO

### 5.1 Via Webhook (Upload de Extrato)

```bash
# Endpoint
POST https://seu-n8n.com/webhook/cashflow/ingest

# Headers obrigatórios
X-Client-Id: uuid-do-cliente
X-Bank-Account-Id: uuid-da-conta (opcional)
Content-Type: application/octet-stream (OFX) ou text/csv (CSV)

# Exemplo com curl - OFX
curl -X POST \
  -H "X-Client-Id: 11111111-1111-1111-1111-111111111111" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @extrato.ofx \
  https://seu-n8n.com/webhook/cashflow/ingest

# Exemplo com curl - CSV
curl -X POST \
  -H "X-Client-Id: 11111111-1111-1111-1111-111111111111" \
  -H "Content-Type: text/csv" \
  --data-binary @extrato.csv \
  https://seu-n8n.com/webhook/cashflow/ingest
```

### 5.2 Formato CSV Esperado

```csv
data;descricao;valor;tipo
01/01/2024;PIX RECEBIDO - CLIENTE ABC;5800.00;C
01/01/2024;PAGTO BOLETO ENERGIA;-1234.56;D
02/01/2024;TED RECEBIDO NF 1234;12500.00;C
```

Colunas aceitas:
- **data/date/dt**: Data da transação (DD/MM/YYYY ou YYYY-MM-DD)
- **descricao/historico/memo**: Descrição da transação
- **valor/amount/vlr**: Valor (positivo ou negativo)
- **tipo/type/d/c**: Opcional (C/D ou in/out)

### 5.3 Via Cron (Automático)

O workflow está configurado para rodar a cada 6 horas. Para usar com arquivo:
1. Configure um node adicional para buscar o extrato (IMAP, Google Drive, etc.)
2. Conecte antes do node "Demo ou Produção?"

---

## 6. CADASTRAR CLIENTE E CONTAS

```sql
-- Criar cliente
INSERT INTO clients (name, document, email) VALUES
('Empresa ABC Ltda', '12345678000199', 'financeiro@empresaabc.com')
RETURNING id;

-- Criar conta bancária
INSERT INTO bank_accounts (client_id, bank_code, bank_name, agency, account_number, nickname) VALUES
('uuid-do-cliente', '341', 'Itaú', '1234', '12345-6', 'Conta Principal')
RETURNING id;
```

---

## 7. CRIAR REGRAS DE CLASSIFICAÇÃO PERSONALIZADAS

```sql
-- Exemplo: Regra para fornecedor específico
INSERT INTO classification_rules (
  client_id, priority, name,
  match_description, match_direction,
  category_id, cost_center
) VALUES (
  'uuid-do-cliente',
  5,  -- Prioridade alta (menor número = maior prioridade)
  'Fornecedor ABC - Material',
  '%FORNECEDOR ABC%',  -- Pattern ILIKE
  'out',
  (SELECT id FROM categories WHERE code = 'DOP009'), -- Serviços de Terceiros
  'operacional'
);

-- Regra por valor
INSERT INTO classification_rules (
  client_id, priority, name,
  match_amount_min, match_amount_max, match_direction,
  category_id
) VALUES (
  'uuid-do-cliente',
  50,
  'Pequenas despesas < R$100',
  0, 100, 'out',
  (SELECT id FROM categories WHERE code = 'DOP008')  -- Material de escritório
);
```

---

## 8. CHECKLIST DE ONBOARDING (30 minutos)

### Para cada novo cliente:

- [ ] **5 min** - Criar registro em `clients`
- [ ] **5 min** - Criar conta(s) em `bank_accounts`
- [ ] **10 min** - Criar 5-10 regras de classificação específicas
- [ ] **5 min** - Testar com extrato de amostra
- [ ] **5 min** - Configurar email de notificação

### Script de onboarding rápido:

```sql
-- Execute tudo de uma vez
DO $$
DECLARE
  v_client_id UUID;
  v_account_id UUID;
BEGIN
  -- Criar cliente
  INSERT INTO clients (name, document, email)
  VALUES ('NOME_EMPRESA', 'CNPJ', 'EMAIL')
  RETURNING id INTO v_client_id;

  -- Criar conta
  INSERT INTO bank_accounts (client_id, bank_code, bank_name, agency, account_number)
  VALUES (v_client_id, 'COD_BANCO', 'NOME_BANCO', 'AGENCIA', 'CONTA')
  RETURNING id INTO v_account_id;

  -- Output
  RAISE NOTICE 'Cliente criado: %', v_client_id;
  RAISE NOTICE 'Conta criada: %', v_account_id;
END $$;
```

---

## 9. SUGESTÃO DE PRECIFICAÇÃO (MRR)

### Modelo de Pricing Recomendado:

| Plano | Transações/mês | Contas | IA | Preço |
|-------|----------------|--------|-----|-------|
| **Starter** | até 100 | 1 | ❌ | R$ 97/mês |
| **Professional** | até 500 | 3 | ✅ | R$ 297/mês |
| **Business** | até 2.000 | 10 | ✅ | R$ 597/mês |
| **Enterprise** | ilimitado | ilimitado | ✅ | Sob consulta |

### Custos Operacionais Estimados:

- **Supabase Free**: até 500MB (suficiente para ~50 clientes pequenos)
- **Supabase Pro**: $25/mês (500 clientes)
- **OpenAI**: ~$0.01 por 10 transações classificadas
- **n8n Cloud**: $20-50/mês (ou self-hosted)

### ROI para o Cliente:

- Economia de tempo: 4-6h/semana × R$50/hora = R$800-1200/mês
- Redução de erros: Inestimável
- Visibilidade: Tomada de decisão melhor

---

## 10. QUERIES ÚTEIS PARA MONITORAMENTO

```sql
-- Resumo de execuções
SELECT
  DATE(started_at) as data,
  COUNT(*) as execucoes,
  SUM(records_created) as transacoes_criadas,
  AVG(duration_ms)::int as tempo_medio_ms
FROM automation_runs
WHERE started_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(started_at)
ORDER BY data DESC;

-- Transações pendentes de revisão
SELECT
  c.name as cliente,
  COUNT(*) as pendentes,
  SUM(t.amount) as valor_total
FROM transactions t
JOIN clients c ON t.client_id = c.id
WHERE t.needs_review = true
GROUP BY c.name
ORDER BY pendentes DESC;

-- Acurácia de classificação
SELECT
  classification_method,
  COUNT(*) as total,
  AVG(classification_confidence) as confianca_media
FROM transactions
WHERE classification_method IS NOT NULL
GROUP BY classification_method;

-- Alertas ativos por cliente
SELECT
  c.name as cliente,
  a.alert_type,
  a.severity,
  COUNT(*) as total
FROM alerts a
JOIN clients c ON a.client_id = c.id
WHERE a.status = 'active'
GROUP BY c.name, a.alert_type, a.severity
ORDER BY c.name, a.severity DESC;
```

---

## 11. TROUBLESHOOTING

### Erro: "client_id não informado"
- Verifique se o header `X-Client-Id` está sendo enviado
- Ou configure `DEFAULT_CLIENT_ID` nas variáveis

### Erro: "Nenhuma transação encontrada"
- Verifique o formato do arquivo (OFX ou CSV)
- Para CSV, certifique-se que tem as colunas obrigatórias

### Transações duplicadas
- O sistema usa hash de idempotência
- Verificar: `SELECT hash_idempotency, COUNT(*) FROM transactions GROUP BY 1 HAVING COUNT(*) > 1`

### Classificação não funcionando
- Verificar se existem regras: `SELECT * FROM classification_rules WHERE is_active = true`
- Testar pattern: `SELECT 'PAGTO CPFL' ILIKE '%CPFL%'` → deve retornar true

### Webhook não responde
- Verificar se o workflow está ativo
- Verificar logs do n8n
- Testar com curl simples primeiro

---

## 12. PRÓXIMOS PASSOS (ROADMAP)

### V1.1 - Integração Bancária
- [ ] API Open Banking (Pluggy, Belvo)
- [ ] Sincronização automática de extratos

### V1.2 - Dashboards
- [ ] Metabase/Superset templates
- [ ] Relatórios PDF automatizados

### V1.3 - Integrações
- [ ] WhatsApp Business API para alertas
- [ ] Slack/Discord webhooks
- [ ] Integração com ERPs (Omie, Bling, Tiny)

---

## Suporte

Para dúvidas ou sugestões:
- Criar issue no repositório
- Email: suporte@seudominio.com

---

**Versão:** 1.0.0
**Última atualização:** Janeiro 2025
**Compatível com:** n8n 1.0+, Postgres 13+
