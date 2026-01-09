# ✅ USAR PORTA 5432 ESTÁ OK!

## 📝 IMPORTANTE

Se o Supabase está mostrando a porta **5432** mesmo com "Session pooler" selecionado, **está correto!**

O formato da connection string que você tem agora está **CORRETO**:
```
postgresql://postgres.tbbjqvvtsotjqgfygaaj:[YOUR-PASSWORD]@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

**O que importa:**
- ✅ Tem `postgres.tbbjqvvtsotjqgfygaaj` (com o PROJECT-REF)
- ✅ Usa `pooler.supabase.com` (não `db.xxx.supabase.co`)
- ✅ Porta 5432 está OK para Session Pooler neste caso

---

## 🔧 O QUE FAZER AGORA

### **1. Copiar a Connection String do Supabase**

1. Na tela do Supabase, copie a connection string completa
2. Ela deve estar assim:
   ```
   postgresql://postgres.tbbjqvvtsotjqgfygaaj:[YOUR-PASSWORD]@aws-0-us-west-2.pooler.supabase.com:5432/postgres
   ```

### **2. Substituir [YOUR-PASSWORD] pela Senha Real**

**IMPORTANTE:** Você precisa substituir `[YOUR-PASSWORD]` pela senha real do banco!

**Onde encontrar a senha:**
- É a senha que você criou quando criou o projeto no Supabase
- Se não lembrar, pode resetar:
  - Na mesma tela, role até "Reset your database password"
  - Clique em "Database Settings"
  - Reset a senha e anote a nova

**Se a senha tiver caracteres especiais, codifique:**
- `@` → `%40`
- `#` → `%23`
- `%` → `%25`
- `&` → `%26`

**Exemplo:**
- Senha: `MinhaSenha@123`
- Connection string: `postgresql://postgres.tbbjqvvtsotjqgfygaaj:MinhaSenha%40123@aws-0-us-west-2.pooler.supabase.com:5432/postgres`

### **3. Atualizar o Arquivo .env.local**

1. Abra o arquivo `.env.local` na raiz do projeto
2. Encontre a linha `DATABASE_URL=`
3. Substitua pela connection string completa (com a senha real)
4. Salve o arquivo

**Exemplo no .env.local:**
```bash
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:MinhaSenha123@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

### **4. Testar a Conexão**

```bash
python3 scripts/test_database_connection.py
```

---

## ⚠️ PROBLEMA COMUM

O erro "Tenant or user not found" geralmente acontece quando:
- ❌ A senha está errada ou não foi substituída
- ❌ A senha tem caracteres especiais e não foi codificada
- ❌ O projeto Supabase está pausado

---

## ✅ CHECKLIST

- [ ] Connection string copiada do Supabase
- [ ] `[YOUR-PASSWORD]` substituído pela senha real
- [ ] Caracteres especiais codificados (se houver)
- [ ] Arquivo `.env.local` atualizado e salvo
- [ ] Teste executado

---

**Última atualização:** 27/01/2025

