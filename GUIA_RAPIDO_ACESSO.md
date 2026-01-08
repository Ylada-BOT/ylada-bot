# 🚀 Guia Rápido de Acesso - IladaBot

## ✅ SISTEMA ESTÁ FUNCIONANDO!

O servidor está rodando e o sistema de autenticação está operacional.

---

## 🔐 COMO ACESSAR

### **Opção 1: Login (Se já tem conta)**
1. Acesse: `http://localhost:5002/login`
2. Use suas credenciais:
   - **Email:** `portalmagra@gmail.com`
   - **Senha:** `123456` (ou a senha que você definiu)

### **Opção 2: Criar Nova Conta**
1. Acesse: `http://localhost:5002/register`
2. Preencha:
   - **Nome:** Seu nome
   - **Email:** Seu email
   - **Senha:** Mínimo 6 caracteres
3. Clique em "Cadastrar"

---

## 🎯 PRÓXIMOS PASSOS PARA TER TUDO FUNCIONANDO

### **1. ✅ AUTENTICAÇÃO (JÁ FUNCIONANDO)**
- ✅ Login/Registro funcionando
- ✅ Separação de contas por usuário
- ✅ Sistema de sessões

**Status:** ✅ **COMPLETO**

---

### **2. 🔄 CONECTAR WHATSAPP (PRÓXIMO)**
**O que fazer:**
1. Após fazer login, vá para o Dashboard
2. Clique em "Conectar WhatsApp"
3. Escaneie o QR Code com seu WhatsApp
4. Aguarde conexão

**Requisitos:**
- ✅ Servidor Node.js (`whatsapp_server.js`) deve estar rodando
- ✅ Porta 5001 disponível (ou a porta configurada)

**Como iniciar servidor WhatsApp:**
```bash
cd "/Users/air/Ylada BOT"
node whatsapp_server.js
```

**Status:** ⏳ **PRECISA CONECTAR**

---

### **3. 🤖 CONFIGURAR IA (IMPORTANTE)**
**O que fazer:**
1. No Dashboard, vá em "Configurações de IA"
2. Configure:
   - **Provider:** OpenAI
   - **API Key:** Sua chave (já está no `.env`)
   - **Model:** `gpt-4o-mini` (recomendado)
   - **System Prompt:** Já configurado (Carol/Portal Magra)

**Status:** ✅ **JÁ CONFIGURADO** (via `.env`)

---

### **4. 💬 TESTAR IA (ANTES DE HABILITAR)**
**O que fazer:**
1. No Dashboard, use a seção "💬 Teste a IA"
2. Digite mensagens de teste
3. Veja as respostas da IA
4. Ajuste o System Prompt se necessário

**Status:** ✅ **DISPONÍVEL**

---

### **5. 🚀 HABILITAR RESPOSTAS AUTOMÁTICAS**
**O que fazer:**
1. Após testar e aprovar as respostas da IA
2. Edite o arquivo `.env`:
   ```
   AUTO_RESPOND=true
   ```
3. Reinicie o servidor Flask

**⚠️ IMPORTANTE:** Só habilite depois de testar!

**Status:** ⏳ **AGUARDANDO SUA APROVAÇÃO**

---

## 📋 CHECKLIST RÁPIDO

### **Para ter tudo funcionando AGORA:**

- [x] ✅ Servidor Flask rodando (porta 5002)
- [ ] ⏳ Fazer login/registro
- [ ] ⏳ Iniciar servidor WhatsApp (`node whatsapp_server.js`)
- [ ] ⏳ Conectar WhatsApp (escanear QR)
- [x] ✅ IA configurada (já está no `.env`)
- [ ] ⏳ Testar IA no dashboard
- [ ] ⏳ Habilitar respostas automáticas (se aprovado)

---

## 🛠️ COMANDOS ÚTEIS

### **Iniciar Servidor Flask:**
```bash
cd "/Users/air/Ylada BOT"
source venv/bin/activate
python web/app.py
```

### **Iniciar Servidor WhatsApp:**
```bash
cd "/Users/air/Ylada BOT"
node whatsapp_server.js
```

### **Verificar se está rodando:**
```bash
# Flask
curl http://localhost:5002/health

# WhatsApp
curl http://localhost:5001/health
```

---

## 🎯 SUGESTÃO: O QUE FAZER AGORA

### **PRIORIDADE 1: Entrar no Sistema**
1. ✅ Acesse: `http://localhost:5002/login`
2. ✅ Use: `portalmagra@gmail.com` / `123456`
3. ✅ Ou crie nova conta em `/register`

### **PRIORIDADE 2: Conectar WhatsApp**
1. ⏳ Inicie servidor WhatsApp: `node whatsapp_server.js`
2. ⏳ No Dashboard, clique em "Conectar WhatsApp"
3. ⏳ Escaneie o QR Code

### **PRIORIDADE 3: Testar IA**
1. ⏳ Use o chat de teste no Dashboard
2. ⏳ Valide as respostas
3. ⏳ Ajuste System Prompt se necessário

### **PRIORIDADE 4: Habilitar (Se Aprovado)**
1. ⏳ Edite `.env`: `AUTO_RESPOND=true`
2. ⏳ Reinicie servidor Flask
3. ⏳ Pronto! IA responderá automaticamente

---

## ⚡ RESUMO: O QUE ESTÁ PRONTO

✅ **Sistema de Login/Registro** - Funcionando
✅ **Dashboard** - Funcionando
✅ **Configuração de IA** - Já configurada
✅ **Chat de Teste** - Disponível
✅ **Sistema de Filas** - Implementado
✅ **Rate Limiting** - Ativo

⏳ **Conectar WhatsApp** - Precisa fazer
⏳ **Testar IA** - Precisa validar
⏳ **Habilitar Auto-resposta** - Aguardando aprovação

---

**Última atualização:** Hoje
**Status:** Sistema funcional, aguardando conexão WhatsApp e testes







