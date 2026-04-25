# CashFlow Conciliador - Deploy em Produção

> **Data**: 29/01/2026
> **Status**: Pronto para produção
> **Autor**: Loop Noturno #4

---

## Checklist de Deploy

### 1. Banco de Dados (Supabase - Recomendado)

```bash
# 1. Criar projeto em supabase.com
# 2. Copiar Connection String de Settings > Database
# 3. Executar schema no SQL Editor
```

**Connection String formato:**
```
postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
```

### 2. Credenciais n8n

| Credencial | Tipo | Obrigatório |
|------------|------|-------------|
| Postgres CashFlow | PostgreSQL | ✅ Sim |
| OpenAI API | OpenAI | ❌ Opcional |
| SMTP Gmail | SMTP | ❌ Opcional |

### 3. Variáveis de Ambiente

```env
# Modo Produção
DEMO_MODE=false
DEFAULT_CLIENT_ID=<uuid-cliente>

# IA (opcional mas recomendado)
ENABLE_AI_CLASSIFICATION=true
OPENAI_API_KEY=sk-...

# Anomalias
ANOMALY_HIGH_EXPENSE=10000

# Notificações
SEND_NOTIFICATIONS=true
NOTIFICATION_EMAIL=financeiro@cliente.com
```

### 4. Importar Workflow

1. n8n > Workflows > Import from File
2. Selecionar `n8n-workflow/cashflow-conciliador.json`
3. Configurar credenciais em cada nó "DB:"
4. Salvar e Ativar

### 5. Testar

```bash
# Teste em modo demo primeiro
curl -X POST "https://seu-n8n/webhook/cashflow/ingest" \
  -H "X-Client-Id: 11111111-1111-1111-1111-111111111111" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

---

## Onboarding de Cliente (5 minutos)

```sql
-- 1. Criar cliente
INSERT INTO clients (name, document, email)
VALUES ('Nome da Empresa', '00000000000000', 'email@empresa.com')
RETURNING id;

-- 2. Criar conta bancária
INSERT INTO bank_accounts (client_id, bank_code, bank_name, agency, account_number, nickname)
VALUES ('<UUID_CLIENTE>', '001', 'Banco do Brasil', '1234', '56789-0', 'Conta Principal')
RETURNING id;

-- 3. Criar regras de classificação
INSERT INTO classification_rules (client_id, priority, name, match_description, match_direction, category_id)
SELECT
  '<UUID_CLIENTE>',
  10,
  'Tarifas Bancárias',
  '%TARIFA%',
  'out',
  id
FROM categories WHERE code = 'DFI002';
```

---

## Webhook - Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/webhook/cashflow/ingest` | POST | Upload de extrato OFX/CSV |

**Headers:**
- `X-Client-Id`: UUID do cliente (obrigatório)
- `X-Bank-Account-Id`: UUID da conta (opcional)
- `Content-Type`: `application/octet-stream` (OFX) ou `text/csv`

---

## Custos Estimados

| Item | Custo/mês |
|------|-----------|
| Supabase Pro | $25 |
| n8n Cloud Starter | $20 |
| OpenAI (500 transações) | ~$5 |
| **Total** | **~$50/mês** |

**Break-even**: 1 cliente no plano Professional (R$ 297/mês)

---

## Métricas de Sucesso

- Taxa de classificação automática > 80%
- Taxa de conciliação > 70%
- Tempo de processamento < 30s para 100 transações
- Zero falhas críticas em 7 dias

---

*Gerado automaticamente - Loop Noturno #4*
