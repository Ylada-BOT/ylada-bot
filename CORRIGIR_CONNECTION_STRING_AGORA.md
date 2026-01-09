# 🔧 CORRIGIR CONNECTION STRING - URGENTE

## ⚠️ PROBLEMA ENCONTRADO

Sua connection string está com formato incorreto:
```
postgresql://postgres:***@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

**Problemas:**
1. ❌ Porta errada: `5432` (deveria ser `6543` para pooler)
2. ❌ Formato incorreto: falta o PROJECT-REF após `postgres.`

---

## ✅ SOLUÇÃO RÁPIDA

### **1. Obter Connection String Correta no Supabase**

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Settings** (⚙️) → **Database**
4. Role até **"Connection string"**
5. Selecione a aba **"URI"**
6. Você verá algo assim:

**Formato CORRETO (Pooler):**
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**Exemplo:**
```
postgresql://postgres.abcdefghijklmnop:MinhaSenha123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

---

### **2. Codificar Senha (se tiver caracteres especiais)**

Se sua senha tem `@`, `#`, `%`, etc., codifique:

| Caractere | Código |
|-----------|--------|
| `@` | `%40` |
| `#` | `%23` |
| `%` | `%25` |
| `&` | `%26` |
| `+` | `%2B` |
| `=` | `%3D` |

**Exemplo:**
- Senha: `Afo@1974`
- Codificada: `Afo%401974`

---

### **3. Atualizar .env.local**

1. Abra o arquivo `.env.local` na raiz do projeto
2. Encontre a linha `DATABASE_URL=`
3. Substitua pela connection string correta do Supabase
4. **IMPORTANTE:** Use a porta **6543** (não 5432)
5. **IMPORTANTE:** Inclua o PROJECT-REF após `postgres.`

**Exemplo correto:**
```bash
DATABASE_URL=postgresql://postgres.abcdefghijklmnop:MinhaSenha123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

---

### **4. Testar Conexão**

Após atualizar, teste:

```bash
python3 scripts/test_database_connection.py
```

Deve mostrar: ✅ **Conexão bem-sucedida!**

---

## 🔍 VERIFICAÇÕES

- [ ] Connection string copiada diretamente do Supabase
- [ ] Porta **6543** (não 5432) quando usar pooler
- [ ] PROJECT-REF incluído após `postgres.`
- [ ] Senha codificada (se tiver caracteres especiais)
- [ ] Arquivo `.env.local` salvo

---

## 📝 NOTAS

- ⚠️ **NUNCA** commite o `.env.local` no Git
- ✅ O arquivo já está no `.gitignore`
- ✅ Use sempre o formato **pooler** (porta 6543) quando possível

---

**Última atualização:** 27/01/2025

