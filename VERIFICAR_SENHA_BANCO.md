# 🔐 Verificar Senha do Banco

## ⚠️ PROBLEMA

Erro de autenticação ao conectar no Supabase. A senha pode estar incorreta.

## ✅ SOLUÇÃO

### **Opção 1: Verificar Senha Atual**

A senha que está no `.env.local` é: `Afo@1974` (codificada como `Afo%401974`)

**Se você resetou a senha:**
- A senha antiga não funciona mais
- Precisa atualizar o `.env.local` com a nova senha

### **Opção 2: Resetar Senha no Supabase**

1. No Supabase, vá em **Settings** → **Database**
2. Role até **"Database password"**
3. Clique em **"Reset database password"**
4. **ANOTE A NOVA SENHA** que aparecer
5. Me envie a nova senha e eu atualizo o `.env.local`

### **Opção 3: Usar Senha Atual (se não resetou)**

Se você **NÃO** resetou a senha, a senha atual é: `Afo@1974`

Vou testar novamente com essa senha.

---

## 📝 IMPORTANTE

- Se você resetou a senha, preciso da **nova senha** para atualizar
- A senha será codificada automaticamente (ex: `@` vira `%40`)
- O arquivo `.env.local` está protegido no `.gitignore`

---

**Me diga:**
1. Você resetou a senha? (Sim ou Não)
2. Se sim, qual é a nova senha?

