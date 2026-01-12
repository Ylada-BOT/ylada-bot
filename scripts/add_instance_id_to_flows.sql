-- Adiciona a coluna instance_id na tabela flows se não existir
-- Esta coluna permite que fluxos sejam específicos de uma instância ou compartilhados (NULL)

-- Adiciona a coluna instance_id
ALTER TABLE flows 
ADD COLUMN IF NOT EXISTS instance_id INTEGER REFERENCES instances(id);

-- Cria índice para melhor performance
CREATE INDEX IF NOT EXISTS idx_flows_instance_id ON flows(instance_id);

-- Comentário para documentação
COMMENT ON COLUMN flows.instance_id IS 'ID da instância (NULL = fluxo compartilhado entre todas as instâncias)';
