-- ============================================
-- REMOVER USUÁRIO CRIADO POR ENGANO
-- Email: faulaandre@gmail.com
-- Use este script no Supabase onde você executou por engano
-- ============================================

-- OPÇÃO 1: Verificar se o usuário existe
SELECT 
    id, 
    email, 
    name, 
    is_active, 
    created_at
FROM users 
WHERE email = 'faulaandre@gmail.com';

-- ============================================
-- OPÇÃO 2: REMOVER O USUÁRIO COMPLETAMENTE
-- ============================================
-- ⚠️ ATENÇÃO: Isso vai deletar o usuário permanentemente!
-- Descomente as linhas abaixo apenas se tiver certeza:

/*
-- Deletar o usuário (isso também remove dados relacionados se houver foreign keys)
DELETE FROM users 
WHERE email = 'faulaandre@gmail.com';

-- Verificar se foi removido
SELECT COUNT(*) as total_usuarios_com_este_email
FROM users 
WHERE email = 'faulaandre@gmail.com';
*/

-- ============================================
-- OPÇÃO 3: APENAS REVERTER O NOME (se você souber o nome original)
-- ============================================
-- Se você souber qual era o nome original, descomente e ajuste:

/*
UPDATE users
SET 
    name = 'NOME_ORIGINAL_AQUI',  -- ⚠️ Substitua pelo nome original
    updated_at = NOW()
WHERE email = 'faulaandre@gmail.com';
*/

-- ============================================
-- OPÇÃO 4: DESATIVAR O USUÁRIO (mais seguro)
-- ============================================
-- Isso mantém o usuário mas o desativa:

/*
UPDATE users
SET 
    is_active = false,
    updated_at = NOW()
WHERE email = 'faulaandre@gmail.com';
*/

