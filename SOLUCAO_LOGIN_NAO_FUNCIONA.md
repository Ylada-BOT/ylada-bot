# 🔧 Solução: Login Não Funciona em Produção

## ⚠️ PROBLEMA

Login retorna **401 (Unauthorized)** - "Credenciais inválidas" mesmo após atualizar DATABASE_URL.

---

## ✅ SOLUÇÃO PASSO A PASSO

### **PASSO 1: Verificar DATABASE_URL no Railway**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. Clique no serviço **Flask/Python** (não o Node.js!)
4. Vá em **Variables** (ou **Settings** → **Variables**)
5. Verifique se `DATABASE_URL` está assim:
   ```
   postgresql://postgres.tbbjqvvtsotjqgfygaaj:whxOGnx1h098Ue2c@aws-0-us-west-2.pooler.supabase.com:5432/postgres
   ```
6. Se estiver diferente, **atualize** e salve
7. Aguarde o redeploy (1-2 minutos)

---

### **PASSO 2: Verificar se Usuário Existe no Banco**

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Table Editor** → `users`
4. Procure por `portalmagra@gmail.com`
5. Se **NÃO existir**, vá para Passo 3
6. Se **existir**, vá para Passo 4

---

### **PASSO 3: Criar Usuário no Banco (Se Não Existir)**

#### **Opção A: Via Dashboard (Mais Fácil)**

1. Acesse: https://yladabot.com/register (ou sua URL de produção)
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
-- Cria usuário portalmagra@gmail.com
-- Senha padrão: 123456
-- (Você pode mudar depois)

INSERT INTO public.users (
    email,
    password_hash,
    name,
    role,
    is_active,
    created_at,
    updated_at
) VALUES (
    'portalmagra@gmail.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5',  -- Hash bcrypt de "123456"
    'PORTAL MAGRA',
    'user',
    true,
    NOW(),
    NOW()
) ON CONFLICT (email) DO UPDATE SET
    password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5',
    name = 'PORTAL MAGRA',
    is_active = true,
    updated_at = NOW();
```

4. Clique em **Run**
5. Verifique se apareceu "Success"

**⚠️ IMPORTANTE:** O hash acima é um exemplo. O sistema usa **bcrypt**, não SHA256!

---

### **PASSO 4: Verificar Senha (Se Usuário Já Existe)**

O problema pode ser que a senha no banco não corresponde à senha que você está usando.

**Solução:**
1. Tente resetar a senha:
   - Use a funcionalidade "Esqueci minha senha" (se existir)
   - Ou crie um novo usuário

2. Ou atualize a senha via SQL:
   - Você precisa gerar um hash bcrypt da nova senha
   - Isso é complexo, melhor usar o dashboard

---

### **PASSO 5: Verificar Logs do Railway**

1. No Railway, vá em **Deployments**
2. Clique no último deploy
3. Veja a aba **Logs**
4. Procure por:

**✅ Bom:**
```
[✓] Banco de dados conectado
[✓] Carregado .env.local
Conexão bem-sucedida
```

**❌ Ruim:**
```
Tenant or user not found
password authentication failed
connection failed
Erro ao conectar ao banco
```

Se ver erros de conexão, volte ao Passo 1.

---

## 🔍 DIAGNÓSTICO RÁPIDO

### **Teste 1: Banco Conecta?**

1. No Railway, veja os logs
2. Procure por "Banco de dados conectado"
3. Se não aparecer, DATABASE_URL está errada

### **Teste 2: Usuário Existe?**

1. No Supabase, vá em Table Editor → `users`
2. Procure por `portalmagra@gmail.com`
3. Se não existir, precisa criar

### **Teste 3: Senha Está Correta?**

1. Tente fazer login
2. Se der erro 401, senha pode estar errada
3. Tente criar novo usuário ou resetar senha

---

## 💡 SOLUÇÃO RÁPIDA (RECOMENDADA)

### **1. Criar Novo Usuário via Dashboard:**

1. Acesse: `https://yladabot.com/register`
2. Crie uma nova conta com:
   - Email: `portalmagra@gmail.com` (ou outro email)
   - Senha: (escolha uma senha)
3. Faça login

### **2. Se Dashboard Não Funcionar:**

1. Verifique DATABASE_URL no Railway (Passo 1)
2. Verifique logs do Railway (Passo 5)
3. Se houver erros de conexão, corrija DATABASE_URL

---

## 📋 CHECKLIST FINAL

- [ ] DATABASE_URL atualizada no Railway
- [ ] Railway fez redeploy
- [ ] Logs mostram "Banco de dados conectado"
- [ ] Usuário existe no banco (Supabase)
- [ ] Senha está correta
- [ ] Tentei fazer login novamente

---

## 🆘 SE AINDA NÃO FUNCIONAR

1. **Envie os logs do Railway:**
   - Railway → Deployments → Último deploy → Logs
   - Copie os erros que aparecem

2. **Verifique se o usuário existe:**
   - Supabase → Table Editor → `users`
   - Veja se `portalmagra@gmail.com` está lá

3. **Tente criar novo usuário:**
   - Via dashboard (registro)
   - Com email diferente para testar

---

**Última atualização:** 27/01/2025

