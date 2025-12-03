# 🔄 Migração Vercel para Multi-Instance - Guia Rápido

## ✅ Você já está na Vercel!

Agora vamos atualizar para suportar **4 telefones simultaneamente**.

---

## 🎯 O que precisa fazer:

### **1. Atualizar Entry Point** ✅ (Já feito!)

O `api/index.py` já foi atualizado para usar `app_multi.py`.

### **2. Configurar Banco Supabase**

Você precisa criar as tabelas no Supabase:

1. Acesse seu projeto Supabase
2. Vá em **SQL Editor**
3. Execute o SQL do arquivo `VERCEL_MULTI_INSTANCE.md` (seção 2.1)

### **3. Adicionar Variáveis de Ambiente na Vercel**

No dashboard da Vercel:
1. Vá em **Settings** > **Environment Variables**
2. Adicione estas variáveis:

```
DB_HOST=db.xxxxx.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_PORT=5432
```

**Onde encontrar:**
- `DB_HOST`: No Supabase, Settings > Database > Connection string
- `DB_PASSWORD`: A senha que você criou ao criar o projeto
- `DB_USER`: Geralmente é `postgres`

### **4. WhatsApp Web.js (Servidor Separado)**

⚠️ **IMPORTANTE:** WhatsApp Web.js **NÃO funciona** em serverless.

Você precisa de um servidor separado (Railway ou Render):

#### **Railway (Recomendado):**

1. Acesse: https://railway.app
2. **New Project** > **Deploy from GitHub**
3. Selecione seu repositório
4. Configure:
   - **Start Command**: `node whatsapp_server.js`
5. Deploy!

**Resultado:** WhatsApp Web.js rodando 24/7 sem seu computador ligado!

---

## 🚀 Fazer Deploy:

```bash
cd "/Users/air/Ylada BOT"
git add .
git commit -m "Update to multi-instance support"
git push
```

A Vercel vai fazer deploy automático! 🎉

---

## ✅ Após Deploy:

### **Criar suas 4 contas:**

Você pode fazer via API ou SQL:

#### **Via API:**
```bash
curl -X POST https://seu-projeto.vercel.app/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"name": "Conta 1", "phone": "5511999999999", "plan": "owner"}'
```

#### **Via SQL (Supabase):**
```sql
INSERT INTO accounts (name, phone, plan) VALUES
    ('Conta 1', '5511999999999', 'owner'),
    ('Conta 2', '5511888888888', 'owner'),
    ('Conta 3', '5511777777777', 'owner'),
    ('Conta 4', '5511666666666', 'owner');
```

---

## 📋 Checklist Rápido:

- [x] `api/index.py` atualizado
- [ ] Tabelas criadas no Supabase
- [ ] Variáveis de ambiente adicionadas na Vercel
- [ ] Servidor WhatsApp Web.js no Railway/Render
- [ ] Commit e push (deploy automático)
- [ ] Criar 4 contas
- [ ] Testar!

---

## 🎉 Resultado:

Depois disso, você terá:
- ✅ Backend na Vercel (24/7)
- ✅ WhatsApp Web.js no Railway (24/7)
- ✅ Banco no Supabase (24/7)
- ✅ **4 telefones funcionando simultaneamente**
- ✅ **Tudo online sem seu computador ligado!**

---

## 📞 Precisa de ajuda?

Veja o guia completo em: `VERCEL_MULTI_INSTANCE.md`

