-- ============================================
-- CORRIGIR PASSWORD HASHES NO BANCO
-- BOT by YLADA
-- Execute este script no SQL Editor do Supabase
-- ============================================
-- 
-- PROBLEMA: Os password_hash estão em SHA256, mas o sistema usa bcrypt
-- SOLUÇÃO: Atualizar para hash bcrypt correto
--
-- IMPORTANTE: Este script atualiza a senha para "123456" para todos os usuários
-- Se você quiser senhas diferentes, gere o hash bcrypt e atualize manualmente
-- ============================================

-- Hash bcrypt da senha "123456"
-- Gerado com: bcrypt.hashpw(b'123456', bcrypt.gensalt())
-- Este hash é único a cada geração, então você precisa gerar um novo

-- ATENÇÃO: Substitua o hash abaixo por um hash bcrypt gerado no Python!
-- Execute: python3 -c "import bcrypt; print(bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8'))"

-- Hash bcrypt de exemplo (SUBSTITUA pelo hash que você gerar):
-- $2b$12$02SDNg2ZX6Ul5CbcuT8YFeqV/9DDJvqrhibrz.M0IOTCsRgfOcp3e

-- ============================================
-- ATUALIZAR SENHA DO USUÁRIO portalmagra@gmail.com
-- ============================================

UPDATE public.users
SET 
    password_hash = '$2b$12$02SDNg2ZX6Ul5CbcuT8YFeqV/9DDJvqrhibrz.M0IOTCsRgfOcp3e',
    updated_at = NOW()
WHERE email = 'portalmagra@gmail.com';

-- ============================================
-- ATUALIZAR SENHA DO USUÁRIO admin@ylada.com
-- ============================================

UPDATE public.users
SET 
    password_hash = '$2b$12$02SDNg2ZX6Ul5CbcuT8YFeqV/9DDJvqrhibrz.M0IOTCsRgfOcp3e',
    updated_at = NOW()
WHERE email = 'admin@ylada.com';

-- ============================================
-- ATUALIZAR SENHA DO USUÁRIO yladanutri@gmail.com
-- ============================================

UPDATE public.users
SET 
    password_hash = '$2b$12$02SDNg2ZX6Ul5CbcuT8YFeqV/9DDJvqrhibrz.M0IOTCsRgfOcp3e',
    updated_at = NOW()
WHERE email = 'yladanutri@gmail.com';

-- ============================================
-- ATUALIZAR SENHA DO USUÁRIO faulaandre@gmail.com
-- ============================================

UPDATE public.users
SET 
    password_hash = '$2b$12$02SDNg2ZX6Ul5CbcuT8YFeqV/9DDJvqrhibrz.M0IOTCsRgfOcp3e',
    updated_at = NOW()
WHERE email = 'faulaandre@gmail.com';

-- ============================================
-- VERIFICAÇÃO: Lista usuários atualizados
-- ============================================

SELECT 
    id,
    email,
    name,
    role,
    CASE 
        WHEN password_hash LIKE '$2b$%' THEN '✅ bcrypt (correto)'
        WHEN password_hash LIKE '$2a$%' THEN '✅ bcrypt (correto)'
        ELSE '❌ SHA256 ou outro formato (incorreto)'
    END as formato_hash,
    LENGTH(password_hash) as tamanho_hash,
    is_active,
    updated_at
FROM public.users
ORDER BY id;

-- ============================================
-- NOTAS:
-- ============================================
-- 1. Todos os usuários terão senha "123456" após executar este script
-- 2. O hash bcrypt é único a cada geração (salt aleatório)
-- 3. Se quiser senhas diferentes, gere hashes separados para cada usuário
-- 4. Para gerar novo hash: python3 -c "import bcrypt; print(bcrypt.hashpw(b'SENHA', bcrypt.gensalt()).decode('utf-8'))"
-- 5. Após atualizar, teste o login com email e senha "123456"

