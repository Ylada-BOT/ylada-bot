-- ============================================
-- SCRIPT DE LIMPEZA COMPLETA - SUPABASE
-- Remove TODAS as tabelas antigas e novas
-- Use este script se houver conflitos
-- ============================================

-- ============================================
-- REMOVER TODAS AS TABELAS (CUIDADO: APAGA DADOS!)
-- ============================================

-- Remove tabelas do novo sistema
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS leads CASCADE;
DROP TABLE IF EXISTS flows CASCADE;
DROP TABLE IF EXISTS instances CASCADE;
DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;
DROP TABLE IF EXISTS plans CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Remove tabelas antigas do sistema anterior
DROP TABLE IF EXISTS campaigns CASCADE;
DROP TABLE IF EXISTS contacts CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;

-- Remove todas as sequências
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public') 
    LOOP
        EXECUTE 'DROP SEQUENCE IF EXISTS ' || quote_ident(r.sequence_name) || ' CASCADE';
    END LOOP;
END $$;

-- Remove todas as foreign keys restantes (se houver)
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (
        SELECT constraint_name, table_name 
        FROM information_schema.table_constraints 
        WHERE constraint_type = 'FOREIGN KEY' 
        AND table_schema = 'public'
    ) 
    LOOP
        EXECUTE 'ALTER TABLE ' || quote_ident(r.table_name) || ' DROP CONSTRAINT IF EXISTS ' || quote_ident(r.constraint_name) || ' CASCADE';
    END LOOP;
END $$;

-- Verificar: Listar todas as tabelas restantes (deve estar vazio)
SELECT 
    'Tabelas restantes (devem ser 0):' as status,
    COUNT(*) as total
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';

-- Listar nomes (se houver alguma)
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- ============================================
-- FIM DO SCRIPT DE LIMPEZA
-- ============================================
-- 
-- Após executar este script, execute:
-- scripts/clean_and_create_tables.sql
-- para criar todas as tabelas do zero
-- ============================================
