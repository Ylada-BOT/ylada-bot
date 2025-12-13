-- ============================================
-- SCRIPT CORRIGIDO - CRIAR TABELAS SUPABASE
-- Use este script se o anterior deu erro
-- ============================================

-- Primeiro, vamos limpar tabelas existentes (CUIDADO: apaga dados!)
-- Descomente as linhas abaixo apenas se quiser recriar tudo do zero
/*
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS leads CASCADE;
DROP TABLE IF EXISTS flows CASCADE;
DROP TABLE IF EXISTS instances CASCADE;
DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;
DROP TABLE IF EXISTS plans CASCADE;
DROP TABLE IF EXISTS users CASCADE;
*/

-- ============================================
-- CRIAR TABELAS NA ORDEM CORRETA
-- ============================================

-- 1. users (sem dependências)
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

-- 2. plans (sem dependências)
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

-- 3. tenants (depende de users e plans)
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'trial',
    plan_id INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_tenants_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_tenants_plan FOREIGN KEY (plan_id) REFERENCES plans(id)
);

-- 4. subscriptions (depende de tenants e plans)
CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER UNIQUE NOT NULL,
    plan_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'trial',
    start_date TIMESTAMP NOT NULL DEFAULT NOW(),
    end_date TIMESTAMP,
    trial_end_date TIMESTAMP,
    payment_method VARCHAR(50),
    payment_id VARCHAR(255),
    payment_status VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_subscriptions_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    CONSTRAINT fk_subscriptions_plan FOREIGN KEY (plan_id) REFERENCES plans(id)
);

-- 5. instances (depende de tenants)
CREATE TABLE IF NOT EXISTS instances (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
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
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_instances_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- 6. flows (depende de tenants)
CREATE TABLE IF NOT EXISTS flows (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
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
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_flows_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- 7. leads (depende de tenants)
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
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
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_leads_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- 8. conversations (depende de tenants e instances)
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    instance_id INTEGER NOT NULL,
    phone VARCHAR(20) NOT NULL,
    contact_name VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    message_count INTEGER NOT NULL DEFAULT 0,
    unread_count INTEGER NOT NULL DEFAULT 0,
    last_message_at TIMESTAMP,
    is_lead BOOLEAN NOT NULL DEFAULT false,
    lead_id INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_conversations_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    CONSTRAINT fk_conversations_instance FOREIGN KEY (instance_id) REFERENCES instances(id) ON DELETE CASCADE,
    CONSTRAINT fk_conversations_lead FOREIGN KEY (lead_id) REFERENCES leads(id)
);

-- 9. messages (depende de conversations e flows)
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    flow_id INTEGER,
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
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_messages_conversation FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    CONSTRAINT fk_messages_flow FOREIGN KEY (flow_id) REFERENCES flows(id)
);

-- 10. notifications (depende de tenants, leads, conversations, flows)
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    message TEXT NOT NULL,
    sent_to VARCHAR(20) NOT NULL,
    sent_to_name VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    sent_at TIMESTAMP,
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    related_lead_id INTEGER,
    related_conversation_id INTEGER,
    related_flow_id INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_notifications_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    CONSTRAINT fk_notifications_lead FOREIGN KEY (related_lead_id) REFERENCES leads(id),
    CONSTRAINT fk_notifications_conversation FOREIGN KEY (related_conversation_id) REFERENCES conversations(id),
    CONSTRAINT fk_notifications_flow FOREIGN KEY (related_flow_id) REFERENCES flows(id)
);

-- ============================================
-- CRIAR ÍNDICES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_tenants_user_id ON tenants(user_id);
CREATE INDEX IF NOT EXISTS idx_tenants_subdomain ON tenants(subdomain);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tenant_id ON subscriptions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_instances_tenant_id ON instances(tenant_id);
CREATE INDEX IF NOT EXISTS idx_flows_tenant_id ON flows(tenant_id);
CREATE INDEX IF NOT EXISTS idx_flows_status ON flows(status);
CREATE INDEX IF NOT EXISTS idx_leads_tenant_id ON leads(tenant_id);
CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);
CREATE INDEX IF NOT EXISTS idx_conversations_tenant_id ON conversations(tenant_id);
CREATE INDEX IF NOT EXISTS idx_conversations_instance_id ON conversations(instance_id);
CREATE INDEX IF NOT EXISTS idx_conversations_phone ON conversations(phone);
CREATE INDEX IF NOT EXISTS idx_conversations_status ON conversations(status);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_flow_id ON messages(flow_id);
CREATE INDEX IF NOT EXISTS idx_messages_whatsapp_id ON messages(whatsapp_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_notifications_tenant_id ON notifications(tenant_id);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

-- ============================================
-- DADOS INICIAIS
-- ============================================

INSERT INTO plans (name, description, price, max_instances, max_flows, max_messages_month, features, is_active)
VALUES 
    ('Grátis', 'Plano Grátis', 0.00, 1, 3, 1000, '["basic_ai", "basic_flows"]'::jsonb, true),
    ('Básico', 'Plano Básico', 49.90, 2, 10, 5000, '["ai", "flows", "notifications", "analytics"]'::jsonb, true),
    ('Profissional', 'Plano Profissional', 149.90, 5, 50, 20000, '["ai", "flows", "notifications", "analytics", "api", "templates"]'::jsonb, true),
    ('Enterprise', 'Plano Enterprise', 499.90, -1, -1, -1, '["all", "white_label", "priority_support", "custom_integrations"]'::jsonb, true)
ON CONFLICT (name) DO NOTHING;

-- ============================================
-- VERIFICAÇÃO
-- ============================================

SELECT 'Tabelas criadas:' as status;
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
