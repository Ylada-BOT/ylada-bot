-- ============================================
-- CRIAR USUÁRIO ADMINISTRADOR
-- Email: faulaandre@gmail.com
-- Nome: Deise
-- Senha: Hbl@0842
-- Role: admin
-- ============================================

-- Criar usuário administrador
INSERT INTO users (email, password_hash, name, role, is_active)
VALUES (
    'faulaandre@gmail.com',
    '$2b$12$DYSStWJ2bJsUaDJ/a4QJvug8XBDUwMxI/dx/mI/3ubNM8Zv9.cfC.',
    'Deise',
    'admin',
    true
)
ON CONFLICT (email) 
DO UPDATE SET
    password_hash = EXCLUDED.password_hash,
    name = EXCLUDED.name,
    role = EXCLUDED.role,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- Verificar se usuário foi criado
SELECT id, email, name, role, is_active, created_at 
FROM users 
WHERE email = 'faulaandre@gmail.com';

