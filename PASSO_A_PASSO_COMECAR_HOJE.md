# 🚀 PASSO A PASSO: COMEÇAR A USAR O BOTTI HOJE

**Data:** 2025-01-27  
**Objetivo:** Colocar o Botti em funcionamento hoje mesmo

---

## ✅ O QUE JÁ ESTÁ PRONTO (Você Pode Usar Agora!)

### 1. Integração WhatsApp ✅
- ✅ Servidor Node.js funcionando
- ✅ QR Code para conectar
- ✅ Envio e recebimento de mensagens
- ✅ Listagem de conversas

### 2. Inteligência Artificial ✅
- ✅ Integração OpenAI (GPT-4o-mini, etc)
- ✅ Integração Anthropic (Claude)
- ✅ System Prompt configurável
- ✅ Histórico de conversas
- ✅ Respostas automáticas com contexto

### 3. Sistema de Fluxos ✅
- ✅ Motor de fluxos funcionando
- ✅ Triggers (palavras-chave, sempre)
- ✅ Ações: Enviar mensagem, Aguardar, Condições, IA, Webhook
- ✅ API completa de fluxos

### 4. Captação de Leads ✅
- ✅ Captura automática de leads
- ✅ Scoring de leads
- ✅ Extração de dados (nome, email, telefone)
- ✅ Histórico de leads

### 5. Notificações ✅
- ✅ Notificações para outro WhatsApp
- ✅ Notificações de fluxos e leads

### 6. Dashboard ✅
- ✅ Interface web completa
- ✅ Métricas básicas
- ✅ Gerenciamento de fluxos
- ✅ Visualização de conversas e leads

---

## ⚠️ O QUE FALTA PARA USAR HOJE (30 minutos)

### 1. Templates de Fluxos Prontos ⚠️ **CRÍTICO - 15 min**

**Problema:** Você precisa criar fluxos do zero via JSON, o que é difícil.

**Solução:** Criar 3-5 templates prontos que você pode ativar com 1 clique.

**O que fazer:**
- [ ] Criar template "Boas-vindas"
- [ ] Criar template "Atendimento Básico"
- [ ] Criar template "Captação de Lead"
- [ ] Adicionar botão "Usar Template" na interface

---

## 🎯 PASSO A PASSO PARA COMEÇAR AGORA

### PASSO 1: Verificar Dependências (2 minutos)

```bash
# Verificar se Node.js está instalado
node --version

# Verificar se Python está instalado
python3 --version

# Instalar dependências Python (se necessário)
pip3 install --user flask flask-cors python-dotenv sqlalchemy psycopg2-binary openai anthropic

# Instalar dependências Node.js (se necessário)
npm install whatsapp-web.js qrcode-terminal express axios
```

---

### PASSO 2: Configurar Variáveis de Ambiente (3 minutos)

Crie ou edite o arquivo `.env` na raiz do projeto:

```bash
# Banco de dados (Supabase)
DATABASE_URL=postgresql://usuario:senha@host:porta/database

# Autenticação
SECRET_KEY=sua-chave-secreta-aqui
AUTH_REQUIRED=true

# IA (escolha uma)
AI_PROVIDER=openai  # ou anthropic
AI_API_KEY=sua-api-key-aqui
AI_MODEL=gpt-4o-mini  # ou claude-3-haiku

# WhatsApp
WHATSAPP_PORT=5001
FLASK_PORT=5002

# Auto-resposta (opcional)
AUTO_RESPOND=true
```

---

### PASSO 3: Iniciar Servidores (2 minutos)

**Terminal 1 - Servidor WhatsApp:**
```bash
cd "/Users/air/Ylada BOT"
node whatsapp_server.js
```

**Terminal 2 - Servidor Flask:**
```bash
cd "/Users/air/Ylada BOT"
source venv/bin/activate  # Se usar venv
python3 web/app.py
```

**Verificar se estão rodando:**
```bash
# WhatsApp (porta 5001)
curl http://localhost:5001/health

# Flask (porta 5002)
curl http://localhost:5002/health
```

---

### PASSO 4: Conectar WhatsApp (5 minutos)

1. **Acesse:** `http://localhost:5002/qr`
2. **Escaneie o QR Code** com seu WhatsApp
3. **Aguarde conexão** (pode levar 10-30 segundos)
4. **Verifique status:** `http://localhost:5002/api/whatsapp-status`

**Se o QR Code não aparecer:**
- Aguarde 5-10 segundos e recarregue a página (F5)
- Verifique se o servidor Node.js está rodando
- Verifique os logs: `tail -f whatsapp_server.log`

---

### PASSO 5: Configurar IA (3 minutos)

1. **Acesse:** `http://localhost:5002/dashboard`
2. **Vá em "Configurações de IA"**
3. **Configure:**
   - Provider: OpenAI ou Anthropic
   - API Key: Sua chave da API
   - Model: gpt-4o-mini ou claude-3-haiku
   - System Prompt: Personalize conforme necessário
4. **Salve**

**Testar IA:**
- Use o chat de teste no dashboard
- Envie uma mensagem de teste
- Verifique se a resposta está correta

---

### PASSO 6: Criar Primeiro Fluxo (10 minutos)

**Opção A: Via Interface (Recomendado)**

1. **Acesse:** `http://localhost:5002/tenant/flows`
2. **Clique em "Novo Fluxo"**
3. **Preencha:**
   - Nome: "Boas-vindas"
   - Descrição: "Responde automaticamente a cumprimentos"
   - Trigger: Palavras-chave: "oi", "olá", "bom dia"
   - Steps:
     - Step 1: Enviar mensagem: "Olá! Como posso ajudar?"
4. **Salve e ative**

**Opção B: Via API (Se interface não funcionar)**

```bash
curl -X POST http://localhost:5002/api/flows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Boas-vindas",
    "description": "Responde automaticamente a cumprimentos",
    "trigger_keywords": ["oi", "olá", "bom dia"],
    "flow_data": {
      "trigger": {
        "type": "keyword",
        "keywords": ["oi", "olá", "bom dia"]
      },
      "steps": [
        {
          "type": "send_message",
          "message": "Olá! Como posso ajudar?"
        }
      ]
    },
    "status": "active"
  }'
```

---

### PASSO 7: Testar o Bot (5 minutos)

1. **Envie uma mensagem** para o WhatsApp conectado
2. **Verifique se o fluxo foi executado:**
   - Acesse: `http://localhost:5002/tenant/conversations`
   - Veja a conversa e as mensagens
3. **Verifique se o lead foi capturado:**
   - Acesse: `http://localhost:5002/tenant/leads`
   - Veja se o lead aparece na lista

---

## 🎯 TEMPLATES PRONTOS PARA CRIAR AGORA

### Template 1: Boas-vindas

```json
{
  "name": "Boas-vindas",
  "description": "Responde automaticamente a cumprimentos",
  "trigger": {
    "type": "keyword",
    "keywords": ["oi", "olá", "bom dia", "boa tarde", "boa noite"]
  },
  "steps": [
    {
      "type": "send_message",
      "message": "Olá! 👋 Bem-vindo! Como posso ajudar você hoje?"
    }
  ]
}
```

### Template 2: Atendimento Básico

```json
{
  "name": "Atendimento Básico",
  "description": "Responde perguntas comuns usando IA",
  "trigger": {
    "type": "always"
  },
  "steps": [
    {
      "type": "ai_response",
      "message": "Analisando sua mensagem..."
    }
  ]
}
```

### Template 3: Captação de Lead

```json
{
  "name": "Captação de Lead",
  "description": "Captura leads quando detecta interesse",
  "trigger": {
    "type": "keyword",
    "keywords": ["quero", "interessado", "preço", "valor", "quanto custa"]
  },
  "steps": [
    {
      "type": "send_message",
      "message": "Ótimo! Vou te ajudar. Pode me passar seu nome e email?"
    },
    {
      "type": "wait",
      "duration": 5
    },
    {
      "type": "ai_response",
      "message": "Processando suas informações..."
    }
  ]
}
```

---

## 📋 CHECKLIST FINAL

### Para Conectar WhatsApp:
- [ ] Servidor Node.js rodando (`node whatsapp_server.js`)
- [ ] Servidor Flask rodando (`python3 web/app.py`)
- [ ] QR Code escaneado
- [ ] WhatsApp conectado (verificar status)

### Para Configurar IA:
- [ ] API Key configurada
- [ ] Provider selecionado (OpenAI ou Anthropic)
- [ ] System Prompt configurado
- [ ] IA testada (chat de teste)

### Para Criar Fluxos:
- [ ] Pelo menos 1 fluxo criado
- [ ] Fluxo ativado
- [ ] Fluxo testado (enviar mensagem)

### Para Captar Leads:
- [ ] Lead capturado após teste
- [ ] Lead visível na interface
- [ ] Notificação funcionando (se configurada)

---

## 🚨 PROBLEMAS COMUNS E SOLUÇÕES

### Problema 1: QR Code não aparece
**Solução:**
- Aguarde 5-10 segundos e recarregue (F5)
- Verifique se servidor Node.js está rodando
- Verifique logs: `tail -f whatsapp_server.log`

### Problema 2: Erro ao conectar WhatsApp
**Solução:**
- Feche todas as sessões do WhatsApp Web no celular
- Tente conectar novamente
- Limpe a sessão: `rm -rf data/sessions/*`

### Problema 3: IA não responde
**Solução:**
- Verifique se API Key está correta
- Verifique se `AUTO_RESPOND=true` no `.env`
- Teste no chat de teste do dashboard
- Verifique logs: `tail -f /tmp/flask.log`

### Problema 4: Fluxo não executa
**Solução:**
- Verifique se fluxo está ativo
- Verifique se trigger está correto
- Verifique logs: `tail -f /tmp/flask.log`
- Teste com palavra-chave exata

### Problema 5: Erro de banco de dados
**Solução:**
- Verifique `DATABASE_URL` no `.env`
- Verifique se Supabase está acessível
- Verifique se tabelas foram criadas
- Execute migrações se necessário

---

## 🎯 PRÓXIMOS PASSOS (Após Funcionar)

### Esta Semana:
1. ✅ Criar mais 2-3 fluxos personalizados
2. ✅ Configurar notificações para seu WhatsApp
3. ✅ Testar captação de leads
4. ✅ Personalizar System Prompt

### Próxima Semana:
1. ⚠️ Implementar envio de mídia
2. ⚠️ Criar mais templates de fluxos
3. ⚠️ Melhorar interface de fluxos
4. ⚠️ Adicionar status de entrega

---

## 💡 DICAS IMPORTANTES

1. **Sempre teste antes de ativar** - Use o chat de teste
2. **Monitore os logs** - Ajuda a identificar problemas
3. **Comece simples** - Fluxos básicos primeiro
4. **Personalize o System Prompt** - Faz toda diferença
5. **Use templates** - Economiza tempo

---

## 📞 SUPORTE

Se encontrar problemas:
1. Verifique os logs
2. Consulte a documentação
3. Teste passo a passo
4. Verifique configurações

---

**Última atualização:** 2025-01-27  
**Status:** ✅ Pronto para usar (após criar templates)

