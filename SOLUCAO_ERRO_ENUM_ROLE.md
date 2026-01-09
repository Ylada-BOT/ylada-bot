# 🔧 Solução: Erro Enum UserRole

## ⚠️ PROBLEMA IDENTIFICADO

Nos logs do Railway aparece:

```
[!] Erro ao conectar com banco: 'user' is not among the defined enum values. 
Enum name: userrole. Possible values: ADMIN, RESELLER, USER
```

**Causa:**
- O campo `role` no banco está com valor `'user'` (minúsculo)
- Mas o enum `UserRole` no código espera `'USER'` (maiúsculo)
- Por isso a autenticação falha!

---

## ✅ SOLUÇÃO

### **Executar Script SQL no Supabase:**

1. Acesse: https://supabase.com/dashboard
2. Vá em **SQL Editor**
3. Clique em **New query**
4. Abra o arquivo `scripts/corrigir_roles_enum.sql`
5. Copie todo o conteúdo
6. Cole no editor
7. Clique em **Run**

**Ou copie este SQL direto:**

```sql
-- Atualiza role 'user' para 'USER'
UPDATE public.users
SET 
    role = 'USER',
    updated_at = NOW()
WHERE LOWER(role) = 'user';

-- Atualiza role 'admin' para 'ADMIN' (se houver)
UPDATE public.users
SET 
    role = 'ADMIN',
    updated_at = NOW()
WHERE LOWER(role) = 'admin';
```

---

## 🔍 VERIFICAÇÃO

Após executar, verifique:

```sql
SELECT id, email, name, role 
FROM public.users;
```

Todos os `role` devem estar em **MAIÚSCULO**:
- ✅ `USER`
- ✅ `ADMIN`
- ✅ `RESELLER`

**NÃO devem estar:**
- ❌ `user` (minúsculo)
- ❌ `admin` (minúsculo)

---

## 🚀 DEPOIS DE CORRIGIR

1. **Aguarde alguns segundos** (para o banco atualizar)
2. **Tente fazer login novamente:**
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`
3. **Deve funcionar agora!** ✅

---

## 📋 CHECKLIST

- [ ] Script SQL executado no Supabase
- [ ] Todos os roles estão em MAIÚSCULO (USER, ADMIN, RESELLER)
- [ ] Tentei fazer login novamente
- [ ] Login funcionou!

---

**Última atualização:** 27/01/2025

