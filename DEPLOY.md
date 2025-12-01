# 🚀 Guia de Deploy - Ylada BOT

## 📋 Pré-requisitos

- ✅ Conta Vercel criada
- ✅ Conta Supabase criada
- ✅ Repositório GitHub criado

## 🔧 Passo 1: Configurar Supabase

### 1.1 Criar Banco de Dados

1. Acesse [Supabase Dashboard](https://app.supabase.com)
2. Crie um novo projeto
3. Anote a **URL** e **API Key** do projeto

### 1.2 Criar Tabelas

Execute este SQL no SQL Editor do Supabase:

```sql
-- Tabela de Contatos
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    tags TEXT[],
    category VARCHAR(100),
    notes TEXT
);

-- Tabela de Conversas
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    from_me BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW(),
    flow_id VARCHAR(100),
    metadata JSONB
);

-- Tabela de Campanhas
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    message TEXT,
    qr_code_url TEXT,
    link TEXT,
    participants INTEGER DEFAULT 0,
    executions INTEGER DEFAULT 0,
    ctr DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de Usuários (para múltiplos atendentes)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'attendant',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_conversations_phone ON conversations(phone);
CREATE INDEX idx_conversations_timestamp ON conversations(timestamp);
```

## 🔧 Passo 2: Configurar Variáveis de Ambiente

### 2.1 No Supabase

1. Vá em **Settings** > **API**
2. Copie:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_KEY`
   - **service_role key** → `SUPABASE_SERVICE_KEY`

### 2.2 No Vercel

1. Vá em seu projeto no Vercel
2. **Settings** > **Environment Variables**
3. Adicione:

```
BOT_MODE=webjs
SUPABASE_URL=sua_url_aqui
SUPABASE_KEY=sua_key_aqui
SUPABASE_SERVICE_KEY=sua_service_key_aqui
SECRET_KEY=gerar_uma_chave_secreta_aleatoria
ENVIRONMENT=production
PORT=5002
```

## 🔧 Passo 3: Preparar Repositório GitHub

### 3.1 Inicializar Git (se ainda não fez)

```bash
git init
git add .
git commit -m "Initial commit - Ylada BOT"
```

### 3.2 Conectar ao GitHub

```bash
# Crie o repositório no GitHub primeiro, depois:
git remote add origin https://github.com/seu-usuario/ylada-bot.git
git branch -M main
git push -u origin main
```

## 🔧 Passo 4: Deploy na Vercel

### 4.1 Via Dashboard

1. Acesse [Vercel Dashboard](https://vercel.com/dashboard)
2. Clique em **Add New Project**
3. Importe seu repositório GitHub
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `.` (raiz)
   - **Build Command**: (deixe vazio ou `pip install -r requirements.txt`)
   - **Output Directory**: (deixe vazio)
5. Adicione as variáveis de ambiente (Passo 2.2)
6. Clique em **Deploy**

### 4.2 Via CLI (Alternativa)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy em produção
vercel --prod
```

## 🔧 Passo 5: Configurar Domínio (Opcional)

1. No Vercel, vá em **Settings** > **Domains**
2. Adicione seu domínio
3. Configure DNS conforme instruções

## 🔧 Passo 6: Atualizar Código para Supabase

O código precisa ser atualizado para usar Supabase ao invés de arquivos locais. Isso será feito no próximo passo.

## ✅ Checklist Pós-Deploy

- [ ] Verificar se o site está acessível
- [ ] Testar endpoint `/health`
- [ ] Verificar logs no Vercel
- [ ] Testar conexão com Supabase
- [ ] Configurar WhatsApp Web.js (será em servidor separado)

## 🚨 Notas Importantes

1. **WhatsApp Web.js**: O servidor Node.js precisa rodar em um servidor separado (não funciona em serverless). Considere:
   - Railway
   - Render
   - DigitalOcean
   - AWS EC2

2. **Banco de Dados**: Supabase é gratuito até 500MB

3. **Limites Vercel**:
   - Funções serverless: 10s (hobby) ou 60s (pro)
   - Bandwidth: 100GB/mês (hobby)

## 📞 Próximos Passos

Após o deploy, precisaremos:
1. Criar integração com Supabase
2. Configurar servidor separado para WhatsApp Web.js
3. Testar todas as funcionalidades

