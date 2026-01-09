# 🔧 Solução: Erro "Tenant or user not found" no Supabase

## ⚠️ PROBLEMA

O erro indica que a conexão com o Supabase está falhando:
```
FATAL: Tenant or user not found
connection to server at "aws-0-us-west-2.pooler.supabase.com" (35.160.209.8), port 5432 failed
```

## 🔍 CAUSAS POSSÍVEIS

1. **Connection string incorreta ou desatualizada**
2. **Senha do banco errada ou alterada**
3. **Projeto Supabase pausado ou deletado**
4. **Formato incorreto da connection string (caracteres especiais não codificados)**
5. **Uso de porta/formato errado (5432 vs 6543)**

## ✅ SOLUÇÃO PASSO A PASSO

### **1. Verificar Status do Projeto Supabase**

1. Acesse: https://supabase.com/dashboard
2. Verifique se o projeto está **ativo** (não pausado)
3. Se estiver pausado, clique em **"Restore project"**

### **2. Obter Connection String Correta**

1. No Supabase, vá em **Settings** (⚙️) → **Database**
2. Role até **"Connection string"**
3. Selecione a aba **"URI"**
4. **IMPORTANTE:** Copie a string EXATA que aparece lá

**Formato esperado (Pooler - Recomendado):**
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**Formato alternativo (Direto):**
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### **3. Codificar Senha com Caracteres Especiais**

Se sua senha tem caracteres especiais, **codifique-os**:

| Caractere | Código |
|-----------|--------|
| `@` | `%40` |
| `#` | `%23` |
| `%` | `%25` |
| `&` | `%26` |
| `+` | `%2B` |
| `=` | `%3D` |
| `/` | `%2F` |
| `?` | `%3F` |
| ` ` (espaço) | `%20` |

**Exemplo:**
- Senha original: `Afo@1974`
- Senha codificada: `Afo%401974`

### **4. Verificar/Criar Arquivo .env.local**

1. Na raiz do projeto, verifique se existe `.env.local`
2. Se não existir, crie o arquivo:
```bash
touch .env.local
```

3. Adicione a `DATABASE_URL` com a connection string correta:

```bash
# Database - Supabase
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[SENHA_CODIFICADA]@aws-0-[REGION].pooler.supabase.com:6543/postgres

# Exemplo real (substitua pelos seus valores):
# DATABASE_URL=postgresql://postgres.abcdefghijklmnop:MinhaSenha123%40@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### **5. Testar Conexão**

Execute o script de teste:

```bash
python3 scripts/test_database_connection.py
```

Ou teste manualmente:

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

### **6. Se Ainda Não Funcionar**

#### **Opção A: Resetar Senha do Banco**

1. No Supabase, vá em **Settings** → **Database**
2. Role até **"Database password"**
3. Clique em **"Reset database password"**
4. **ANOTE A NOVA SENHA**
5. Atualize a `DATABASE_URL` no `.env.local`

#### **Opção B: Verificar Região do Projeto**

O erro mostra `aws-0-us-west-2` (Oregon, EUA). Verifique:

1. No Supabase, vá em **Settings** → **General**
2. Verifique a **"Region"** do projeto
3. Se for diferente, atualize a connection string com a região correta

#### **Opção C: Usar Formato Direto (sem Pooler)**

Se o pooler não funcionar, tente o formato direto:

```bash
DATABASE_URL=postgresql://postgres:[SENHA_CODIFICADA]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### **7. Reiniciar Servidor**

Após corrigir a connection string:

```bash
# Pare o servidor (Ctrl+C)
# E inicie novamente
python3 web/app.py
```

## 🔍 VERIFICAÇÕES FINAIS

- [ ] Projeto Supabase está ativo (não pausado)
- [ ] Connection string copiada diretamente do Supabase
- [ ] Senha codificada (se tiver caracteres especiais)
- [ ] Formato correto (pooler ou direto)
- [ ] Arquivo `.env.local` existe e está na raiz do projeto
- [ ] Servidor reiniciado após alterações

## 📝 NOTAS IMPORTANTES

- ⚠️ **NUNCA** commite o arquivo `.env.local` no Git
- ⚠️ A senha do banco é **confidencial**
- ✅ O arquivo `.env.local` já está no `.gitignore`
- ✅ Use sempre o formato **pooler** (porta 6543) quando possível (melhor performance)

---

**Última atualização:** 27/01/2025

