# 🚀 Como Usar o BOT Agora

**Data:** 2025-01-27  
**Status:** ✅ Servidores Rodando

---

## ✅ STATUS ATUAL

### **Servidor Flask** ✅
- ✅ Rodando na porta 5002
- ✅ Dashboard acessível: http://localhost:5002
- ✅ Ambiente virtual configurado

### **Servidor WhatsApp** ✅
- ✅ Rodando na porta 5001
- ⏳ Aguardando QR Code ser gerado

---

## 📱 PASSO 1: Conectar WhatsApp

### **1.1 Acessar Página de QR Code**
- URL: http://localhost:5002/qr
- Ou clique em "📱 Conectar WhatsApp" no dashboard

### **1.2 Aguardar QR Code**
- O QR Code pode levar 10-30 segundos para aparecer
- A página atualiza automaticamente a cada 3 segundos
- Aguarde até ver o QR Code na tela

### **1.3 Escanear QR Code**
1. Abra WhatsApp no seu celular
2. Vá em: **Configurações** > **Aparelhos conectados**
3. Toque em: **"Conectar um aparelho"**
4. Escaneie o QR Code que aparece na tela
5. Aguarde a confirmação de conexão

### **1.4 Verificar Conexão**
- O dashboard deve mostrar "✅ Conectado" em verde
- Ou acesse: http://localhost:5002/api/whatsapp-status

---

## 🔄 PASSO 2: Criar Fluxo de Atendimento

### **2.1 Acessar Fluxos**
- URL: http://localhost:5002/tenant/flows
- Ou clique em "🔄 Fluxos" no menu lateral

### **2.2 Usar Template Pronto (Recomendado)**
1. Clique em "📋 Templates"
2. Escolha um template:
   - **Boas-vindas** - Responde a "oi", "olá", etc
   - **Atendimento com IA** - Responde todas as mensagens com IA
   - **Informações de Produto** - Responde sobre produtos
3. Clique em "Usar Template"
4. O fluxo será criado automaticamente

### **2.3 Criar Fluxo Manual**
1. Clique em "➕ Novo Fluxo"
2. Preencha:
   - **Nome:** Ex: "Atendimento Básico"
   - **Trigger:** Escolha como ativar (palavras-chave, sempre, etc)
   - **Steps:** Adicione ações (enviar mensagem, IA, etc)
3. Clique em "Salvar"
4. Ative o fluxo

### **2.4 Ativar Fluxo**
- Na lista de fluxos, clique em "Ativar"
- Ou edite o fluxo e mude status para "Ativo"

---

## 🧪 PASSO 3: Testar

### **3.1 Enviar Mensagem de Teste**
1. Envie uma mensagem do seu celular para o número conectado
2. Exemplo: "oi" ou "olá"

### **3.2 Verificar Resposta**
- O bot deve responder automaticamente
- Se usar template "Boas-vindas", deve responder: "Olá! 👋 Bem-vindo! Como posso ajudar você hoje?"

### **3.3 Verificar Logs**
- No terminal do Flask, você verá logs das mensagens
- No terminal do WhatsApp server, você verá logs de envio

---

## 📋 ESTRUTURA DE UM FLUXO BÁSICO

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
      "duration": 3
    },
    {
      "type": "ai_response"
    }
  ]
}
```

---

## 🎯 O QUE VOCÊ PODE FAZER AGORA

### **✅ Já Funciona:**
1. ✅ Conectar WhatsApp (escanear QR Code)
2. ✅ Criar fluxos de atendimento
3. ✅ Usar templates prontos
4. ✅ Respostas automáticas
5. ✅ Integração com IA

### **⚠️ Melhorias Futuras:**
1. ⏳ Builder visual de fluxos (drag & drop)
2. ⏳ Mais templates prontos
3. ⏳ Analytics de fluxos
4. ⏳ Agendamentos

---

## 🐛 TROUBLESHOOTING

### **QR Code não aparece:**
- Aguarde 10-30 segundos (pode demorar)
- Recarregue a página (F5)
- Verifique se WhatsApp server está rodando: `curl http://localhost:5001/health`

### **WhatsApp não conecta:**
- Verifique se escaneou o QR Code corretamente
- QR Code expira em ~20 segundos, escaneie rapidamente
- Se não funcionar, limpe sessão: `rm -rf .wwebjs_auth/session-ylada_bot`

### **Fluxo não executa:**
- Verifique se está ativo (status = "active")
- Verifique se trigger está correto
- Verifique logs do Flask

---

## 📝 RESUMO RÁPIDO

1. ✅ **Servidores rodando** - Flask (5002) e WhatsApp (5001)
2. ⏳ **Conectar WhatsApp** - Escanear QR Code em http://localhost:5002/qr
3. ⏳ **Criar fluxo** - Acessar http://localhost:5002/tenant/flows
4. ⏳ **Testar** - Enviar mensagem e ver resposta

---

**Pronto para usar!** 🚀



