-- ============================================
-- SCRIPT DE VERIFICAÇÃO - Ver o que existe
-- Execute este script ANTES de limpar
-- ============================================

-- Ver todas as tabelas existentes
SELECT 
    table_name,
    'Tabela existe' as status
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Ver tipos das colunas 'id' em cada tabela
SELECT 
    table_name,
    column_name,
    data_type,
    CASE 
        WHEN data_type = 'integer' THEN '✅ Correto (INTEGER)'
        WHEN data_type = 'uuid' THEN '❌ ERRADO (UUID - precisa corrigir)'
        WHEN data_type = 'bigint' THEN '⚠️ BIGINT (pode funcionar)'
        ELSE '⚠️ ' || data_type
    END as status
FROM information_schema.columns
WHERE table_schema = 'public'
AND column_name = 'id'
ORDER BY table_name;

-- Ver foreign keys existentes
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    tc.constraint_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_schema = 'public'
ORDER BY tc.table_name;

-- Ver sequências existentes
SELECT 
    sequence_name,
    data_type
FROM information_schema.sequences
WHERE sequence_schema = 'public'
ORDER BY sequence_name;
