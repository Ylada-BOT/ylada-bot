# 🔧 Solução: Tabelas Antigas no Supabase

## 🔍 Problema Identificado

Você tem **tabelas antigas** do sistema anterior que estão causando conflitos:

### Tabelas Antigas (UUID):
- ✅ `accounts` (id: uuid)
- ✅ `campaigns` (id: uuid) 
- ✅ `contacts` (id: uuid)

### Tabelas Novas (INTEGER):
- ✅ `users` (id: integer)
- ✅ `tenants` (id: integer)
- ✅ `plans` (id: integer)
- ✅ E outras...

### Conflito:
- Foreign keys antigas referenciam `accounts` (que não existe no novo schema)
- Tipos incompatíveis (UUID vs INTEGER)

---

## ✅ Solução: Limpar TUDO e Recriar

### Passo 1: Limpar TUDO (Incluindo Tabelas Antigas)

1. No Supabase: **SQL Editor** > **New query**
2. Abra o arquivo: `scripts/limpar_tudo_supabase.sql`
3. **Copie TODO o conteúdo**
4. **Cole no SQL Editor**
5. **Execute** (Run)

Este script:
- ✅ Remove TODAS as tabelas (novas e antigas)
- ✅ Remove TODAS as sequências
- ✅ Remove TODAS as foreign keys
- ✅ Deixa o banco limpo

**Resultado esperado**: "Tabelas restantes: 0"

### Passo 2: Criar Tabelas Novas

1. No Supabase: **SQL Editor** > **New query**
2. Abra o arquivo: `scripts/clean_and_create_tables.sql`
3. **Copie TODO o conteúdo**
4. **Cole no SQL Editor**
5. **Execute** (Run)

Este script:
- ✅ Cria todas as 10 tabelas do novo sistema
- ✅ Todas com INTEGER (tipos consistentes)
- ✅ Cria índices
- ✅ Insere dados iniciais (planos)

**Resultado esperado**: "Tabelas criadas: 10"

---

## 📋 Ordem de Execução

```
1. scripts/limpar_tudo_supabase.sql    → Limpa TUDO
2. scripts/clean_and_create_tables.sql → Cria tabelas novas
```

---

## ✅ Verificação Final

Após executar ambos os scripts, verifique:

```sql
-- Deve retornar 10 tabelas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

**Deve mostrar:**
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

**NÃO deve ter:**
- ❌ accounts
- ❌ campaigns
- ❌ contacts

---

## 🎯 Por que isso resolve?

1. **Remove tabelas antigas**: `accounts`, `campaigns`, `contacts` são removidas
2. **Remove foreign keys antigas**: Que referenciam tabelas que não existem mais
3. **Cria tudo do zero**: Com tipos consistentes (INTEGER)
4. **Sem conflitos**: Não há mais referências a tabelas antigas

---

## ⚠️ ATENÇÃO

- **Isso apaga TODOS os dados** (antigos e novos)
- **Faça backup** se tiver dados importantes
- **Execute na ordem correta**: primeiro limpar, depois criar

---

## 🚀 Após Criar as Tabelas

1. **Configure .env**:
```env
DATABASE_URL=postgresql://postgres:[SENHA]@db.[PROJETO].supabase.co:5432/postgres
```

2. **Execute script Python**:
```bash
python3 scripts/init_db.py
```

3. **Inicie servidor**:
```bash
python3 web/app.py
```

4. **Acesse**: http://localhost:5002/register

---

## ✅ Pronto!

Agora você tem um banco limpo com apenas as tabelas do novo sistema, sem conflitos!

---

**Dica**: Salve esses scripts - você pode precisar deles novamente se precisar recriar tudo.
