-- ============================================
-- REMOVER ADMINISTRADOR CRIADO POR ENGANO
-- Email: faulaandre@gmail.com
-- Use este script no Supabase onde você executou por engano
-- ============================================

-- ============================================
-- PASSO 1: VERIFICAR O QUE FOI CRIADO
-- ============================================
-- Execute primeiro para ver o que existe:

SELECT 
    id, 
    email, 
    name, 
    role,
    is_active, 
    created_at,
    updated_at
FROM users 
WHERE email = 'faulaandre@gmail.com';

-- ============================================
-- PASSO 2: VERIFICAR DEPENDÊNCIAS
-- ============================================
-- Verificar se há dados relacionados (tenants, etc.):

SELECT 
    'tenants' as tabela,
    COUNT(*) as total_registros
FROM tenants 
WHERE user_id IN (SELECT id FROM users WHERE email = 'faulaandre@gmail.com')

UNION ALL

SELECT 
    'subscriptions' as tabela,
    COUNT(*) as total_registros
FROM subscriptions 
WHERE tenant_id IN (
    SELECT id FROM tenants 
    WHERE user_id IN (SELECT id FROM users WHERE email = 'faulaandre@gmail.com')
)

UNION ALL

SELECT 
    'instances' as tabela,
    COUNT(*) as total_registros
FROM instances 
WHERE tenant_id IN (
    SELECT id FROM tenants 
    WHERE user_id IN (SELECT id FROM users WHERE email = 'faulaandre@gmail.com')
);

-- ============================================
-- PASSO 3: REMOVER COMPLETAMENTE
-- ============================================
-- ⚠️ ATENÇÃO: Isso vai deletar o usuário e TODOS os dados relacionados!
-- ⚠️ Se houver foreign keys com CASCADE, vai deletar tenants, subscriptions, etc.
-- 
-- Descomente as linhas abaixo apenas se tiver CERTEZA:

/*
-- Primeiro, remover dados relacionados (se não tiver CASCADE)
DELETE FROM instances 
WHERE tenant_id IN (
    SELECT id FROM tenants 
    WHERE user_id IN (SELECT id FROM users WHERE email = 'faulaandre@gmail.com')
);

DELETE FROM subscriptions 
WHERE tenant_id IN (
    SELECT id FROM tenants 
    WHERE user_id IN (SELECT id FROM users WHERE email = 'faulaandre@gmail.com')
);

DELETE FROM tenants 
WHERE user_id IN (SELECT id FROM users WHERE email = 'faulaandre@gmail.com');

-- Por último, remover o usuário
DELETE FROM users 
WHERE email = 'faulaandre@gmail.com';

-- Verificar se foi removido
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '✅ Usuário removido com sucesso'
        ELSE '❌ Ainda existe ' || COUNT(*) || ' usuário(s) com este email'
    END as status
FROM users 
WHERE email = 'faulaandre@gmail.com';
*/

-- ============================================
-- PASSO 4: OPÇÃO MAIS SEGURA - APENAS DESATIVAR
-- ============================================
-- Isso mantém o usuário mas o desativa (não pode fazer login):

/*
UPDATE users
SET 
    is_active = false,
    role = 'user',  -- Remove privilégios de admin
    updated_at = NOW()
WHERE email = 'faulaandre@gmail.com';

-- Verificar
SELECT 
    id, 
    email, 
    name, 
    role,
    is_active,
    '✅ Usuário desativado' as status
FROM users 
WHERE email = 'faulaandre@gmail.com';
*/

-- ============================================
-- PASSO 5: REMOVER APENAS O USUÁRIO (se não houver dependências)
-- ============================================
-- Se não houver tenants ou dados relacionados, pode deletar direto:

/*
DELETE FROM users 
WHERE email = 'faulaandre@gmail.com'
AND NOT EXISTS (
    SELECT 1 FROM tenants 
    WHERE user_id = users.id
);

-- Verificar
SELECT COUNT(*) as usuarios_restantes
FROM users 
WHERE email = 'faulaandre@gmail.com';
*/

