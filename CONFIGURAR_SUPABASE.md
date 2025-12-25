# 🚀 Configurar Supabase - Passo a Passo

## 📋 RESUMO RÁPIDO

1. Criar conta no Supabase
2. Criar projeto
3. Copiar connection string
4. Criar arquivo `.env.local`
5. Executar script SQL para criar tabelas
6. Testar conexão

---

## 🔧 PASSO A PASSO DETALHADO

### **1. Criar Conta e Projeto no Supabase**

1. Acesse: **https://supabase.com**
2. Clique em **"Start your project"** ou **"Sign up"**
3. Faça login (recomendado: GitHub)
4. Clique em **"New Project"**
5. Preencha:
   - **Name:** `ylada-bot`
   - **Database Password:** (crie uma senha forte e anote!)
   - **Region:** South America (São Paulo) ou mais próxima
6. Clique em **"Create new project"**
7. Aguarde ~2 minutos

---

### **2. Obter Connection String**

1. No dashboard do projeto, vá em **Settings** (⚙️) → **Database**
2. Role até **"Connection string"**
3. Selecione a aba **"URI"**
4. Você verá algo assim:
   ```
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
   ```
5. **IMPORTANTE:** Substitua `[YOUR-PASSWORD]` pela senha que você criou no passo 1

**Exemplo final:**
```
postgresql://postgres.abcdefghijklmnop:[SUA_SENHA]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

---

### **3. Criar Arquivo `.env.local`**

Na raiz do projeto, crie o arquivo `.env.local`:

```bash
# Database - Supabase
DATABASE_URL=postgresql://postgres.xxxxx:[SUA_SENHA]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres

# Chave secreta (gere uma aleatória)
SECRET_KEY=dev-secret-key-change-in-production

# Autenticação (false para desenvolvimento)
AUTH_REQUIRED=false
```

**⚠️ IMPORTANTE:**
- Substitua `[SUA_SENHA]` pela senha real
- Substitua `xxxxx` pelo ID do seu projeto
- **NUNCA** commite este arquivo no Git (já está no `.gitignore`)

---

### **4. Criar Tabelas no Supabase**

1. No Supabase, vá em **SQL Editor** (menu lateral)
2. Clique em **"New query"**
3. Abra o arquivo `scripts/create_tables_supabase_fix.sql` do projeto
4. Copie TODO o conteúdo
5. Cole no editor SQL do Supabase
6. Clique em **"Run"** (ou `Cmd+Enter` / `Ctrl+Enter`)
7. Aguarde a execução (deve mostrar "Success")

**Verificar:**
- Vá em **Table Editor**
- Você deve ver as tabelas: `users`, `plans`, `tenants`, `instances`, `flows`, `leads`, `conversations`, `messages`, `notifications`

---

### **5. Testar Conexão**

Reinicie o servidor Flask:

```bash
# Pare o servidor atual (Ctrl+C)
# E inicie novamente
python3 web/app.py
```

**Se tudo estiver OK, você verá:**
```
[✓] Banco de dados conectado
[✓] Rotas de organizations registradas
```

**Teste criar uma organização:**
1. Acesse: `http://localhost:5002/admin/organizations`
2. Clique em **"+ Nova Organização"**
3. Preencha o nome e clique em **"Criar Organização"**
4. Se funcionar, os dados estarão salvos no Supabase! 🎉

---

## 🐛 TROUBLESHOOTING

### **Erro: "Connection refused"**
- ✅ Verifique se a connection string está correta
- ✅ Confirme que substituiu `[YOUR-PASSWORD]` pela senha real
- ✅ Verifique se o projeto Supabase está ativo

### **Erro: "Password authentication failed"**
- ✅ Verifique se a senha está correta
- ✅ Pode resetar: Settings → Database → Reset database password

### **Erro: "Table already exists"**
- ✅ Normal se já executou o script antes
- ✅ Pode ignorar ou usar `DROP TABLE IF EXISTS` antes

### **Erro: "psycopg2 not found"**
- ✅ Instale: `pip install psycopg2-binary`

---

## ✅ CHECKLIST

- [ ] Conta criada no Supabase
- [ ] Projeto criado
- [ ] Connection string copiada
- [ ] Arquivo `.env.local` criado com `DATABASE_URL`
- [ ] Script SQL executado no Supabase
- [ ] Tabelas criadas (verificado no Table Editor)
- [ ] Servidor Flask reiniciado
- [ ] Teste de criar organização funcionando

---

## 📚 RECURSOS

- **Supabase Docs:** https://supabase.com/docs
- **Connection Pooling:** Use a porta `6543` (pooler) ao invés de `5432` (direto)
- **Dashboard:** https://app.supabase.com

---

**Última atualização:** 23/12/2024

