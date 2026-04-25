# 🚀 EXECUTAR AGORA - CashFlow Conciliador

## Passo 1: Abra o Terminal

No seu Mac, abra o **Terminal** (Cmd + Space, digite "Terminal")

## Passo 2: Navegue até a pasta

```bash
cd ~/cashflow-conciliador
```

## Passo 3: Inicie os containers

```bash
docker compose up -d
```

Aguarde uns 30-60 segundos para os containers iniciarem.

## Passo 4: Verifique se está rodando

```bash
docker compose ps
```

Você deve ver 2 containers rodando:
- `cashflow-postgres` (healthy)
- `cashflow-n8n` (healthy)

## Passo 5: Acesse o n8n

Abra no navegador: **http://localhost:5678**

## Passo 6: Importe o workflow

1. No n8n, clique em **Workflows** no menu lateral
2. Clique em **Import from File**
3. Selecione o arquivo: `~/cashflow-conciliador/n8n-workflow/cashflow-conciliador.json`

## Passo 7: Configure a credencial Postgres

1. Vá em **Settings** (engrenagem) > **Credentials**
2. Clique em **Add Credential**
3. Selecione **Postgres**
4. Preencha:
   - **Name**: `Postgres CashFlow`
   - **Host**: `postgres`
   - **Port**: `5432`
   - **Database**: `cashflow`
   - **User**: `cashflow`
   - **Password**: `cashflow123`
5. Clique **Save**

## Passo 8: Associe a credencial ao workflow

1. Volte ao workflow importado
2. Clique em cada node que diz "DB:" (são vários)
3. Em cada um, selecione a credencial `Postgres CashFlow`

## Passo 9: Execute em modo demo!

1. Clique no botão **Execute Workflow** (play)
2. Observe os dados fluindo pelos nodes
3. O modo demo gera ~15 transações fictícias automaticamente

## Passo 10: Verifique os dados no banco

```bash
docker exec -it cashflow-postgres psql -U cashflow -d cashflow -c "SELECT COUNT(*) as total, direction FROM transactions GROUP BY direction;"
```

---

## 📋 Comandos Úteis

```bash
# Ver logs
docker compose logs -f

# Parar tudo
docker compose down

# Reiniciar
docker compose restart

# Ver dados no banco
docker exec -it cashflow-postgres psql -U cashflow -d cashflow

# Query de exemplo
docker exec -it cashflow-postgres psql -U cashflow -d cashflow -c "SELECT date, description, amount, direction FROM transactions ORDER BY date DESC LIMIT 10;"
```

---

## ⚠️ Problemas Comuns

### "Port 5432 already in use"
Outro Postgres está rodando. Mude a porta no docker-compose.yml:
```yaml
ports:
  - "5433:5432"  # Use 5433 ao invés de 5432
```

### "Cannot connect to Docker"
Verifique se o Docker Desktop está rodando.

### Workflow não executa
Verifique se todas as credenciais Postgres estão configuradas em todos os nodes "DB:".

---

🎉 **Pronto! Seu robô financeiro está funcionando!**
