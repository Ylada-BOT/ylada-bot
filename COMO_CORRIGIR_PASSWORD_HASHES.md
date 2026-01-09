# 🔧 Como Corrigir Password Hashes no Banco

## ⚠️ PROBLEMA IDENTIFICADO

Os `password_hash` no banco estão em formato **SHA256**, mas o sistema usa **bcrypt**:

- ❌ **SHA256**: `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92` (64 caracteres)
- ✅ **bcrypt**: `$2b$12$02SDNg2ZX6Ul5CbcuT8YFeqV/9DDJvqrhibrz.M0IOTCsRgfOcp3e` (60 caracteres, começa com `$2b$`)

**Por isso o login não funciona!** O sistema tenta verificar com bcrypt, mas o hash está em SHA256.

---

## ✅ SOLUÇÃO RÁPIDA

### **Opção 1: Executar Script SQL (Recomendado)**

1. **Gere um hash bcrypt novo:**
   ```bash
   python3 -c "import bcrypt; print(bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8'))"
   ```

2. **Copie o hash gerado** (será diferente a cada vez)

3. **No Supabase:**
   - Vá em **SQL Editor**
   - Clique em **New query**
   - Abra o arquivo `scripts/corrigir_password_hashes.sql`
   - **Substitua** o hash no script pelo hash que você gerou
   - Cole no editor
   - Clique em **Run**

4. **Teste o login:**
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`

---

### **Opção 2: Atualizar Manualmente no Table Editor**

1. **Gere hash bcrypt:**
   ```bash
   python3 -c "import bcrypt; print(bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8'))"
   ```

2. **No Supabase:**
   - Vá em **Table Editor** → `users`
   - Clique no usuário `portalmagra@gmail.com`
   - Edite o campo `password_hash`
   - Cole o hash bcrypt gerado
   - Salve

3. **Teste o login**

---

### **Opção 3: Usar Script Python (Mais Automático)**

1. **Execute o script:**
   ```bash
   python3 scripts/atualizar_senha_portalmagra.py
   ```

2. **Isso vai:**
   - Gerar hash bcrypt automaticamente
   - Conectar ao banco
   - Atualizar a senha
   - Verificar se funcionou

---

## 🔍 VERIFICAR SE ESTÁ CORRETO

### **Hash Bcrypt (Correto):**
- ✅ Começa com `$2b$` ou `$2a$`
- ✅ Tem 60 caracteres
- ✅ Exemplo: `$2b$12$02SDNg2ZX6Ul5CbcuT8YFeqV/9DDJvqrhibrz.M0IOTCsRgfOcp3e`

### **Hash SHA256 (Incorreto):**
- ❌ Tem 64 caracteres
- ❌ Não começa com `$`
- ❌ Exemplo: `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`

---

## 📋 CHECKLIST

- [ ] Gerei hash bcrypt novo
- [ ] Atualizei no banco (via SQL ou Table Editor)
- [ ] Verifiquei que o hash começa com `$2b$`
- [ ] Testei login com senha "123456"

---

## 💡 DICA

**Para cada usuário, você pode ter senhas diferentes:**

1. Gere hash para senha 1:
   ```bash
   python3 -c "import bcrypt; print(bcrypt.hashpw(b'minhasenha1', bcrypt.gensalt()).decode('utf-8'))"
   ```

2. Gere hash para senha 2:
   ```bash
   python3 -c "import bcrypt; print(bcrypt.hashpw(b'minhasenha2', bcrypt.gensalt()).decode('utf-8'))"
   ```

3. Atualize cada usuário com seu hash específico

---

## 🚀 PRÓXIMOS PASSOS

1. **Execute o script SQL** ou atualize manualmente
2. **Teste o login** com senha "123456"
3. **Se funcionar**, o problema estava nos password hashes!
4. **Se não funcionar**, verifique os logs do Railway

---

**Última atualização:** 27/01/2025

