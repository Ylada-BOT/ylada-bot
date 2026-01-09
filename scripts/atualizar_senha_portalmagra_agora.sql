-- ============================================
-- ATUALIZAR SENHA DO USUÁRIO portalmagra@gmail.com
-- BOT by YLADA
-- Execute este script no SQL Editor do Supabase
-- ============================================

-- Hash bcrypt da senha "123456"
-- Gerado em: 2025-01-27
-- Hash: $2b$12$BkxUzEYyKsR851SHI8WU6uafukNJydWzduk99hHGN.d5.nVeMUAb6

UPDATE public.users
SET 
    password_hash = '$2b$12$BkxUzEYyKsR851SHI8WU6uafukNJydWzduk99hHGN.d5.nVeMUAb6',
    updated_at = NOW()
WHERE email = 'portalmagra@gmail.com';

-- Verifica se foi atualizado
SELECT 
    id,
    email,
    name,
    CASE 
        WHEN password_hash LIKE '$2b$%' THEN '✅ bcrypt (correto)'
        WHEN password_hash LIKE '$2a$%' THEN '✅ bcrypt (correto)'
        ELSE '❌ Formato incorreto'
    END as formato_hash,
    LENGTH(password_hash) as tamanho_hash,
    updated_at
FROM public.users
WHERE email = 'portalmagra@gmail.com';

