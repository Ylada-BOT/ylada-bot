-- Script para atualizar a senha do usuário portalmagra
-- ATENÇÃO: Este script requer que você gere o hash bcrypt primeiro
-- Execute o script Python: python3 scripts/atualizar_senha_portalmagra.py
-- OU use a função do PostgreSQL para gerar bcrypt (se disponível)

-- Opção 1: Se você já tem o hash bcrypt, substitua 'SEU_HASH_BCRYPT_AQUI' abaixo
-- UPDATE public.users
-- SET password_hash = 'SEU_HASH_BCRYPT_AQUI',
--     updated_at = NOW()
-- WHERE email = 'portalmagra@gmail.com';

-- Opção 2: Execute o script Python que gera o hash automaticamente
-- python3 scripts/atualizar_senha_portalmagra.py

-- Verifica o usuário atual
SELECT 
    id,
    email,
    name,
    role,
    is_active,
    LEFT(password_hash, 20) as hash_preview,
    created_at
FROM public.users
WHERE email = 'portalmagra@gmail.com';

