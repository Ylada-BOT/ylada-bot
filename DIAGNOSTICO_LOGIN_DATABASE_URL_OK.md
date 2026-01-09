# 🔍 Diagnóstico: DATABASE_URL Correta mas Login Não Funciona

## ✅ DATABASE_URL ESTÁ CORRETA

A connection string está correta, então o problema é outro.

---

## 🔍 POSSÍVEIS CAUSAS

### **1. Usuário Não Existe no Banco de Dados** ⚠️ (Mais Provável)

O usuário `portalmagra@gmail.com` pode não existir no banco de produção.

**Como verificar:**
1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Table Editor** → `users`
4. Procure por `portalmagra@gmail.com`
5. Se **NÃO existir**, esse é o problema!

**Solução:**
- Criar usuário via dashboard (registro)
- Ou criar via SQL no Supabase

---

### **2. Senha do Usuário Está Errada**

O usuário existe, mas a senha que você está usando não corresponde.

**Solução:**
- Tentar resetar senha
- Ou criar novo usuário
- Ou atualizar senha via SQL

---

### **3. Sistema Está Usando Modo Simplificado (Arquivo JSON)**

O sistema pode estar tentando autenticar via arquivo JSON em vez do banco.

**Como verificar:**
1. No Railway, veja os logs
2. Procure por:
   - `[DEBUG LOGIN] DB_AVAILABLE: True` ou `False`
   - `[DEBUG LOGIN] SIMPLE_AUTH_AVAILABLE: True` ou `False`

**Se `DB_AVAILABLE: False`:**
- O sistema não está conseguindo conectar ao banco
- Mesmo com DATABASE_URL correta, pode haver outro problema

---

### **4. Erro de Conexão no Logs**

Mesmo com DATABASE_URL correta, pode haver erro de conexão.

**Como verificar:**
1. Railway → Deployments → Último deploy → Logs
2. Procure por:
   - ❌ "Tenant or user not found"
   - ❌ "password authentication failed"
   - ❌ "connection failed"
   - ❌ "Erro ao conectar ao banco"

---

## ✅ SOLUÇÃO PASSO A PASSO

### **PASSO 1: Verificar se Usuário Existe no Banco**

1. Acesse: https://supabase.com/dashboard
2. Table Editor → `users`
3. Procure por `portalmagra@gmail.com`

**Se NÃO existir:**
- Vá para Passo 2

**Se existir:**
- Vá para Passo 3

---

### **PASSO 2: Criar Usuário no Banco**

#### **Opção A: Via Dashboard (Mais Fácil)**

1. Acesse: `https://yladabot.com/register`
2. Preencha:
   - Email: `portalmagra@gmail.com`
   - Senha: (escolha uma senha)
   - Nome: `PORTAL MAGRA`
3. Clique em **"Cadastrar"**
4. Tente fazer login

#### **Opção B: Via SQL (Se Dashboard Não Funcionar)**

1. No Supabase, vá em **SQL Editor**
2. Clique em **New query**
3. Cole este script:

```sql
-- Verifica se usuário existe
SELECT * FROM public.users WHERE email = 'portalmagra@gmail.com';

-- Se não existir, cria (senha: 123456)
-- IMPORTANTE: O sistema usa bcrypt, não SHA256!
-- Este é um exemplo - você precisa gerar o hash bcrypt correto

INSERT INTO public.users (
    email,
    password_hash,
    name,
    role,
    is_active,
    created_at,
    updated_at
) 
SELECT 
    'portalmagra@gmail.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5',  -- Hash bcrypt de "123456"
    'PORTAL MAGRA',
    'user',
    true,
    NOW(),
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM public.users WHERE email = 'portalmagra@gmail.com'
);
```

4. Clique em **Run**
5. Verifique se apareceu "Success"

**⚠️ IMPORTANTE:** O hash acima é um exemplo. Para funcionar, você precisa:
- Gerar um hash bcrypt da senha que você quer usar
- Ou usar o dashboard para criar o usuário (mais fácil)

---

### **PASSO 3: Verificar Logs do Railway**

1. Railway → Deployments → Último deploy → Logs
2. Procure por mensagens de login:
   - `[DEBUG LOGIN] Tentando login para: portalmagra@gmail.com`
   - `[DEBUG LOGIN] DB_AVAILABLE: True/False`
   - `[DEBUG LOGIN] Usuário não encontrado`
   - `[DEBUG LOGIN] Senha incorreta`

3. Procure por erros:
   - Erros de conexão com banco
   - Erros de autenticação

---

### **PASSO 4: Testar Conexão do Banco**

1. No Railway, veja os logs de inicialização
2. Procure por:
   - ✅ `[✓] Banco de dados conectado`
   - ✅ `Conexão bem-sucedida`
   - ❌ Erros de conexão

Se houver erros de conexão, mesmo com DATABASE_URL correta, pode ser:
- Projeto Supabase pausado
- Firewall bloqueando
- Outro problema de rede

---

## 💡 SOLUÇÃO RÁPIDA (RECOMENDADA)

### **Criar Novo Usuário via Dashboard:**

1. Acesse: `https://yladabot.com/register`
2. Crie uma nova conta
3. Faça login

**Isso vai:**
- ✅ Criar o usuário no banco automaticamente
- ✅ Gerar o hash bcrypt correto
- ✅ Funcionar imediatamente

---

## 🔍 VERIFICAÇÕES FINAIS

- [ ] DATABASE_URL está correta no Railway ✅
- [ ] Railway fez redeploy após atualizar
- [ ] Usuário existe no banco (Supabase → Table Editor → users)
- [ ] Logs do Railway mostram "Banco de dados conectado"
- [ ] Tentei criar novo usuário via dashboard

---

## 🆘 PRÓXIMOS PASSOS

1. **Verifique se o usuário existe no Supabase**
2. **Se não existir, crie via dashboard (registro)**
3. **Verifique os logs do Railway para ver o erro exato**

---

**Última atualização:** 27/01/2025

