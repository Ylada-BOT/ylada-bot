# 🔐 Atualizar .env.local com Chaves Supabase

## ✅ Chaves Configuradas

Criei um arquivo **`.env.local.SUPABASE`** com todas as chaves do Supabase.

## 📋 PRÓXIMOS PASSOS

### **1. Copiar para .env.local**

**Opção A: Via Terminal**
```bash
# Na raiz do projeto:
cat .env.local.SUPABASE >> .env.local
```

**Opção B: Manualmente**
1. Abra o arquivo `.env.local.SUPABASE`
2. Copie TODO o conteúdo
3. Abra o arquivo `.env.local`
4. Cole no final do arquivo (ou substitua se preferir)

---

### **2. Obter Connection String do Banco**

**⚠️ IMPORTANTE:** Você ainda precisa adicionar a `DATABASE_URL` com a senha do banco!

1. No Supabase, vá em **Settings** → **Database**
2. Role até **"Connection string"**
3. Selecione a aba **"URI"**
4. Copie a string e substitua `[YOUR-PASSWORD]` pela senha do banco
5. Cole no `.env.local` na linha `DATABASE_URL=`

**Exemplo:**
```bash
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:MinhaSenha123!@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

---

### **3. Verificar Segurança**

✅ O arquivo `.env.local` está no `.gitignore` (não será commitado)
✅ As chaves estão protegidas
✅ Nunca compartilhe essas chaves publicamente

---

### **4. Testar**

Depois de configurar, reinicie o servidor:

```bash
# Pare o servidor (Ctrl+C)
# E inicie novamente
python3 web/app.py
```

---

## 📝 O QUE ESTÁ CONFIGURADO

✅ **SUPABASE_PROJECT_REF** - ID do projeto
✅ **SUPABASE_URL** - URL do projeto
✅ **SUPABASE_ANON_KEY** - Chave pública (anon)
✅ **SUPABASE_SERVICE_ROLE_KEY** - Chave privada (service role)
✅ **SUPABASE_JWT_ANON** - Token JWT anon
✅ **SUPABASE_JWT_SERVICE_ROLE** - Token JWT service role
⬅️ **DATABASE_URL** - Precisa adicionar a senha do banco

---

## 🔒 SEGURANÇA

- ✅ Arquivo `.env.local` está no `.gitignore`
- ✅ Nunca commite essas chaves
- ✅ Nunca compartilhe publicamente
- ✅ As chaves são confidenciais

---

**Última atualização:** 23/12/2024

