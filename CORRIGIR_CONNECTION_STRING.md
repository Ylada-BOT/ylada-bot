# 🔧 Corrigir Connection String do Supabase

## ⚠️ PROBLEMA

A connection string pode estar com formato incorreto ou usando hostname errado.

## ✅ SOLUÇÃO

### **1. Verificar Connection String no Supabase**

1. No Supabase, vá em **Settings** → **Database**
2. Role até **"Connection string"**
3. Selecione a aba **"URI"**
4. **IMPORTANTE:** Use a connection string que aparece lá (não invente)

### **2. Formatos Possíveis**

O Supabase pode mostrar diferentes formatos:

**Formato 1 (Pooler - Recomendado):**
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

**Formato 2 (Direto):**
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### **3. Codificar Senha com Caracteres Especiais**

Se sua senha tem caracteres especiais (`@`, `#`, `%`, etc.), codifique:

- `@` → `%40`
- `#` → `%23`
- `%` → `%25`
- `&` → `%26`
- `+` → `%2B`
- `=` → `%3D`

**Exemplo:**
- Senha: `Afo@1974`
- Codificada: `Afo%401974`

### **4. Atualizar .env.local**

Edite o arquivo `.env.local` e atualize a `DATABASE_URL`:

```bash
# Formato Pooler (recomendado - porta 6543)
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:Afo%401974@aws-0-sa-east-1.pooler.supabase.com:6543/postgres

# OU Formato Direto (porta 5432)
DATABASE_URL=postgresql://postgres:Afo%401974@db.tbbjqvvtsotjqgfygaaj.supabase.co:5432/postgres
```

### **5. Testar Conexão**

```bash
python3 -c "
from config.database import engine
from sqlalchemy import text
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Conexão OK!')
except Exception as e:
    print(f'❌ Erro: {e}')
"
```

---

## 🔍 VERIFICAR

1. ✅ Connection string copiada diretamente do Supabase
2. ✅ Senha codificada (se tiver caracteres especiais)
3. ✅ Formato correto (pooler ou direto)
4. ✅ Projeto Supabase está ativo

---

**Última atualização:** 23/12/2024

