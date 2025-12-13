# 🔧 CORREÇÃO: Erro "column tenant_id does not exist"

## ❌ Problema

Ao executar o script SQL, você recebeu:
```
ERROR: 42703: column "tenant_id" does not exist
```

## ✅ Solução

O problema ocorre quando as tabelas são criadas fora de ordem ou quando há dependências circulares.

### Opção 1: Usar Script Corrigido (Recomendado)

1. **Abra o arquivo**: `scripts/create_tables_supabase_fix.sql`
2. **Copie TODO o conteúdo**
3. **Cole no SQL Editor do Supabase**
4. **Execute** (Run)

Este script:
- ✅ Cria tabelas na ordem correta
- ✅ Usa constraints nomeadas (mais seguro)
- ✅ Cria índices depois das tabelas
- ✅ Tem tratamento melhor de erros

### Opção 2: Limpar e Recriar (Se já tentou antes)

Se você já tentou executar o script anterior e deu erro:

1. **Execute primeiro** (para limpar):
```sql
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
```

2. **Depois execute** o script `create_tables_supabase_fix.sql`

### Opção 3: Criar Manualmente (Passo a Passo)

Se ainda der erro, crie as tabelas uma por uma:

#### 1. Criar users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### 2. Criar plans
```sql
CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500),
    price DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    currency VARCHAR(3) NOT NULL DEFAULT 'BRL',
    max_instances INTEGER NOT NULL DEFAULT 1,
    max_flows INTEGER NOT NULL DEFAULT 3,
    max_messages_month INTEGER NOT NULL DEFAULT 1000,
    features JSONB NOT NULL DEFAULT '[]',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### 3. Criar tenants
```sql
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'trial',
    plan_id INTEGER REFERENCES plans(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### 4. Continuar com as outras tabelas na ordem:
- subscriptions
- instances
- flows
- leads
- conversations
- messages
- notifications

---

## 🎯 Ordem Correta de Criação

1. ✅ **users** (sem dependências)
2. ✅ **plans** (sem dependências)
3. ✅ **tenants** (depende de users e plans)
4. ✅ **subscriptions** (depende de tenants e plans)
5. ✅ **instances** (depende de tenants)
6. ✅ **flows** (depende de tenants)
7. ✅ **leads** (depende de tenants)
8. ✅ **conversations** (depende de tenants e instances)
9. ✅ **messages** (depende de conversations e flows)
10. ✅ **notifications** (depende de tenants, leads, conversations, flows)

---

## ✅ Verificação

Após criar as tabelas, verifique:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

Deve retornar 10 tabelas:
- conversations
- flows
- instances
- leads
- messages
- notifications
- plans
- subscriptions
- tenants
- users

---

## 📝 Próximo Passo

Depois de criar as tabelas com sucesso:

1. Execute: `python3 scripts/init_db.py` (para criar dados iniciais)
2. Configure `.env` com DATABASE_URL
3. Inicie o servidor: `python3 web/app.py`

---

**Use o arquivo `create_tables_supabase_fix.sql` - ele resolve o problema!** ✅
