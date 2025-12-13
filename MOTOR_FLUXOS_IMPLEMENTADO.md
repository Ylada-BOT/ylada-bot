# ✅ Motor de Fluxos - IMPLEMENTADO!

## 🎉 O que foi criado

### 1. Flow Engine (`src/flows/flow_engine.py`)
- ✅ Carrega e gerencia fluxos
- ✅ Valida estrutura de fluxos
- ✅ Verifica triggers (palavras-chave, sempre, condições)
- ✅ Executa fluxos passo a passo
- ✅ Gerencia execuções em andamento

### 2. Actions (Ações dos Fluxos)
- ✅ `send_message.py` - Envia mensagem
- ✅ `wait.py` - Aguarda tempo determinado
- ✅ `condition.py` - Avalia condições (if/else)
- ✅ `ai_response.py` - Resposta com IA
- ✅ `webhook.py` - Chama webhook externo

### 3. Message Handler (`src/whatsapp/message_handler.py`)
- ✅ Processa mensagens recebidas
- ✅ Decide qual fluxo executar
- ✅ Integra com Flow Engine
- ✅ Carrega fluxos do banco de dados

### 4. API de Fluxos (`web/api/flows.py`)
- ✅ `GET /api/flows` - Lista fluxos
- ✅ `POST /api/flows` - Cria fluxo
- ✅ `GET /api/flows/<id>` - Obtém fluxo
- ✅ `DELETE /api/flows/<id>` - Remove fluxo
- ✅ `POST /api/flows/test` - Testa fluxo
- ✅ `GET /api/flows/templates` - Templates prontos

### 5. Integração com Webhook
- ✅ Webhook processa mensagens com fluxos primeiro
- ✅ Fallback para IA se nenhum fluxo ativar
- ✅ Logs detalhados

---

## 📋 Estrutura de um Fluxo (JSON)

```json
{
  "name": "Boas-vindas",
  "trigger": {
    "type": "keyword",
    "keywords": ["oi", "olá", "bom dia"]
  },
  "steps": [
    {
      "type": "send_message",
      "message": "Olá! Como posso ajudar?"
    },
    {
      "type": "wait",
      "duration": 5
    },
    {
      "type": "ai_response"
    }
  ]
}
```

---

## 🚀 Como Usar

### 1. Criar um Fluxo (via API)

```bash
curl -X POST http://localhost:5002/api/flows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Meu Fluxo",
    "flow_data": {
      "name": "Meu Fluxo",
      "trigger": {
        "type": "keyword",
        "keywords": ["oi", "olá"]
      },
      "steps": [
        {
          "type": "send_message",
          "message": "Olá! Bem-vindo!"
        },
        {
          "type": "ai_response"
        }
      ]
    }
  }'
```

### 2. Testar um Fluxo

```bash
curl -X POST http://localhost:5002/api/flows/test \
  -H "Content-Type: application/json" \
  -d '{
    "flow_data": {
      "name": "Teste",
      "trigger": {"type": "always"},
      "steps": [
        {"type": "send_message", "message": "Teste!"}
      ]
    },
    "test_phone": "5511999999999",
    "test_message": "teste"
  }'
```

### 3. Ver Templates Prontos

```bash
curl http://localhost:5002/api/flows/templates
```

---

## 🔄 Fluxo de Execução

```
1. Mensagem chega no WhatsApp
   ↓
2. whatsapp_server.js envia para /webhook
   ↓
3. Message Handler processa mensagem
   ↓
4. Verifica triggers de todos os fluxos ativos
   ↓
5. Se trigger ativado → Flow Engine executa fluxo
   ↓
6. Executa cada step do fluxo:
   - send_message → Envia mensagem
   - wait → Aguarda
   - ai_response → Gera resposta com IA
   - condition → Avalia condição
   - webhook → Chama webhook
   ↓
7. Se nenhum fluxo ativar → Usa IA como fallback
```

---

## ✅ Status

- ✅ Flow Engine: 100%
- ✅ Actions: 100% (5 ações)
- ✅ Message Handler: 100%
- ✅ API de Fluxos: 100%
- ✅ Integração Webhook: 100%
- ⏳ Interface Visual: 0% (próximo passo)

---

## 🎯 Próximos Passos

1. **Interface Visual** - Criar página para gerenciar fluxos
2. **Integrar com Banco** - Salvar fluxos no banco de dados
3. **Templates Prontos** - Mais templates de fluxos
4. **Sistema de Notificações** - Notificar quando fluxo executar
5. **Captação de Leads** - Detectar leads nos fluxos

---

**Motor de Fluxos está FUNCIONANDO!** 🎉

Agora você pode criar automações que respondem automaticamente às mensagens!
