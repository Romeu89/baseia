# n8n Patterns — BaseIA

Regras obrigatórias ao criar ou editar workflows n8n da BaseIA.

## Infraestrutura

| Serviço | URL |
|---------|-----|
| Editor | `https://n8n.baseia.cloud` |
| Webhooks | `https://webhook.baseia.cloud/webhook/{path}` |
| MCP Server | `https://n8n.baseia.cloud/mcp-server/http` |
| API | `https://n8n.baseia.cloud/api/v1` |

**NUNCA** usar `n8n.baseia.cloud/webhook/` — falhará. Queue mode roteia webhooks para container separado.

## Traquejos Obrigatórios

| Traquejo | Regra |
|----------|-------|
| JSON dinâmico em HTTP Request | SEMPRE usar `JSON.stringify()` ao redor de objetos dinâmicos |
| Expression mode | Campo JSON DEVE estar em modo Expression (não Fixed) para `{{ }}` serem avaliados |
| Acessar resposta OpenAI | `$json.choices[0].message.content` — NUNCA colocar aspas ao redor de variáveis dentro de `JSON.stringify()` |
| fetch() em Code Nodes | PROIBIDO — usar `this.helpers.httpRequest()` |
| Multi-output em Code Node v2 | PROIBIDO `return [[...], [...]]` — usar Router + IF Node |
| Timeout Opus | HTTP Request default 120s insuficiente — usar 600s para chamadas Opus |
| Backticks aninhados | PROIBIDO em Code Nodes — usar concatenação de string |
| Renomear nós | Atualizar TODAS as referências de connection source keys e targets |

## API — Campos Proibidos no PUT

Remover antes de PUT em `/api/v1/workflows/{id}`:
`id`, `active`, `createdAt`, `updatedAt`, `tags`, `versionId`, `shared`, `meta`, `usedCredentials`

O campo `active` é READ-ONLY. Para ativar/desativar usar:
- `POST /api/v1/workflows/{id}/activate`
- `POST /api/v1/workflows/{id}/deactivate`

## Após Deploy via API

Webhook retorna 404? Executar na ordem:
1. Toggle deactivate → activate via API
2. Se persistir: salvar o workflow na UI (Ctrl+S)
3. Alternativa: redeploy do stack no Portainer com `Prune:true`

## Credenciais

Credenciais completas em `projects/BaseIA_Projetos/00_Memoria/MEMORIA_TECNICA.md`.
IDs de credentials (para referenciar em JSON):
- Anthropic: `K784AEQKuaGopUJk`
- Resend: `3zy3hlsLDEKxSUok`
