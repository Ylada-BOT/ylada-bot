# 🚀 Atualizar DATABASE_URL em Produção

## ⚠️ IMPORTANTE

- ❌ **NÃO** faça commit do arquivo `.env.local` (contém senhas!)
- ✅ O arquivo `.env.local` é apenas para **desenvolvimento local**
- ✅ Em **produção**, configure a variável `DATABASE_URL` na plataforma (Railway, Render, etc.)

---

## 📍 ONDE ATUALIZAR

### **Se você usa Railway:**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. Clique no serviço Python/Flask
4. Vá em **"Variables"** (ou **"Settings"** → **"Variables"**)
5. Encontre `DATABASE_URL`
6. Clique em **"Edit"** ou **"Update"**
7. Cole a nova connection string:
   ```
   postgresql://postgres.tbbjqvvtsotjqgfygaaj:whxOGnx1h098Ue2c@aws-0-us-west-2.pooler.supabase.com:5432/postgres
   ```
8. Clique em **"Save"**
9. O Railway vai fazer **redeploy automático**

---

### **Se você usa Render:**

1. Acesse: https://render.com
2. Selecione seu serviço
3. Vá em **"Environment"**
4. Encontre `DATABASE_URL`
5. Clique em **"Edit"**
6. Cole a nova connection string
7. Clique em **"Save Changes"**
8. O Render vai fazer **redeploy automático**

---

### **Se você usa Vercel:**

1. Acesse: https://vercel.com
2. Selecione seu projeto
3. Vá em **"Settings"** → **"Environment Variables"**
4. Encontre `DATABASE_URL`
5. Clique em **"Edit"**
6. Cole a nova connection string
7. Clique em **"Save"**
8. Faça um novo deploy

---

## ✅ CONNECTION STRING COMPLETA

Use esta connection string (já com a senha atualizada):

```bash
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:whxOGnx1h098Ue2c@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

---

## 🔍 VERIFICAR SE ESTÁ EM PRODUÇÃO

Para verificar se seu projeto está em produção:

1. Veja se há arquivos como:
   - `railway.json`
   - `Procfile`
   - `.railway/`
   - `vercel.json`

2. Ou verifique se você tem um serviço rodando em:
   - Railway
   - Render
   - Vercel
   - Outra plataforma

---

## 📝 RESUMO

- ✅ **Local:** Já está atualizado no `.env.local`
- ✅ **Produção:** Atualize a variável `DATABASE_URL` na plataforma
- ❌ **NÃO commite** o `.env.local`
- ✅ Após atualizar, o deploy será automático

---

**Última atualização:** 27/01/2025

