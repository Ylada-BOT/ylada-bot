-- ============================================
-- ATUALIZAÇÃO: Aumentar tamanho do campo phone
-- BOT by YLADA
-- Execute este script no SQL Editor do Supabase
-- ============================================

-- Atualiza o tamanho do campo phone para suportar números internacionais
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'users' 
        AND column_name = 'phone'
    ) THEN
        -- Altera o tamanho do campo de VARCHAR(20) para VARCHAR(30)
        ALTER TABLE public.users ALTER COLUMN phone TYPE VARCHAR(30);
        RAISE NOTICE 'Campo phone atualizado para VARCHAR(30) com sucesso';
    ELSE
        RAISE NOTICE 'Coluna phone não existe. Execute primeiro o script add_user_profile_fields.sql';
    END IF;
END $$;

-- Verificação: Mostra o tamanho atual do campo
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name = 'users' 
AND column_name = 'phone';

