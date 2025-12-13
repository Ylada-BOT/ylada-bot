-- ============================================
-- SCRIPT DE CRIAÇÃO DE TABELAS - SUPABASE
-- BOT by YLADA
-- Execute este script completo no SQL Editor do Supabase
-- ============================================

-- ============================================
-- PARTE 1: TABELAS BASE (sem dependências)
-- ============================================

-- Tabela: users (Usuários/Revendedores)
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

-- Tabela: plans (Planos de Assinatura)
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

-- ============================================
-- PARTE 2: TABELAS QUE DEPENDEM DE users e plans
-- ============================================

-- Tabela: tenants (Clientes Finais - Multi-tenant)
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
CREATE INDEX IF NOT EXISTS idx_tenants_subdomain ON tenants(subdomain);

-- Tabela: subscriptions (Assinaturas)
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

-- ============================================
-- PARTE 3: TABELAS QUE DEPENDEM DE tenants
-- ============================================

-- Tabela: instances (Instâncias WhatsApp)
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

-- Tabela: flows (Fluxos de Automação)
CREATE TABLE IF NOT EXISTS flows (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
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

-- Tabela: leads (Leads Capturados)
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
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);

-- Tabela: notifications (Notificações)
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
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

-- ============================================
-- PARTE 4: TABELAS QUE DEPENDEM DE instances e flows
-- ============================================

-- Tabela: conversations (Conversas)
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
CREATE INDEX IF NOT EXISTS idx_conversations_status ON conversations(status);

-- Tabela: messages (Mensagens)
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
CREATE INDEX IF NOT EXISTS idx_messages_whatsapp_id ON messages(whatsapp_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);

-- ============================================
-- PARTE 5: ATUALIZAR FOREIGN KEYS DEPENDENTES
-- ============================================

-- Adicionar foreign key para conversations em notifications (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'notifications_related_conversation_id_fkey'
    ) THEN
        ALTER TABLE notifications 
        ADD CONSTRAINT notifications_related_conversation_id_fkey 
        FOREIGN KEY (related_conversation_id) REFERENCES conversations(id);
    END IF;
END $$;

-- ============================================
-- PARTE 6: DADOS INICIAIS
-- ============================================

-- Inserir planos padrão
INSERT INTO plans (name, description, price, max_instances, max_flows, max_messages_month, features, is_active)
VALUES 
    ('Grátis', 'Plano Grátis', 0.00, 1, 3, 1000, '["basic_ai", "basic_flows"]'::jsonb, true),
    ('Básico', 'Plano Básico', 49.90, 2, 10, 5000, '["ai", "flows", "notifications", "analytics"]'::jsonb, true),
    ('Profissional', 'Plano Profissional', 149.90, 5, 50, 20000, '["ai", "flows", "notifications", "analytics", "api", "templates"]'::jsonb, true),
    ('Enterprise', 'Plano Enterprise', 499.90, -1, -1, -1, '["all", "white_label", "priority_support", "custom_integrations"]'::jsonb, true)
ON CONFLICT (name) DO NOTHING;

-- ============================================
-- FIM DO SCRIPT
-- ============================================

-- Verificação: Listar todas as tabelas criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
