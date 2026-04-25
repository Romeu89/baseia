# 🤖 CashFlow Conciliador

**Robô de Conciliação Bancária Automática para PMEs Brasileiras**

[![n8n](https://img.shields.io/badge/n8n-workflow-orange)](https://n8n.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)](https://postgresql.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🎯 O que é?

O **CashFlow Conciliador** é um robô de automação financeira que processa extratos bancários, classifica transações automaticamente, concilia com contas a pagar/receber, detecta anomalias e gera relatórios — tudo sem intervenção manual.

### Principais Funcionalidades

- ✅ **Ingestão de Extratos**: OFX, CSV ou API
- ✅ **Classificação Automática**: Regras + IA (OpenAI opcional)
- ✅ **Conciliação Inteligente**: Match com A/P e A/R
- ✅ **Detecção de Anomalias**: Alertas em tempo real
- ✅ **Relatórios Automáticos**: Email diário/semanal
- ✅ **Multi-tenant**: Um sistema, múltiplos clientes
- ✅ **Idempotência**: Processa o mesmo arquivo N vezes sem duplicar

---

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CASHFLOW CONCILIADOR                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [Extrato]      [Parser]       [Classificar]     [Conciliar]          │
│   OFX/CSV   →   Normalizar  →   Regras + IA   →   Match A/P-A/R        │
│      │              │                │                  │               │
│      │              ↓                ↓                  ↓               │
│      │         [Dedupe]        [Categorias]      [Links]              │
│      │         Hash único      Plano contas      Score match           │
│      │              │                │                  │               │
│      │              └────────────────┴──────────────────┘               │
│      │                              │                                   │
│      │                              ↓                                   │
│      │                       [Persistir]                               │
│      │                       PostgreSQL                                │
│      │                              │                                   │
│      │              ┌───────────────┼───────────────┐                  │
│      │              ↓               ↓               ↓                  │
│      │         [Anomalias]    [Alertas]      [Relatório]              │
│      │         Detecção       Gerar           Sumário                  │
│      │              │               │               │                  │
│      │              └───────────────┼───────────────┘                  │
│      │                              ↓                                   │
│      │                        [Notificar]                              │
│      │                        Email/WhatsApp                           │
│      │                                                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/cashflow-conciliador.git
cd cashflow-conciliador
```

### 2. Configure o banco de dados
```bash
# Com Docker
docker run -d --name cashflow-db \
  -e POSTGRES_USER=cashflow \
  -e POSTGRES_PASSWORD=cashflow123 \
  -e POSTGRES_DB=cashflow \
  -p 5432:5432 postgres:15

# Aplicar schema
./scripts/setup-database.sh
```

### 3. Importe o workflow no n8n
1. Abra seu n8n
2. Workflows > Import from File
3. Selecione `n8n-workflow/cashflow-conciliador.json`
4. Configure as credenciais (Postgres, SMTP, OpenAI)

### 4. Teste em modo demo
```bash
# Configure variáveis
export DEMO_MODE=true

# Execute o workflow manualmente no n8n
```

### 5. Teste em produção
```bash
./scripts/test-webhook.sh
```

---

## 📁 Estrutura do Projeto

```
cashflow-conciliador/
├── README.md                    # Este arquivo
├── GUIA-IMPLEMENTACAO.md        # Guia detalhado de deploy
├── database/
│   └── schema.sql               # DDL completo do PostgreSQL
├── n8n-workflow/
│   └── cashflow-conciliador.json # Workflow exportável
├── exemplos/
│   ├── extrato-exemplo.csv      # Exemplo de CSV
│   └── extrato-exemplo.ofx      # Exemplo de OFX
└── scripts/
    ├── setup-database.sh        # Setup do banco
    └── test-webhook.sh          # Teste do webhook
```

---

## 📋 Pré-requisitos

- **n8n** 1.0+ (self-hosted ou cloud)
- **PostgreSQL** 13+ (ou Supabase)
- **OpenAI API** (opcional, para classificação IA)

---

## 🔧 Configuração

Veja o arquivo [GUIA-IMPLEMENTACAO.md](GUIA-IMPLEMENTACAO.md) para:

- Variáveis de ambiente
- Configuração de credenciais
- Onboarding de clientes
- Criação de regras personalizadas
- Troubleshooting

---

## 💰 Modelo de Negócio Sugerido

| Plano | Transações/mês | Preço Sugerido |
|-------|----------------|----------------|
| Starter | até 100 | R$ 97/mês |
| Professional | até 500 | R$ 297/mês |
| Business | até 2.000 | R$ 597/mês |

**ROI para o cliente**: 4-6h/semana economizadas = R$ 800-1.200/mês

---

## 📈 Métricas de Sucesso

- **Tempo economizado**: 4-6h/semana → 30min/semana
- **Acurácia de classificação**: >90% após 30 dias
- **Taxa de conciliação automática**: >70%

---

## 🛣️ Roadmap

- [ ] V1.1: Integração Open Banking (Pluggy, Belvo)
- [ ] V1.2: Dashboards Metabase/Superset
- [ ] V1.3: WhatsApp Business API
- [ ] V1.4: Integração ERPs (Omie, Bling, Tiny)

---

## 📝 Licença

MIT License - veja [LICENSE](LICENSE)

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

**Desenvolvido com 🤖 para PMEs brasileiras**
