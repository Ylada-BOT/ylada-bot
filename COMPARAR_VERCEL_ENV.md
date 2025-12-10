# 🔍 Comparar Variáveis: .env.local vs Vercel

## 📋 Lista Completa de Variáveis que DEVEM estar na Vercel:

### **1. Banco de Dados (Supabase):**
```
DB_HOST=db.tbbjqvvtsotjqgfygaaj.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Afo@1974
DB_PORT=5432
```

### **2. Supabase API:**
```
SUPABASE_URL=https://tbbjqvvtsotjqgfygaaj.supabase.co
SUPABASE_KEY=eyJ... (chave anon - deve começar com eyJ)
SUPABASE_SERVICE_KEY=eyJ... (chave service_role - deve começar com eyJ)
```

### **3. Aplicação:**
```
SECRET_KEY=49073da7c373f1bd73340a345201ce20ecdf4d965dd1a2015ceac9f7870f2c28
BOT_MODE=webjs
ENVIRONMENT=production
PORT=5002
```

### **4. Render (WhatsApp):**
```
RENDER_WHATSAPP_URL=https://ylada-bot.onrender.com
```

---

## ✅ Como Verificar na Vercel:

1. **Acesse:** https://vercel.com
2. **Selecione:** Seu projeto `ylada-bot-8fyl`
3. **Vá em:** Settings → Environment Variables
4. **Verifique:** Se TODAS as 13 variáveis acima estão lá

---

## ⚠️ Nomes que PODEM estar Diferentes na Vercel:

### **Se na Vercel estiver com nome diferente, CORRIJA:**

| ❌ Nome Errado na Vercel | ✅ Nome Correto |
|-------------------------|----------------|
| `SUPABASE_ANON_KEY` | `SUPABASE_KEY` |
| `SUPABASE_SERVICE_ROLE_KEY` | `SUPABASE_SERVICE_KEY` |
| `WHATSAPP_SERVER_URL` | `RENDER_WHATSAPP_URL` |
| `FLASK_PORT` | `PORT` |
| `NODE_ENV` | `ENVIRONMENT` |

---

## 🔧 Como Adicionar/Corrigir na Vercel:

### **Para cada variável que faltar ou estiver com nome errado:**

1. **Se estiver com nome errado:**
   - Clique nos 3 pontinhos da variável
   - Clique em **"Delete"**
   - Adicione novamente com o nome correto

2. **Se estiver faltando:**
   - Clique em **"Add New"**
   - **Key:** Nome exato (ex: `SUPABASE_KEY`)
   - **Value:** Valor do seu `.env.local`
   - **Environment:** Selecione **TODAS** (Production, Preview, Development)
   - Clique em **"Save"**

---

## 📝 Checklist Completo:

Marque cada variável que você encontrar na Vercel:

- [ ] `DB_HOST`
- [ ] `DB_NAME`
- [ ] `DB_USER`
- [ ] `DB_PASSWORD`
- [ ] `DB_PORT`
- [ ] `SUPABASE_URL`
- [ ] `SUPABASE_KEY` ⚠️ (verifique se não está como `SUPABASE_ANON_KEY`)
- [ ] `SUPABASE_SERVICE_KEY` ⚠️ (verifique se não está como `SUPABASE_SERVICE_ROLE_KEY`)
- [ ] `SECRET_KEY`
- [ ] `BOT_MODE`
- [ ] `ENVIRONMENT` ⚠️ (verifique se não está como `NODE_ENV`)
- [ ] `PORT` ⚠️ (verifique se não está como `FLASK_PORT`)
- [ ] `RENDER_WHATSAPP_URL` ⚠️ (verifique se não está como `WHATSAPP_SERVER_URL`)

---

## 🎯 Importante:

**Os nomes devem ser EXATAMENTE iguais ao do `.env.local`!**

Se encontrar nomes diferentes na Vercel, **corrija para os nomes corretos** listados acima.

---

## ✅ Depois de Verificar:

1. **Adicione as que faltam**
2. **Corrija os nomes que estiverem errados**
3. **Faça um Redeploy** na Vercel
4. **Teste a aplicação**

---

**Verifique na Vercel agora e compare com esta lista!** 🔍



