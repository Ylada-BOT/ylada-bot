-- ============================================
-- CORRIGIR ROLES NO BANCO DE DADOS
-- BOT by YLADA
-- Execute este script no SQL Editor do Supabase
-- ============================================
--
-- PROBLEMA: O campo 'role' está com valores minúsculos ('user')
-- mas o enum UserRole espera valores maiúsculos ('USER')
--
-- SOLUÇÃO: Atualizar todos os roles para maiúsculo
-- ============================================

-- Atualiza role 'user' para 'USER'
UPDATE public.users
SET 
    role = 'USER',
    updated_at = NOW()
WHERE LOWER(role) = 'user';

-- Atualiza role 'admin' para 'ADMIN' (se houver)
UPDATE public.users
SET 
    role = 'ADMIN',
    updated_at = NOW()
WHERE LOWER(role) = 'admin';

-- Verifica o resultado
SELECT 
    id,
    email,
    name,
    role,
    CASE 
        WHEN role IN ('ADMIN', 'RESELLER', 'USER') THEN '✅ Correto'
        ELSE '❌ Incorreto - deve ser ADMIN, RESELLER ou USER'
    END as status_role,
    is_active,
    updated_at
FROM public.users
ORDER BY id;

