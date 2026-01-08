# 📊 CRIAR TABELAS NO SUPABASE - PASSO A PASSO

**Data:** 2025-01-27  
**Objetivo:** Criar todas as tabelas necessárias no Supabase

---

## 🚀 MÉTODO RÁPIDO (5 minutos)

### Passo 1: Acessar SQL Editor

1. **Acesse:** https://supabase.com
2. **Faça login** no seu projeto
3. **No menu lateral esquerdo**, clique em **"SQL Editor"** (ícone de código `</>`)
4. **Clique em "New query"** (Nova consulta)

### Passo 2: Copiar Script SQL

1. **Abra o arquivo:** `scripts/create_tables_supabase.sql`
2. **Selecione TODO o conteúdo** (Ctrl+A / Cmd+A)
3. **Copie** (Ctrl+C / Cmd+C)

### Passo 3: Colar e Executar

1. **Cole o script** no SQL Editor do Supabase
2. **Clique em "Run"** (ou pressione Ctrl+Enter / Cmd+Enter)
3. **Aguarde alguns segundos**
4. **Deve aparecer:** "Success. No rows returned" ou lista de tabelas

### Passo 4: Verificar Tabelas Criadas

1. **No menu lateral**, clique em **"Table Editor"** (ícone de tabela)
2. **Você deve ver 10 tabelas:**
   - ✅ users
   - ✅ plans
   - ✅ tenants
   - ✅ subscriptions
   - ✅ instances
   - ✅ flows
   - ✅ conversations
   - ✅ messages
   - ✅ leads
   - ✅ notifications

---

## 📋 SCRIPT SQL COMPLETO

Se você não encontrar o arquivo, aqui está o script completo:

```sql
-- ============================================
-- SCRIPT DE CRIAÇÃO DE TABELAS - SUPABASE
-- BOT by YLADA
-- Execute este script completo no SQL Editor do Supabase
-- ============================================

-- PARTE 1: TABELAS BASE
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500),
    price DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    currency VARCHAR(3) NOT NULL DEFAULT 'BRL',
    max_instances INTEGER NOT NULL DEFAULT 1,
    max_flows INTEGER NOT NULL DEFAULT 3,
    max_messages_month INTEGER NOT NULL DEFAULT 1000,
    features JSONB NOT NULL DEFAULT '[]',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- PARTE 2: TABELAS DEPENDENTES
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'trial',
    plan_id INTEGER REFERENCES plans(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tenants_user_id ON tenants(user_id);

CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER UNIQUE NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    plan_id INTEGER NOT NULL REFERENCES plans(id),
    status VARCHAR(20) NOT NULL DEFAULT 'trial',
    start_date TIMESTAMP NOT NULL DEFAULT NOW(),
    end_date TIMESTAMP,
    trial_end_date TIMESTAMP,
    payment_method VARCHAR(50),
    payment_id VARCHAR(255),
    payment_status VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_tenant_id ON subscriptions(tenant_id);

CREATE TABLE IF NOT EXISTS instances (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'disconnected',
    session_data TEXT,
    session_dir VARCHAR(500),
    port INTEGER NOT NULL DEFAULT 5001,
    webhook_url VARCHAR(500),
    messages_sent INTEGER NOT NULL DEFAULT 0,
    messages_received INTEGER NOT NULL DEFAULT 0,
    last_message_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_instances_tenant_id ON instances(tenant_id);

CREATE TABLE IF NOT EXISTS flows (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    instance_id INTEGER REFERENCES instances(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    flow_data JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    trigger_keywords JSONB DEFAULT '[]',
    trigger_conditions JSONB DEFAULT '{}',
    times_executed INTEGER NOT NULL DEFAULT 0,
    last_executed_at TIMESTAMP,
    is_template BOOLEAN NOT NULL DEFAULT false,
    template_category VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_flows_tenant_id ON flows(tenant_id);
CREATE INDEX IF NOT EXISTS idx_flows_status ON flows(status);

CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    source VARCHAR(100),
    source_details JSONB DEFAULT '{}',
    score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    metadata JSONB DEFAULT '{}',
    tags JSONB DEFAULT '[]',
    conversation_id INTEGER,
    first_contact_at TIMESTAMP,
    last_contact_at TIMESTAMP,
    converted_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_leads_tenant_id ON leads(tenant_id);
CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    message TEXT NOT NULL,
    sent_to VARCHAR(20) NOT NULL,
    sent_to_name VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    sent_at TIMESTAMP,
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    related_lead_id INTEGER REFERENCES leads(id),
    related_conversation_id INTEGER,
    related_flow_id INTEGER REFERENCES flows(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notifications_tenant_id ON notifications(tenant_id);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status);

CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    instance_id INTEGER NOT NULL REFERENCES instances(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    contact_name VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    message_count INTEGER NOT NULL DEFAULT 0,
    unread_count INTEGER NOT NULL DEFAULT 0,
    last_message_at TIMESTAMP,
    is_lead BOOLEAN NOT NULL DEFAULT false,
    lead_id INTEGER REFERENCES leads(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversations_tenant_id ON conversations(tenant_id);
CREATE INDEX IF NOT EXISTS idx_conversations_instance_id ON conversations(instance_id);
CREATE INDEX IF NOT EXISTS idx_conversations_phone ON conversations(phone);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    flow_id INTEGER REFERENCES flows(id),
    direction VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL DEFAULT 'text',
    content TEXT,
    media_url VARCHAR(500),
    whatsapp_id VARCHAR(255),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    is_ai_generated BOOLEAN NOT NULL DEFAULT false,
    ai_provider VARCHAR(50),
    processed BOOLEAN NOT NULL DEFAULT false,
    flow_executed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_flow_id ON messages(flow_id);

-- PARTE 3: DADOS INICIAIS
INSERT INTO plans (name, description, price, max_instances, max_flows, max_messages_month, features, is_active)
VALUES 
    ('Grátis', 'Plano Grátis', 0.00, 1, 3, 1000, '["basic_ai", "basic_flows"]'::jsonb, true),
    ('Básico', 'Plano Básico', 49.90, 2, 10, 5000, '["ai", "flows", "notifications", "analytics"]'::jsonb, true),
    ('Profissional', 'Plano Profissional', 149.90, 5, 50, 20000, '["ai", "flows", "notifications", "analytics", "api", "templates"]'::jsonb, true),
    ('Enterprise', 'Plano Enterprise', 499.90, -1, -1, -1, '["all", "white_label", "priority_support", "custom_integrations"]'::jsonb, true)
ON CONFLICT (name) DO NOTHING;

-- Verificação
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

---

## ✅ VERIFICAÇÃO

Após executar, você deve ver:

1. **Mensagem de sucesso** no SQL Editor
2. **Lista de 10 tabelas** no final do resultado
3. **No Table Editor**, todas as tabelas aparecem

---

## 🚨 SE DER ERRO

### Erro: "relation already exists"
- ✅ **Tudo OK!** As tabelas já existem
- Você pode continuar usando

### Erro: "permission denied"
- Verifique se você tem permissão de administrador
- Verifique se está no projeto correto

### Erro: "syntax error"
- Verifique se copiou o script completo
- Verifique se não há caracteres estranhos

---

## 🎯 APÓS CRIAR TABELAS

1. **Teste a conexão:**
   - A aplicação deve conseguir conectar ao banco
   - Login deve funcionar com banco de dados

2. **Crie um usuário:**
   - Acesse: https://yladabot.com/register
   - Cadastre seu usuário
   - Agora será salvo no banco de dados!

---

**Última atualização:** 2025-01-27

