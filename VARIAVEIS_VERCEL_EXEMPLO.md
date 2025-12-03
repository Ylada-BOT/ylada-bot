# 🔑 Variáveis da Vercel - Exemplo Prático

## 📋 Onde Encontrar Cada Valor no Supabase

### **1. DB_HOST** (A mais importante!)

**Onde encontrar:**
1. Supabase → **Settings** → **Database**
2. Role até encontrar **Connection string** ou **Connection pooling**
3. Você vai ver algo assim:

```
postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**O que copiar:**
- A parte entre `@` e `:5432`
- **Exemplo:** `db.abcdefghijklmnop.supabase.co`

**Como fica na Vercel:**
```
DB_HOST=db.abcdefghijklmnop.supabase.co
```

---

### **2. DB_NAME**

**Sempre é:**
```
DB_NAME=postgres
```

**Não precisa procurar, é sempre `postgres`!**

---

### **3. DB_USER**

**Sempre é:**
```
DB_USER=postgres
```

**Não precisa procurar, é sempre `postgres`!**

---

### **4. DB_PASSWORD**

**Onde encontrar:**
- É a senha que você criou quando criou o projeto Supabase
- Se esqueceu:
  1. Supabase → **Settings** → **Database**
  2. Clique em **Reset database password**
  3. Anote a nova senha!

**Como fica na Vercel:**
```
DB_PASSWORD=MinhaSenhaSegura123!
```

**⚠️ IMPORTANTE:** Use a senha REAL que você criou!

---

### **5. DB_PORT**

**Sempre é:**
```
DB_PORT=5432
```

**Não precisa procurar, é sempre `5432`!**

---

### **6. SUPABASE_URL**

**Onde encontrar:**
1. Supabase → **Settings** → **API**
2. Procure por **Project URL**
3. Você vai ver:

```
Project URL
https://abcdefghijklmnop.supabase.co
```

**O que copiar:**
- A URL completa (começa com `https://`)

**Como fica na Vercel:**
```
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
```

---

### **7. SUPABASE_KEY**

**Onde encontrar:**
1. Supabase → **Settings** → **API**
2. Procure por **anon public key**
3. Você vai ver uma chave longa (começa com `eyJ...`)

**Exemplo do que você vai ver:**
```
anon public
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk2NzI4MCwiZXhwIjoxOTU0NTQzMjgwfQ.abcdefghijklmnopqrstuvwxyz1234567890
```

**O que copiar:**
- A chave completa (tudo que começa com `eyJ...`)

**Como fica na Vercel:**
```
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk2NzI4MCwiZXhwIjoxOTU0NTQzMjgwfQ.abcdefghijklmnopqrstuvwxyz1234567890
```

---

### **8. SUPABASE_SERVICE_KEY**

**Onde encontrar:**
1. Supabase → **Settings** → **API**
2. Procure por **service_role key**
3. Você vai ver uma chave longa (começa com `eyJ...`)

**⚠️ CUIDADO:** Esta chave é SECRETA! Não compartilhe!

**O que copiar:**
- A chave completa (tudo que começa com `eyJ...`)

**Como fica na Vercel:**
```
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjM4OTY3MjgwLCJleHAiOjE5NTQ1NDMyODB9.xyz1234567890abcdefghijklmnopqrstuvw
```

---

### **9. SECRET_KEY**

**Esta você cria você mesmo!**

Pode ser qualquer string aleatória segura.

**Opções:**

**Opção A: Gerar no terminal**
```bash
openssl rand -hex 32
```

**Opção B: Usar gerador online**
- Acesse: https://randomkeygen.com
- Use uma "CodeIgniter Encryption Keys"

**Opção C: Criar manualmente**
- Qualquer string aleatória (ex: `MinhaChaveSecreta123!@#`)

**Como fica na Vercel:**
```
SECRET_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

---

### **10. BOT_MODE**

**Sempre é:**
```
BOT_MODE=webjs
```

**Não precisa procurar, é sempre `webjs`!**

---

### **11. ENVIRONMENT**

**Sempre é:**
```
ENVIRONMENT=production
```

**Não precisa procurar, é sempre `production`!**

---

## 📝 Exemplo Completo (Substitua pelos seus valores!)

```
DB_HOST=db.abcdefghijklmnop.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=MinhaSenhaSegura123!
DB_PORT=5432
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk2NzI4MCwiZXhwIjoxOTU0NTQzMjgwfQ.abcdefghijklmnopqrstuvwxyz1234567890
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjM4OTY3MjgwLCJleHAiOjE5NTQ1NDMyODB9.xyz1234567890abcdefghijklmnopqrstuvw
SECRET_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
BOT_MODE=webjs
ENVIRONMENT=production
```

**⚠️ LEMBRE-SE:**
- Substitua `abcdefghijklmnop` pelo ID do SEU projeto
- Substitua `MinhaSenhaSegura123!` pela SUA senha real
- Substitua as chaves longas pelas SUAS chaves reais do Supabase

---

## 🎯 Resumo Rápido:

| Variável | Onde Encontrar | Valor Exemplo |
|----------|----------------|---------------|
| `DB_HOST` | Settings → Database → Connection string (parte entre @ e :5432) | `db.xxxxx.supabase.co` |
| `DB_NAME` | Sempre o mesmo | `postgres` |
| `DB_USER` | Sempre o mesmo | `postgres` |
| `DB_PASSWORD` | Senha que você criou (ou resetar) | `SuaSenha123!` |
| `DB_PORT` | Sempre o mesmo | `5432` |
| `SUPABASE_URL` | Settings → API → Project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | Settings → API → anon public key | `eyJ...` (chave longa) |
| `SUPABASE_SERVICE_KEY` | Settings → API → service_role key | `eyJ...` (chave longa) |
| `SECRET_KEY` | Você cria (gerador ou manual) | Qualquer string aleatória |
| `BOT_MODE` | Sempre o mesmo | `webjs` |
| `ENVIRONMENT` | Sempre o mesmo | `production` |

---

**Agora está mais claro? Se ainda tiver dúvida, me avise qual variável específica!** 😊

