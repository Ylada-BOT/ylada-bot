# ⚡ Resumo Rápido: Configurar Railway

## 🎯 Objetivo
Fazer deploy do bot no Railway e obter todas as configurações.

---

## 📝 Passos Rápidos (5 minutos)

### **1. Criar Conta Railway**
- Acesse: https://railway.app
- Login com GitHub
- Autorizar acesso

### **2. Criar Projeto**
- **New Project** → **Deploy from GitHub repo**
- Selecionar: `ylada-bot`
- **Deploy Now**

### **3. Configurar Serviço Python**
- **Settings** → **Deploy**
- **Build:** `pip install -r requirements.txt`
- **Start:** `python3 web/app.py`
- **Variables** → Adicionar:

```bash
PORT=5002
SECRET_KEY=oy6b1MKDEOEJnBW1Pfd_9jQYgeiMzgRMMRBDiouSUjU
JWT_SECRET_KEY=0jSTAVhN5CCZ5GdFZp_8pztRymfP7IFf1DkeeJPlrG4
DATABASE_URL=postgresql://... (do Supabase)
```

### **4. Criar Serviço Node.js**
- **New** → **Empty Service**
- Nome: `whatsapp-server`
- **Build:** `npm install`
- **Start:** `node whatsapp_server.js`
- **Variables:**
```bash
PORT=5001
```

### **5. Obter URLs**
- Serviço Python → **Settings** → **Networking** → **Generate Domain**
- Serviço Node.js → **Settings** → **Networking** → **Generate Domain**
- Atualizar no Python:
```bash
WHATSAPP_SERVER_URL=https://whatsapp-server.up.railway.app
APP_URL=https://seu-projeto.up.railway.app
```

### **6. Deploy**
- Aguardar deploy automático
- Verificar logs
- Testar URL

---

## 🔑 Chaves Necessárias

✅ **SECRET_KEY:** `oy6b1MKDEOEJnBW1Pfd_9jQYgeiMzgRMMRBDiouSUjU`  
✅ **JWT_SECRET_KEY:** `0jSTAVhN5CCZ5GdFZp_8pztRymfP7IFf1DkeeJPlrG4`  
⚠️ **DATABASE_URL:** Obter do Supabase  
⚠️ **AI_API_KEY:** Obter da OpenAI (opcional)  

---

## 📚 Documentação Completa

Veja: `PASSO_A_PASSO_RAILWAY_COMPLETO.md` para guia detalhado.

---

**Última atualização:** 27/01/2025


