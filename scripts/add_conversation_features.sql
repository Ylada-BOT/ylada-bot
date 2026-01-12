-- Script para adicionar funcionalidades avançadas às conversas
-- Baseado na análise do BotConversa

-- 1. Adicionar campos de atribuição e automação
ALTER TABLE conversations 
ADD COLUMN IF NOT EXISTS assigned_to INTEGER REFERENCES users(id),
ADD COLUMN IF NOT EXISTS tags JSONB DEFAULT '[]'::jsonb,
ADD COLUMN IF NOT EXISTS automation_enabled BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS contact_email VARCHAR(255),
ADD COLUMN IF NOT EXISTS contact_cpf VARCHAR(20),
ADD COLUMN IF NOT EXISTS extra_metadata JSONB DEFAULT '{}'::jsonb;

-- 2. Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_conversations_assigned_to ON conversations(assigned_to);
CREATE INDEX IF NOT EXISTS idx_conversations_tags ON conversations USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_conversations_status ON conversations(status);
CREATE INDEX IF NOT EXISTS idx_conversations_automation_enabled ON conversations(automation_enabled);

-- 3. Comentários para documentação
COMMENT ON COLUMN conversations.assigned_to IS 'ID do usuário/agente atribuído à conversa';
COMMENT ON COLUMN conversations.tags IS 'Array de tags/etiquetas da conversa (JSON)';
COMMENT ON COLUMN conversations.automation_enabled IS 'Se a automação está habilitada para este contato';
COMMENT ON COLUMN conversations.contact_email IS 'Email do contato (se disponível)';
COMMENT ON COLUMN conversations.contact_cpf IS 'CPF do contato (se disponível)';
COMMENT ON COLUMN conversations.extra_metadata IS 'Metadados adicionais da conversa (JSON)';

