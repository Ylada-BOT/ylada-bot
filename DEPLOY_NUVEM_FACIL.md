# 🚀 Deploy na Nuvem - Guia Fácil (Sem Computador Ligado)

## 🎯 Objetivo:
Fazer seu bot funcionar 24/7 **SEM precisar deixar seu computador ligado**

---

## 📋 O que você vai precisar:

1. ✅ Conta GitHub (grátis)
2. ✅ Conta Vercel (grátis)
3. ✅ Conta Railway ou Render (grátis)
4. ✅ Conta Supabase (grátis)

**Total: R$ 0,00** 🎉

---

## 🚀 Passo 1: Preparar Código no GitHub

### 1.1 Inicializar Git (se ainda não fez)

```bash
cd "/Users/air/Ylada BOT"
git init
git add .
git commit -m "Ylada BOT - Multi-instance ready"
```

### 1.2 Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome: `ylada-bot` (ou outro nome)
3. Clique em **Create repository**

### 1.3 Conectar e Enviar

```bash
git remote add origin https://github.com/SEU-USUARIO/ylada-bot.git
git branch -M main
git push -u origin main
```

**Substitua `SEU-USUARIO` pelo seu usuário do GitHub!**

---

## 🗄️ Passo 2: Configurar Supabase (Banco de Dados)

### 2.1 Criar Projeto

1. Acesse: https://app.supabase.com
2. Clique em **New Project**
3. Preencha:
   - **Name**: `ylada-bot`
   - **Database Password**: (anote essa senha!)
   - **Region**: Escolha mais próxima (ex: South America)
4. Clique em **Create new project**
5. Aguarde ~2 minutos para criar

### 2.2 Criar Tabelas

1. No Supabase, vá em **SQL Editor**
2. Clique em **New Query**
3. Cole este SQL:

```sql
-- Tabela de Contas
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'owner',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de Instâncias
CREATE TABLE instances (
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
CREATE TABLE contacts (
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
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id),
    message TEXT NOT NULL,
    from_me BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Tabela de Campanhas
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    message TEXT,
    qr_code_url TEXT,
    link TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_contacts_account ON contacts(account_id);
CREATE INDEX idx_conversations_account ON conversations(account_id);
CREATE INDEX idx_campaigns_account ON campaigns(account_id);
CREATE INDEX idx_instances_account ON instances(account_id);
```

4. Clique em **Run** (ou F5)
5. Deve aparecer: "Success. No rows returned"

### 2.3 Copiar Credenciais

1. No Supabase, vá em **Settings** > **API**
2. Copie:
   - **Project URL** (ex: `https://xxxxx.supabase.co`)
   - **anon public key** (chave longa)
   - **service_role key** (chave longa - **MANTENHA SECRETO!**)

**Guarde essas informações! Você vai precisar no próximo passo.**

---

## 🌐 Passo 3: Deploy Backend/Frontend (Vercel)

### 3.1 Criar Conta

1. Acesse: https://vercel.com
2. Clique em **Sign Up**
3. Escolha **Continue with GitHub**
4. Autorize o Vercel

### 3.2 Importar Projeto

1. No Vercel, clique em **Add New Project**
2. Selecione seu repositório `ylada-bot`
3. Clique em **Import**

### 3.3 Configurar Build

- **Framework Preset**: Other
- **Root Directory**: `.` (raiz)
- **Build Command**: (deixe vazio)
- **Output Directory**: (deixe vazio)

### 3.4 Adicionar Variáveis de Ambiente

Clique em **Environment Variables** e adicione:

```
DB_HOST=db.xxxxx.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=SUA_SENHA_DO_SUPABASE
DB_PORT=5432
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=sua_anon_key_aqui
SUPABASE_SERVICE_KEY=sua_service_key_aqui
SECRET_KEY=qualquer_chave_aleatoria_segura_aqui
BOT_MODE=webjs
ENVIRONMENT=production
PORT=5002
```

**Substitua:**
- `xxxxx` pelo ID do seu projeto Supabase
- `SUA_SENHA_DO_SUPABASE` pela senha que você criou
- `sua_anon_key_aqui` pela anon key do Supabase
- `sua_service_key_aqui` pela service_role key
- `qualquer_chave_aleatoria_segura_aqui` por uma chave aleatória (ex: `openssl rand -hex 32`)

### 3.5 Deploy

1. Clique em **Deploy**
2. Aguarde ~2-3 minutos
3. Quando terminar, você terá uma URL: `https://seu-projeto.vercel.app`

**✅ Pronto! Backend/Frontend está online 24/7!**

---

## 📱 Passo 4: Deploy WhatsApp Web.js (Railway)

### 4.1 Criar Conta

1. Acesse: https://railway.app
2. Clique em **Start a New Project**
3. Escolha **Login with GitHub**
4. Autorize o Railway

### 4.2 Criar Novo Projeto

1. Clique em **New Project**
2. Escolha **Deploy from GitHub repo**
3. Selecione seu repositório `ylada-bot`

### 4.3 Configurar Serviço

1. Railway vai detectar automaticamente
2. Vá em **Settings**
3. Configure:
   - **Start Command**: `node whatsapp_server.js`
   - **Healthcheck Path**: `/health` (se tiver)

### 4.4 Adicionar Variáveis (se necessário)

Se o `whatsapp_server.js` precisar de variáveis, adicione em **Variables**

### 4.5 Deploy

1. Railway vai fazer deploy automaticamente
2. Aguarde alguns minutos
3. Você terá uma URL: `https://seu-projeto.railway.app`

**✅ Pronto! WhatsApp Web.js está online 24/7!**

---

## 🔗 Passo 5: Conectar Tudo

### 5.1 Atualizar Código para Usar PostgreSQL

No `web/app_multi.py`, mude:

```python
# De:
db = Database(use_sqlite=True)

# Para:
db = Database(use_sqlite=False)  # Usa PostgreSQL do Supabase
```

### 5.2 Fazer Commit e Push

```bash
git add .
git commit -m "Configure PostgreSQL for production"
git push
```

O Vercel vai fazer deploy automático!

---

## ✅ Pronto!

Agora seu bot está:
- ✅ **Online 24/7**
- ✅ **Funciona mesmo com seu computador desligado**
- ✅ **Domínio personalizado** (pode configurar depois)
- ✅ **Pronto para comercializar**

---

## 🎯 URLs Finais:

- **Backend/Frontend**: `https://seu-projeto.vercel.app`
- **WhatsApp Web.js**: `https://seu-projeto.railway.app`
- **Banco de Dados**: Supabase (interno)

---

## 📝 Próximos Passos:

1. ✅ Acesse sua URL do Vercel
2. ✅ Configure suas 4 contas (via API ou interface)
3. ✅ Conecte os telefones escaneando QR Codes
4. ✅ Teste enviando mensagens
5. ✅ **Use normalmente - tudo online!**

---

## 💡 Dicas:

- **Domínio personalizado**: No Vercel, vá em **Settings** > **Domains** e adicione seu domínio
- **Monitoramento**: Vercel e Railway têm dashboards para ver logs
- **Backup**: Supabase faz backup automático
- **Escalabilidade**: Tudo escala automaticamente quando precisar

---

## 🆘 Problemas?

- **Deploy falhou?** Veja os logs no Vercel/Railway
- **Banco não conecta?** Verifique as variáveis de ambiente
- **WhatsApp não conecta?** Verifique se o servidor Node.js está rodando no Railway

---

**Agora você pode desligar seu computador e tudo continua funcionando! 🎉**

