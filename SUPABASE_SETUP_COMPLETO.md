# 🗄️ Configurar Supabase - Guia Completo Passo a Passo

## 📋 O que você vai fazer:

1. Criar tabelas no Supabase (SQL)
2. Copiar credenciais (URLs e senhas)
3. Configurar na Vercel

---

## 🔧 PASSO 1: Criar Tabelas (SQL)

### 1.1 Acessar SQL Editor

1. Acesse: https://app.supabase.com
2. Faça login
3. Selecione seu projeto (ou crie um novo)
4. No menu lateral esquerdo, clique em **SQL Editor**
5. Clique no botão **New Query** (ou use o atalho: `Ctrl+K` / `Cmd+K`)

### 1.2 Copiar e Colar o SQL

**Copie TODO este SQL abaixo e cole no editor:**

```sql
-- Tabela de Contas
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'owner',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de Instâncias
CREATE TABLE IF NOT EXISTS instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    instance_name VARCHAR(100) NOT NULL,
    port INTEGER UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'disconnected',
    qr_code TEXT,
    last_connected TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(account_id, instance_name)
);

-- Tabela de Contatos
CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(account_id, phone)
);

-- Tabela de Conversas
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id),
    message TEXT NOT NULL,
    from_me BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Tabela de Campanhas
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    message TEXT,
    qr_code_url TEXT,
    link TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_contacts_account ON contacts(account_id);
CREATE INDEX IF NOT EXISTS idx_conversations_account ON conversations(account_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_account ON campaigns(account_id);
CREATE INDEX IF NOT EXISTS idx_instances_account ON instances(account_id);
```

### 1.3 Executar SQL

1. Cole o SQL no editor
2. Clique no botão **Run** (ou pressione `Ctrl+Enter` / `Cmd+Enter`)
3. Deve aparecer: **"Success. No rows returned"** ✅

**Pronto! Tabelas criadas!**

---

## 🔑 PASSO 2: Copiar Credenciais

### 2.1 Acessar Settings

1. No Supabase, clique em **Settings** (ícone de engrenagem no menu lateral)
2. Clique em **API** (no submenu)

### 2.2 Copiar Project URL

Você vai ver uma seção chamada **Project URL**

**Exemplo do que você vai ver:**
```
Project URL
https://abcdefghijklmnop.supabase.co
```

**O que fazer:**
- Copie essa URL completa (começa com `https://`)
- **Esta é a `SUPABASE_URL`**

**Exemplo:**
```
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
```

### 2.3 Copiar API Keys

Na mesma página, você vai ver duas chaves:

#### **anon public key:**
- É uma chave longa (começa com `eyJ...`)
- **Esta é a `SUPABASE_KEY`**

#### **service_role key:**
- Também é uma chave longa (começa com `eyJ...`)
- ⚠️ **CUIDADO:** Esta é secreta! Não compartilhe!
- **Esta é a `SUPABASE_SERVICE_KEY`**

**Exemplo:**
```
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk2NzI4MCwiZXhwIjoxOTU0NTQzMjgwfQ.abcdefghijklmnopqrstuvwxyz1234567890
```

---

## 🗄️ PASSO 3: Copiar Credenciais do Banco de Dados

### 3.1 Acessar Database Settings

1. No Supabase, clique em **Settings**
2. Clique em **Database** (no submenu)

### 3.2 Encontrar Connection String

Role a página até encontrar a seção **Connection string** ou **Connection pooling**

Você vai ver algo assim:

```
Connection string
postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnop.supabase.co:5432/postgres
```

### 3.3 Extrair Valores

Dessa string, você precisa extrair:

#### **DB_HOST:**
- É a parte depois de `@` e antes de `:5432`
- **Formato:** `db.xxxxx.supabase.co`

**Exemplo:**
```
DB_HOST=db.abcdefghijklmnop.supabase.co
```

#### **DB_NAME:**
- Sempre é `postgres`

**Exemplo:**
```
DB_NAME=postgres
```

#### **DB_USER:**
- Sempre é `postgres`

**Exemplo:**
```
DB_USER=postgres
```

#### **DB_PASSWORD:**
- É a senha que você criou quando criou o projeto Supabase
- Se esqueceu, você pode resetar em **Settings** > **Database** > **Reset database password**

**Exemplo:**
```
DB_PASSWORD=MinhaSenhaSegura123!
```

#### **DB_PORT:**
- Sempre é `5432`

**Exemplo:**
```
DB_PORT=5432
```

---

## 📝 RESUMO: Todas as Variáveis

Aqui está um exemplo completo de como devem ficar:

```
DB_HOST=db.abcdefghijklmnop.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=MinhaSenhaSegura123!
DB_PORT=5432
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk2NzI4MCwiZXhwIjoxOTU0NTQzMjgwfQ.abcdefghijklmnopqrstuvwxyz1234567890
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjM4OTY3MjgwLCJleHAiOjE5NTQ1NDMyODB9.xyz1234567890abcdefghijklmnopqrstuvw
SECRET_KEY=qualquer_chave_aleatoria_segura_aqui_123456
BOT_MODE=webjs
ENVIRONMENT=production
```

**⚠️ IMPORTANTE:**
- Substitua `abcdefghijklmnop` pelo ID do seu projeto
- Substitua `MinhaSenhaSegura123!` pela sua senha real
- Substitua as chaves longas (`eyJ...`) pelas suas chaves reais
- `SECRET_KEY` pode ser qualquer string aleatória (ex: `openssl rand -hex 32`)

---

## 🚀 PASSO 4: Adicionar na Vercel

### 4.1 Acessar Vercel

1. Acesse: https://vercel.com
2. Faça login
3. Selecione seu projeto

### 4.2 Adicionar Variáveis

1. Clique em **Settings** (no topo)
2. Clique em **Environment Variables** (no menu lateral)
3. Para cada variável:
   - Clique em **Add New**
   - **Key:** Nome da variável (ex: `DB_HOST`)
   - **Value:** Valor da variável (ex: `db.xxxxx.supabase.co`)
   - **Environment:** Selecione todas (Production, Preview, Development)
   - Clique em **Save**

### 4.3 Adicionar Todas

Adicione uma por uma:
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`
- `SECRET_KEY`
- `BOT_MODE`
- `ENVIRONMENT`

### 4.4 Fazer Redeploy

Após adicionar todas as variáveis:

1. Vá em **Deployments**
2. Clique nos 3 pontinhos do último deploy
3. Clique em **Redeploy**
4. Aguarde alguns minutos

**Pronto! Agora está configurado!**

---

## ✅ Checklist:

- [ ] SQL executado no Supabase (tabelas criadas)
- [ ] `SUPABASE_URL` copiada
- [ ] `SUPABASE_KEY` copiada
- [ ] `SUPABASE_SERVICE_KEY` copiada
- [ ] `DB_HOST` extraída da connection string
- [ ] `DB_PASSWORD` anotada (ou resetada)
- [ ] Todas as variáveis adicionadas na Vercel
- [ ] Redeploy feito

---

## 🆘 Problemas?

### "Não encontro a connection string"
- Vá em **Settings** > **Database**
- Role a página até encontrar **Connection string** ou **Connection pooling**

### "Esqueci a senha do banco"
- Vá em **Settings** > **Database**
- Clique em **Reset database password**
- Anote a nova senha!

### "Onde está o DB_HOST?"
- É a parte da connection string entre `@` e `:5432`
- Formato: `db.xxxxx.supabase.co`
- Exemplo: Se a connection string é `postgresql://postgres:senha@db.abc123.supabase.co:5432/postgres`
- Então `DB_HOST=db.abc123.supabase.co`

---

**Agora está tudo claro? Se tiver dúvida em algum passo, me avise!** 😊

