# 🔑 Como Resetar a Senha do Banco de Dados no Supabase

## 📍 ONDE ENCONTRAR/RESETAR A SENHA

### **PASSO 1: Acessar Database Settings**

1. No Supabase, vá em **Settings** (⚙️) no menu lateral
2. Clique em **Database**
3. Role a página até encontrar a seção **"Database password"**

### **PASSO 2: Resetar a Senha**

1. Você verá um botão **"Reset database password"** ou **"Reset password"**
2. Clique nele
3. Uma nova senha será gerada
4. **IMPORTANTE:** Copie e anote essa senha imediatamente!
5. Você não conseguirá ver a senha novamente depois

### **PASSO 3: Usar a Nova Senha**

1. Copie a senha que foi gerada
2. Se tiver caracteres especiais, codifique:
   - `@` → `%40`
   - `#` → `%23`
   - `%` → `%25`
   - `&` → `%26`
   - `+` → `%2B`
   - `=` → `%3D`

3. Use na connection string:
```bash
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:SUA_NOVA_SENHA_AQUI@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

---

## ⚠️ IMPORTANTE

- ✅ A senha do **banco de dados** é diferente da senha da **conta Supabase**
- ✅ Você pode resetar a senha do banco mesmo tendo entrado pelo GitHub
- ✅ Anote a senha em um lugar seguro
- ✅ Se perder a senha, pode resetar novamente

---

## 📝 LOCALIZAÇÃO EXATA

```
Supabase Dashboard
  └─> Settings (⚙️)
      └─> Database
          └─> Database password
              └─> Reset database password
```

---

**Última atualização:** 27/01/2025

