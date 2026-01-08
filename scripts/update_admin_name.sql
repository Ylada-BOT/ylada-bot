-- ============================================
-- ATUALIZAR NOME DO ADMINISTRADOR
-- Email: faulaandre@gmail.com
-- Nome: André Paula (atualizado)
-- ============================================

-- Atualizar nome do administrador
UPDATE users
SET 
    name = 'André Paula',
    updated_at = NOW()
WHERE email = 'faulaandre@gmail.com';

-- Verificar se nome foi atualizado
-- (Seleciona apenas colunas básicas que sempre existem)
SELECT 
    id, 
    email, 
    name, 
    is_active, 
    updated_at
FROM users 
WHERE email = 'faulaandre@gmail.com';

-- Se quiser verificar se a coluna role existe e seu valor:
-- (Execute separadamente se necessário)
/*
SELECT column_name 
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name = 'users' 
AND column_name = 'role';
*/

