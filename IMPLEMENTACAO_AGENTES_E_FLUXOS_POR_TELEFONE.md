# ✅ Implementação: Sistema de Agentes e Fluxos por Telefone

## 📋 RESUMO

Implementação completa do sistema de múltiplos telefones com agentes de IA e fluxos específicos por telefone.

**Data:** 2024-12-23

---

## 🎯 O QUE FOI IMPLEMENTADO

### 1. ✅ Sistema de Agentes (Agents)

**Arquivos criados/modificados:**
- `src/models/agent.py` - Model de Agent
- `web/api/agents.py` - API completa para gerenciar agentes (CRUD)
- `web/app.py` - Registro do blueprint de agentes

**Funcionalidades:**
- ✅ Criação de agentes com configuração de IA personalizada
- ✅ Agentes podem ser específicos de uma instance ou padrão da organização
- ✅ Suporte para diferentes providers (OpenAI, Anthropic)
- ✅ Configuração de system prompt, temperatura, max_tokens
- ✅ API REST completa: GET, POST, PUT, DELETE
- ✅ Endpoint especial: `/api/agents/by-instance/<id>` para buscar agente de uma instance

### 2. ✅ Fluxos por Telefone (Instance)

**Arquivos modificados:**
- `src/models/flow.py` - Adicionado campo `instance_id` (opcional)
- `src/flows/flow_engine.py` - Atualizado `get_active_flows()` para filtrar por `instance_id`
- `src/whatsapp/message_handler.py` - Atualizado para filtrar fluxos por instance
- `web/api/flows.py` - API atualizada para suportar `instance_id`

**Funcionalidades:**
- ✅ Fluxos podem ser específicos de uma instance (`instance_id` = X)
- ✅ Fluxos podem ser compartilhados (`instance_id` = NULL)
- ✅ MessageHandler filtra automaticamente:
  - Fluxos específicos da instance
  - Fluxos compartilhados do tenant
- ✅ API de flows suporta criar/atualizar fluxos com `instance_id`

### 3. ✅ Associação Instance ↔ Agent

**Arquivos modificados:**
- `src/models/instance.py` - Adicionado campo `agent_id`
- `web/api/instances.py` - API atualizada para suportar `agent_id`

**Funcionalidades:**
- ✅ Cada instance pode ter um agente configurado
- ✅ Se não tiver agente, usa agente padrão do tenant
- ✅ API de instances suporta criar/atualizar com `agent_id`

### 4. ✅ Integração com AIHandler

**Arquivos modificados:**
- `src/ai_handler.py` - Atualizado para usar agentes configurados
- `src/actions/ai_response.py` - Atualizado para passar `tenant_id` e `instance_id`

**Funcionalidades:**
- ✅ AIHandler busca agente da instance ou agente padrão do tenant
- ✅ Usa configuração do agente (provider, model, system_prompt, etc)
- ✅ Mantém histórico separado por instance
- ✅ Fallback para configuração global se agente não encontrado

### 5. ✅ Webhook Atualizado

**Arquivos modificados:**
- `web/app.py` - Webhook atualizado para identificar instance

**Funcionalidades:**
- ✅ Identifica `instance_id` através da conversa
- ✅ Passa `instance_id` e `tenant_id` para MessageHandler e AIHandler
- ✅ Fluxos e agentes são aplicados corretamente por telefone

### 6. ✅ Script de Migração SQL

**Arquivo criado:**
- `scripts/migration_add_agents_and_instance_flows.sql`

**Conteúdo:**
- ✅ Criação da tabela `agents`
- ✅ Adição de coluna `instance_id` em `flows`
- ✅ Adição de coluna `agent_id` em `instances`
- ✅ Índices para performance
- ✅ Comentários de documentação

---

## 📊 ESTRUTURA DE DADOS

### Tabela `agents`
```sql
- id (PK)
- tenant_id (FK)
- instance_id (FK, nullable) - NULL = agente padrão da org
- name
- description
- provider (openai, anthropic)
- model (gpt-4o-mini, claude-3-haiku, etc)
- system_prompt
- temperature
- max_tokens
- behavior_config (JSON)
- is_default (boolean)
- is_active (boolean)
- created_at, updated_at
```

### Tabela `flows` (atualizada)
```sql
- instance_id (FK, nullable) - NULL = compartilhado, valor = específico
```

### Tabela `instances` (atualizada)
```sql
- agent_id (FK, nullable) - Agente configurado para esta instance
```

---

## 🔄 FLUXO DE PROCESSAMENTO

```
1. Mensagem chega no WhatsApp
   ↓
2. Webhook identifica instance_id (via conversa ou parâmetro)
   ↓
3. MessageHandler busca fluxos:
   - Fluxos específicos da instance (instance_id = X)
   - Fluxos compartilhados (instance_id = NULL) do tenant
   ↓
4. Se trigger ativado → Executa fluxo
   ↓
5. Se fluxo tem "ai_response" → Usa agente da instance
   ↓
6. Se nenhum fluxo → Usa agente da instance como fallback
```

---

## 📡 ENDPOINTS DA API

### Agentes
- `GET /api/agents` - Lista agentes
- `GET /api/agents/<id>` - Obtém agente
- `POST /api/agents` - Cria agente
- `PUT /api/agents/<id>` - Atualiza agente
- `DELETE /api/agents/<id>` - Remove agente
- `GET /api/agents/by-instance/<id>` - Obtém agente de uma instance

### Fluxos (atualizado)
- `POST /api/flows` - Agora aceita `instance_id` (opcional)
- `GET /api/flows` - Retorna `instance_id` na resposta

### Instances (atualizado)
- `POST /api/instances` - Agora aceita `agent_id` (opcional)
- `PUT /api/instances/<id>` - Agora aceita `agent_id` (opcional)
- `GET /api/instances` - Retorna `agent_id` na resposta

---

## 🚀 COMO USAR

### 1. Executar Migração SQL

```bash
# Conecte ao banco e execute:
psql -U seu_usuario -d seu_banco -f scripts/migration_add_agents_and_instance_flows.sql
```

### 2. Criar um Agente

```bash
curl -X POST http://localhost:5002/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "name": "Agente Vendas",
    "provider": "openai",
    "model": "gpt-4o-mini",
    "system_prompt": "Você é um vendedor amigável...",
    "temperature": 0.7,
    "is_default": true
  }'
```

### 3. Associar Agente a uma Instance

```bash
curl -X PUT http://localhost:5002/api/instances/1 \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": 1
  }'
```

### 4. Criar Fluxo Específico de uma Instance

```bash
curl -X POST http://localhost:5002/api/flows \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "instance_id": 1,
    "flow_data": {
      "name": "Boas-vindas Vendas",
      "trigger": {
        "type": "keyword",
        "keywords": ["oi", "olá"]
      },
      "steps": [
        {
          "type": "send_message",
          "message": "Olá! Bem-vindo à nossa loja!"
        }
      ]
    }
  }'
```

### 5. Criar Fluxo Compartilhado

```bash
curl -X POST http://localhost:5002/api/flows \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "instance_id": null,
    "flow_data": {
      "name": "Promoção Black Friday",
      "trigger": {
        "type": "keyword",
        "keywords": ["promoção", "black friday"]
      },
      "steps": [
        {
          "type": "send_message",
          "message": "Confira nossas promoções!"
        }
      ]
    }
  }'
```

---

## ✅ TESTES REALIZADOS

- ✅ Model Agent criado e importado corretamente
- ✅ API de agentes registrada no app
- ✅ Relacionamentos SQLAlchemy configurados
- ✅ MessageHandler filtra fluxos por instance_id
- ✅ AIHandler busca e usa agentes configurados
- ✅ Webhook identifica instance_id automaticamente
- ✅ Sem erros de lint

---

## 📝 PRÓXIMOS PASSOS (Opcional)

1. **Interface Web:**
   - Criar interface para gerenciar agentes
   - Interface para associar fluxos a telefones
   - Interface para configurar agente por telefone

2. **Melhorias:**
   - Adicionar campo `api_key` no Agent (atualmente usa global)
   - Suporte para múltiplos agentes por instance (escolha dinâmica)
   - Templates de agentes pré-configurados

3. **Documentação:**
   - Atualizar documentação da API
   - Criar guia de uso para usuários

---

## 🎉 CONCLUSÃO

Todas as funcionalidades foram implementadas com sucesso:

✅ Sistema de agentes completo
✅ Fluxos por telefone (instance)
✅ Associação instance ↔ agent
✅ Integração com AIHandler
✅ Webhook atualizado
✅ Script de migração SQL

O sistema agora suporta múltiplos telefones, cada um com seus próprios fluxos e agentes configurados!

---

**Última atualização:** 2024-12-23


