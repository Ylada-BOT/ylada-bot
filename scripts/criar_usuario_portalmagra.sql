-- Script para criar usuário PORTAL MAGRA no banco de dados
-- Execute este script no Supabase SQL Editor

-- Hash SHA256 da senha "123456"
-- Hash: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92

-- Verifica se o usuário já existe
DO $$
BEGIN
    -- Verifica se o usuário já existe
    IF NOT EXISTS (SELECT 1 FROM public.users WHERE email = 'portalmagra@gmail.com') THEN
        -- Cria o usuário
        INSERT INTO public.users (
            email,
            password_hash,
            name,
            role,
            is_active,
            created_at,
            updated_at
        ) VALUES (
            'portalmagra@gmail.com',
            '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
            'PORTAL MAGRA',
            'user',
            true,
            NOW(),
            NOW()
        );
        
        RAISE NOTICE 'Usuário portalmagra@gmail.com criado com sucesso!';
    ELSE
        RAISE NOTICE 'Usuário portalmagra@gmail.com já existe.';
        
        -- Atualiza a senha caso necessário
        UPDATE public.users
        SET 
            password_hash = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
            name = 'PORTAL MAGRA',
            is_active = true,
            updated_at = NOW()
        WHERE email = 'portalmagra@gmail.com';
        
        RAISE NOTICE 'Senha e dados do usuário atualizados.';
    END IF;
END $$;

-- Verifica o resultado
SELECT 
    id,
    email,
    name,
    role,
    is_active,
    created_at
FROM public.users
WHERE email = 'portalmagra@gmail.com';

