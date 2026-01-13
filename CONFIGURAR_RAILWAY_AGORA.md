# ⚡ CONFIGURAR RAILWAY AGORA - Passo a Passo

## ⚠️ PROBLEMA ATUAL

O erro "Servidor WhatsApp não está rodando na porta 5001" aparece porque:
- O Flask está tentando usar `localhost:5001` em produção
- Mas em produção (Railway), não existe "localhost"
- Precisa usar o **nome do serviço** para comunicação interna

---

## ✅ SOLUÇÃO RÁPIDA (5 minutos)

### **PASSO 1: Verificar se Serviço WhatsApp Existe**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. Veja se há um serviço chamado `whatsapp-server-2` (ou similar)

**Se NÃO existir:**
- Vá para PASSO 2

**Se existir:**
- Vá para PASSO 3

---

### **PASSO 2: Criar Serviço WhatsApp**

1. No Railway, clique em **"New"** → **"Empty Service"**
2. Nome: `whatsapp-server-2` (ou o nome que você preferir)
3. **Settings** → **Deploy**:
   - **Build Command:** `npm install`
   - **Start Command:** `node whatsapp_server.js`
   - **Root Directory:** `/` (raiz do projeto)
4. **Settings** → **Variables**:
   ```bash
   PORT=5001
   NODE_ENV=production
   ```
5. **Settings** → **Networking**:
   - NÃO precisa gerar domínio público
   - O Flask vai usar comunicação interna

---

### **PASSO 3: Configurar Nome do Serviço no Flask**

1. No Railway, selecione o serviço **Flask/Python**
2. Vá em **Settings** → **Variables**
3. Procure por `WHATSAPP_SERVICE_NAME`
   - **Se NÃO existir:** Clique em **"+ New Variable"**
   - **Se existir:** Clique em **"Edit"**
4. Configure:
   - **Nome:** `WHATSAPP_SERVICE_NAME`
   - **Valor:** Nome exato do serviço WhatsApp
     - Exemplo: Se o serviço se chama `whatsapp-server-2`, use: `whatsapp-server-2`
     - Exemplo: Se o serviço se chama `whatsapp`, use: `whatsapp`
5. **Salve**

---

### **PASSO 4: Verificar Status dos Serviços**

1. **Serviço WhatsApp:**
   - Deve estar **"Online"** (verde)
   - Se estiver "Crashed", veja os logs

2. **Serviço Flask:**
   - Deve estar **"Online"** (verde)
   - Aguarde 1-2 minutos após configurar a variável

---

### **PASSO 5: Testar**

1. Acesse: `https://yladabot.com/qr`
2. O erro "Servidor WhatsApp não está rodando na porta 5001" **NÃO deve mais aparecer**
3. Deve aparecer QR Code ou mensagem de "Gerando QR Code..."

---

## 🔍 VERIFICAR SE ESTÁ FUNCIONANDO

### **Nos Logs do Flask (Railway):**

Procure por:
```
🔗 Railway detectado! Usando comunicação interna: http://whatsapp-server-2:5001
```

**Se aparecer isso:** ✅ Está correto!

**Se aparecer:**
```
🔗 Modo desenvolvimento! Usando: http://localhost:5001
```

❌ Ainda está usando localhost. Verifique:
- Se `WHATSAPP_SERVICE_NAME` está configurado
- Se o nome está correto (exatamente igual ao nome do serviço)

---

## 📋 RESUMO DAS VARIÁVEIS

### **Serviço Flask (Python):**
```bash
WHATSAPP_SERVICE_NAME=whatsapp-server-2  # Nome exato do serviço WhatsApp
```

### **Serviço WhatsApp (Node.js):**
```bash
PORT=5001
NODE_ENV=production
```

---

## ⚠️ IMPORTANTE

- O nome do serviço deve ser **exatamente igual** em ambos os lugares
- Se o serviço se chama `whatsapp-server-2`, use `whatsapp-server-2`
- Não use espaços ou caracteres especiais
- Após configurar, aguarde 1-2 minutos para o deploy aplicar

---

**Última atualização:** 13/01/2026
