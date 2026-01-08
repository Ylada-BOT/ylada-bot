-- ============================================
-- MIGRAÇÃO: Adicionar campos de perfil ao usuário
-- BOT by YLADA
-- Execute este script no SQL Editor do Supabase
-- ============================================

-- Adiciona coluna phone (telefone) se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'phone'
    ) THEN
        ALTER TABLE users ADD COLUMN phone VARCHAR(20);
        RAISE NOTICE 'Coluna phone adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna phone já existe';
    END IF;
END $$;

-- Adiciona coluna photo_url (URL da foto de perfil) se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'photo_url'
    ) THEN
        ALTER TABLE users ADD COLUMN photo_url VARCHAR(500);
        RAISE NOTICE 'Coluna photo_url adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna photo_url já existe';
    END IF;
END $$;

-- Verificação: Lista colunas da tabela users
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

