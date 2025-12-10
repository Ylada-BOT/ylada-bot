# 🔧 Adicionar URL do Render na Vercel

## ⚠️ Problema:
O código está tentando conectar com `localhost:5001`, mas o servidor WhatsApp Web.js está no Render (`ylada-bot.onrender.com`).

## ✅ Solução:
Adicionar variável de ambiente na Vercel apontando para o Render.

---

## 📋 Passo a Passo:

### 1. Acessar Vercel
1. Acesse: https://vercel.com
2. Selecione seu projeto
3. Vá em: **Settings** → **Environment Variables**

### 2. Adicionar Nova Variável
1. Clique em **"Add New"**
2. **Key:** `RENDER_WHATSAPP_URL`
3. **Value:** `https://ylada-bot.onrender.com`
4. **Environment:** Selecione **TODAS** (Production, Preview, Development)
5. Clique em **"Save"**

### 3. Fazer Redeploy
1. Vá em **Deployments**
2. Clique nos 3 pontinhos do último deploy
3. Clique em **"Redeploy"**
4. Aguarde alguns minutos

---

## ✅ Pronto!

Depois do redeploy, a página `/qr` vai funcionar corretamente!

---

## 📝 Explicação:

- **PORT=5002** → Porta do Flask (backend na Vercel) ✅
- **RENDER_WHATSAPP_URL** → URL do servidor WhatsApp Web.js (no Render) ✅

São coisas diferentes:
- Flask (Vercel) = Backend/API = Porta 5002
- WhatsApp Web.js (Render) = Servidor WhatsApp = `ylada-bot.onrender.com`

---

**Adicione a variável e faça redeploy!** 🚀

