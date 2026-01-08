# 🚀 Configurar WhatsApp em Produção

## ⚠️ Problema Resolvido

O sistema agora detecta automaticamente se está em produção e usa a URL correta do servidor WhatsApp.

## ✅ O que foi ajustado

1. **Detecção automática de ambiente**
   - Detecta Railway, Vercel, Render automaticamente
   - Usa `localhost` em desenvolvimento
   - Usa URL configurável em produção

2. **Variável de ambiente `WHATSAPP_SERVER_URL`**
   - Configura a URL do servidor Node.js WhatsApp
   - Se não configurada, tenta detectar automaticamente

3. **Todas as chamadas atualizadas**
   - `/api/qr` - Buscar QR Code
   - `/api/conversations` - Listar conversas
   - `/api/conversations/<id>/messages` - Mensagens
   - `/api/whatsapp-status` - Status da conexão
   - `/api/whatsapp-disconnect` - Desconectar

---

## 🔧 Como Configurar em Produção

### **Opção 1: Railway (Recomendado)** ⭐

Railway suporta múltiplos serviços (Python + Node.js).

#### **Passo 1: Criar Serviço Node.js**

1. No Railway, adicione um novo serviço
2. Escolha "Deploy from GitHub repo"
3. Configure:
   - **Nome:** `whatsapp-server`
   - **Build Command:** `npm install`
   - **Start Command:** `node whatsapp_server.js`
   - **Port:** `5001` (ou a porta que você configurou)

#### **Passo 2: Configurar Variáveis de Ambiente**

No serviço Python (Flask), adicione:

```bash
WHATSAPP_SERVER_URL=http://whatsapp-server:5001
```

Ou se estiver em serviços separados:

```bash
WHATSAPP_SERVER_URL=https://seu-whatsapp-server.railway.app
```

#### **Passo 3: Deploy**

Railway faz deploy automático via Git push!

---

### **Opção 2: Render**

#### **Passo 1: Criar Web Service para Node.js**

1. Acesse: https://render.com
2. New > Web Service
3. Conecte seu repositório
4. Configure:
   - **Name:** `whatsapp-server`
   - **Environment:** `Node`
   - **Build Command:** `npm install`
   - **Start Command:** `node whatsapp_server.js`
   - **Port:** `5001`

#### **Passo 2: Configurar Variáveis**

No serviço Python (Flask), adicione:

```bash
WHATSAPP_SERVER_URL=https://whatsapp-server.onrender.com
```

---

### **Opção 3: Vercel (Frontend) + Railway (Backend)**

Vercel não suporta processos longos, então:

1. **Vercel:** Frontend/Dashboard (grátis)
2. **Railway:** Backend + WhatsApp Server (R$ 0-200/mês)

#### **Configuração:**

No Vercel, adicione variável:

```bash
WHATSAPP_SERVER_URL=https://seu-backend.railway.app:5001
```

---

## 📋 Variáveis de Ambiente Necessárias

### **Serviço Python (Flask):**

```bash
# WhatsApp
WHATSAPP_SERVER_URL=http://whatsapp-server:5001  # URL do servidor Node.js
WHATSAPP_SERVER_PORT=5001

# Banco de dados
DATABASE_URL=postgresql://...

# Outras
SECRET_KEY=seu-secret-key
APP_URL=https://seu-app.com
```

### **Serviço Node.js (WhatsApp):**

```bash
PORT=5001
NODE_ENV=production
```

---

## 🧪 Testar em Produção

1. **Acesse:** `https://seu-app.com/qr`
2. **Verifique console do navegador:**
   - Não deve ter erro 500
   - Deve mostrar QR Code ou status de conexão

3. **Verifique logs:**
   - Servidor Node.js deve estar rodando
   - Flask deve conseguir conectar no servidor Node.js

---

## ⚠️ Importante

### **Vercel NÃO suporta processos longos**

Se você está usando Vercel:
- ❌ Não pode rodar `whatsapp_server.js` no Vercel
- ✅ Use Railway ou Render para o servidor Node.js
- ✅ Configure `WHATSAPP_SERVER_URL` apontando para o servidor externo

### **Railway é a melhor opção**

- ✅ Suporta múltiplos serviços
- ✅ Processos longos (24/7)
- ✅ Deploy automático
- ✅ R$ 0-200/mês

---

## 🔍 Troubleshooting

### **Erro 500 ao buscar QR Code**

1. Verifique se o servidor Node.js está rodando
2. Verifique se `WHATSAPP_SERVER_URL` está configurada corretamente
3. Verifique logs do servidor Node.js

### **Erro "Servidor WhatsApp não está rodando"**

1. Verifique se o serviço Node.js está ativo no Railway/Render
2. Verifique se a porta está correta
3. Verifique se `WHATSAPP_SERVER_URL` aponta para o serviço correto

### **QR Code não aparece**

1. Verifique logs do servidor Node.js
2. Verifique se o WhatsApp Web.js está instalado
3. Tente recarregar a página (F5)

---

**Última atualização:** 27/01/2025

