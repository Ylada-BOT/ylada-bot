# 🔍 Debug: Login 401 - O que Verificar

## ⚠️ PROBLEMA

Login ainda retorna **401 (Unauthorized)** mesmo após:
- ✅ DATABASE_URL atualizada
- ✅ Password hash atualizado para bcrypt
- ✅ Usuário existe no banco

---

## 🔍 VERIFICAÇÕES NECESSÁRIAS

### **1. Verificar Logs do Railway**

1. Railway → Deployments → Último deploy → Logs
2. Procure por:
   - `[DEBUG LOGIN] Tentando login para: portalmagra@gmail.com`
   - `[DEBUG LOGIN] DB_AVAILABLE: True/False`
   - `[DEBUG LOGIN] Usuário encontrado`
   - `[DEBUG LOGIN] Senha incorreta`
   - `[DEBUG LOGIN] Usuário não encontrado`

**O que procurar:**
- Se `DB_AVAILABLE: False` → Banco não está conectando
- Se "Usuário não encontrado" → Problema na query
- Se "Senha incorreta" → Hash pode estar errado ou senha diferente

---

### **2. Verificar se Railway Fez Redeploy**

Após atualizar a senha no banco:
- O Railway pode precisar de um redeploy
- Ou pode estar usando cache

**Solução:**
1. Railway → Deployments → **Redeploy**
2. Aguarde completar
3. Tente login novamente

---

### **3. Verificar Senha no Banco**

1. Supabase → Table Editor → `users`
2. Clique no usuário `portalmagra@gmail.com`
3. Veja o campo `password_hash`
4. Verifique:
   - ✅ Começa com `$2b$` ou `$2a$`
   - ✅ Tem 60 caracteres
   - ✅ Foi atualizado recentemente

---

### **4. Testar Senha Localmente**

Execute este script para testar se o hash funciona:

```python
import bcrypt

# Hash do banco
hash_banco = "$2b$12$BkxUzEYyKsR851SHI8WU6uafukNJydWzduk99hHGN.d5.nVeMUAb6"

# Senha que você está usando
senha = "123456"

# Verifica
if bcrypt.checkpw(senha.encode('utf-8'), hash_banco.encode('utf-8')):
    print("✅ Senha está correta!")
else:
    print("❌ Senha está incorreta!")
```

---

### **5. Verificar se Sistema Está Usando Banco ou JSON**

Nos logs do Railway, procure por:
- `[DEBUG LOGIN] DB_AVAILABLE: True` → Usando banco ✅
- `[DEBUG LOGIN] DB_AVAILABLE: False` → Usando JSON ❌

Se estiver usando JSON, o problema é que não está conectando ao banco.

---

## 🚀 SOLUÇÃO PASSO A PASSO

### **Passo 1: Verificar Logs do Railway**

1. Railway → Deployments → Último deploy → Logs
2. Procure por mensagens de login
3. Copie os erros que aparecem

### **Passo 2: Verificar Conexão com Banco**

Nos logs, procure por:
- ✅ `[✓] Banco de dados conectado`
- ✅ `Conexão bem-sucedida`
- ❌ `Tenant or user not found`
- ❌ `password authentication failed`
- ❌ `connection failed`

### **Passo 3: Fazer Redeploy no Railway**

1. Railway → Deployments → **Redeploy**
2. Aguarde completar
3. Tente login novamente

### **Passo 4: Verificar Hash no Banco**

1. Supabase → Table Editor → `users`
2. Verifique o `password_hash` do usuário
3. Deve começar com `$2b$` e ter 60 caracteres

---

## 💡 TESTE RÁPIDO

Execute este comando para testar o hash:

```bash
python3 -c "import bcrypt; hash_banco = '$2b$12$BkxUzEYyKsR851SHI8WU6uafukNJydWzduk99hHGN.d5.nVeMUAb6'; senha = '123456'; print('✅ Correto!' if bcrypt.checkpw(senha.encode('utf-8'), hash_banco.encode('utf-8')) else '❌ Incorreto!')"
```

---

## 📋 CHECKLIST

- [ ] Logs do Railway verificados
- [ ] DB_AVAILABLE está True nos logs
- [ ] Hash no banco começa com `$2b$`
- [ ] Hash tem 60 caracteres
- [ ] Railway fez redeploy após atualizar senha
- [ ] Testei hash localmente (comando acima)

---

## 🆘 PRÓXIMOS PASSOS

1. **Envie os logs do Railway** (especialmente as mensagens de login)
2. **Verifique se o hash foi atualizado** no banco
3. **Teste o hash localmente** com o comando acima

---

**Última atualização:** 27/01/2025

