-- ============================================
-- Migração: Sistema de Agentes e Fluxos por Instance
-- ============================================
-- Data: 2024-12-23
-- Descrição: Adiciona suporte para agentes de IA e fluxos específicos por telefone
-- ============================================

-- 1. Criar tabela de agentes
CREATE TABLE IF NOT EXISTS agents (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    instance_id INTEGER REFERENCES instances(id) ON DELETE CASCADE,
    
    -- Informações básicas
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Configuração de IA
    provider VARCHAR(50) NOT NULL DEFAULT 'openai',
    model VARCHAR(100) NOT NULL DEFAULT 'gpt-4o-mini',
    system_prompt TEXT NOT NULL DEFAULT 'Você é um assistente útil e amigável.',
    temperature FLOAT NOT NULL DEFAULT 0.7,
    max_tokens INTEGER NOT NULL DEFAULT 1000,
    
    -- Configurações extras (JSON)
    behavior_config JSONB DEFAULT '{}'::jsonb,
    
    -- Status
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Índices para agents
CREATE INDEX IF NOT EXISTS idx_agents_tenant_id ON agents(tenant_id);
CREATE INDEX IF NOT EXISTS idx_agents_instance_id ON agents(instance_id);
CREATE INDEX IF NOT EXISTS idx_agents_is_default ON agents(is_default);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);

-- 2. Adicionar coluna instance_id na tabela flows (NULL = compartilhado)
ALTER TABLE flows 
ADD COLUMN IF NOT EXISTS instance_id INTEGER REFERENCES instances(id) ON DELETE CASCADE;

-- Índice para flows.instance_id
CREATE INDEX IF NOT EXISTS idx_flows_instance_id ON flows(instance_id);

-- 3. Adicionar coluna agent_id na tabela instances
ALTER TABLE instances 
ADD COLUMN IF NOT EXISTS agent_id INTEGER REFERENCES agents(id) ON DELETE SET NULL;

-- Índice para instances.agent_id
CREATE INDEX IF NOT EXISTS idx_instances_agent_id ON instances(agent_id);

-- 4. Comentários para documentação
COMMENT ON TABLE agents IS 'Agentes de IA configurados para tenants ou instances específicas';
COMMENT ON COLUMN agents.instance_id IS 'NULL = agente padrão da organização, valor = agente específico da instance';
COMMENT ON COLUMN flows.instance_id IS 'NULL = fluxo compartilhado, valor = fluxo específico da instance';
COMMENT ON COLUMN instances.agent_id IS 'Agente configurado para esta instance (opcional)';

-- ============================================
-- FIM DA MIGRAÇÃO
-- ============================================


